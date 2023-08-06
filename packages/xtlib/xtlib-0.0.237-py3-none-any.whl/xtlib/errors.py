#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# errors.py: functions related to error handling
import os
import sys
import logging
import traceback

from xtlib import utils
from .console import console

logger = logging.getLogger(__name__)

def exception_msg(ex):
    parts = str(ex).split("\n")
    return parts[0]

def user_exit(msg):
    raise Exception(msg)

def early_exit_without_error(msg=None):
    '''
    This is not an error; just information that request terminated early.
    '''
    if msg:
        console.print(msg, flush=True)
    sys.exit(0)

def syntax_error_exit():
    # use "os._exit" to prevent exception from being thrown
    os._exit(1)

def report_exception(ex, operation=None):
    #console.print("Error: " + exception_msg(ex))
    raise ex

def process_exception(ex_type, ex_value, ex_traceback, exit_app=True):
    msg = str(ex_value)

    if issubclass(ex_type, XTUserException):
        # user-related exception: don't show stack trace
        console.print()
        console.print("Exception: " + msg, flush=True)
       
        if issubclass(ex_type, SyntaxError):
            # show syntax/args for command
            from .qfe import current_dispatcher
            current_dispatcher.show_current_command_syntax()

        if ex_value.show_stack:
            raise ex_value   # show stack tracke and exit
        
        #traceback.print_exc()
    else:
        # XT or other exception that requires stack trace
        # show stack trace and exit
        if exit_app:
            # this will show stack trace and exit
            raise ex_value
        else:
            # for use in REPL command: just show stack trace but do not exit
            traceback.print_exception(ex_type, ex_value, ex_traceback, flush=True)

    if exit_app:
        # use "os._exit" to prevent a 2nd exception from being thrown
        os._exit(1)

# all XT exceptions subclass this
class XTBaseException(Exception):
    def __init__(self, msg, show_stack=False):
        self.show_stack = show_stack

# user-related XT exceptions subclass this
# for this, we do *not* show a stack trace
class XTUserException(XTBaseException): pass

class UserError(XTUserException): pass
class SyntaxError(XTUserException): pass
class ComboError(XTUserException): pass
class ConfigError(XTUserException): pass
class EnvError(XTUserException): pass
class CredentialsError(XTUserException): pass
class GeneralError(XTUserException): pass

class InternalError(XTBaseException): pass
class StoreError(XTBaseException): pass
class ServiceError(XTBaseException): pass
class APIError(XTBaseException): pass

class ControllerNotYetRunning(XTBaseException): pass

# following functions handle the different classes of errors

def internal_error(msg, show_stack=False):
    raise InternalError(msg, show_stack=show_stack)

def syntax_error(msg, show_stack=False):    
    raise SyntaxError(msg, show_stack=show_stack)

def creds_error(msg, show_stack=False):    
    raise CredentialsError(msg, show_stack=show_stack)

def combo_error(msg, show_stack=False):    
    raise ComboError(msg, show_stack=show_stack)

def env_error(msg, show_stack=False):    
    raise EnvError(msg, show_stack=show_stack)

def config_error(msg, show_stack=False):    
    raise ConfigError(msg, show_stack=show_stack)

def store_error(msg, show_stack=False):    
    raise StoreError(msg, show_stack=show_stack)

def service_error(msg, show_stack=False):    
    raise ServiceError(msg, show_stack=show_stack)

def general_error(msg, show_stack=False):
    raise GeneralError(msg, show_stack=show_stack)

def api_error(msg, show_stack=False):
    raise APIError(msg, show_stack=show_stack)

def controller_not_yet_running(msg, show_stack=False):
    raise ControllerNotYetRunning(msg, show_stack=show_stack)

def argument_error(arg_type, token):
    if token.startswith("-"):
        token2 = "-" + token
    else:
        token2 = "--" + token
    #syntax_error("expected {}, but found '{}'.  Did you mean '{}'?".format(arg_type, token, token2))    
    syntax_error("unrecognized argument: {}".format(token))

def warning(msg):
    console.print("Warning: " + msg, flush=True)