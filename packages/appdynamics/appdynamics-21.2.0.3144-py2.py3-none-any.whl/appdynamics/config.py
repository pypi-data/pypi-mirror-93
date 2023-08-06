# Copyright (c) AppDynamics, Inc., and its affiliates
# 2015
# All Rights Reserved

"""Reads agent configuration from environment variables.

Each attribute defined below may be configured by setting an environment
variable with the name of the attribute prefixed by ``APPDYNAMICS_``. For example,
the ``AGENT_APPLICATION_NAME`` variable's value is read from ``APPDYNAMICS_AGENT_APPLICATION_NAME``.

Attributes that are marked ``optional`` have sensible defaults that will
often work (unless you have an unusual configuration that requires setting
them).

Attributes
----------
AGENT_APPLICATION_NAME : str
    The name of this AppDynamics application. The agent will be disabled if
    this is **not** set.
AGENT_TIER_NAME : str
    The name of this AppDynamics tier. The agent will be disabled if this is
    **not** set.
AGENT_NODE_NAME : str
    The name of this AppDynamics node. The agent will be disabled if this is
    **not** set.
CONTROLLER_HOST_NAME : str
    The IP address or hostname of the AppDynamics controller. The agent is
    disabled if this is **not** set.
CONTROLLER_PORT : int, optional
    The port the AppDynamics controller is listening on. The default value is
    80/443 depending on whether SSL is enabled. You may need to change this
    if your controller is listening on a different port.
CONTROLLER_SSL_CERTFILE: str, optional
    SSL cert file for the controller. Must be the absolute path to the certfile.
    This is applicable if a certificate is installed in a non-standard location.
    By default, the agent ships with its own certficate in a standard location.
CONTROLLER_SSL_ENABLED : bool, optional
    Indicates whether SSL should be used to talk to the controller. This
    attribute is set to True if the APPDYNAMICS_CONTROLLER_SSL_ENABLED environment variable is
    set to 'on', otherwise it is set to False. The default is False.

WSGI_SCRIPT : str, optional
    If you are instrumenting a pure WSGI application or an application that
    uses a WSGI-compatible framework, set this to the full path to your real
    WSGI script. By default, WSGI applications are not automatically
    instrumented.
WSGI_MODULE : str, optional
    As an alternative to WSGI_SCRIPT, WSGI_MODULE can be set to the fully
    qualified module, class or function name of your WSGI application e.g.
    ``django.core.handlers.wsgi:WSGIHandler()``, ``mysite.wsgi``,
    ``flask_app:application``.
WSGI_CALLABLE_OBJECT : str, optional
    This is the name of the symbol for your WSGI callable that is defined in
    WSGI_SCRIPT or WSGI_MODULE. The default is ``application``.  If you
    specified a class or function name in WSGI_MODULE, this setting will have
    no effect.

Advanced Attributes
-------------------
AGENT_REUSE_NODE_NAME : bool, optional
    If the AGENT_REUSE_NODE_NAME is set to true, node will be marked as historical during
    shutdown.

AGENT_REUSE_NODE_NAME_PREFIX: str, optional
    The name of this AppDynamics node will be AGENT_REUSE_NODE_NAME_PREFIX with some
    integer number as suffix, when AGENT_REUSE_NODE_NAME is set.

AGENT_BASE_DIR : str, optional
    The base directory for agent temporary files and logs.  This defaults to
    /tmp/appd/.
LOGS_DIR : str, optional
    The directory that the agent and proxy should log to.  This defaults to
    AGENT_BASE_DIR/logs/.

AGENT_ACCOUNT_NAME : str, optional
    Your AppDynamics account name.
AGENT_ACCOUNT_ACCESS_KEY : str, optional
    Your AppDynamics account access key.

HTTP_PROXY_HOST : str, optional
    The IP address or hostname of your HTTP proxy if the machine that the
    agent is running on must use an HTTP proxy to talk to the AppDynamics
    controller. The default is to not use an HTTP proxy.
HTTP_PROXY_PORT : int, optional
    The port number of the HTTP proxy. This is only relevant if
    HTTP_PROXY_HOST is set. The default is to use port 80/443 based on
    CONTROLLER_SSL_ENABLED.
HTTP_PROXY_USER : str, optional
    If HTTP_PROXY_HOST is set, and your proxy requires authentication, this is
    used as the username for the proxy.
HTTP_PROXY_PASSWORD_FILE : str, optional
    If HTTP_PROXY_HOST is set, and your proxy requires authentication, this
    stores the full path to a file readable by the AppDynamics proxy daemon
    that stores the password for the HTTP proxy user.

EUM_DISABLE_COOKIE : bool, optional
    If EUM_DISABLE_COOKIE is set, the agent will not add EUM correlation data
    to WSGI response headers.
EUM_USER_AGENT_WHITELIST : str, optional
    By default, EUM correlation data is added for browsers with the following
    user agent headers: 'Mozilla, Opera, WebKit, Nokia'.  Specify alternate
    user agents in EUM_USER_AGENT_WHITELIST as a comma seperated list.  Use '*'
    to allow all user agents.

Debugging Attributes
--------------------
LOGGING_LEVEL : str, optional
    The logging level for the agent.  Can be one of 'warning', 'info' or
    'debug'.  The default is 'warning'.
DEBUG_LOG : bool, optional
    If DEBUG_LOG is True, the agent logging level is set to 'debug' and logs
    are written to stdout, as well as LOGS_DIR.

INCLUDE_AGENT_FRAMES : bool, optional
    By default, the agent excludes frames from call graphs and exceptions that
    it determines are part of its own code. Set ``APPDYNAMICS_INCLUDE_AGENT_FRAMES``
    to ``on`` to change this behavior and have the agent include its own code.
    This can be useful for debugging if a snapshot indicates that the agent is
    spending significant time in its own code.
SNAPSHOT_PROFILER_INTERVAL_MS : int, optional
    By default, the agent samples frames at a interval of 10ms during snapshots.
    Use SNAPSHOT_PROFILER_INTERVAL_MS to alter this interval.
EXIT_CALL_DETAILS_LENGTH : int, optional
    By default, exit calls have their 'detailString' attribute truncated to 500
    characters.  Use EXIT_CALL_DETAILS_LENGTH to alter this length.

Private Attributes
------------------
PROXY_CONTROL_PATH : str, optional
    The path to the UNIX domain socket that will be used for communication
    over the AppDynamics proxy control channel.
PROXY_CONFIG_SOCKET_NAME : str, optional
    The name of the socket to connect to the AppDynamics proxy for retrieving
    application configuration from the controller.
PROXY_INFO_SOCKET_NAME : str, optional
    The name of the socket to connect to the AppDynamics proxy for retrieving
    transaction info from the controller.
PROXY_REPORTING_SOCKET_NAME : str, optional
    The name of the socket to connect to the AppDynamics proxy for reporting
    transactions to the controller.

PROXY_STARTUP_READ_TIMEOUT_MS : int, optional
    The timeout (in milliseconds) for attempting to read the startup node
    request. The default is 1000ms. If set to zero or an empty number, the
    timeout is disabled, and the read returns immediately regardless of
    whether data was available. If set to a negative integer, the read blocks
    until data is available (**not recommended**).
PROXY_STARTUP_INITIAL_RETRY_DELAY_MS : int, optional
    The initial delay (in milliseconds) to wait before retrying a failed
    startup node request. We do exponential backoff for startup node request
    failures, starting at this delay and maxing out at the value specified by
    ``PROXY_STARTUP_MAX_RETRY_DELAY_MS``. The default is 5 seconds.
PROXY_STARTUP_MAX_RETRY_DELAY_MS : int, optional
    The maximum delay (in milliseconds) to wait before retrying a failed
    startup node request. We do exponential backoff for startup node request
    failures up to this delay, starting at the value specified by
    ``PROXY_STARTUP_INITIAL_RETRY_DELAY_MS``. The default is 5 minutes.

CONFIG_SERVICE_RELOAD_INTERVAL_MS : int, optional
    The time to wait (in milliseconds) between checking for new configuration
    from the controller (via the AppDynamics proxy). The default is 5 seconds.
CONFIG_SERVICE_MAX_RETRIES : int, optional
    The maximum number of retries for failed configuration reloads before we
    disable the agent and initiate a new startup request. The default is 3.

BT_INFO_REQUEST_TIMEOUT_MS : int, optional
    The maximum duration (in milliseconds) that we wait for a BTInfoResponse
    before continuing on. The BT may still be reported with MISSING_RESPONSE
    in the BTDetails.

BT_MAX_DURATION_MS : int, optional
    By default, BTs lasting over 2 minutes are killed without being reported.
    Use BT_MAX_DURATION_MS to alter the maximum BT duration allowed.

"""

from __future__ import unicode_literals
import logging
import os

from appdynamics.lang import keys, SafeConfigParser, values

int_or_none = lambda v: int(v) if v != '' else None
on_off = lambda v: v.lower() in ('on', 'true', 'yes', 'y', 't', '1')
comma_seperated_list = lambda v: v.replace(' ', '').split(',')


# Configuration Options

_CONFIG_OPTIONS_BY_SECTION = {
    'agent': {
        'app': ('AGENT_APPLICATION_NAME', None),
        'tier': ('AGENT_TIER_NAME', None),
        'node': ('AGENT_NODE_NAME', None),
        'uniquehostid': ('AGENT_UNIQUE_HOST_ID', None),
        'dir': ('AGENT_BASE_DIR', None),
        'nodereuse': ('AGENT_REUSE_NODE_NAME', on_off),
        'nodereuseprefix': ('AGENT_REUSE_NODE_NAME_PREFIX', None),
    },

    'wsgi': {
        'script': ('WSGI_SCRIPT_ALIAS', None),
        'callable': ('WSGI_CALLABLE_OBJECT', None),
        'module': ('WSGI_MODULE', None),
    },

    'log': {
        'dir': ('LOGS_DIR', None),
        'level': ('LOGGING_LEVEL', None),
        'debugging': ('DEBUG_LOG', on_off),
        'format': ('LOG_FORMAT', None),
    },

    'controller': {
        'account': ('AGENT_ACCOUNT_NAME', None),
        'accesskey': ('AGENT_ACCOUNT_ACCESS_KEY', None),
        'host': ('CONTROLLER_HOST_NAME', None),
        'port': ('CONTROLLER_PORT', int),
        'ssl': ('CONTROLLER_SSL_ENABLED', on_off),
        'certfile': ('CONTROLLER_SSL_CERTFILE', None),
    },

    'controller:http-proxy': {
        'host': ('HTTP_PROXY_HOST', None),
        'port': ('HTTP_PROXY_PORT', int),
        'user': ('HTTP_PROXY_USER', None),
        'password-file': ('HTTP_PROXY_PASSWORD_FILE', None),
    },

    'proxy': {
        'max-heap-size': ('MAX_HEAP_SIZE', None),
        'min-heap-size': ('MIN_HEAP_SIZE', None),
        'max-perm-size': ('MAX_PERM_SIZE', None),
        'proxy-debug-port': ('PROXY_DEBUG_PORT', int_or_none),
        'start-suspended': ('START_SUSPENDED', on_off),
        'debug-opt': ('DEBUG_OPT', None),
        'agent': ('AGENT_TYPE', None)
    },

    'services:control': {
        'socket': ('PROXY_CONTROL_PATH', None),
        'read-timeout-ms': ('PROXY_STARTUP_READ_TIMEOUT_MS', int_or_none),
        'initial-retry-delay-ms': ('PROXY_STARTUP_INITIAL_RETRY_DELAY_MS', int),
        'max-retry-delay-ms': ('PROXY_STARTUP_MAX_RETRY_DELAY_MS', int),
    },

    'services:config': {
        'socket-name': ('PROXY_CONFIG_SOCKET_NAME', None),
        'reload-interval-ms': ('CONFIG_SERVICE_RELOAD_INTERVAL_MS', int),
        'max-retries': ('CONFIG_SERVICE_MAX_RETRIES', int),
    },

    'services:snapshot': {
        'include-agent-frames': ('INCLUDE_AGENT_FRAMES', on_off),
        'profiler-interval-ms': ('SNAPSHOT_PROFILER_INTERVAL_MS', int),
        'exit-call-details-length': ('EXIT_CALL_DETAILS_LENGTH', int),
        'forced-snapshot-interval': ('FORCED_SNAPSHOT_INTERVAL', int),
    },

    'services:transaction': {
        'info-request-timeout-ms': ('BT_INFO_REQUEST_TIMEOUT_MS', int),
    },

    'services:transaction-monitor': {
        'bt-max-duration-ms': ('BT_MAX_DURATION_MS', int),
    },

    'eum': {
        'disable-cookie': ('EUM_DISABLE_COOKIE', on_off),
        'user-agent-whitelist': ('EUM_USER_AGENT_WHITELIST', comma_seperated_list)
    },
}

# Kept for backward compatibility of environment variables (Remove when making old vars obsolete)
OLD_CONFIG_OPTIONS_MAP = {
    'AGENT_APPLICATION_NAME': 'APP_NAME',
    'AGENT_TIER_NAME': 'TIER_NAME',
    'AGENT_NODE_NAME': 'NODE_NAME',
    'AGENT_UNIQUE_HOST_ID': 'UNIQUE_HOST_ID',
    'AGENT_BASE_DIR': 'DIR',
    'AGENT_REUSE_NODE_NAME': 'NODE_REUSE',
    'AGENT_REUSE_NODE_NAME_PREFIX': 'NODE_REUSE_PREFIX',

    'AGENT_ACCOUNT_NAME': 'ACCOUNT_NAME',
    'AGENT_ACCOUNT_ACCESS_KEY': 'ACCOUNT_ACCESS_KEY',
    'CONTROLLER_HOST_NAME': 'CONTROLLER_HOST',
    'CONTROLLER_SSL_ENABLED': 'SSL_ENABLED',
}

# Defaults ###########

CONFIG_FILE = ''

# Agent
AGENT_APPLICATION_NAME = 'MyApp'
AGENT_TIER_NAME = ''
AGENT_NODE_NAME = ''
AGENT_UNIQUE_HOST_ID = ''
AGENT_BASE_DIR = '/tmp/appd'
AGENT_REUSE_NODE_NAME = False
AGENT_REUSE_NODE_NAME_PREFIX = ''

# Logging
LOGS_DIR = ''
LOGGING_LEVEL = 'WARNING'
DEBUG_LOG = False
LOG_FORMAT = ''

# WSGI
WSGI_MODULE = ''
WSGI_SCRIPT_ALIAS = ''
WSGI_CALLABLE_OBJECT = ''

# Controller
CONTROLLER_HOST_NAME = ''
CONTROLLER_PORT = None
CONTROLLER_SSL_CERTFILE = None
CONTROLLER_SSL_ENABLED = False
AGENT_ACCOUNT_NAME = ''
AGENT_ACCOUNT_ACCESS_KEY = ''
HTTP_PROXY_HOST = ''
HTTP_PROXY_PORT = None
HTTP_PROXY_USER = ''
HTTP_PROXY_PASSWORD_FILE = ''

# Proxy
MAX_HEAP_SIZE = '300m'
MIN_HEAP_SIZE = '50m'
MAX_PERM_SIZE = '120m'
PROXY_DEBUG_PORT = None
START_SUSPENDED = False
DEBUG_OPT = None
AGENT_TYPE = 'PYTHON_APP_AGENT'

# Proxy Runtime
PROXY_RUN_DIR = ''

# Proxy Control Service
PROXY_CONTROL_PATH = ''
PROXY_STARTUP_READ_TIMEOUT_MS = 2000
PROXY_STARTUP_INITIAL_RETRY_DELAY_MS = 5000
PROXY_STARTUP_MAX_RETRY_DELAY_MS = 300000

# Config Service
PROXY_CONFIG_SOCKET_NAME = '0'
CONFIG_SERVICE_RELOAD_INTERVAL_MS = 5000
CONFIG_SERVICE_MAX_RETRIES = 3

# Transaction Service
PROXY_INFO_SOCKET_NAME = '0'
PROXY_REPORTING_SOCKET_NAME = '1'
BT_INFO_REQUEST_TIMEOUT_MS = 100

# Snapshot Service
INCLUDE_AGENT_FRAMES = False
SNAPSHOT_PROFILER_INTERVAL_MS = 10
EXIT_CALL_DETAILS_LENGTH = 500
FORCED_SNAPSHOT_INTERVAL = 10

# Transaction Monitor Service
BT_MAX_DURATION_MS = 30 * 60 * 1000
BT_ABANDON_THRESHOLD_MULTIPLIER = 6

# EUM
EUM_DISABLE_COOKIE = False
EUM_USER_AGENT_WHITELIST = ['Mozilla', 'Opera', 'WebKit', 'Nokia']


def validate_config(config):
    """Return true if the configuration in the environment is valid.

    """
    try:
        return (
            config['AGENT_APPLICATION_NAME'] and config['AGENT_TIER_NAME'] and config['AGENT_NODE_NAME'] and
            config['CONTROLLER_HOST_NAME'] and config['PROXY_CONTROL_PATH'] and
            os.path.exists(config['PROXY_CONTROL_PATH']))
    except:
        return False


def parse_environ(environ=None, prefix='APPDYNAMICS_'):
    """Read AppDynamics configuration from an environment dictionary.

    Parameters
    ----------
    environ : mapping, optional
        A dict of environment variable names to values (strings). If not
        specified, `os.environ` is used.

    Other Parameters
    ----------------
    prefix: str, optional
        The prefix that environment variables are expected to have to be
        recognized as AppDynamics configuration. Defaults to `APPDYNAMICS_`.

    """
    logger = logging.getLogger('appdynamics')
    environ = environ if environ is not None else os.environ

    config = {}
    config_file = environ.get('APPD_CONFIG_FILE')

    if config_file:
        config = parse_config_file(config_file)

    option_descrs = {}

    for options in values(_CONFIG_OPTIONS_BY_SECTION):
        for name, handler in values(options):
            # Kept for backward compatibility of environment variables (Remove when making old vars obsolete)
            if name in OLD_CONFIG_OPTIONS_MAP:
                option_descrs['APPD_' + OLD_CONFIG_OPTIONS_MAP[name]] = (name, handler)
            else:
                option_descrs['APPD_' + name] = (name, handler)

            option_descrs[prefix + name] = (name, handler)

    for option in keys(environ):
        if option not in option_descrs:
            continue

        name, handler = option_descrs[option]

        try:
            value = environ[option]
            if handler:
                value = handler(value)
            config[name] = value
        except:
            logger.exception('ignoring %s from environment, parsing value caused exception', option)

    return config


def parse_config_file(filename):
    """Parse an AppDynamics configuration file.

    """
    logger = logging.getLogger('appdynamics')

    try:
        config = {}
        parser = SafeConfigParser()

        with open(filename) as fp:
            parser.readfp(fp)

        for section_name in parser.sections():
            try:
                options_map = _CONFIG_OPTIONS_BY_SECTION[section_name]
            except KeyError:  # Unknown section
                logger.warning('%s: skipping unrecognized section [%s]', filename, section_name)
                continue

            for option_name in parser.options(section_name):
                try:
                    env_name, handler = options_map[option_name]

                    value = parser.get(section_name, option_name)
                    if handler:
                        value = handler(value)

                    config[env_name] = value
                except KeyError:  # Unknown option
                    logger.warning('%s: skipping unrecognized option %r of section [%s]',
                                   filename, option_name, section_name)
                except:  # Other errors
                    logger.exception('%s: parsing value for option %r of section [%s] raised exception',
                                     filename, option_name, section_name)

        return config
    except:
        logger.exception('Parsing config file failed.')


def merge(config):
    """Merge configuration into the module globals and update the computed defaults.

    """
    mod = globals()
    mod.update(config)
    update_computed_defaults()


def update_computed_defaults():
    global LOGS_DIR, PROXY_CONTROL_PATH, PROXY_RUN_DIR

    PROXY_RUN_DIR = os.path.join(AGENT_BASE_DIR, 'run')

    if not PROXY_CONTROL_PATH:
        PROXY_CONTROL_PATH = os.path.join(PROXY_RUN_DIR, 'comm')

    if not LOGS_DIR:
        LOGS_DIR = os.path.join(AGENT_BASE_DIR, 'logs')
