# coding=UTF-8
import random 
_word54 = random.shuffle
import os
_word55 = os.path.exists

from kivy.app import App as _word56
from kivy.uix.button import Button as _word57
from kivy.uix.label import Label as _word58
from kivy.uix.popup import Popup as _word59
from kivy.graphics import Color as _word60
from kivy.graphics import Rectangle as _word61
from kivy.core.window import Window as _word62
from kivy.uix.boxlayout import BoxLayout as _word63
_word58._word64 = _word58.pos
_word58._word65 = _word58.bind
#כתווית.הבד = כתווית.canvas
_word57._word65 = _word57.bind
_word63._word66 = _word63.add_widget
_word59.open = _word59.open
_word56._word67 = _word56.stop 
_word56._word68 = _word56.run 
_word56._word69 = _word56.build
_word70 = "./DroidSans.ttf"

def _word71(_word72):
    return[[_word72[1][0], _word72[0][0]], [_word72[1][1], _word72[0][1]]]

def _word73(_word74):
    return [[_word74[0], _word74[1]], [_word74[2], _word74[3]]]

def _word75(_word76, _word77):
    _word78 = []
    for _word79 in range(_word77):
        _word80 = []
        _word81 = []
        for _word82 in range(_word76):
            _word80 = _word80 + ['']
            _word81 = _word81 + ['']
        _word78.append(_word80)
        _word78.append(_word81)
    return _word78

def _word83(_word72, _word84, _word85, _word78):
    _word78[_word84 * 2]    [_word85] = _word72[0][0] + _word72[0][1]
    _word78[_word84 * 2 + 1][_word85] = _word72[1][0] + _word72[1][1]

def _word86(_word84, _word85, _word78):
    _word72 = [['',''],['','']]
    _word72[0][0] = _word78[_word84 * 2][_word85][0]
    _word72[0][1] = _word78[_word84 * 2][_word85][1]
    _word72[1][0] = _word78[_word84 * 2 + 1][_word85][0]
    _word72[1][1] = _word78[_word84 * 2 + 1][_word85][1]
    return _word72

def _word87(_word88, _word89, _word90):
    _word91 = []   
    for _word92 in _word88:
        for _word93 in _word89:
            _word91.append(_word92 + _word93)
    if len(_word91) >= 16:
      return _word91[:_word90]
    return _word87(_word91, _word89, _word90)

def _word94(_word95, _word78):
    _word96 = int(len(_word78) / 2)
    _word76 = len(_word78[0])
    print (_word96, _word76)
    _word54(_word95)
    for _word79 in range(_word96):
        for _word82 in range(_word76):
            _word83(_word95[_word79 * _word76 + _word82], _word79, _word82, _word78)

def _word97(_word78):
    _word98 = []
    for _word99 in range(int(len(_word78) / 2)):
        _word98.append("|".join(_word78[_word99*2]) + "|")
        _word98.append("|".join(_word78[_word99*2 + 1]) + "|")
        _word98.append("--+"*len(_word78[0]))
    return "\n".join(_word98)

def _word100(_word84, _word85, _word78):
    if (_word84 * 2) < len(_word78) and _word85 < len(_word78[0]):
        return True
    return False

def _word101(_word78):
     for _word99 in range(len(_word78)):
         for _word102 in range(len(_word78[0])):
             if _word102 > 0 and (_word78[_word99][_word102][0] != _word78[_word99][_word102-1][1]):
                 return False
             if _word99 % 2 and _word99 < len(_word78) - 1:
                 if (_word78[_word99][_word102] != _word78[_word99+1][_word102]):
                     return False
     return True

def _word103(_word76, _word77):
    _word89 = ['X', 'O']
    _word95 = _word89[:]
    _word104 = _word77 * _word76
    _word95 = _word87(_word95, _word89, _word104)
    _word95 = [_word73(_word79) for _word79 in _word95]
    _word78 = _word75(_word76, _word77)
    _word94(_word95, _word78)
    return _word78

class _word105(_word56): 
    def _word106(self):
                self._word107.text ="Level: "+ str(self._word108)

    def _word109(self):
                self._word110.text = "Score: "+str(self._word111)

    def _word112(self):
            _word113 = open("./status.txt", "wb")
            _word113.write(str(self._word108))
            _word113.close()

    def _word114(self):
        if _word55("./status.txt"): 
            _word115 = open("./status.txt").read()
            _word116 = _word115.split("\n")
            self._word108 = int(_word116[0])
        else:
            self._word108 = 0
            self._word112()
        self._word117()
        
    def _word118(self, _word119):
        _word119._word64 = _word119.pos
        #להדפיס ("START:", המגע.מיקום)
        _word120 = self._word121._word64[1]
        if (_word119._word64[1] - _word120) > 0:
            self._word122 = int(_word119._word64[0] / (self._word123 * 2))
            self._word124 = int((_word119._word64[1] - _word120) / (self._word125 * 2))
        else:
            self._word122 = -1
            self._word124 = -1

    def _word126(self, _word119):
        _word120 = self._word121._word64[1]
        if self._word127:
            return
        if self._word124 == -1 or self._word122 == -1:
            return
        _word128 = int(_word119._word64[0] / (self._word123 * 2))
        _word129 = int((_word119._word64[1] - _word120) / (self._word125 * 2))
        #להדפיס ("END:", המגע.מיקום)
        if _word128 == self._word122 and _word129 == self._word124:
            _word85 = _word129
            _word84 = _word128
            if _word100(_word84, _word85, self._word78):
                _word72 = _word86 (_word84, _word85, self._word78)
                _word72 = _word71(_word72)
                _word83(_word72, _word84, _word85, self._word78)
                self._word127 = _word101(self._word78)
                self._word130(self._word78, self._word121)
                self._word111 = self._word111+1
                self._word110.text = str(self._word111)
        else:
            _word131 = self._word122
            _word132 = self._word124
            _word133 = _word128
            _word134 = _word129
            #להדפיס ("להזיז משורה", שורת_מקור, "וטור", טור_מקור, "אל שורה", שורת_יעד, "וטור", טור_יעד)
            if _word100(_word131, _word132, self._word78) and _word100(_word133, _word134, self._word78):
                #להדפיס("מזיזים")
                _word135 = _word86(_word131, _word132, self._word78)
                _word136 = _word86(_word133, _word134, self._word78)
                _word83(_word135, _word133, _word134, self._word78)
                _word83(_word136, _word131, _word132, self._word78)
                self._word127 = _word101(self._word78)
                self._word130(self._word78, self._word121)
                self._word111 = self._word111+1
                self._word109()
        self._word122 = -1
        self._word124 = -1

    def _word130(self, _word78, _word121):
        _word121._word137 = _word121.canvas
        _word121._word137.clear()
        _word77 = len(_word78)
        _word76 = len(_word78[0])
        _word120 = self._word121._word64[1]
        #להדפיס("בסיס הלוח=", בסיס_הלוח)
        for _word99 in range(_word77):
            for _word138 in range(_word76):
                for _word139 in range(2):
                    with _word121._word137:
                        if _word78[_word99][_word138][_word139] == 'X':
                            _word60(0.8, 0.8, 1.0)
                        else:
                            _word60(0, 0, 1.0)
                        _word61(pos=(_word99 * self._word123, (_word138 * 2 + _word139) * self._word125 + _word120), size=(self._word123, self._word125))
        if not self._word127:
            for _word99 in range(_word77):
                if not _word99 % 2:
                    with _word121._word137:
                        _word60(0.0, 0.0, 0.0)
                        _word61(pos=(0, self._word125 * _word99 + _word120), size=(_word76 * self._word123 * 2, 4))
            for _word102 in range(_word76):
                with _word121._word137:
                    _word60(0.0, 0.0, 0.0)
                    _word61(pos=(self._word123 * _word102 * 2, 0 +_word120), size=(4, _word77 * self._word125))
        else:
            self._word140()
    
    def _word140(self):   
            self._word108 = self._word108 + 1
            self._word106()
            self._word112()
            _word141 = "Wonderful!"
            _word142 = _word58(text=_word141, size=(20,40))
            _word143 = _word59(title="", content=_word142, size_hint=(0.25,0.1))
            _word143.on_dismiss = self._word144
            _word143.open()

    def _word117(self):
        if self._word108 >= 0:
            self._word77 = 2
            self._word76 = 2
        if self._word108 >= 2:
            self._word77 = 3
            self._word76 = 3
        if self._word108 >= 4:
            self._word77 = 4
            self._word76 = 4

    def _word144(self, _word145=None):
        self._word117()
        self._word111 = 0
        self._word106()
        self._word109()
        self._word125 = _word62.width / (self._word77 * 2)
        self._word123 = self._word125
        self._word122 = -1
        self._word124 = -1
        _word78 = _word103(self._word76, self._word77)
        self._word127 = False
        self._word130(_word78, self._word121)
        self._word78 = _word78        

    def _word146(self, _word79, _word82):
        self._word130(self._word78, self._word121)

    def _word147(self, _word145=None):
        _word148 = """
QBits!
Drag squares or rotate them.
Match white to white, blue to blue.
Screen will freeze when you succeed."""
        _word149 = _word58(text=_word148, size=(200,200))
        _word143 = _word59(title="Instructions", content=_word149, size_hint=(0.5,0.5))
        _word143.open()

    def _word150(self, _word145=None):
        self._word67()

    def build(self):
        self._word114()
       
        self._word111 = 0
        self._word125 = _word62.width / (self._word77 * 2)
        self._word123 = self._word125
        self._word151 = _word63(orientation='vertical')
        _word152 = _word63(orientation='horizontal', size_hint=(1.0,0.1))
        _word153 = _word63(orientation='horizontal', size_hint=(1.0,0.1))
        self._word121 = _word58(size_hint=(1.0, 0.5))
        self._word110 = _word57(text="")
        self._word107 = _word57(text="")

        self._word144()
        self._word121.on_touch_down = self._word118
        self._word121.on_touch_up = self._word126
        self._word154 = _word57(size_hint=(1.0, 0.1))

        self._word154.background_down = "./media/QbitsTitle.jpg"
        self._word154.background_normal = "./media/QbitsTitle.jpg"
        self._word110.background_down = "atlas://data/images/defaulttheme/button"
        self._word107.background_down = "atlas://data/images/defaulttheme/button"
        self._word155 = _word57(text='Reset' , font_name=_word70)
        self._word155._word65(on_press=self._word144)
        self._word156 = _word57(text='Quit' , font_name=_word70)
        self._word156._word65(on_press=self._word150)
        self._word157 = _word57(text='Instructions' , font_name=_word70)
        self._word157._word65(on_press=self._word147)
        self._word151._word66(self._word154)
        self._word151._word66(self._word121)
        _word152._word66(self._word110)
        _word152._word66(self._word107)
        self._word151._word66(_word152)
        _word153._word66(self._word157)
        _word153._word66(self._word155)
        _word153._word66(self._word156)
        self._word151._word66(_word153)
        self._word121._word65(size=self._word146)
        return self._word151
       

if (__name__ == "__main__") :
    _word105()._word68()


# לערבב_אקראית = _word54
# אכן_קיים_הקובץ = _word55
# כיישום = _word56
# ככפתור = _word57
# כתווית = _word58
# כחלון_קופץ = _word59
# כצבע = _word60
# כמרובע = _word61
# כחלון = _word62
# כתבנית_קופסה = _word63
# מיקום = _word64
# לקשור = _word65
# להוסיף_רכיב = _word66
# לעצור = _word67
# להריץ = _word68
# לבנות = _word69
# גופן_עברית = _word70
# לסובב_ימינה = _word71
# האריח = _word72
# לעצב_כריבוע = _word73
# הרצף = _word74
# לייצר_את_הלוח = _word75
# רוחב_הלוח = _word76
# גובה_הלוח = _word77
# הלוח = _word78
# א = _word79
# השורה0 = _word80
# השורה1 = _word81
# ב = _word82
# למקם_אריח = _word83
# השורה = _word84
# הטור = _word85
# לקבל_אריח = _word86
# לייצר_אריחים = _word87
# הרשימה = _word88
# הקוביות = _word89
# היעד = _word90
# הרשימה_החדשה = _word91
# איבר = _word92
# קוביה = _word93
# לפזר_על_הלוח = _word94
# האריחים = _word95
# אורך_הלוח = _word96
# להדפיס_את_הלוח = _word97
# פלט = _word98
# ש = _word99
# הלחיצה_בתוך_הלוח = _word100
# המשחק_הסתיים = _word101
# ט = _word102
# לאתחל_את_הלוח = _word103
# מספר_האריחים = _word104
# כיישום_שלי = _word105
# לעדכן_כפתור_הרמה = _word106
# כפתור_הרמה = _word107
# הרמה = _word108
# לעדכן_כפתור_הניקוד = _word109
# כפתור_הניקוד = _word110
# הניקוד = _word111
# לעדכן_סטטוס = _word112
# ק = _word113
# לקרוא_סטטוס = _word114
# גלם = _word115
# שורות = _word116
# לקבוע_את_מימדי_הלוח = _word117
# לטפל_בנגיעה = _word118
# המגע = _word119
# בסיס_הלוח = _word120
# התווית = _word121
# נקודת_הרוחב_של_המגע = _word122
# רוחב_תא = _word123
# נקודת_הגובה_של_המגע = _word124
# גובה_תא = _word125
# לטפל_בסיום_נגיעה = _word126
# המשחק_אכן_הסתיים = _word127
# נקודת_הרוחב_של_סיום_המגע = _word128
# נקודת_הגובה_של_סיום_המגע = _word129
# לצייר_את_הלוח = _word130
# שורת_מקור = _word131
# טור_מקור = _word132
# שורת_יעד = _word133
# טור_יעד = _word134
# אריח_המקור = _word135
# אריח_היעד = _word136
# הבד = _word137
# תא = _word138
# מ = _word139
# לטפל_בסיום_רמה = _word140
# ההודעה = _word141
# תווית_ההודעה = _word142
# חלון_קופץ = _word143
# לאתחל_מחדש = _word144
# הכפתור = _word145
# לצייר_לראשונה = _word146
# להציג_הוראות = _word147
# ההוראות = _word148
# תווית_ההוראות = _word149
# לפרוש = _word150
# התבנית = _word151
# תבנית_הכפתורים1 = _word152
# תבנית_הכפתורים2 = _word153
# כפתור_הכותרת = _word154
# כפתור_לאתחל_מחדש = _word155
# כפתור_לפרוש = _word156
# כפתור_הוראות = _word157