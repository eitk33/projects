import re
import sys
import requests
import numpy as np

els = []
response = requests.get(
    'https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json').json()
"""
Els used to prepare a list of elements with their characteristics taken from response
"""
for item in response['elements']:
    els.append(item)


def main():
    """
    Simple app to help with some fundamental chemistry calculations

    This is the main section. from here the user will be prompted to decide what action should program take

    user will need to choose his action;\n
    **molarmass**\n
    **missing**\n
    **ige**\n
    **exit**\n
    Return a value depend on user desired function
    """

    while True:
        x = input('action: ')
        match x:
            case 'molarmass':
                s = input('element: ')
                print(molarmass(s))
            case 'missing':
                s = input('element: ')
                w = input('total weight: ')
                print(missing(s, w))
            case 'ige':
                mydict = dict.fromkeys(['V', 'P', 'T', 'n'])
                print('Please insert known values with precaution to units (L for volume, atm for pressure, and Kelvin'
                      ' for temperature')
                for key in mydict.keys():
                    a = input(f'{key}: ')
                    try:
                        mydict[key] = float(a)
                    except ValueError:
                        mydict[key] = a
                mydict['Rr'] = 0.082057366080960
                print(ige(mydict))
            case 'exit':
                sys.exit(0)


def molarmass(s):
    """

    _Return the MW (molar mass) of a given compound_

    param s: Molecular formula. case-sensitive. has to be in the format:
    [atomic_symbol][number_of_atoms].by default [number_of_atoms] = 1 (if no other value submitted).
    for instance:
    He2 will be the notation for a molecule composed of 2 atoms of Helium (although, of course, not possible).

    type s: string\n
    raise TypeError: not sure\n
    return: either the molar mass of the given compound, or an error message. if one of the submitted segments doesn't
    respond to a valid atom, there will not be an error message, and the function will ignore this value\n
    return type: int
    """
    global els
    mass = 0

    if elements := re.findall(r'(?:[A-Z][a-z]?)(?:\d?\d)?', s):
        for elem in elements:
            if sub := re.search(r'([A-Z][a-z]?)(\d?\d)?', elem):
                for items in els:
                    if sub[1] == items['symbol']:
                        if not sub[2]:
                            mul = 1
                        else:
                            mul = int(sub[2])
                        mass += float(items['atomic_mass']) * mul
        return mass
    else:
        return 'not a valid format'


def missing(s, v):
    """
    _Return the atomic symbol of an unknown element in a given compound if total weight is known_\n
    param s: Molecular formula with unknown atom represented by X. case-sensitive. has to be in the format:
    atomic_symbol_number_of_atoms. in addition, the unknown element must be notated as 'X'
    for instance:
    He2 will be the notation for a molecule composed of 2 atoms of Helium (although, of course, not possible).
    Let's say we have a molecule with two carbon atoms connected  to four unknown atoms? so the input should be:
    C2X4\n
    type s: string\n
    raise TypeError: not sure\n
    param v: total weight. e.g. input the total weight of the molecule given\n
    type v: string or int\n
    raise TypeError: if empty\n
    return: either the symbol of the unknown atom, or an error message\n
    rtype: str or an int (depend on the usage) in the case of a successful attempt, str in the case of an error
    """
    global els
    known = molarmass(s)
    un = float(v) - known

    try:
        if a := re.search(r'(?:[X|x](\d?\d)?)', s):
            a = int(a[1])
    except TypeError:
        a = 1

    unn = np.format_float_positional(un / a, precision=3, unique=False, fractional=True, trim='k')
    for items in els:

        if float(unn) == items['atomic_mass']:
            ele = items['symbol']
            return ele
    return 'non found'


def ige(mydict):
    """
    _Calculating the ideal gas equation (ige) for one unknown parameter_\n
    This function get passed in a dict from the main(). This dict contains the user's input about
    the parameters of the ige, including one unknown value that needs to be specified by 'x'.\n
    param mydict: dict object\n
    raise TypeError: if any other character other than 'x' is submitted, or more than 1 x is submitted\n
    return: str of resulted float
    """

    res = 0
    v = mydict['V']
    p = mydict['P']
    t = mydict['T']
    n = mydict['n']
    r = mydict['Rr']
    for parameter in mydict.items():

        if parameter[1] == 'x':
            match (parameter[0]):
                case 'V':
                    res = r * n * t / p
                case 'n':
                    res = (p * v) / (r * t)
                case 'P':
                    res = r * n * t / v
                case 'T':
                    res = r * n / (p * v)
            return f'{parameter[0]} = {res:.3f}'

        elif not type(parameter[1]) == float:
            raise ValueError(f"{parameter[0]} value must be 'x' or a number")

    return


if __name__ == '__main__':
    main()
