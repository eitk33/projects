from ing import Ing
from demo1 import Phase
from demo3 import Formula
from datetime import date
from cs50 import SQL
import sys


db = SQL("sqlite:///formula.db")

ing = Ing("sls", "sodlasu","2006523", '55',"anti aging_active")
ing2 = Ing("sci", "sci","2006563", "35","active")
ing3 = Ing("BG", "BG","2007843", "10","active")
ing4 = Ing('CA', 'cetyl alcohol', '2013565', '5', 'condition', '5')

ing5 = Ing('montanov 68', 'cetyl monta', '2013564', '5', 'emulsifier', '10')
ing6 = Ing('montanov 202', 'kaka', '2013544', '5', 'emulsifier', '9')
ing7 = Ing('ipm', 'pipi', '2019544', '5', 'condition', '3')

phase = Phase("P1")
phase2 = Phase('P2')
phase.adding(ing6, "10")
phase.adding(ing7, "5")
phase.adding(ing, "10")
phase.adding(ing2, "58")
phase.adding(ing3, "55")
phase.adding(ing3, "33")
phase2.adding(ing4, '7')
phase2.adding(ing5, '8')

x = Formula()
x.adding_phase(phase)

x.adding_phase(phase2)
check = ''
check = db.execute('SELECT name from formula')
counter = 0
a = ''
name = x.name_formula
for i in check:
    print((name))
    a = i['name'].split('.', 1)[0]
    print(a)
    if name == a:
        print('does')
        counter += 1
        name = x.name_formula  + '-' + str(counter)
cus = input("Name of customer: ")
pro = input('Name of prodcut: ')
name = name + '. ' + cus + '. ' + pro
mylist = []
for item in x.phase:
    mylist.append(str(item))
mylist = str(mylist)
#print(mylist)
db.execute("INSERT INTO formula (phase, hlb_em, hlb_ing, name) values (?, ?, ?, ?)", mylist, x.hlb_em, x.hlb_ing, name)