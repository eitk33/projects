import re
import sys
import requests

els = []
response = requests.get('https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json').json()

for item in response['elements']:
    els.append(item)

def main():

    """
    simple app to help with some fundamental chemistry calculations

    This is the main section. from here the user will be prompt to decide what action shoulf program take

    user will need to choose his action;\n
    molarmass\n
    missing\n
    ige\n
    exit\n
    probably a type error in none of the above
    """
    while True:
        x = input('action: ')
        match (x):
            case 'molarmass':
                s = input('element: ')
                print(molarmass(s))
            case 'missing':
                s = input('element: ')
                w = input('total weight: ')
                print(missing(s, w))
            case 'ige':

                """
                Calculating the ideal gas equation for one unknown parameter
                """
                mydict = dict.fromkeys(['V','P', 'T', 'n'])
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

    parameter s: Molecular formula\n
    type s: string\n
    raise TypeError: not sure\n
    return: either the molar mass of the given compound, or an error messege. if one of the sobmited segments doesn't respond
    to a valid atom, there will not be an error messege, and the function will ignore this value\n
    return type: int
    """
    global els
    mass = 0

    if elements := re.findall(r'(?:[A-Z][a-z]?)(?:\d?\d)?', s):
        for item in elements:
            if sub := re.search(r'([A-Z][a-z]?)(\d?\d)?', item):
                for items in els:
                    if sub[1] == items['symbol']:
                        if not sub[2]:
                            mul = 1
                        else:
                            mul = int(sub[2])
                        mass += round(float(items['atomic_mass'])) * mul
        return(mass)
    else:
        return('not a valid format')

def missing(s, v):
    """
    Return the atomic symbole of an unknown element in a given compound if total weight is known\n

    param s: Molecular formula with unknown atom represented by X. case sensitive. has to be in the format:
    atomic_symbol_number_of_atoms. in addition, the unknown element must be notated as 'X'
    for instance:
    He2 will be the notation for a molecule composed from 2 atoms of Helium (altough, of course, not possible).
    Let's say we have a molecule with two carbon atoms conected to four unknown atoms? so the input should be:
    C2X4\n
    type s: string\n
    raise TypeError: not sure\n
    param v: total weight. e.g. input the total weight of the molecule given\n
    type v: string or int\n
    raise TypeError: if empty\n
    return: either the symbol of the unknown atom, or an error messege\n
    rtype: str or an int (depend on the usage) in the case of a successful attempt, str in the case of an error
    """
    global els
    known = molarmass(s)
    un = int(v) - int(known)
    try:
        if a := re.search(r'(?:[X|x](\d?\d)?)', s):
            a = int(a[1])
    except TypeError:
        a = 1
    unn = un/a
    for items in els:
        if unn == int(items['atomic_mass']):
            ele = items['symbol']
            return(ele)
    return('non found')

def ige(mydict):
    """
    Calculating the ideal gas equation for one unknown parameter
    """

    res = 0
    v = mydict['V']
    p = mydict['P']
    t = mydict['T']
    n = mydict['n']
    Rr = mydict['Rr']
    for item in mydict.items():
        if item[1] == 'x':
            match(item[0]):
                case 'V':
                    res = Rr * n * t / p
                case 'n':
                    res = (p * v) / (Rr * t)
                case 'P':
                    res = Rr * n * t / v
                case 'T':
                    res = Rr * n / ( p * v)
            return(f'{item[0]} = {res:.3f}')

    return
if __name__ == '__main__':
    main()