#### `formup(x)`

handling the process of create new formula in the database
:param x: Formula object
:return: None

#### `ing(req_list_ing)`

managing the process of getting new ingredient to the system
:param req_list_ing: list of characteristics required for the new ingredient
:return: none

#### `main()`

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


formup(x):

#### `new_ing()`


:return: newly created ing object (out of existing data)

#### `new_phase(x)`

creating the additional  requirements for the new created phase
:param x: is Phase class
:return: completed new phase object with its additional requirements

#### `new(y, z)`


:param y: list of characteristics needed for the creation of the desired item
:param z: the newly created item
:return: None

#### `update(x, y)`

insert created ingredient to database
:param x: new ingredient (Ing object)
:param y: list of characteristics to update in the database
:return: None

#### `upload(x, r)`


:param x: list pf existing ingredients
:param r: Name of ingredient user wants to add
:return: updated list of ingredients for the current phase
