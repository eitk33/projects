import re
from ing import Ing
import inspect
class Phase():
    def __init__(self, name, temp=31, grind=['no', '0 RPM'], stir=['yes', '30 RPM'], time=5):
        self.name = name
        self.ingr = []
        self.temp = temp
        self.grind = grind
        self.stir = stir
        self.time = time
    def __str__(self):
        newlist = []
        sublist = []
        newdict = {}
        lol = str()
        fin = str()
        #        return str(self.time)
        for item in (self.ingr):
            lol = str()
            print(item)
            for k, v in item.items():
                if v:
                    sublist.append({k: v})
            newlist.append(sublist)
            #temp = f"{key}: {value}, "
            #lol += temp
            #fin += lol + '\n'
        grind = self.list_mod(self.grind)
        stir = self.list_mod(self.stir)
        newdict.update(grind)
        newdict.update(stir)
        return (f"{str(newlist)}\nname: {self.name}\ntemp: {self.temp}\ngrind: {grind}\nstir: {stir}\ntime: {self.time}")
    def list_mod(self, s):
        if s[0] == 'yes':
            return s[0] + " " + s[1]
        return s[0]
    def adding(self, s, am):
        self.am_veri(am)
        if isinstance(s, Ing):
            r = self.usedict(s)
            temp_dict = {'weight': am}
            for item in self.ingr:
                if item:
                    if (s.search('key', 'serial')) == item['serial']:
                        item['weight'] = am
                        return
                    else:
                        pass
            r.update(temp_dict)
            x = r.copy()
            for k,v in r.items():
                if not v:
                    del x[k]
            self.ingr.append(x)

#                self.ingr[s] = r
    def update(self, s, am):
        self.am_veri(am)
        if isinstance(s, Ing):
            s = self.usedict(s)
            temp_dict = {'weight': am}
            s.update(temp_dict)
            if s['serial'] in self.ingr:
                raise ValueError('alrdy have')
            self.ingr.append(s)
    def am_veri(self, s):
        try:
            s = int(s)
        except ValueError:
            raise ValueError("amount must be an int")
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        if not re.search(r"^(P\d\d?)$", name):
            raise ValueError("only P(Number) is valid")
        self._name = name
#    @property
#    def ingr(self):
#        return self._ingr
#    @ingr.setter
#    def ingr(self, ingr):
#        pass
        #לבדוק שהאינגר נמצא כאינסטנס של אינג
    @property
    def temp(self):
        return self._temp
    @temp.setter
    def temp(self, temp):
        try:
            temp = int(temp)
        except ValueError:
            return("temp must be an int")
        if not 30 < temp < 90:
            raise ValueError("temp must be 30 <temp <90")
        self._temp = temp
    @property
    def grind(self):
        return self._grind
    @grind.setter
    def grind(self, grind):
        if not grind[0] == 'yes' and not grind[0] == 'no':
            raise ValueError("first arg of grind must be yes or no")
        if not re.search(r"[0-9][0-9]?[0-9]?[0-9]?\sRPM", grind[1]):
            raise ValueError("grind format: (number) RPM")
        self._grind = grind
    @property
    def stir(self):
        return self._stir
    @stir.setter
    def stir(self, stir):
        if not stir[0] == 'yes' and not stir[0] == 'no':
            raise ValueError("first arg of stir must be yes or no")
        if not re.search(r"[0-9][0-9]?[0-9]?[0-9]?\sRPM", stir[1]):
            raise ValueError("stir format: (number) RPM")
        self._stir = stir
    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, time):
        if not re.search(r"\d\d?\d?", str(time)):
            raise ValueError("time must be 1-digit min to 3-digit max")
        try:
            time = int(time)
        except ValueError:
            return("time must be an int")
        self._time = time
    def usedict(self, s):
        mydict = {}
        for _,var in vars(s).items():
            _ = _.strip("_")
            temp_dict = {_ : var}
            mydict.update(temp_dict)
        return mydict

#class IngAdd(Ing):
#    def __init__(self, name, inci, serial, temp, phil, type, remarks, concen, inco, sup, manu, weight=0):
#        super().__init__( name, inci, serial, temp, phil, type,remarks, concen, inco, sup, manu)
#        self.weight = weight

def main():
    phase = None
    ing = Ing("sls", "sodlasu","2006523", '55',"anti aging_active")
    ing2 = Ing("sci", "sci","2006563", "35","active")
    ing3 = Ing("BG", "BG","2007843", "10","active")
    ing4 = Ing('CA', 'cetyl alcohol', '2013565', '5', 'condition', '5')

    ing5 = Ing('montanov 68', 'cetyl monta', '2013564', '5', 'emulsifier', '10')
    phase = Phase("P1")
    phase2 = Phase('P2')
    phase.adding(ing, "10")
    phase.adding(ing2, "58")
    phase.adding(ing3, "55")
    phase.adding(ing3, "33")
    phase2.adding(ing4, '7')
    phase2.adding(ing5, '8')
#    print(phase.ingr)
    print(phase2.ingr)
if __name__ == "__main__":
    main()