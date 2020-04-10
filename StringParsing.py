from tkinter import *
from GeoIP2.geoip2.database import *
from pyperclip import *
# from myutils import *

def isIP(stroka):
    """True если строка stroka является IP адресом"""
    main_list = stroka.split('.')
    if len(main_list) == 4:
        try:
            for i in range(0, 4):
                if len(main_list[i]) <= 3:
                    if int(main_list[i]) > 255 or int(main_list[i]) < 0:
                        return False
                else:
                    return False
        except ValueError:
            return False
        return True
    else:
        return False

def getIPList(s):
    """получение IP адресов из строки"""
    main_list = s.split('\n')
    inner_list = []
    ip_list = []
    for i in range(0, len(main_list)):
        main_list[i] = main_list[i].split(';')
        for j in range(0, len(main_list[i])):
            if isIP(main_list[i][j]):
                main_list[i][j] = main_list[i][j].split('.')
                if [main_list[i][j][0], main_list[i][j][1]] not in inner_list:
                    ip_list.append([main_list[i][0],
                                    main_list[i][j][0] + '.' + main_list[i][j][1] + '.' + main_list[i][j][2] + '.' +
                                    main_list[i][j][3]])
                    inner_list.append([main_list[i][j][0], main_list[i][j][1]])
    return ip_list


def ShowUniqueIPsClick():
    outputText.delete(1.0, END)
    stroka = inputText.get(1.0, END)
    ip_list = getIPList(stroka)
    if len(ip_list) != 0:
        reader = Reader(
            'GeoIP2/GeoLite2-City_20190416/GeoLite2-City.mmdb')
        for i in ip_list:
            try:
                response = reader.city(i[1])
                stroka = ''
                try:
                    stroka = i[0] + ' ' + i[1] + ' ' + response.country.name
                except TypeError:
                    stroka = i[0] + ' ' + i[1] + ' Unknown country'
                try:
                    if response.country.iso_code == 'RU':
                        stroka += ', ' + response.city.name
                except TypeError:
                    pass
            except geoip2.errors.AddressNotFoundError:
                stroka = i[1] + ' Unknown IP'
            outputText.insert(END, stroka + '\n')
        copy(outputText.get(1.0, END))
        outputText.insert(END, '-------------\nCopied!')
    else:
        outputText.insert(END, 'IP adresses not found!')


def PasteClick():
    inputText.delete(1.0, END)
    inputText.insert(1.0, paste())
    inputText.insert(END, '\n-------------\nPasted!')


def CheckIPClick():
    outputText.delete(1.0, END)
    stroka = inputText.get(1.0, '1.end')
    if isIP(stroka):
        reader = Reader(
            'GeoIP2/GeoLite2-City_20190416/GeoLite2-City.mmdb')
        try:
            response = reader.city(stroka)
            # ToDo
            # stroka = response.location.latitude
            # stroka = response.location.longitude
            try:
                stroka = ''
                stroka += response.country.name
            except TypeError:
                stroka = 'Unknown country'
            try:
                if response.country.iso_code == 'RU':
                    stroka += ', ' + response.city.name
            except TypeError:
                pass
        except geoip2.errors.AddressNotFoundError:
            stroka = ' Unknown IP'
        outputText.delete(1.0, END)
        outputText.insert(END, stroka + '\n')
        copy(outputText.get(1.0, END))
        outputText.insert(END, '-------------\nCopied!')
    else:
        outputText.delete(1.0, END)
        outputText.insert(1.0, 'Unknown IP format!')



root = Tk(className=' Check IP utility')

buttonPaste = Button(root, text="Paste", command=PasteClick)
buttonPaste.pack()

buttonOK = Button(root, text="Show unique IPs", command=ShowUniqueIPsClick)
buttonOK.pack()

buttonCheckIP = Button(root, text="Check IP", command=CheckIPClick)
buttonCheckIP.pack()

inputText = Text(root)
inputText.pack()
outputText = Text(root, bg='lightgrey')
outputText.pack()

root.mainloop()
