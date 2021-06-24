import sys
import os
import requests
from functools import wraps

'''
Function description: Output version information
:param s: Command entered
Usage example: python *.py --version | -V | -v
output:
3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)]
'''


def v():
    result = sys.version
    return result


'''
Function description: Output the path of the specified file
:param s: Command entered
Usage example: python *.py PATH 1.txt
output:
E:\lab3\1.txt
'''


def PATH(s):
    result = os.getcwd() + '\\' + s
    return result


'''
Function description: Output help information
e.g:
usage: [--version | -V |-v ] [-h] [PATH] [-r][cat a|n|d] [-hex]
sub-commands:
                cat a: add data to the file
                cat n: create a new file
                cat d: download files
position-arguments:
                PATH : Print the absolute path of the file
named-arguments:
                --version : Show the current command-line interface version(also -v -V)
                -h: show this help method and exit
                -r: Read the contents in the file
                -hex: Change the input value to hex and save it to the hex.txt
:param s: Command entered
Usage example: python *.py -h usage
output:
usage: [--version | -V |-v ] [-h] [PATH] [-r][cat a|n|d] [-hex]
'''


def Help(s):
    if s in ['usage', 'sub-commands', 'position-arguments','named-arguments']:
        result = s + ': '
        if s == 'usage':
            result = result + '\n [--version | -V |-v ] [-h] [PATH] [-r][cat a|n|d] [-hex]'
        elif s == 'sub-commands':
            result = result + '\n cat a: add data to the file \n cat n: create a new file\n cat d: download files'
        elif s == 'position-arguments':
            result = result + '\n PATH : Print the absolute path of the file'
        elif s == 'named-arguments':
            result = result + '\n --version : Show the current command-line interface version(also -v -V) \n -h: show this help method and exit \n -r: Read the contents in the file \n -hex: Change the input value to hex and save it to the hex.txt'
    else:
        result = 'no help topic match ' + s
    return result


'''
Function description: Read the contents in the file
:param s: Command entered
Usage example: python *.py -r 1.txt
output:
This is 1.txt
This file is created at 2020/5/28 10:39 in Beijing time.
1234
'''


def read(s):
    with open (s, 'r') as f:
        lines = f.readlines()
    return lines


'''
Function description:          
    cat a: add data to the file
    cat n: create a new file
    cat d: delete a file
:param s: Command entered
cat a Usage example: python *.py cat a 1.txt 'the text you want to add'
cat n Usage example: python *.py cat n new.txt
cat d Usage example: python *.py cat d name.txt
'''


def cat(s):
    while len(s) > 0 and s[0] in ['n', 'a', 'd']:
        if s[0] == 'n':
            s.pop(0)
            f = open(s[0], 'w')
            f.close()
            s.pop(0)
        elif s[0] == 'a':
            s.pop(0)
            with open(s[0], 'a') as f:
                f.write(s[1] + "\n")
            s = s[2:]
        elif s[0] == 'd':
            s.pop(0)
            if os.path.exists(s[0]): os.remove(s[0])
            s.pop(0)


'''
Function description: Change the input value to hex and save it to the hex.txt
:param s: Command entered 
Usage example: python *.py  10
output:
Write A to hex.txt
'''


def hex(s):
    result = ""
    HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    num = int(s)
    while num > 15:
        ret = HEX[num % 16] + result
        num = num // 16
    result = HEX[num] + result
    with open('hex.txt', 'a') as f:
        f.write(result + "\n")
    return result


option_command = {}
Coms = []
fun = {'-v': v, '-V': v, '--version': v, 'PATH': PATH, '-h': Help, '-r': read, 'cat': cat, '-hex': hex}
subcommand_name=[]

#Used to decorate a function so that the function serves as a command line interface
def command(f):
    def r(*args, **kwargs):
        global Coms
        Coms = sys.argv[1:]
        return f(*args, **kwargs)
    return r

#Used to decorate a function
def option(func_name, default=None, Help='help'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            global option_command
            option_command[fun[func_name]] = default
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator

#Pass a simple variable value
def argument(func_name, default=None, Help='help'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            global option_command
            global  Coms
            argu=default
            subcommand_name.append(func_name)
            fun[func_name] = func_name
            option_command[fun[func_name]] = args
            Coms = sys.argv[1:]
            if func_name in Coms:
                index=Coms.index(func_name)
                argu=Coms[index+1]
            func(argu)
        return wrapped_function
    return logging_decorator

def run():
    global  Coms
    while len(Coms) > 0:
        if fun[Coms[0]] not in option_command:
            print('\'' + Coms[0] + '\' is not availiable')
            raise KeyError
            break
        elif fun[Coms[0]] is v:
            v()
            Coms = Coms[1:]
        elif fun[Coms[0]] is Help:
            if len(Coms)==1 or Coms[1] in fun:
                print('Invalid instruction ')
            else:
                c = []
                Coms.pop(0)
                while Coms[0] in ['usage', 'sub-commands', 'position-arguments','named-arguments']:
                    c.append(Coms[0])
                    Coms.pop(0)
                    c.append(Coms[0])
                    Coms.pop(0)
                    if len(Coms) == 0 :
                        break
                Help(c)
        elif fun[Coms[0]] in subcommand_name:
            break
        elif fun[Coms[0]] is PATH :
            if len(Coms)==1 :
                PATH(option_command[PATH])
                break
            elif Coms[1] in fun:
                PATH(option_command[PATH])
                Coms = Coms[1:]
            else:
                PATH(Coms[1])
                Coms = Coms[2:]
        elif fun[Coms[0]] is read:
            if len(Coms)==1 :
                read(option_command[read])
                break
            elif Coms[1] in fun:
                read(option_command[read])
                Coms = Coms[1:]
            else:
                read(Coms[1])
                Coms = Coms[2:]
        elif fun[Coms[0]] is hex:
            if len(Coms)==1 :
                hex(option_command[hex])
                break
            elif Coms[1] in fun:
                hex(option_command[hex])
                Coms = Coms[1:]
            else:
                hex(Coms[1])
                Coms = Coms[2:]
        elif fun[Coms[0]] is cat:
            if len(Coms)==1 or Coms[1] in fun:
                print('Invalid instruction ')
            else:
                c = []
                Coms.pop(0)
                while Coms[0] in ['n', 'a', 'd']:
                    if Coms[0] == 'a':
                        c.append(Coms[0])
                        Coms.pop(0)
                        c.append(Coms[0])
                        Coms.pop(0)
                        c.append(Coms[0])
                        Coms.pop(0)
                    else:
                        c.append(Coms[0])
                        Coms.pop(0)
                        c.append(Coms[0])
                        Coms.pop(0)
                    if len(Coms) == 0 :
                        break
                cat(c)


if __name__ == '__main__':
    Help()
