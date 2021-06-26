import CLI_decorator
import os

@CLI_decorator.command
@CLI_decorator.option('-v', default=None, Help='vision')
@CLI_decorator.option('-h', default=None, Help='help information')
@CLI_decorator.option('PATH', default=' ', Help='get the file\'s path')
@CLI_decorator.option('-r', default='1.txt', Help='read file')
@CLI_decorator.option('-hex', default='0', Help='Change the input value to hex and save it to the hex.txt')
@CLI_decorator.option('cat', default=None, Help='This is a subcommand')
@CLI_decorator.argument('name',default='',Help='your name')
def test(name):
    print("%s\n" % name)

if __name__ == '__main__':
    test('')
    CLI_decorator.run()

