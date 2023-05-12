# Standard imports
from colorama import Fore


def red(text: str):
    print(Fore.RED + text + Fore.RESET, end = "")


def green(text: str):
    print(Fore.GREEN + text + Fore.RESET, end = "")


def blue(text: str):
    print(Fore.BLUE + text + Fore.RESET, end = "")


def white(text: str):
    print(Fore.WHITE + text + Fore.RESET, end = "")


def yellow(text: str):
    print(Fore.YELLOW + text + Fore.RESET, end = "")


def black(text: str):
    print(Fore.BLACK + text + Fore.RESET, end = "")
