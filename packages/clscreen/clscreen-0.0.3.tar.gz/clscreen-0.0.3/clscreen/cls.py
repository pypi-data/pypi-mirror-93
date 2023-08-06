from platform import system as sysname
from os import system

if sysname() == 'Windows':
    def clear():
        system('cls')

    def cls():
        system('cls')

else:
    def clear():
        system('clear')
    
    def cls():
        system('clear')
