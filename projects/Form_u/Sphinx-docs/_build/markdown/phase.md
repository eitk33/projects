# phase module


### _class_ phase.Phase(name, temp=31, grind=['no', '0 RPM'], stir=['yes', '30 RPM'], time=5)
Bases: `object`


#### \__init__(name, temp=31, grind=['no', '0 RPM'], stir=['yes', '30 RPM'], time=5)

#### adding(s, am)
this handles the addition of a new Ing object to phase, and what happens if Ing already in phase
:param s: Ing object
:param am: has to be an int.
:return:


#### am_veri(s)

#### _property_ grind()

#### list_mod(s)
needed for some fixings in the text written
:param s: self.grind/stir
:return:


#### _property_ name()

#### _property_ stir()

#### _property_ temp()

#### _property_ time()

#### usedict(s)
building a dict out of ing object
:param s: Ing object
:return: dict
