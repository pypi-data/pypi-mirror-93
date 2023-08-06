from pathlib import Path
from threading import Thread as Thread
from fcp import CANMessage, Fcp, Spec
from termcolor import colored, cprint
from colored import fg, bg, attr
from .console import print_console
from .supervisor import Supervisor
from .essentials import launch_essentials, kill_essentials
from .register import register_functions
import math
import operator as op
import os
import signal
import time
import pprint
import subprocess
import sys
import json
import socket
import click
import toml
import atexit
import inspect

Symbol = str  # A Lisp Symbol is implemented as a Python str
List = list  # A Lisp List is implemented as a Python list
Int = int
Float = float

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."

    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer is not None:
            self.outer.find(var)
        else:
            raise Exception(f"Failed to find {var}")


def standard_env():
    "An environment with some Scheme standard procedures."
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...

    def last(*x):
        """Returns the last element of a list."""
        return x[1],

    def car(*x):
        """Returns the first element of a list."""
        return x[0]

    def cdr(*x):
        """Returns the elements of a list except for the first one."""
        return x[1:]

    def cons(x, y):
        """Returns the list x and the element y at its tail."""
        return x + [y]

    def _list(*x):
        """Returns a list of arguments"""
        return list(x)

    def list_pred(x):
        """Check if argument is a list"""
        return isinstance(x, List)

    def null_pred(x):
        """Check if argument is null"""
        return x==[]

    def number_pred(x):
        """Check if argument is a number"""
        return isinstance(x, Int) or isinstance(x, Float)

    def symbol_pred(x):
        """Check if argument is a symbol"""
        return isinstance(x, Symbol)


    env.update(
        {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "**": op.pow,
            "/": op.truediv,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "=": op.eq,
            "abs": abs,
            "append": op.add,
            "last": last,
            "car": car,
            "cdr": cdr,
            "cons": cons,
            "eq?": op.is_,
            "equal?": op.eq,
            "length": len,
            "list": _list,
            "list?": list_pred,
            "map": map,
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": null_pred,
            "number?": number_pred,
            "procedure?": callable,
            "round": round,
            "symbol?": symbol_pred,
            "print": print,
        }
    )
    return env


def tokenize(s):
    "Convert a string into a list of tokens."
    if s.startswith(";"):
        return []
    return s.replace("(", " ( ").replace(")", " ) ").split()

global_env = standard_env()


def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


def read_from_tokens(tokens):
    if len(tokens) == 0:
        return None

    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("unexpected )")
    else:
        return atom(token)

def test(x, cfg):
    print_console("Starting test...", False, cfg)
    _, name, *exps = x
    exps_results = []
    cprint(colored(f"Running test: {name}", "green"))
    for exp in exps:
        exps_result = eval(exp, cfg)
        if exps_result == 404:
            return False
        exps_results.append(exps_result)

    print_console('%sEnd of test %s' % (fg(243), attr(0)), False, cfg)
    return not any([exp is False for exp in exps_results])


def eval(x, cfg, env=global_env):
    if isinstance(x, Int) or isinstance(x, Float):
        return x
    elif x[0] == '"':
        return x[1:-1]
    elif isinstance(x, Symbol):
        return env.find(x)[x]
    elif not isinstance(x, List):
        return x
    elif x[0] == "test":
        return test(x, cfg)
    elif x[0] == "exit":
        return "exit"
    else:
        proc = eval(x[0], cfg, env)
        args = [eval(exp, cfg, env) for exp in x[1:]]
        return proc(*args)



class Program:
    def __init__(self, lines):
        self.lines = lines

    def take(self):
        open_count = close_count = 0
        acc = ""
        while len(self.lines) > 0:
            line = self.lines.pop(0)
            open_count += line.count("(")
            close_count += line.count(")")
            acc += line
            if open_count - close_count == 0:
                return acc

        return None



def rep(config, line):
    r = read_from_tokens(tokenize(line))
    if r is not None:
        r = eval(r, config)
        if r == "exit":
            return "exit"
        return r

def parse(file, config):
    with open(file, "r") as f:
        program = Program(f.readlines())

    count = 0
    while True:
        line = program.take()
        if line is None:
            return count
        try:
            r = rep(config, line)
            if r is False:
                count += 1

        except Exception as e:
            print("Parser Error:", e)

    return count

def is_ftest_file(file):
    if not os.path.isfile(file):
        print(f"Error: {file} doesn't exit")
        sys.exit(1)
    elif ".ftest" not in os.path.splitext(file)[1]:
        print(f"Error: {file} doesn't have a .ftest extension")
        sys.exit(1)


def cleanup(launch_table, supervisor_proc, supervisor, middle_obj, vsniff_obj):
    print("Cleanup")
    for value in launch_table.values():
        os.killpg(os.getpgid(value.pid), signal.SIGTERM)

    supervisor.terminate()
    supervisor_proc.join()
    os.system("rm *.log")
    kill_essentials(middle_obj, vsniff_obj)


@click.group(invoke_without_command=True)
@click.argument("ftest_file")
@click.argument("config")
@click.option("-i/-ni", default=False, help="launches interpreter")
@click.option("--verbose/--noverbose", default=False, help="hides debug output")
def main(ftest_file, config, i, verbose):

    with open(config) as f:
        config = toml.loads(f.read())

    config["verbose"] = verbose

    launch_table = {}

    is_ftest_file(ftest_file)

    vsniff_obj, middle_obj = launch_essentials(config)

    supervisor= Supervisor(config)
    supervisor_proc = Thread(target=supervisor.run)
    supervisor_proc.start()

    register_functions(global_env, config, launch_table, supervisor)

    count = 0
    if not i:
        count = parse(ftest_file, config)
    else:
        def clean():
            cleanup(launch_table, supervisor_proc, supervisor, middle_obj, vsniff_obj)
        atexit.register(clean)
        while True:
            line = input(">> ")
            r = rep(config, line)
            if r == "exit":
                break

    cleanup(launch_table, supervisor_proc, supervisor, middle_obj, vsniff_obj)
    sys.exit(count)

if __name__ == "__main__":
    main()
