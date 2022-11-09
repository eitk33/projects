import csv
from ing import Ing
from cs50 import SQL
import random
db = SQL("sqlite:///formula.db")
with open ('temp.csv', 'r') as file:
     reader = csv.DictReader(file)
     for row in reader:
        if row['typeo']:
            hlb = ''
            ing = Ing()
            setattr(ing, 'name', row['name'])
            name = ing.name
            setattr(ing, 'serial', row['serial'])
            serial = ing.serial
            setattr(ing, 'inci', row['inci'])
            inci = ing.inci
            typeo = row['typeo']
            typeo = typeo.strip('[')
            typeo = typeo.strip(']')
            typeo = str(typeo)
            try:
                setattr(ing, 'typeo', str(typeo))
            except ValueError:
                pass

            if row['hlb']:
                setattr(ing, 'hlb', row['hlb'])
                hlb = ing.hlb
            temp = str(random.randint(31 , 80))
            db.execute('INSERT INTO ingridients(name, serial, inci, typeo, hlb, temp) VALUES (?,?,?,?,?,?)', name, serial, inci, typeo, hlb, temp)
        else:
            pass