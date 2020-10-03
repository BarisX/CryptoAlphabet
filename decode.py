# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 04:50:53 2020

@author: Barcode
"""
import PySimpleGUI as sg
import pyperclip
from random import randint
#import pickle
started_indice = 100
alphabet = ['a','b','c','ç','d','e','f','g','ğ','h','ı','i','j','k','l','m','n','o','ö','p','q','r','s','ş','t','u','ü','v','w','x','y','z',' ','.']
encoded = sorted(range(started_indice,started_indice+len(alphabet)))

def NumberToLetter(number):
    #print("Number::",number)
    return alphabet[findLetter(number)]

def findNumber(letter):
    #print(letter)
    for ind,_ in enumerate(alphabet,start=0):
        if str(_) == letter:
            return ind
        else:
            print("Not this:",_)
def findLetter(number):
    #print("Number:",number)
    for ind,_ in enumerate(encoded,start=0):
        #print("fH",number,_)
        if _ == number:
            return ind
        else:
            pass

def changeHS(letter, number):
    #print(letter,number)
    encoded[findNumber(letter)] = number
def changeSH(number, letter):
    alphabet[findLetter(number)] = number
    printHS()
def printHS():
    y=""
    for x in range(0,len(encoded)):
        y+=(str(alphabet[x])+" : "+str(encoded[x])+"\n")
    return y
def Convert(string): 
    arr = []
    b=""
    nstring = [ _ for _ in string[0][::]]
    #print("nstring:",nstring)
    for ind,_ in enumerate(nstring, start=0):
        #print(_)
        b += _
        if (ind+1)%3 == 0:
            #print(b)
            arr.append(int(b))
            b=""
    return arr

def Decode(mlist):
    arr = Convert(mlist)
    #print("x",arr)
    cumle = ""
    for _ in arr:
        #print(_)
        cumle += NumberToLetter(_)
    return cumle
def Encode(mlist):
    #print(mlist)
    number = ""
    for letter in mlist:
        try: number += str(encoded[findNumber(letter)])
        except: pass
    return number

def EmptyStringCheck(str):
    return len(str) > 0

def IsInAlphabet(str):
    return str in alphabet

def CheckThisInEncoded(integer_or_str_number):
    if type(integer_or_str_number) == int: return integer_or_str_number in encoded
    if type(integer_or_str_number) == str: return int(integer_or_str_number) in encoded if integer_or_str_number.isdigit() else False

ThreeDigit = lambda x : int(x) if (999 > int(x) > 100) else 999
    

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
layout = [  
            [sg.Multiline(default_text=printHS(), size=(32, 20), key='-ML1-'),
             sg.Frame("Decrypt, Upload Key, Crypt",
                [
                    [ 
                        sg.Button('Crypt it!', size=(24, 2))
                    ],
                    [
                      
                        sg.Multiline(size=(26, 6)) #0
                    ],
                    [ 
                        sg.Button('Decrypt'), sg.InputText(size=(20, 2)) #1
                    ],
                    [  
                        
                        sg.Input(tooltip="Install key text file.", size=(20, 2)),
                        sg.FileBrowse('Open'),
                        sg.Button('Load',size=(4, 1))
                    ],
                    [ 
                        sg.Button('Change'),
                        sg.InputText(tooltip="Put a letter which is want to change.",size=(8, 2)),
                        sg.InputText(tooltip="Put a 3 digit number which is equal a letter.",size=(8, 2)), #5
                        sg.Button('Add')
                    ],
                    
                ]),
            ],
            [sg.Button('Save as key.txt', size=(30, 9)), sg.Button('Exit', size=(30, 9))]]
text = []
# Create the Window
if len(encoded) == len(alphabet):
    window = sg.Window('Crypt Alphabet', layout)
else: print("Error: Indices are not equal\n",len(encoded), len(alphabet))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    #print('You entered ', values[0])
    if event == 'Crypt it!':
        #print(len(values[0]))
        if len(values[0]) > 1:
            sg.popup_ok("Copied to the clipboard.\n",Encode(values[0]))
            pyperclip.copy(Encode(values[0]))
        else: sg.popup_ok("Write something..")
    if event == 'Decrypt':
        if len(values[1]) > 1:
            text.append(values[1])
            sg.popup('Decrypt copied to the clipboard.', Decode(text[-1:])) # text always getting last element for next elements
        else: sg.popup_ok("Enter the crypted text")
    
    if event == 'Change' and EmptyStringCheck(values[4]) and EmptyStringCheck(values[3]):
        if not str(values[3]) in alphabet: sg.popup_error('This is not in alphabet.\n',values[3]) # Checking char in list
        else : 
            changeHS(str(values[3]),int(values[4]))
            window['-ML1-'].update(printHS())
    elif event == 'Change': sg.popup_error("Boxes are empty.")

    if event == 'Add' and EmptyStringCheck(values[4]) and EmptyStringCheck(values[3]):
        #print(len(values[3]),len(values[4]),CheckThisInEncoded(values[4]),IsInAlphabet(values[3]),EmptyStringCheck(values[3]))
        if IsInAlphabet(values[3]) and EmptyStringCheck(values[3]): sg.popup_error('This letter already in alphabet.\n',values[3]) # Checking char in list 
        elif CheckThisInEncoded(values[4]) and EmptyStringCheck(values[4]): 
            sg.popup_error('This number was using from another letter or char.\nWe just add it with random number\n',values[4]) # Checking code in encoded list
            while True:
                random_number = randint(100, 999) # Only 3 digits working with 
                #print(random_number)
                if not random_number in encoded:
                    encoded.append(ThreeDigit(random_number))
                    break
            alphabet.append(values[3])
        elif not CheckThisInEncoded(values[4]) and not IsInAlphabet(values[4]):
            #print(values[4],IsInAlphabet(values[4]),EmptyStringCheck(values[4]))
            encoded.append(ThreeDigit(values[4])) # Protection from another digits
            alphabet.append(values[3])
            sg.popup_ok("Success.")
        #print(alphabet,encoded)
        window['-ML1-'].update(printHS())
    elif event == 'Add': sg.popup_error("Boxes are empty.")

    if event == "Save":
        with open('key.txt', 'w') as f:
            for item in encoded:
                f.write("%s" % item)
        with open("key.txt", "r") as f:
            if not f: sg.popup_ok('Load is success.') # checking writing

    if event == "Load":
        if values[2]:
            empty_list = []
            with open(values[2], 'r') as f:
                empty_list = Convert(f.readlines())
                #print(empty_list)
                if empty_list: 
                    sg.popup_ok('Load is success.') # Checking reading
                    encoded = empty_list
                    window['-ML1-'].update(printHS())
                else: sg.popup_error('Error while reading file.\n',values[1]) # Checking reading
                f.close()
        else: sg.popup_ok("Choose a file.")

window.close()
