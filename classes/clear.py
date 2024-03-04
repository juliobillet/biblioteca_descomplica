from os import system, name

# função para limpar o terminal
def clear():
 
    # comando para windows
    if name == 'nt':
        _ = system('cls')
 
    # comando para mac e linux
    else:
        _ = system('clear')