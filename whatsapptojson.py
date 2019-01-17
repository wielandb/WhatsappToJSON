import json
import sys
import codecs
import hashlib
import glob
 
 
def setup():
    chat_dictionary = {}
    if (len(sys.argv) == 5):
        txtfile = sys.argv[0]
    else:
        #txtfile = str(raw_input("Please specify the WhatsApp Chat .txt-File:"))
        txtfile = "Chat.txt"
 
def isDigit(text):
    text = ''.join([i if ord(i) < 128 else '' for i in text])
    text = str(text)
    if text == "0":
        return True
    if text == "1":
        return True    
    if text == "2":
        return True
    if text == "3":
        return True
    if text == "4":
        return True
    if text == "5":
        return True
    if text == "6":
        return True
    if text == "7":
        return True
    if text == "8":
        return True
    if text == "9":
        return True
    return False
 
def gethash(text):
    import hashlib
    text = ''.join([i if ord(i) < 128 else ' ' for i in text])
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()
 
def istMsgStart(text):
    try:
        #isMsgBegin = True
        if not isDigit(text[0]):
            return False
        if not isDigit(text[1]):
            return False
        if not (str(text[2]) == "."):
            return False
        if not isDigit(text[3]):
            return False
        if not isDigit(text[4]):
            return False
        if not (str(text[5]) == "."):
            return False
        if not isDigit(text[6]):
            return False
        if not isDigit(text[7]):
            return False
        if not (str(text[8]) == ","):
            return False
        if not (str(text[9]) == " "):
            return False
        if not isDigit(text[10]):
            return False
        if not isDigit(text[11]):
            return False
        if not (str(text[12]) == ":"):
            return False
        if not isDigit(text[13]):
            return False
        if not isDigit(text[14]):
            return False
        if not (str(text[15] == " ")):
            return False
        if not (str(text[16] == "-")):
            return False
        if not (str(text[17] == " ")):
            return False
    except IndexError:
        return False
    return True
 
 
def convert(file):
    msg = {"id":"00000000000000000000000000000","nr":-1, "realnr":-1, "day":1, "day_0": "01", "month":1, "month_0":"01", "year":18, "year_full": 2018, "hour":23, "hour_0": "23", "minute": 59, "minute_0":"59", "sender": "(unknown)", "text": "none", "isExcludedMedia":False, "isDeletedMessage": False, "isGroupMetaChange":False}
    chat = [msg, msg, msg]            
 
    message_number = 0
    real_message_number = 0
    chat = []
    with codecs.open(file,'r',encoding='utf8') as f:
        chattxtlines = f.readlines()
    # Hier beginnt die bearbeitung des Textes
    for line in chattxtlines:
        is_real_message = True 
        #line = chattxtlines[nr]
        line = line.replace("\n","").rstrip('\r\n').replace('\n', ' ')
        if istMsgStart(line):
            msg = {"id":"00000000000000000000000000000","nr":-1, "realnr":-1, "day":1, "day_0": "01", "month":1, "month_0":"01", "year":18, "year_full": 2018, "hour":23, "hour_0": "23", "minute": 59, "minute_0":"59", "sender": "(unknown)", "text": "none", "isExcludedMedia":False, "isDeletedMessage": False, "isGroupMetaChange":False}
            msg["nr"] = message_number
            msg["realnr"] = real_message_number
            msg["realnumber"] = real_message_number
            msg["day_0"] = str(line[0:2])
            msg["month_0"] = str(line[3:5])
            msg["year"] = str(line[6:8])
            msg["year_full"] = "20" + msg["year"] #if you are using this in 2118, get a life!
            #msg["raw_line"] = line
            msg["date"] = msg["day_0"] + "." + msg["month_0"] + "." + msg["year_full"]        
            msg["sender"] = line[18:].split(": ")[0]
            msg["hour_0"] = str(line[10:12])
            msg["minute_0"] = str(line[13:15])
            msg["minute"] = int(msg["minute_0"])
            msg["hour"] = int(msg["hour_0"])
            msg["month"] = int(msg["month_0"])
            msg["day"] = int(msg["day_0"])
            msg["time"] = msg["hour_0"] + ":" + msg["minute_0"]
            msg["id"] = gethash(msg["date"] + msg["time"] + msg["text"])
            try:
                msg["text"] = line[18:].split(": ")[1]
            except IndexError:
                msg["text"] = "none"
            if "Diese Nachricht wurde gel" in line:
                msg["isDeletedMessage"] = True
                msg["text"] = "none"
            if "<Medien ausgeschlossen>" in line:
                msg["isExcludedMedia"] = True
                msg["text"] = "none"
                is_real_message = False
            if "Die Sicherheitsnummer von" in line or "Nachrichten in diesem Chat sowie Anrufe sind jetzt mit Ende-zu-Ende-Versch" in line:
                msg["isGroupMetaChange"] = True
                msg["text"] = "none"
                msg["sender"] = "none"
                is_real_message = False       
 
            chat.append(msg)
        else:
            chat[len(chat)-1]["text"] = chat[len(chat)-1]["text"] + "\n" + line 
        print(msg)
        if is_real_message:
            real_message_number += 1
        message_number += 1
        #print("----END OF ONE LINE----")
    newfilename = file
    newfilename = newfilename.replace(".txt", ".json").replace(" ","_")
    newfilename = ''.join([i if ord(i) < 128 else '' for i in newfilename])
    with open(newfilename, "w") as f:
        f.write(json.dumps(chat))    
 
def all():
    for k in glob.glob("WhatsApp*.txt"):
        convert(k)
