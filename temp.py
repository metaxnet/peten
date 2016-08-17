# coding=UTF-8
import random
_word1 = ['''

  +---+
  |   |
      |
      |
      |
      |
=========''', '''

  +---+
  |   |
  0   |
      |
      |
      |
=========''', '''

  +---+
  |   |
  0   |
  |   |
      |
      |
=========''', '''

  +---+
  |   |
  0   |
 /|   |
      |
      |
=========''', '''

  +---+
  |   |
  0   |
 /|\  |
      |
      |
=========''', '''

  +---+
  |   |
  0   |
 /|\  |
 /    |
      |
=========''', '''

  +---+
  |   |
  0   |
 /|\  |
 / \  |
      |
=========''']
_word2 = 'כלב חתול ארנבת היפופוטמ'.split(" ")

def _word3(_word2):
    # הפונקציה הזו מחזירה מחרוזת אקראית מתוך רשימת המילים המועברת אליה.
    _word4 = random.randint(0, len(_word2) - 1)
    return _word2[_word4]
    
def _word5(_word1, _word6, _word7, _word8):
    print(_word1[len(_word6)])
    print()
    print("האותיות השגויות:", end=" ")
    for _word9 in _word6:
        print(_word9, end=" ")
    print()
    _word10 = "_" * len(_word8)    
    for _word11 in range(len(_word8)): #להחליף רווחים באותיות שנוחשו נכון.
        if _word8[_word11] in _word7:
            _word10 = _word10[:_word11] + _word8[_word11]+_word10[_word11+1:]

    for _word9 in _word10: #להציג את מילת הסוד עם רווחים בין האותיות
        print (_word9, end=" ")
    print()

def _word12(_word13):
    # מחזירה את האות שהשחקן הקליד. הפונקציה מוודאת שהשחקן הקליד אות בודדת ולא משהו אחר.
    while True:
        print ("נחש אות.")
        _word14 = input()
        _word14 = _word14.lower()
        if len(_word14) != 1:
            print("נא להקליד אות בודדת.")
        elif _word14 in _word13:
            print("כבר ניחשת את האות הזה. נסה שוב.")
        elif _word14 not in "אבגדהוזחטיכלמנסעפצקרשת":
            print("נא להקליד אות.")
        else:
            return _word14

def _word15():
    # הפונקציה הזו מחזירה אמיתי אם השחקן רוצה לשחק שוב. אחרת היא מחזירה שיקרי.
    print("האם תרצה לשחק שוב? (כן או לא)")
    return input().lower().startswith("כ")

print ("ה ת ל י י ן")
_word6 = ""
_word7 = ""
_word8 = _word3(_word2)
_word16 = False

while True:
    _word5(_word1, _word6, _word7, _word8)
   
    #להזמין את השחקן להקליד אות
    _word14 = _word12(_word6+_word7)

    if _word14 in _word8:
        _word7 = _word7 + _word14

        #בדוק אם השחקן ניצח
        _word17 = True
        for _word11 in range(len(_word8)):
            if _word8[_word11] not in _word7:
                _word17 = False
                break
        if _word17:
            print("כן! מילת הסוד היא '" + _word8 + "'! ניצחת!")
            _word16 = True

    else:
        _word6 = _word6 + _word14
        # לבדוק אם השחקן ניחש יותר מדי פעמים והפסיד.
        if len(_word6) == len(_word1) - 1:
            _word5(_word1, _word6, _word7, _word8)
            print("נגמרו לך הניחושים!\nאחרי "+_word18(len(_word6)) + " ניחושים שגויים ו "+_word18(len(_word7))+ "ניחושים נכונים. המילה היתה '"+ _word8 + "'")
            _word16 = True

    #לשאול את השחקן אם הוא רוצה לשחק שוב, אבל רק אם המשחק הסתיים.
    if _word16:
        if _word15():
            _word6 = ""
            _word7 = ""
            _word16 = False
            _word8 = _word3(_word2)
        else:
            break


### PETEN TRANSLATION COMMENTS ###
### PETEN TRANSLATION COMMENTS #### המונח_בעברית = python_or_english_translation### END OF TRANSLATION COMMENTS ###
# תמונות_התליין = _word1
# רשימת_המילים = _word2
# לקבל_מילה_אקראית = _word3
# מספר_המילה = _word4
# להציג_לוח = _word5
# אותיות_שגויות = _word6
# אותיות_נכונות = _word7
# מילת_הסוד = _word8
# אות = _word9
# רווחים = _word10
# א = _word11
# לקבל_ניחוש = _word12
# ניחושים_עד_כה = _word13
# הניחוש = _word14
# לשחק_שוב = _word15
# המשחק_הסתיים = _word16
# כל_האותיות_נמצאו = _word17
# מחרוזת = _word18
### END OF TRANSLATION COMMENTS ###