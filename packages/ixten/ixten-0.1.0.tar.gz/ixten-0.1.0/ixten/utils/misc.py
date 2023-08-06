################################################################################
#    Copyright 2021 @ Telefónica
#
#    This program is part of Ixten. You can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

import colorama
colorama.init(autoreset=True)


LICENSE_URL = "https://www.gnu.org/licenses/gpl-3.0.txt"


def colorize(text, messageType=None):
    """Function that colorizes a message.

    Args:
        text (str): The string to be colorized. If not a string, it is converted.
        messageType (str): Possible options include "ERROR", "WARNING", "SUCCESS",
            "INFO" or "BOLD".

    Returns:
        string: Colorized if the option is correct, including a tag at the end
            to reset the formatting.
    """
    formatted_text = str(text)

    # Set colors
    if "ERROR" in messageType:
        formatted_text = colorama.Fore.RED + formatted_text
    elif "WARNING" in messageType:
        formatted_text = colorama.Fore.YELLOW + formatted_text
    elif "SUCCESS" in messageType:
        formatted_text = colorama.Fore.GREEN + formatted_text
    elif "INFO" in messageType:
        formatted_text = colorama.Fore.BLUE + formatted_text

    # Set emphashis mode
    if "BOLD" in messageType:
        formatted_text = colorama.Style.BRIGHT + formatted_text

    return formatted_text + colorama.Style.RESET_ALL


def error(text):
    """Bolds the given text and uses a red font

    Args:
        text (str): Object to be colorized.

    Returns:
        str. Colorized text.
    """
    return colorize(text, ["ERROR", "BOLD"])


def warning(text):
    """Uses an orange font

    Args:
        text (str): Object to be colorized.

    Returns:
        str. Colorized text.
    """
    return colorize(text, ["WARNING"])


def success(text):
    """Bolds the given text and uses a green font

    Args:
        text (str): Object to be colorized.

    Returns:
        str. Colorized text.
    """
    return colorize(text, ["SUCCESS", "BOLD"])


def info(text):
    """Uses a blue font

    Args:
        text (str): Object to be colorized.

    Returns:
        str. Colorized text.
    """
    return colorize(text, ["INFO"])


def title(text):
    """Bolds the given text and uses a blue flont

    Args:
        text (str): Object to be colorized.

    Returns:
        str. Colorized text
    """
    return colorize(text, ["INFO", "BOLD"])


def emphasis(text):
    """Bolds the given text

    Args:
        text (str): Object to be colorized.

    Returns:
        str. Colorized text.
    """
    return colorize(text, ["BOLD"])
