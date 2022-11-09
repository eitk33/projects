from ing import Ing
from phase import Phase
from formula import Formula
from datetime import date
from cs50 import SQL
import sys

# setting database for the app
db = SQL("sqlite:///formula.db")

# declaring some global lists
req_list_ing = ['name', 'inci', 'serial', 'temp', 'typeo', 'hlb', 'remarks', 'concen', 'phil', 'incapabilities',
                'suppliar', 'manu']
req_list_phase = ['name', 'temp', 'grind', 'stir', 'time']
tot_ing_list = []
phases = []


def main():
    # uploading info from database to exist classes
    upload(tot_ing_list, req_list_ing)

    # this is the menu for the user
    while True:
        x = (input('choose action: '))

        # setting the menu options
        match (x):
            # creating new ing that will aotumaticaly upload to the database - working
            case 'new_ing':
                ing = new_ing()
            # exit the app - working
            case 'exit':
                sys.exit(0)
            # creating new phase. this one does not getting saved externally
            case 'create_phase':
                phase = None
                a = 'P' + input('phase number: ')
                phase = Phase(a)
                while True:
                    # this is in order to uplad ing to the phase
                    nameofing = input('ing name: ')
                    if nameofing == 'done':
                        break
                    else:
                        for item in tot_ing_list:
                            if nameofing in str(item.name):
                                nameofing = item
                                weightofing = input('weight: ')
                                phase.adding(nameofing, weightofing)
                                break
                phases.append(new_phase((phase)))

            case 'create_formula':
                form = Formula()
                while True:
                    nameofphase = input('phase name: ')
                    if nameofphase == 'done':
                        break
                    else:
                        for item in phases:
                            if nameofphase == item.name:
                                nameofphase = item
                                form.adding_phase(nameofphase)
                formup(form)
            case other:
                print('unknown action')


def formup(x):
    """
    handling the process of create new formula in the database
    :param x: Formula object
    :return: None
    """

    check = db.execute('SELECT name from formula')
    counter = 0
    a = ''
    name = x.name_formula

#   Making sure consistency is retained in formula's names
    for i in check:
        a = i['name'].split('.', 1)[0]
        if name == a:
            counter += 1
            name = x.name_formula + '-' + str(counter)
    cus = input("Name of customer: ")
    pro = input('Name of prodcut: ')
    name = name + '. ' + cus + '. ' + pro
    mylist = []
    for item in x.phase:
        mylist.append(str(item))
    mylist = str(mylist)
    db.execute("INSERT INTO formula (phase, hlb_em, hlb_ing, name) values (?, ?, ?, ?)", mylist, x.hlb_em, x.hlb_ing,
               name)


def ing(req_list_ing):
    """
    managing the process of getting new ingredient to the system
    :param req_list_ing: list of characteristics required for the new ingredient
    :return: none
    """
    while True:
        try:
            new_ingr = new_ing(req_list_ing)
            update(new_ingr, req_list_ing)
        except EOFError:
            break


def update(x, y):
    """
    insert created ingredient to database
    :param x: new ingredient (Ing object)
    :param y: list of characteristics to update in the database
    :return: None
    """
    db.execute("INSERT INTO ingridients (serial) values (?) ", x.serial)
    for item in y:
        b = getattr(x, item)
        db.execute("UPDATE ingridients SET (?) = (?) WHERE serial = ?", item, b, x.serial)


# this works as expected
def new_ing():
    """

    :return: newly created ing object (out of existing data)
    """
    ing = Ing()
    return new(req_list_ing, ing)


def new_phase(x):
    """
    creating the additional  requirements for the new created phase
    :param x: is Phase class
    :return: completed new phase object with its additional requirements
    """
#   Getting the right RPM
    a = input('grind: ')
    if a == 'yes':
        b = input('RPM: ')
        b += ' RPM'
        a = [a, b]
    else:
        a = [a, '0 RPM']
    setattr(x, 'grind', a)
#   Getting the right RPM
    a = input('stir: ')
    if a == 'yes':
        b = input('RPM: ')
        b += ' RPM'
        a = [a, b]
    else:
        a = [a, '0 RPM']
    setattr(x, 'stir', a)

#   Getting the rest of the requirements
    temp = input('temp: ')
    setattr(x, 'temp', temp)
    time = input('time: ')
    setattr(x, 'time', time)

#   Not sure why, but this helps to cut process in current fault
    ph1 = Phase('P8')
    return x


def new(y, z):
    """

    :param y: list of characteristics needed for the creation of the desired item
    :param z: the newly created item
    :return: None
    """
    for i in range(len(y)):
        a = (input(f'{y[i]}: ').strip())
        setattr(z, y[i], a)
    if isinstance(z, Ing):
        update(z, req_list_ing)


def upload(x, r):
    """

    :param x: list pf existing ingredients
    :param r: Name of ingredient user wants to add
    :return: updated list of ingredients for the current phase

    """
    sdb = db.execute("SELECT * FROM ingridients")
    for item in sdb:
        ing = Ing()
        for k, v in item.items():
            v = str(v)
            for char in r:
                if k == char:
                    setattr(ing, str(k), v)
                else:
                    pass
        x.append(ing)


if __name__ == "__main__":
    main()
