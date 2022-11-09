from ing import Ing
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
        """

        :return: printed formula - its ingredients nested within its phases. optionally addition info if relevant
        """
        new_list = []
        more_list = []
        for item in self.phase:
            new_list.append(str(item))
        if self.hlb_ing and self.hlb_em:
            more_list = ['hlb_ing: ' f'{self.hlb_ing:.2f}', 'hlb_em: ' f'{self.hlb_em:.2f}']
        return f'{new_list} {more_list}'

    def adding_phase(self, s):
        """
        adding Phase object to formula
        :param s: Phase object
        :return: none
        """
        if isinstance(s, Phase):
            self.phase.append(s)
            self.hlb_update()

    def hlb_cal(self, s=None):
        """
        calculating HLB if relevant
        :param s: the 'typeo' of the ingredient
        :return: calculated HLB
        """
        w_tot = 0
        hlb_tot = 0
        hlb_f = None
        for items in self.phase:
            for item in vars(items).values():
                if isinstance(item, dict):
                    for d in item.values():

                        # Need to make sure if it's an emulsifier or not
                        if 'hlb' in d and 'typeo' in d:
                            if s:
                                if s in d['typeo']:
                                    w = float(d['weight'])
                                    hlb = float(d['hlb']) * w
                                    w_tot += w
                                    hlb_tot += hlb
                            # in case this is not an emulsifier
                            elif not s and not 'emulsifier' in d['typeo']:
                                w = float(d['weight'])
                                hlb = float(d['hlb']) * w
                                w_tot += w
                                hlb_tot += hlb
                            else:
                                pass
        if w_tot != 0:
            hlb_f = (hlb_tot / w_tot)
        return hlb_f

    def hlb_update(self):
        self.hlb_em = self.hlb_cal('emulsifier')
        self.hlb_ing = self.hlb_cal()
