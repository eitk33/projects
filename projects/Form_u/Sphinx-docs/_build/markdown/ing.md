# ing module


### _class_ ing.Ing(name='', inci='', serial='', temp=40, typeo='', hlb=None, remarks='', concen='', phil='', incapabilities='', suppliar='', manu='')
Bases: `object`


#### \__init__(name='', inci='', serial='', temp=40, typeo='', hlb=None, remarks='', concen='', phil='', incapabilities='', suppliar='', manu='')

#### ch(_ = ['emulsifier', 'emollient', 'thickner', 'condition', 'solubilizer', 'active', 'structuring agent', 'surfactant', 'SPF', 'film_former'_ )

#### _property_ concen()

#### _property_ hlb()

#### _property_ phil()

#### search(comp=(), key=None)
used to search ingredient by all kind of filters (for the purpose of examine it)
can look for its character by using: ing.search(‘key’, ‘name_of_character’)
or by its specific values such as: ing.search(‘value’, ‘character_like_name_of_ingredient’)
:param comp: str (‘key’ or ‘value’)
:param key: str (what to look for - can be left empty to get the full list)
:return: False if did not found, else print results of the search


#### _property_ serial()

#### _property_ temp()

#### _property_ typeo()
