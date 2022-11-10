# ing module


### _class_ ing.Ing(name='[str]', inci='[str]', serial='[int]', temp=40[int], typeo='[str]', hlb=None[int], remarks='[str]', concen='', phil='', incapabilities='', suppliar='', manu='')


#### search(comp=(), key=None)
    used to search ingredient by all kind of filters (for the purpose of examine it)
    can look for its character by using: ing.search(‘key’, ‘name_of_character’)
    or by its specific values such as: ing.search(‘value’, ‘character_like_name_of_ingredient’)

    :param comp: str (‘key’ or ‘value’)

    :param key: str (what to look for - can be left empty to get the full list)

    :return: False if did not found, else print results of the search


[Index](../index.md)