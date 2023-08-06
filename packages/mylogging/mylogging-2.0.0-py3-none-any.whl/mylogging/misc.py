"""
This module is internal module for mylogging library. Do not this if you are a user.
Use main __init__ module if you are user.

"""

import textwrap
from datetime import datetime
import warnings

from . import config


printed_infos = set()


def log_warn(message, log_type):
    """If _TO_FILE is configured, it will log message into file on path _TO_FILE. If not _TO_FILE is configured, it will
    warn or print INFO message.
    Args:
        message (str): Any string content of warning.
        log_type (ctr): Heading of warning if in file, generated automatically from __init__ module.
    """

    if config.TO_FILE:
        with open(config.TO_FILE, 'a+') as f:
            f.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  {log_type}  {message}")

    else:
        if log_type == 'INFO':
            if config.__DEBUG == 1:
                if message not in printed_infos:
                    print(message)
                    printed_infos.add(message)
            elif config.__DEBUG > 1:
                print(message)

        else:
            warnings.warn(message)


def user_message(message, caption="User message", around=False, color='default'):
    """Return enhanced colored message. Used for raising exceptions, assertions or important warninfs mainly.
    You can print returned message, or you can use user_warning function. Then it will be printed only in debug mode.

    Args:
        message (str): Any string content of warning.
        caption (ctr): Headning of warning.

    Returns:
        str: Enhanced message as a string, that is wrapped by and can be colorized.
    """

    updated_str = textwrap.indent(text=f"\n\n========= {caption} =========\n\n{message}\n", prefix='    ')

    if not around:
        updated_str = updated_str + "\n\n"

    if config.COLOR in [True, 1] or (config.COLOR == 'auto' and not config.TO_FILE):
        updated_str = colorize(updated_str)

    # Have to be separatedly because otherwise bottom margin get no colored in tracebacks
    if around:
        if config.COLOR in [True, 1] or (config.COLOR == 'auto' and not config.TO_FILE):
            updated_str = updated_str + textwrap.indent(colorize(f"{'=' * (len(caption) + 20) if around else ''}\n\n\n"), prefix='    ')
        else:
            updated_str = updated_str + textwrap.indent(f"{'=' * (len(caption) + 20) if around else ''}\n\n\n", prefix='    ')

    return objectize_str(updated_str)


def objectize_str(message):
    """Make a class from a string to be able to apply escape characters and colors in tracebacks.

    Args:
        message (str): Any string you use.

    Returns:
        Object: Object, that can return string if printed or used in warning or raise.
    """
    class X(str):
        def __repr__(self):
            return f"{message}"

    return X(message)


def colorize(message):
    """Add color to message - usally warnings and errors, to know what is internal error on first sight.
    Simple string edit.

    Args:
        message (str): Any string you want to color.

    Returns:
        str: Message in yellow color. Symbols added to string cannot be read in some terminals.
            If global _COLORIZE is 0, it return original string.
    """

    return f"\033[93m {message} \033[0m"
