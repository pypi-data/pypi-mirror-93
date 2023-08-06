from termcolor import colored, cprint
from colored import fg, bg, attr

def print_console(str, term, config):
    if config["verbose"]:
        if term:
            cprint(str)
        else:
            print(str)