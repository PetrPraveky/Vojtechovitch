import json
import os
import operator
import math

#Třída kalkulac
def calc_connected():
    print("     calculations.py")

class OpenFile():
    #Otevření "data.json" souborů
    global locale_file, data, locale, locale_default #Registrování proměnných
    with open(os.path.join('','data.json'), "r") as g: #Otevření dat
        data = json.load(g) #Načtení dat
        g.close() #Zavření původního souboru
    

class BasicCalculator():
    def BC_number_sort(self, number):
        number_list = []
        number_var = ""
        if number == "":
            return "0"
        else:
            if number[-1] in data['operators_chars']:
                number = number[:-1]
            n = 0
            while n < len(number):
                try:
                    if int(number[n]) in data['number_list']:
                        number_var += number[n]
                        n += 1
                except:
                    if number[n] == ".":
                        number_var += number[n]
                        n += 1
                    elif number[n] in data['operators_chars'] or number[n] in data['add_operators_char']:
                        number_list.append(number_var)
                        number_list.append(number[n])
                        number_var = ""
                        n += 1
                    else:
                        n += 1
                        pass
            number_list.append(number_var)
            m, lbr, rbr, br_var = 0, 0, 0, 0
            while m < len(number):
                if number[m] == "(":
                    lbr += 1
                    m += 1
                elif number[m] == ")":
                    rbr += 1
                    m += 1
                else:
                    m += 1  
            n = 0
            while n < len(number_list):
                if number_list[n] == "":
                    number_list.pop(n)
                    n += 1
                else:
                    n += 1
            if lbr > rbr:
                br_var = lbr-rbr
                n = 0
                while n < br_var:
                    number_list.append(')')
                    n += 1 
            print(number_list)
            
            """for entry in number_list:
                if entry in data['operators_chars']:
                    print('1')
                elif entry in data['add_operators_char']:
                    print('3')
                else:
                    try:
                        int(entry)
                        print(2)
                    except:
                        pass"""
            
            return "1"
    
    def BC_number_input(self, number):
        return number