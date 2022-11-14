     SimpleChem
     Video Demo:  https://youtu.be/6p00Q22seig
     Description:

Simple app to help with some fundamental chemistry calculations

This is the main section. from here the user will be prompted to decide what action should program take

user will need to choose his action;

**molarmass**

**missing**

**ige**

**exit**


_Return the MW (molar mass) of a given compound_

param s: Molecular formula. case sensitive. has to be in the format: [atomic_symbol][number_of_atoms].by defult [number_of_atoms] = 1 (if no other value submitted). for instance: He2 will be the notation for a molecule composed from 2 atoms of Helium (although, of course, not possible). Let's say we have a molecule with two carbon atoms connected to four unknown atoms? so the input should be: C2X4

type s: string

raise TypeError: not sure

return: either the molar mass of the given compound, or an error message. if one of the submitted segments doesn't respond to a valid atom, there will not be an error message, and the function will ignore this value

return type: int


---


```
missing(s, v)
```

_Return the atomic symbol of an unknown element in a given compound if total weight is known_

param s: Molecular formula with unknown atom represented by X. case sensitive. has to be in the format: atomic_symbol_number_of_atoms. in addition, the unknown element must be notated as 'X' for instance: He2 will be the notation for a molecule composed from 2 atoms of Helium (although, of course, not possible). Let's say we have a molecule with two carbon atoms connected  to four unknown atoms? so the input should be: C2X4

type s: string

raise TypeError: not sure

param v: total weight. e.g. input the total weight of the molecule given

type v: string or int

raise TypeError: if empty

return: either the symbol of the unknown atom, or an error message

rtype: str or an int (depend on the usage) in the case of a successful attempt, str in the case of an error


---


```
ige(mydict)
```

_Calculating the ideal gas equation (ige) for one unknown parameter_

This function get passed in a dict from the main(). This dict contains the user's input about the parameters of the ige, including one unknown value that needs to be specify by 'x'.

param mydict: dict object

raise TypeError: if any other character other than 'x' is submitted, or more then 1 x is submitted

return: str of resulted float


