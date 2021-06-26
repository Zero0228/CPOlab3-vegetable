import sys
import os


'''
Function description: Output version information
:param s: Command entered
Usage example: python *.py --version | -V | -v
output:
3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)]
'''
def v():
    ret = sys.version
    print(ret)
    return ret


'''
Function description: Output the path of the specified file
:param s: Command entered
Usage example: python *.py PATH 1.txt
output:
E:\project\eeg\cpolab3-master\src\1.txt
'''
def PATH(s):
    path = os.getcwd()
    ret = path + '\\' + s
    print(ret)
    return ret


'''
Function description: Output help information
:param s: Command entered
Usage example: python *.py -h usage
output:
usage: [--version | -V |-v ] [-h] [PATH] [-r][cat a|n|d] [-hex]
Usage example: python *.py -h sub-commands
output:
sub-commands:
                cat a: add data to the file
                cat n: create a new file
                cat d: download files
Usage example: python *.py -h position arguments
output:
position arguments:
                PATH : Print the absolute path of the file
Usage example: python *.py -h named arguments
output:
named arguments:
                --version : Show the current command-line interface version(also -v -V)
                -h: show this help method and exit
                -r: Read the contents in the file
                -hex: Change the input value to hex and save it to the hex.txt
'''
def Help(s):
    if s in ['usage', 'sub-commands', 'position-arguments','named-arguments']:
        result = s + ': '
        if s == 'usage':
            result = result + '\n [--version | -V |-v ] [-h] [PATH] [-r][cat a|n|d] [-hex]'
        elif s == 'sub-commands':
            result = result + '\n cat a: add data to the file \n cat n: create a new file\n cat d: delete files'
        elif s == 'position-arguments':
            result = result + '\n PATH : Print the absolute path of the file'
        elif s == 'named-arguments':
            result = result + '\n --version : Show the current command-line interface version(also -v -V) \n -h: show this help method and exit \n -r: Read the contents in the file \n -hex: Change the input value to hex and save it to the hex.txt'
    else:
        result = 'no help topic match ' + s
    print(result)
    return result

'''
Function description: Read the contents in the file
:param s: Command entered
Usage example: python *.py -r 1.txt
output:
This is 1.txt
This file is created at 2021/6/26 10:34 in Beijing time.
'''
def read(s):
    with open(s) as f:
        lines = f.readlines()
        for l in lines:
            print(l, end='')
        return lines


'''
Function description:          
                        cat a: add data to the file
                        cat n: create a new file
                        cat d: Download files via http
:param s: Command entered
cat a Usage example: python *.py cat a 1.txt "hello word"
cat n Usage example: python *.py cat n new.txt
cat d Usage example: python *.py cat d new.txt
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
Usage example: python *.py -hex "10"
output:
a
'''
def hex(s):
    ret = ""
    HEX = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    num = int(s)
    while num > 15:
        ret = HEX[num % 16] + ret
        num = num // 16
    ret = HEX[num] + ret
    with open('hex.txt', 'a') as f:
        f.write(ret + "\n")
    print(ret)
    return ret

