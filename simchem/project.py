import re
import sys
import requests
import numpy as np

elements = []
response = requests.get(
    'https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json').json()
"""
Els used to prepare a list of elements with their characteristics taken from response
"""

for item in response['elements']:
    elements.append(item)

R = 0.082057366080960

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
        match x.lower():
            case 'molarmass':
                molecule = input('element: ')
                print(f'{molarmass(molecule):.2f}')
            case 'missing':
                molecule = input('element: ')
                weight = input('total weight: ')
                print(missing(molecule, weight))
            case 'ige':
                ige_variables = dict.fromkeys(['V', 'P', 'T', 'n'])
                print('Please insert known values with precaution to units (L for volume, atm for pressure, and Kelvin'
                      ' for temperature')
                for key in ige_variables.keys():
                    unknown_variable = input(f'{key}: ')
                    if unknown_variable.isdigit():
                        ige_variables[key] = float(unknown_variable)
                    else:
                        ige_variables[key] = unknown_variable

                print(ige(ige_variables))
            case 'exit':
                sys.exit(0)


def molarmass(molecule):
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
    mass = 0

    if parsed_elements := re.findall(r'(?:[A-Z][a-z]?)(?:\d?\d)?', molecule):
        for elem in parsed_elements:
            if atoms := re.search(r'([A-Z][a-z]?)(\d?\d)?', elem):
                for items in elements:
                    if atoms[1] == items['symbol']:
                        if not atoms[2]:
                            number_of_atoms = 1
                        else:
                            number_of_atoms = int(atoms[2])
                        mass += float(items['atomic_mass']) * number_of_atoms
        return mass
    else:
        return 'Input must be in the format of: CAPITAL_CHAR(char - optional)(numer - optional). See Readme.me file'


def missing(molecule, weight):
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

    known = molarmass(molecule)
    weight_of_unknown_atoms = float(weight) - known
    if not 'x' in molecule.lower():
        return 'Need to notate unknown element by "x"'
    try:
        if atoms := re.search(r'(?:[X|x](\d?\d)?)', molecule):
            number_of_atoms = int(atoms[1])
    except TypeError:
        number_of_atoms = 1

    normalized_atom_weight = np.format_float_positional(weight_of_unknown_atoms / number_of_atoms, precision=2,
                                                        unique=False, fractional=True, trim='k')
    for items in elements:
        if normalized_atom_weight == np.format_float_positional(items['atomic_mass'], precision=2,
                                                          unique=False, fractional=True, trim='k'):
            elem = items['symbol']
            return elem
    return 'none found'


def ige(ige_variables):
    """
    _Calculating the ideal gas equation (ige) for one unknown parameter_\n
    This function get passed in a dict from the main(). This dict contains the user's input about
    the parameters of the ige, including one unknown value that needs to be specified by 'x'.\n
    param ige_variables: dict object\n
    raise TypeError: if any other character other than 'x' is submitted, or more than 1 x is submitted\n
    return: str of resulted float
    """

    result = 0
    v = ige_variables['V']
    p = ige_variables['P']
    t = ige_variables['T']
    n = ige_variables['n']

    list_of_unknown = [x for x in ige_variables if not ige_variables[x]]
    if len(list_of_unknown) > 1:
        return "Can't calculate 2 variables"
    for parameter in ige_variables.items():
        if parameter[1] == 'x' or not parameter[1]:
            match (parameter[0]):
                case 'V':
                    res = R * n * t / p
                case 'n':
                    res = (p * v) / (R * t)
                case 'P':
                    res = R * n * t / v
                case 'T':
                    res = R * n / (p * v)
            return f'{parameter[0]} = {res:.3f}'

        elif not isinstance(parameter[1], float):
            return f"{parameter[0]} value must be 'x/None' or a number"


if __name__ == '__main__':
    main()
