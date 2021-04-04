import json
import os
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
            
            x = self.BC_start(number_list)
            
            time_end = time.time()
            print(f'Operation complete in: {time_end-time_start}')
            return x
    
    def BC_start(self, number_list):
        if '(' in number_list:
            y = self.BC_brackets(number_list)
        else:
            y = self.BC_calculation(number_list)
            y = y[0]
        return y
    
    
    def BC_brackets(self, number_list):
        if "(" in number_list:
            for n in cycle(range(0, 1)):
                global l_bracket_index, r_bracket_index
                l_bracket_index, r_bracket_index = 0, 0
                l_bracket = self.list_duplicates_of(number_list, '(')
                r_bracket = self.list_duplicates_of(number_list, ')')
                
                def brackets_index():
                    l_bracket_index = l_bracket.index(max(l_bracket))
                    r_bracket_index = r_bracket.index(min(r_bracket))
                    for n in cycle(range(0, 1)):
                        if int(l_bracket[l_bracket_index]) > int(r_bracket[r_bracket_index]):
                            r_bracket_index += 1
                            continue
                        else:
                            break
                    return l_bracket_index, r_bracket_index
                
                l_bracket_index, r_bracket_index = brackets_index()

                index = int(l_bracket[l_bracket_index])+1
                brackets_num = []
                for n in cycle(range(0, 1)):
                    if index == r_bracket[r_bracket_index]:
                        break
                    else:
                        brackets_num.append(number_list[index])
                        index += 1
                
                if len(brackets_num) == 1:
                    number_list[l_bracket[l_bracket_index]] = float(brackets_num[0])
                    remove_index = l_bracket[l_bracket_index]+1
                    for n in cycle(range(0, 1)):
                        if remove_index > r_bracket[r_bracket_index]:
                            break
                        else:
                            number_list.pop(l_bracket[l_bracket_index]+1)
                            remove_index += 1
                            continue
                else:
                    for n in range(brackets_num.count('+')+brackets_num.count('-')+brackets_num.count('*')+brackets_num.count('/')+brackets_num.count('^')):
                        y = self.BC_calculation(brackets_num)
                        brackets_num = y
                    number_list[l_bracket[l_bracket_index]] = y[0]
                    remove_index = l_bracket[l_bracket_index]+1
                    for n in cycle(range(0, 1)):
                        if remove_index > r_bracket[r_bracket_index]:
                            break
                        else:
                            number_list.pop(l_bracket[l_bracket_index]+1)
                            remove_index += 1
                            continue
                    
                if "(" not in number_list:
                    break
                else:
                    continue

        if len(number_list) != 1:
            for n in cycle(range(0,1)):
                y = self.BC_calculation(number_list)
                number_list = y
                if len(number_list) == 1:
                    break
                else:
                    continue
            
        return number_list[0]
    
    def BC_calculation(self, number_list):
        for n in cycle(range(0,1)):
            try:
                #Mocnina
                if '^' in number_list:
                    number_list = self.BC_exponent(number_list)
                #Dělení x násobení
                elif "/" in number_list or "*" in number_list:
                    try:
                        div_var =  number_list.index('/')
                        mul_var = number_list.index('*')
                        if div_var < mul_var:
                            number_list = self.BC_div(number_list)
                            continue 
                        elif div_var > mul_var:
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
            
        return number_list
            
    def BC_exponent(self, number_list):
        equal = []
        x = number_list.index("^")
        
        equal.append(str(math.pow(float(number_list[x-1]), float(number_list[x+1]))))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def BC_mul(self, number_list):
        equal = []
        x = number_list.index("*")
        
        equal.append(str(float(number_list[x-1])*float(number_list[x+1])))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def BC_div(self, number_list):
        equal = []
        x = number_list.index("/")
        
        equal.append(str(float(number_list[x-1])/float(number_list[x+1])))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def BC_add(self, number_list):
        equal = []
        x = number_list.index("+")
        
        equal.append(str(float(number_list[x-1])+float(number_list[x+1])))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def BC_sub(self, number_list):
        equal = []
        x = number_list.index("-")
        
        equal.append(str(float(number_list[x-1])-float(number_list[x+1])))
        y = number_list[:(x-1)] + equal + number_list[(x+2):]
        
        return y
    
    def list_duplicates_of(self, seq,item):
        start_at = -1
        locs = []
        while True:
            try:
                loc = seq.index(item,start_at+1)
            except ValueError:
                break
            else:
                locs.append(loc)
                start_at = loc
        return locs