import sys
from functools import wraps
from CLI import *
from typing import TypeVar, List, Iterator, Callable, Generic, Tuple, NewType, Union, Any, Deque, Optional, Dict, Any

class CLIDecorator(object):
    def __init__(self, name: str) -> None:
        print(name)
        self.fun = {'-v': v, '-V': v, '--version': v, 'PATH': PATH, '-h': Help, '-r': read, 'cat': cat, '-hex': hex}
        self.subcommand_name = []  # type: List
        self.Coms = []  # type: List
        self.option_command = {}  # type: Dict

    def command(self, f: Callable) -> Callable:
        '''
        Used to decorate a function so that the function serves as a command line interface
        :param f: Callable
        :return: Callable
        '''
        def r(*args, **kwargs):
            self.Coms = sys.argv[1:]
            return f(*args, **kwargs)
        return r

    def option(self, func_name: str, default=None, Help='help') -> Callable:
        '''
        Used to decorate a function
        :param func_name: str
        :param default: Union[str, None]
        :param Help: str
        :return: Callable
        '''
        def logging_decorator(func):
            @wraps(func)
            def wrapped_function(*args, **kwargs):
                self.option_command[self.fun[func_name]] = default
                return func(*args, **kwargs)
            return wrapped_function
        return logging_decorator

    def argument(self, func_name: str, default=None, Help='help') -> Callable:
        '''
        Pass a simple variable value
        :param func_name: str
        :param default: Union[str, None]
        :param Help: str
        :return: Callable
        '''
        def logging_decorator(func):
            @wraps(func)
            def wrapped_function(*args, **kwargs):
                argu = default
                self.subcommand_name.append(func_name)
                self.fun[func_name] = func_name
                self.option_command[self.fun[func_name]] = args
                self.Coms = sys.argv[1:]
                if func_name in self.Coms:
                    index = self.Coms.index(func_name)
                    if len(self.Coms) == 1:
                        argu = None
                    else:
                        argu = self.Coms[index + 1]
                func(argu)
            return wrapped_function
        return logging_decorator

    def run(self) -> None:
        while len(self.Coms) > 0:
            if self.fun[self.Coms[0]] not in self.option_command:
                print('\'' + self.Coms[0] + '\' is not availiable')
                raise KeyError
                break
            elif self.fun[self.Coms[0]] is v:
                # print(self.Coms)
                v()
                self.Coms = self.Coms[1:]
            elif self.fun[self.Coms[0]] is Help:
                Help(self.Coms[1])
                self.Coms = self.Coms[2:]
            elif self.fun[self.Coms[0]] in self.subcommand_name:
                break
            elif self.fun[self.Coms[0]] is PATH:
                if len(self.Coms) == 1:
                    PATH(self.option_command[PATH])
                    break
                elif self.Coms[1] in self.fun:
                    PATH(self.option_command[PATH])
                    self.Coms = self.Coms[1:]
                else:
                    PATH(self.Coms[1])
                    self.Coms = self.Coms[2:]
            elif self.fun[self.Coms[0]] is read:
                if len(self.Coms) == 1:
                    read(self.option_command[read])
                    break
                elif self.Coms[1] in self.fun:
                    read(self.option_command[read])
                    self.Coms = self.Coms[1:]
                else:
                    read(self.Coms[1])
                    self.Coms = self.Coms[2:]
            elif self.fun[self.Coms[0]] is hex:
                if len(self.Coms) == 1:
                    hex(self.option_command[hex])
                    break
                elif self.Coms[1] in self.fun:
                    hex(self.option_command[hex])
                    self.Coms = self.Coms[1:]
                else:
                    hex(self.Coms[1])
                    self.Coms = self.Coms[2:]
            elif self.fun[self.Coms[0]] is cat:
                if len(self.Coms) == 1 or self.Coms[1] in self.fun:
                    print('Invalid instruction ')
                else:
                    c = []
                    self.Coms.pop(0)
                    while self.Coms[0] in ['n', 'a', 'd']:
                        if self.Coms[0] == 'a':
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                        else:
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                            c.append(self.Coms[0])
                            self.Coms.pop(0)
                        if len(self.Coms) == 0:
                            break
                    cat(c)

