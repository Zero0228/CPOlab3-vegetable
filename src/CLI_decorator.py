import sys
from functools import wraps
from CLI import *

fun = {'-v': v, '-V': v, '--version': v, 'PATH': PATH, '-h': Help, '-r': read, 'cat': cat, '-hex': hex}
subcommand_name=[]

class global_value():
    Coms = []
    option_command = {}

#Used to decorate a function so that the function serves as a command line interface
def command(f):
    def r(*args, **kwargs):
        global_value.Coms = sys.argv[1:]
        return f(*args, **kwargs)
    return r

#Used to decorate a function
def option(func_name, default=None, Help='help'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            global_value.option_command[fun[func_name]] = default
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

#Pass a simple variable value
def argument(func_name, default=None, Help='help'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            argu=default
            subcommand_name.append(func_name)
            fun[func_name] = func_name
            global_value.option_command[fun[func_name]] = args
            global_value.Coms = sys.argv[1:]
            if func_name in global_value.Coms:
                index=global_value.Coms.index(func_name)
                argu=global_value.Coms[index+1]
            func(argu)
        return wrapped_function
    return logging_decorator

def run():
    while len(global_value.Coms) > 0:
        if fun[global_value.Coms[0]] not in global_value.option_command:
            print('\'' + global_value.Coms[0] + '\' is not availiable')
            raise KeyError
            break
        elif fun[global_value.Coms[0]] is v:
            v()
            global_value.Coms = global_value.Coms[1:]
        elif fun[global_value.Coms[0]] is Help:
            Help(global_value.Coms[1])
            global_value.Coms = global_value.Coms[2:]
        elif fun[global_value.Coms[0]] in subcommand_name:
            break
        elif fun[global_value.Coms[0]] is PATH :
            if len(global_value.Coms)==1 :
                PATH(global_value.option_command[PATH])
                break
            elif global_value.Coms[1] in fun:
                PATH(global_value.option_command[PATH])
                global_value.Coms = global_value.Coms[1:]
            else:
                PATH(global_value.Coms[1])
                global_value.Coms = global_value.Coms[2:]
        elif fun[global_value.Coms[0]] is read:
            if len(global_value.Coms)==1 :
                read(global_value.option_command[read])
                break
            elif global_value.Coms[1] in fun:
                read(global_value.option_command[read])
                global_value.Coms = global_value.Coms[1:]
            else:
                read(global_value.Coms[1])
                global_value.Coms = global_value.Coms[2:]
        elif fun[global_value.Coms[0]] is hex:
            if len(global_value.Coms)==1 :
                hex(global_value.option_command[hex])
                break
            elif global_value.Coms[1] in fun:
                hex(global_value.option_command[hex])
                global_value.Coms = global_value.Coms[1:]
            else:
                hex(global_value.Coms[1])
                global_value.Coms = global_value.Coms[2:]
        elif fun[global_value.Coms[0]] is cat:
            if len(global_value.Coms)==1 or global_value.Coms[1] in fun:
                print('Invalid instruction ')
            else:
                c = []
                global_value.Coms.pop(0)
                while global_value.Coms[0] in ['n', 'a', 'd']:
                    if global_value.Coms[0] is 'a':
                        c.append(global_value.Coms[0])
                        global_value.Coms.pop(0)
                        c.append(global_value.Coms[0])
                        global_value.Coms.pop(0)
                        c.append(global_value.Coms[0])
                        global_value.Coms.pop(0)
                    else:
                        c.append(global_value.Coms[0])
                        global_value.Coms.pop(0)
                        c.append(global_value.Coms[0])
                        global_value.Coms.pop(0)
                    if len(global_value.Coms) == 0 :
                        break
                cat(c)
