from colored import fg, bg, attr
from termcolor import colored, cprint
from .console import print_console
from .vio import adc_pack
import subprocess
import time
import os
import socket


def register(env, config):
    def decorator(fn):
        def f(*args):
            return fn(config, *args)

        env.update({fn.__name__: f})
        return f

    return decorator


def register_functions(global_env, config, launch_table, supervisor):

    @register(global_env, config)
    def launch(config, *args):
        dir_name = args[0].split("-")[0]
        exe = "/".join([config["root"], dir_name, "bin", args[0] + ".out"])
        if not os.path.isfile(exe):
            print('%s[LAUNCH ERROR] Executable file not found: %s %s' % (fg(196), exe, attr(0)))
            return 404
        print_console('%slaunch %s %s' % (fg(243), args[0], attr(0)), False, config)
        if args[0] not in launch_table.keys():
            launch_table[args[0]] = subprocess.Popen(exe + f">> {args[0]}.log", shell=True, preexec_fn=os.setsid)
            print_console('%s[LAUNCH] Component Initializing... %s' % (fg(243), attr(0)), False, config)
            time.sleep(0.01)
        else:
            print_console('%s[LAUNCH] Component already running...Skipping %s' % (fg(243), attr(0)), False, config)


    @register(global_env, config)
    def output(config, *args):
        print("output", *args)

  
    @register(global_env, config)
    def send_adc(config, *args):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(100):
            sock.sendto(adc_pack(args[0], args[1]), ("127.0.0.1", 9999))
        print('%ssend_adc %s %s %s' % (fg(243), args[0], args[1], attr(0)))

 
    @register(global_env, config)
    def assert_eq(config, *args):
        got_value = supervisor.get_signal(args[0])
        input_value = type(got_value)(args[1])

        err = 1e-3*input_value
        if got_value - err/2 < input_value and got_value + err/2 > input_value:
            cprint("ASSERT: "+args[0]+" =~ "+str(input_value)+":" + colored(f" PASSED" , "green"))
            return True
        else:
            print('ASSERT: %s =~ %s: %sFAILED %s Expected ~%s got %s' % (args[0], str(input_value), fg(196), attr(0), str(input_value), str(got_value)))
            return False

    @register(global_env, config)
    def help(config, *args):
        print(inspect.getdoc(args[0]))
