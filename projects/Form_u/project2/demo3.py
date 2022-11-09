import re
from ing import Ing
import inspect
from phase import Phase
from datetime import date
class Formula():
    def __init__(self):
        self.phase = []
        self.hlb_em = None
        self.hlb_ing = None
        y, m, d = str(date.today()).split('-')
        self.name_formula = y + m + d
    def __str__(self):
        new_list = []
        temp_dict = {}
        for items in self.phase:
            for item in items.ingr:
                tempitem = item.copy()
                for k,v in item.items():
                    if not v:
                        del tempitem[k]
                new_list.append(tempitem)
        new_list = str(new_list)
        return f'{new_list} hlb_ing: {self.hlb_ing:.2f}\nhlb_em: {self.hlb_em:.2f}'
    def adding_phase(self, s):
        if isinstance(s, Phase):
            self.phase.append(s)
            self.hlb_update()
    def hlb_cal(self, s=None):
        w_tot = 0
        hlb_tot = 0
        hlb_f = None
        for items in (self.phase):
            for item in vars(items)['ingr']:
                for key, value in item.items():
                    if key == 'hlb' and value and 'typeo' in item:
                        if s:
#                            print(str(s))
                            if s in item['typeo']:
#                                print(str(s))
                                w = float(item['weight'])
                                hlb = float(value) * w
                                w_tot += w
                                hlb_tot += hlb
                        elif not s and not 'emulsifier' in item['typeo']:
                            w = float(item['weight'])
                            hlb = float(value) * w
                            w_tot += w
                            hlb_tot += hlb
                        else:
                            pass
                            #print(str(s))
        if w_tot != 0:
            hlb_f = (hlb_tot/w_tot)
        return hlb_f
    def hlb_update(self):
        self.hlb_em = self.hlb_cal('emulsifier')
        self.hlb_ing = self.hlb_cal()

def main():
    phase = None
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
#    phase2.adding(ing4, '7')
#    phase2.adding(ing5, '8')
    formula = Formula()
    formula.adding_phase(phase)
    formula.adding_phase(phase2)
#    print(phase)
#    print(phase2)
#    print((ing5))
    print(formula)
#    print(ing3.search('key', 'serial'))
if __name__ == "__main__":
    main()