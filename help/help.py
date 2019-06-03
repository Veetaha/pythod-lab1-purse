from os import path, system, name
def clear():
    """
    Clear console function os-independent

    :return: NoneType
    """
    if name == 'nt':
        system('cls')
    else:
        system('clear')
