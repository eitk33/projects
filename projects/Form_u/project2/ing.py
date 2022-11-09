import re
class Ing:
    ch = ["emulsifier", 'emollient', 'thickner','condition','solubilizer', 'active','structuring agent', 'surfactant', 'SPF', 'film_former']
    def __init__(self, name='', inci='', serial='', temp=40,  typeo='', hlb=None , remarks='', concen='', phil='', incapabilities='', suppliar='', manu=''):
        self.name = name
        self.inci = inci
        self.serial = serial
        self.temp = temp
        self.typeo = typeo
        self.hlb = hlb
        self.remarks = remarks
        self.concen = concen
        self.phil = phil
        self.incapabilities = incapabilities
        self.suppliar = suppliar
        self.manu = manu

    def search(self, comp=(), key = None):
        mydict ={}
        for _,var in vars(self).items():
            mydict[(_).strip('_')] = var
        myreg = key
        if comp == 'key':
            if not key:
                return f"{mydict.keys()}"
            elif re.search(myreg, str(mydict.keys())):
                return f'{mydict[key]}'
            else:
                return False
        elif comp == 'value':
            if not key:
                return f"{mydict.values()}"
            elif re.search(myreg, str(mydict.values())):
                return True
            else:
                return False
        else:
            raise SyntaxError("need to submit at least 'key' or 'value'")
    def __str__(self):
        r = f"name: {self.name}\tinci: {self.inci}\tserial: {self.serial}\n"
        return r
    @property
    def concen(self):
        return self._concen
    @concen.setter
    def concen(self, concen):
        if concen != "":
            if congroup := re.search(r"(\d?\d?\.?\d)-?(\d?\d?\.?\d)?", concen):
                for i in range(1, len(congroup.groups())):
                    try:
                        a = int(congroup.group(i))
                    except ValueError:
                        raise ValueError("concen must be an int")
                    else:
                        if not 0 <= a <= 100 :
                            raise ValueError("must be 0-100")
        self._concen = concen
    @property
    def typeo(self):
        return self._typeo
    @typeo.setter
    def typeo(self, typeo):
        if typeo != "":
            typeo = typeo.split("_")
            for item in typeo:
                if item not in Ing.ch:
                    print(Ing.ch)
                    raise ValueError(str(typeo) + "is not in correct format (for allowed formets, pls use print(format)")
        self._typeo = typeo
#    def format(self):
#        return self.ing.ch
    @property
    def serial(self):
        return self._serial
    @serial.setter
    def serial(self, serial):
        if serial != "":
            try:
                int(serial)
            except ValueError:
                raise ValueError("serial must be an int")
            if len(serial) != 7:
                raise ValueError("serial must be 7 digit")
        self._serial = serial
    @property
    def phil(self):
        return self._phil
    @phil.setter
    def phil(self, phil):
        if phil != "":
            ch1 = ["hydro" , "lipo"]
            if phil not in ch1:
                raise ValueError("phil must be either 'hydro' or 'lipo'")
        self._phil = phil
    @property
    def temp(self):
        return self._temp
    @temp.setter
    def temp(self, temp):
        if temp != "":
            try:
                temp = int(temp)
            except ValueError:
                raise ValueError("temp must be an int")
        self._temp = temp
    @property
    def hlb(self):
        return self._hlb
    @hlb.setter
    def hlb(self, hlb):
        if hlb:
            try:
                hlb = str(hlb)
            except ValueError:
                raise ValueError("hlb must be an int")
        self._hlb = hlb
def main():
#ing = Ing("sls", "sodlasu","2006523", "55","hydro","anti aging_active")
#print(ing)
#print(ing.search())
#name='', inci='', serial='', temp=40,  type='', hlb=None , remarks='', concen='', phil='', incapabilities='', suppliar='', manu=''


    ing5 = Ing('montanov 68', 'cetyl monta', '2013565', '5', 'emulsifier', '10')
    print(ing5.hlb)
if __name__ == "__main__":
    main()