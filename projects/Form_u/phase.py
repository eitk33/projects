import re
from ing import Ing


class Phase():
    def __init__(self, name, temp=31, grind=['no', '0 RPM'], stir=['yes', '30 RPM'], time=5):
        self.name = name
        self.ingr = {}
        self.temp = temp
        self.grind = grind
        self.stir = stir
        self.time = time
        self.counter = len(self.ingr.keys())

    def __str__(self):
        """

        :return: dict of the Phase's ingredients and the properties of the phase
        """
        newdict = {}
        newdict['grind'] = self.list_mod(self.grind)
        newdict['stir'] = self.list_mod(self.stir)
        newdict['name'] = self.name
        newdict['time'] = self.time
        newdict['temp'] = self.temp
        return (f"{str(newdict)} {str(self.ingr)}")

    def list_mod(self, s):
        """
        needed for some fixings in the text written
        :param s: self.grind/stir
        :return:
        """
        if s[0] == 'yes':
            return s[0] + " " + s[1]
        return s[0]

    def adding(self, s, am):
        """
        this handles the addition of a new Ing object to phase, and what happens if Ing already in phase
        :param s: Ing object
        :param am: has to be an int.
        :return:
        """

        self.am_veri(am)
        if isinstance(s, Ing):

            # constructing a dict out of the ing object
            r = self.usedict(s)
            temp_dict = {'weight': am}
            x = temp_dict.copy

            # check ig ingredient is already in the phase
            for item in self.ingr.values():
                if item:
                    if (s.search('key', 'serial')) == item['serial']:
                        item['weight'] = am
                        return
                    else:
                        pass
            r.update(temp_dict)
            x = r.copy()
            for item in r.keys():
                if not r[item]:
                    del x[item]
            self.counter += 1

            # numbering how many ingredients in the phase
            self.ingr[self.counter] = x

    def am_veri(self, s):
        try:
            s = int(s)
        except ValueError:
            raise ValueError("amount must be an int")
    # all sorts of getters and setters
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not re.search(r"^(P\d\d?)$", name):
            raise ValueError("only P(Number) is valid")
        self._name = name

    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, temp):
        try:
            temp = int(temp)
        except ValueError:
            return ("temp must be an int")
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
            return ("time must be an int")
        self._time = time

    def usedict(self, s):
        """
        building a dict out of ing object
        :param s: Ing object
        :return: dict
        """
        mydict = {}
        for _, var in vars(s).items():
            _ = _.strip("_")
            temp_dict = {_: var}
            mydict.update(temp_dict)
        return mydict
