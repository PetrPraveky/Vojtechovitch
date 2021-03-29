import json
import os
import operator
import math
from itertools import cycle
import time

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
        time_start = time.time()
        
        number_list = []
        number_var = ""
        if number == "":
            return "0"
        else:
            if number[-1] in data['operators_chars']:
                number = number[:-1]
            n = 0
            for n in range(len(number)):
                print(number_list)
                try:
                    int(number[n])
                    number_var += number[n]
                    n += 1
                    if n == len(number):
                        break
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
            for m in range(len(number)):
                if number[m] == "(":
                    lbr += 1
                    m += 1
                elif number[m] == ")":
                    rbr += 1
                    m += 1
                else:
                    m += 1  
            p = 0
            if lbr > rbr:
                br_var = lbr-rbr
                n = 0
                for n in range(br_var):
                    number_list.append(')')
                    n += 1
            for m in cycle(range(0, 1)):
                if "" in number_list:
                    number_list.remove("")
                    if "" in number_list:
                        continue
                    else:
                        break
                else:
                    break
            
            print(number_list)
            
            x = self.BC_exponent(number_list)
            
            time_end = time.time()
            print(f'Operation complete in: {time_end-time_start}')
            # return x
    
    def BC_brackets(self, number_list):
        
        return
    
    def BC_calculation(self, number_list):
        add_list, equal_list = [], []
        for n in cycle(range(0,1)):
            try:
                #Dělení x násobení
                if "/" in number_list or "*" in number_list:
                    try:
                        div_var =  number_list.index('/')
                        mul_var = number_list.index('*')
                        if div_var < mul_var:
                            print('div')
                            number_list = self.BC_div(number_list)
                            continue 
                        elif div_var > mul_var:
                            print('mul')
                            number_list = self.BC_mul(number_list)
                            continue
                    except:
                        if "/" in number_list:
                            number_list = self.BC_div(number_list)
                            continue 
                        elif "*" in number_list:
                            number_list = self.BC_mul(number_list)
                            continue
                #Sčítání x odčítání
                elif "+" in number_list or "-" in number_list:
                    if '-' in number_list:
                        number_list = self.BC_sub(number_list)
                        continue  
                    else:
                        pass
                    if '+' in number_list:
                        number_list = self.BC_add(number_list)
                        continue  
                    else:
                        pass
                if len(number_list) == 1:
                    break
                else:
                    continue
            except Exception as err:
                print(err)
                break
            
        return number_list[0]
            
    def BC_exponent(self, number_list):
        if "(" in number_list:
            equal = []
            m = 0
            lbr, rbr, lbr_var, rbr_var = 0, 0, 0, 0
            for n in cycle(range(0, 1)):
                if number_list[m] == "(":
                    lbr = m
                    lbr_var += 1
                    m += 1
                elif number_list[m] == ")":
                    rbr = m
                    rbr_var += 1
                    m += 1
                else:
                    m += 1
                if lbr_var != 0:
                    if rbr_var == lbr_var:
                        n = lbr+1
                        print(lbr)
                        print(rbr)
                        print(n)
                        for p in range(0, int(rbr-lbr)):
                            equal.append(number_list[n])
                            n += 1
                            print(equal)
                            if n-lbr == rbr-lbr:
                                break
                        if len(equal) > 1:
                            y = self.BC_calculation(equal)
                            equal.clear()
                            equal.append(y)
                            break
                        
                        
                            
                    if rbr_var > lbr_var:
                        return
                        
                if m == len(number_list):
                    break
            
            # try:
            if lbr == 0:
                number_list = equal + number_list[int(rbr+1):]
            else:
                print(1)
                number_list = number_list[:(lbr)] + equal + number_list[(rbr+1):]
                
            # print(number_list)
            
            return
        else:
            return
        return
    
    def BC_mul(self, number_list):
        equal = []
        x = number_list.index("*")
        
        print(number_list[x+1])
        equal.append(str(float(number_list[x-1])*float(number_list[x+1])))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def BC_div(self, number_list):
        equal = []
        x = number_list.index("/")
        
        print(number_list[x+1])
        equal.append(str(float(number_list[x-1])/float(number_list[x+1])))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def BC_add(self, number_list):
        equal = []
        x = number_list.index("+")
        
        print(number_list[x+1])
        equal.append(str(float(number_list[x-1])+float(number_list[x+1])))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def BC_sub(self, number_list):
        equal = []
        x = number_list.index("-")
        
        print(number_list[x+1])
        equal.append(str(float(number_list[x-1])-float(number_list[x+1])))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def BC_brack_r(self, number_list, num):
        return
    
    def BC_brack_l(self, number_list, num):
        return