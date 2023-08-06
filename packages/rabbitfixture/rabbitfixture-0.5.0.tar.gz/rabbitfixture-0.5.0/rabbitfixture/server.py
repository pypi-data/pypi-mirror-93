# Copyright 2011-2015 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Test server fixtures for RabbitMQ."""

from __future__ import absolute_import, print_function

__metaclass__ = type

__all__ = [
    "RabbitServer",
    "RabbitServerResources",
    ]

from contextlib import contextmanager
import errno
import logging
import os
import re
import signal
import socket
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess
import time

import amqp
from fixtures import (
    EnvironmentVariableFixture,
    Fixture,
    TempDir,
    )
from testtools.content import (
    Content,
    content_from_file,
    )
from testtools.content_type import UTF8_TEXT

# The default binaries have a check that the running use is uid 0 or uname
# 'rabbitmq', neither of which are needed to operate correctly. So we run the
# actual erlang binaries.
RABBITBIN = "/usr/lib/rabbitmq/bin"


def preexec_fn():
    # Revert Python's handling of SIGPIPE. See
    # http://bugs.python.org/issue1652 for more info.
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    # Create a new process group, so we can send signals to both
    # rabbitmq and its child processes.
    os.setsid()


def get_port(socket):
    """Return the port to which a socket is bound."""
    addr, port = socket.getsockname()
    return port


def allocate_ports(*addrs):
    """Allocate `len(addrs)` unused ports.

    A port is allocated for each element in `addrs`.

    There is a small race condition here (between the time we allocate the
    port, and the time it actually gets used), but for the purposes for which
    this function gets used it isn't a problem in practice.
    """
    sockets = [socket.socket() for addr in addrs]
    try:
        for addr, sock in zip(addrs, sockets):
            sock.bind((addr, 0))
        return [get_port(sock) for sock in sockets]
    finally:
        for sock in sockets:
            sock.close()


# Pattern to parse rabbitctl status output to find the nodename of a running
# node. New rabbitmq-servers don't have a running_nodes section, so we can't
# just look for that. Check that the node's status block reports rabbit.
status_regex = re.compile(r"""
    Status\ of\ node\ '?
      (?P<nodename>        # begin capture group
        [^@]+@[^@']+?      # a node is name@hostname
      )'?(?:\ \.\.\.)?\n   # end capture group
    \[(\{pid,\d+\},\n\ )?  # old versions don't show the pid.
    \{running_applications,.*
        \{rabbit,"RabbitMQ"
    """, re.VERBOSE | re.DOTALL)

# RabbitMQ 3.7.0 has a new format for its status output.
new_status_regex = re.compile(r"""
    Status\ of\ node\ '?
      (?P<nodename>        # begin capture group
        [^@]+@[^@']+?      # a node is name@hostname
      )'?(?:\ \.\.\.)?\n   # end capture group
    .*
    ^OS\ PID:\ \d+\n
    .*
    ^RabbitMQ\ version:
    """, re.VERBOSE | re.MULTILINE | re.DOTALL)


def get_nodename_from_status(status_text):
    match = status_regex.search(status_text)
    if match is not None:
        return match.group("nodename")
    match = new_status_regex.search(status_text)
    if match is not None:
        return match.group("nodename")
    return None


class RabbitServerResources(Fixture):
    """Allocate the resources a RabbitMQ server needs.

    :ivar hostname: The host the RabbitMQ is on (always localhost for
        `RabbitServerResources`).
    :ivar port: A port that was free at the time setUp() was called.
    :ivar dist_port: A port that was free at the time setUp() was
        called. Used for the `RABBITMQ_DIST_PORT` environment variable,
        which is related to clustering in RabbitMQ >= 3.3.
    :ivar homedir: A directory to put the RabbitMQ logs in.
    :ivar mnesiadir: A directory for the RabbitMQ db.
    :ivar logfile: The logfile allocated for the server.
    :ivar nodename: The name of the node.

    """

    def __init__(self, hostname=None, port=None, homedir=None,
                 mnesiadir=None, logfile=None, nodename=None,
                 dist_port=None):
        super(RabbitServerResources, self).__init__()
        self._defaults = dict(
            hostname=hostname,
            port=port,
            dist_port=dist_port,
            homedir=homedir,
            mnesiadir=mnesiadir,
            logfile=logfile,
            nodename=nodename,
            )

    def setUp(self):
        super(RabbitServerResources, self).setUp()
        self.__dict__.update(self._defaults)
        if self.hostname is None:
            self.hostname = 'localhost'
        if self.port is None:
            [self.port] = allocate_ports(self.hostname)
        if self.dist_port is None:
            [self.dist_port] = allocate_ports(self.hostname)
        if self.homedir is None:
            self.homedir = self.useFixture(TempDir()).path
        if self.mnesiadir is None:
            self.mnesiadir = self.useFixture(TempDir()).path
        if self.logfile is None:
            self.logfile = os.path.join(self.homedir, 'server.log')
        if self.nodename is None:
            self.nodename = os.path.basename(self.useFixture(TempDir()).path)
        self.pluginsfile = os.path.join(
            self.useFixture(TempDir()).path, 'enabled_plugins')
        with open(self.pluginsfile, 'w') as pluginsfile:
            pluginsfile.write('[].\n')

    @property
    def fq_nodename(self):
        """The node of the RabbitMQ that is being exported."""
        return "%s@%s" % (self.nodename, self.hostname)


class RabbitServerEnvironment(Fixture):
    """Export the environment variables needed to talk to a RabbitMQ instance.

    When setup this exports the key RabbitMQ variables:

    - ``RABBITMQ_MNESIA_BASE``
    - ``RABBITMQ_LOG_BASE``
    - ``RABBITMQ_NODE_IP_ADDRESS``
    - ``RABBITMQ_NODE_PORT``
    - ``RABBITMQ_DIST_PORT``
    - ``RABBITMQ_NODENAME``
    - ``RABBITMQ_PLUGINS_DIR``
    - ``RABBITMQ_ENABLED_PLUGINS_FILE``

    """

    def __init__(self, config, ctltimeout=None):
        """Create a `RabbitServerEnvironment` instance.

        :param config: An object exporting the variables
            `RabbitServerResources` exports.
        :param ctltimeout: Timeout for server control operations.
        """
        super(RabbitServerEnvironment, self).__init__()
        self.config = config
        self._ctltimeout = ctltimeout or 15

    def setUp(self):
        super(RabbitServerEnvironment, self).setUp()
        self.useFixture(EnvironmentVariableFixture(
            "RABBITMQ_MNESIA_BASE", self.config.mnesiadir))
        self.useFixture(EnvironmentVariableFixture(
            "RABBITMQ_LOG_BASE", self.config.homedir))
        self.useFixture(EnvironmentVariableFixture(
            "RABBITMQ_NODE_IP_ADDRESS",
            socket.gethostbyname(self.config.hostname)))
        self.useFixture(EnvironmentVariableFixture(
            "RABBITMQ_NODE_PORT", str(self.config.port)))
        self.useFixture(EnvironmentVariableFixture(
            "RABBITMQ_DIST_PORT", str(self.config.dist_port)))
        self.useFixture(EnvironmentVariableFixture(
            "RABBITMQ_NODENAME", self.config.fq_nodename))
        self.useFixture(EnvironmentVariableFixture(
            "RABBITMQ_ENABLED_PLUGINS_FILE", self.config.pluginsfile))
        self._errors = []
        self.addDetail('rabbit-errors', Content(
            UTF8_TEXT, self._get_errors))

    def _get_errors(self):
        """Yield all errors as UTF-8 encoded text."""
        for error in self._errors:
            if isinstance(error, bytes):
                yield error
            else:
                yield error.encode('utf8')
            yield b'\n'

    @property
    def ctlbin(self):
        return os.path.join(RABBITBIN, "rabbitmqctl")

    @property
    def ctltimeout(self):
        return self._ctltimeout

    def rabbitctl(self, command, strip=False, timeout=None):
        """Executes a ``rabbitctl`` command and returns status."""
        if timeout is None:
            timeout = self.ctltimeout
        nodename = self.config.fq_nodename
        env = dict(os.environ, HOME=self.config.homedir)
        if isinstance(command, str):
            command = (command,)
        ctl = subprocess.Popen(
            (self.ctlbin, "-n", nodename) + command, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            preexec_fn=preexec_fn, universal_newlines=True)
        try:
            outstr, errstr = ctl.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            ctl.kill()
            ctl.communicate()
            raise
        if strip:
            return outstr.strip(), errstr.strip()
        return outstr, errstr

    def is_node_running(self):
        """Checks that our RabbitMQ node is up and running."""
        nodename = self.config.fq_nodename
        try:
            outdata, errdata = self.rabbitctl("status")
        except subprocess.TimeoutExpired:
            return False
        if errdata:
            self._errors.append(errdata)
        if not outdata:
            return False
        found_node = get_nodename_from_status(outdata)
        if found_node is None:
            self._errors.append(outdata)
            return False
        else:
            return found_node == nodename

    def get_connection(self):
        """Get an AMQP connection to the RabbitMQ server.

        :raises socket.error: If the connection cannot be made.
        """
        host_port = "%s:%s" % (self.config.hostname, self.config.port)
        connection = amqp.Connection(
            host=host_port, userid="guest",
            password="guest", virtual_host="/")
        connection.connect()
        return connection


class RabbitServerRunner(Fixture):
    """Run a RabbitMQ server."""

    def __init__(self, config, ctltimeout=None):
        """Create a `RabbitServerRunner` instance.

        :param config: An object exporting the variables
            `RabbitServerResources` exports.
        """
        super(RabbitServerRunner, self).__init__()
        self.config = config
        self._ctltimeout = ctltimeout
        self.process = None

    def setUp(self):
        super(RabbitServerRunner, self).setUp()
        self.environment = self.useFixture(
            RabbitServerEnvironment(self.config, ctltimeout=self._ctltimeout))
        self._start()

    def is_running(self):
        """Is the RabbitMQ server process still running?"""
        if self.process is None:
            return False
        else:
            return self.process.poll() is None

    def check_running(self):
        """Checks that the RabbitMQ server process is still running.

        :raises Exception: If it not running.
        :return: True if it is running.
        """
        if self.is_running():
            return True
        else:
            raise Exception("RabbitMQ server is not running.")

    @contextmanager
    def _handle_sigchld(self):
        # The rabbitmq-server process we're trying to stop is our direct
        # child process, so we need to handle SIGCHLD in order for the
        # process to go away gracefully.
        def sigchld_handler(signum, frame):
            while True:
                try:
                    pid, _ = os.waitpid(-1, os.WNOHANG)
                    if not pid:
                        break
                except OSError as e:
                    if e.errno == errno.ECHILD:
                        break
                    raise

        original_sigchld = signal.signal(signal.SIGCHLD, sigchld_handler)
        if original_sigchld is None:
            logging.warning(
                "Previous SIGCHLD handler was installed by non-Python code; "
                "will restore to default action instead.")
            original_sigchld = signal.SIG_DFL

        try:
            yield
        finally:
            signal.signal(signal.SIGCHLD, original_sigchld)

    def kill(self):
        """Kill the RabbitMQ server process.

        This will send a SIGKILL to the server process and its children, it is
        used as last resort if both 'rabbitmqctl stop' and sending SIGTERM
        haven't managed to shutdown RabbitMQ.

        It is also useful to test your code against scenarios where the server
        dies.
        """
        with self._handle_sigchld():
            self._signal(signal.SIGKILL)
            time.sleep(0.5)
            if self.is_running():
                raise Exception("RabbitMQ server just won't die.")

    def _spawn(self):
        """Spawn the RabbitMQ server process."""
        cmd = os.path.join(RABBITBIN, 'rabbitmq-server')
        env = dict(os.environ, HOME=self.config.homedir)
        with open(self.config.logfile, "wb") as logfile:
            with open(os.devnull, "rb") as devnull:
                self.process = subprocess.Popen(
                    [cmd], stdin=devnull, stdout=logfile, stderr=logfile,
                    close_fds=True, cwd=self.config.homedir, env=env,
                    preexec_fn=preexec_fn)
        self.addDetail(
            os.path.basename(self.config.logfile),
            content_from_file(self.config.logfile))

    def _start(self):
        """Start the RabbitMQ server."""
        # Check if Rabbit is already running. In truth this is really to avoid
        # a race condition around creating $HOME/.erlang.cookie: let rabbitctl
        # create it now, before spawning the daemon.
        if self.environment.is_node_running():
            raise AssertionError(
                "RabbitMQ OTP already running even though it "
                "hasn't been started it yet!")
        self._spawn()
        # Wait for the server to come up: stop when the process is dead, or
        # the timeout expires, or the server responds.
        timeout = time.time() + self.environment.ctltimeout
        while time.time() < timeout and self.is_running():
            if self.environment.is_node_running():
                break
            time.sleep(0.3)
        else:
            raise Exception(
                "Timeout waiting for RabbitMQ server to start: log in %r." %
                (self.config.logfile,))
        # The Erlang OTP is up, but RabbitMQ may not be usable. We need to
        # cleanup up the process from here on in even if the full service
        # fails to get together.
        self.addCleanup(self._stop)
        # `rabbitctl status` can say a node is up before it is ready to accept
        # connections. Wait for the node to come up...
        timeout = max(timeout, time.time() + self.environment.ctltimeout)
        while time.time() < timeout and self.check_running():
            try:
                self.environment.get_connection().close()
            except socket.error:
                time.sleep(0.1)
            else:
                break
        else:
            raise Exception(
                "Timeout waiting for RabbitMQ node to come up: log in %r." %
                (self.config.logfile,))

    def _request_stop(self):
        outstr, errstr = self.environment.rabbitctl("stop", strip=True)
        if outstr:
            self.addDetail('stop-out', Content(UTF8_TEXT, lambda: [outstr]))
        if errstr:
            self.addDetail('stop-err', Content(UTF8_TEXT, lambda: [errstr]))

    def _stop(self):
        """Stop the running server. Normally called by cleanups."""
        with self._handle_sigchld():
            try:
                self._request_stop()
                # Wait for the node to go down...
                timeout = time.time() + self.environment.ctltimeout
                while time.time() < timeout:
                    if not self.environment.is_node_running():
                        break
                    time.sleep(0.3)
                else:
                    raise Exception(
                        "Timeout waiting for RabbitMQ node to go down.")
            except subprocess.TimeoutExpired:
                # Go straight to killing the process directly.
                timeout = time.time()

            # Wait for the process to end...
            timeout = max(timeout, time.time() + self.environment.ctltimeout)
            while time.time() < timeout:
                if not self.is_running():
                    break
                self._signal(signal.SIGTERM)
                time.sleep(0.1)
            else:
                # Die!!!
                if self.is_running():
                    self.kill()

    def _signal(self, code):
        """Send a signal to the server process and all its children."""
        # We need to send the signal to the process group, since on Ubuntu
        # 14.04 an later /usr/sbin/rabbitmq-server is a shell script wrapper
        # that spawns the actual Erlang runtime sub-process which what does
        # actually do the work and listen for connections.
        os.killpg(os.getpgid(self.process.pid), code)


class RabbitServer(Fixture):
    """A RabbitMQ server fixture.

    When setup a RabbitMQ instance will be running and the environment
    variables needed to talk to it will be already configured.

    :ivar config: The `RabbitServerResources` used to start the server.
    :ivar runner: The `RabbitServerRunner` that bootstraps the server.
    """

    def __init__(self, config=None, ctltimeout=None):
        super(RabbitServer, self).__init__()
        self.config = config
        self._ctltimeout = ctltimeout

    def setUp(self):
        super(RabbitServer, self).setUp()
        if self.config is None:
            self.config = RabbitServerResources()
        self.useFixture(self.config)
        self.runner = RabbitServerRunner(
            self.config, ctltimeout=self._ctltimeout)
        self.useFixture(self.runner)
