import json
import os

import calculations as calc
import render as rend
from render import *

def func_connected():
    print("     funcs.py")

class OpenFile():
    #Otevření "data.json" a "locale" souborů
    def file_opener(self):
        global locale_file, data, locale, locale_default #Registrování proměnných
        with open(os.path.join('','data.json'), "r") as g: #Otevření dat
            data = json.load(g) #Načtení dat
            g.close() #Zavření původního souboru
        #Otevření souborů jazka
        with open(os.path.join('','locale', data['locale']), "r", encoding="UTF-8") as f: #Otevření lkkalizace
            locale = json.load(f) #Načtení lokalizace
            f.close() #Zavření původního souboru
            locale_default = 0
    file_opener(0)

class Func(OpenFile, calc.BasicCalculator):
    #Proměnná pro změnu jazyka
    global new_locale
    new_locale = data['locale']
    #Funkce zavření okna
    def func_quit(self, root):
        root.destroy()
        
    #Funkce obnovení okna díky oknu možností
    def func_mode_reload(self, root, val):
        self.func_quit(root) #Zavření okna možnosti
        rend.render_main_frame.pack_forget() #"Zapomenutí" hlavního rámu
        self.func_settings_change(val)
        self.render_main(val) #Znovu vytvoření hlavního rámu
        
    #Funkce pro uložení změny vzhledu
    def func_settings_change(self, val):
        with open(os.path.join('', 'data.json'), "r+") as t: #Otevření dat s módem zapisování
            new_data = json.load(t) #Načtení  dat
            new_data['dark_light_mode'] = val #Přiřazení nové hodnoty
            t.seek(0) #Resetování řádku na 1.
            json.dump(new_data, t, indent=4) #Přepsání starých dat s novými
            t.truncate()
            t.close() #Zavření souboru
            
    #Funkce pro uložení jazyka
    def func_locale_save(self):
        with open(os.path.join('', 'data.json'), "r+") as h: #Otevření dat s módem zapisování
            new_data = json.load(h) #Načtení dat
            new_data['locale'] = self.new_locale #Přiřazení nové hodnoty
            h.seek(0) #Resetování řádku na 1.
            json.dump(new_data, h, indent=4) #Přepsání starých dat s novými
            h.truncate()
            h.close() #Zavření souboru
    
    #Funkce změny vzhledu
    def func_appear_change(self, val):
        print("\ndakr/light mode has been set to: "+str(val)) #Vypsání změny vzhledu do konzole pro debug   
        
    #Funkce na změnu jazyka    
    def func_laguage_change(self, root, value):
        print("\nlocalisation file set to: "+value) #Vypsní změny jazky do koncole pro debug
        self.new_locale = value #Přiřazení nové hodnoty
        self.func_locale_save() #Zavolání funkce pro uložení změny jazyka
        self.func_quit(root) #Zavření okna
        rend.render_main_frame.pack_forget() #Resetování hlavního rámu
        self.file_opener() #Znovu načtení dat se změnou
        self.render_main(data['dark_light_mode']) #Znovu vykreslení rámu
        
    #Funkce pro vyčištění kalkulátoru
    def func_calc_clear(self, mode):
        if mode == 'line': #Vyčištění řádku
            rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku 
        else: #Vyčištění poslední hodnoty/znaku
            current = rend.render_bc_input_box.get() #Získání dat z řádku
            if current != "": #Testuje, zda-li je řádek prázdný
                current = current.replace(current[-1], "") #Vymaže poslední znak
                rend.render_bc_input_box.delete(0, 'end') #Vymazní řádku
                rend.render_bc_input_box.insert(0, str(current)) #Vypsání nového řádku
            else: #Jinak přeskočit příkaz
                pass
    def func_calc_input(self, mode, var):        
        if mode == "num": #Testuje, zda-li je zadané číslo
            if int(var) in data['number_list']: #Testuje, zda-li je číslo platné
                current = rend.render_bc_input_box.get() #Záskání dat z řádku
                if current == "0" and int(var) == 0: #Pokud-li jediné, co řádek obsahuje je 0, nenapíše další nulu
                    pass
                else: #Ostatní možnosti
                    try: #Testování errorů
                        if current == "0": #Pokud-li jediné, co řádek obsahuje je 0, číslo nulu přepíše
                            rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                            rend.render_bc_input_box.insert(0, str(var)) #Vypsání nového řádku
                        else: #Ostatní možnosti
                            rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                            rend.render_bc_input_box.insert(0, str(current)+str(var)) #Vypsání nového řádku
                    except: #Pokud-li přijde error, přeskočí příkaz
                        pass
            else: #Pokud číslo není validní, přeskočí příkaz
                pass
        if mode == "oper": #Testuje, zda-li je zadaná operace
            if str(var) in data['operators_list']: #Testuje, zda-li je operace platná
                if str(var) == "ADD": #Pokud je operace sčítání
                    oper_val = "+" #Vypíše se +
                elif str(var) == "SUB": #Pokud je operace odčítání
                    oper_val = "-" #Vypíše se -
                elif str(var) == "MUL": #Pokud je operace násobení
                    oper_val = "*" #Vypíše se *
                elif str(var) == "DIV": #Pokud je operace dělení
                    oper_val = "/" #Vypíše se /
                if str(var) in data['operators_list'][:4]: #Testuje, zda-li je číslo mezi základníma operacema
                    current = rend.render_bc_input_box.get() #Získání dat z řdku
                    if current == "" and str(var) != 'SUB': #Pokud-li je řádek prázdný a operace není odčítání, přeskočí příkaz
                        pass
                    elif current == "" and str(var) == 'SUB': #Pokud-li je řádek prázdný a operace je odčítání, vypíše "0-"
                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                        rend.ender_bc_input_box.insert(0, "0"+'-') #Vypsání nového řádku
                    elif current != "": #Pokud-li řádek není prázdný
                        if current[-1] == ".": #Pokud-li je poslední znak desetinná čárka, přeskočí
                            pass
                        else:
                            if str(current[-1]) == "(" and var == 'SUB': #Pokudli je poslední znak otevřená závorka a operace je odčítání, vypíše se "0-"
                                rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                rend.render_bc_input_box.insert(0, str(current)+"0"+'-') #Vypsání nového řádku                           
                            else:
                                if str(current[-1]) == "(" and var != 'SUB': #Pokud je poseldní znak optevřená závorka a operace není odčítání, přeskočí příkaz
                                    pass
                                else:
                                    if str(current[-1]) in data["operators_chars"]: #Testuje, jestli je poslední znak mezi znakama operací
                                        if current[-2] == "(": #Pokud je předposlední znak otevřené závorka, příkaz se přeskočí
                                            pass
                                        else:
                                            current = str(current[:-1])+str(oper_val) #Přepsání starého znaku operace za nový
                                            rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                            rend.render_bc_input_box.insert(0, str(current)) #Vypsání nového řádku
                                    else:
                                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku             
                                        rend.render_bc_input_box.insert(0, str(current)+str(oper_val)) #Vypsání nového řádku
                elif str(var) in data['operators_list'][3:] and str(var) not in data['operators_list'][8:]: #Testuje, zda-li jsou operace mezi pokročilými
                    current = rend.render_bc_input_box.get() #Zíkání dat z řádku
                    if current == "": #Pokud je řádek prázdný, příkaz se přeskočí
                        pass
                    else:
                        if current[-1] in data['operators_chars']: #Pokud je poslední znak jiný operátor, příkaz se přeskočí
                            pass
                        else:
                            if current[-1] == "(": #Pokud je poslední znak otevřená závorka, příkaz se přeskočí
                                pass
                            else:
                                if str(var) == "SQ": #Pokud je operace druhá mocnina
                                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                    rend.render_bc_input_box.insert(0, str(current)+"^(2)") #Vypsání nového řádku
                                elif str(var) == "SQROOT": #Pokud je operace druhá odmocnina
                                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                    rend.render_bc_input_box.insert(0, str(current)+"^(1/2)") #Vypsání nového řádku  
                                elif str(var) == "NSQ": #Pokud je operace mocnina na "entou"
                                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                    rend.render_bc_input_box.insert(0, str(current)+"^(") #Vypsání nového řádku
                                elif str(var) == "NROOT": #Pokud je operace odmocnina na "entou"
                                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                    rend.render_bc_input_box.insert(0, str(current)+"^(1/") #Vypsání nového řádku   
                                else:
                                    pass
                else:
                    pass
        elif mode == "add_oper":
            if str(var) in data['add_operators_list']:
                if str(var) == 'LBRACKET':
                    add_oper_val = "("
                elif str(var) == 'RBRACKET':
                    add_oper_val = ")"
                current = rend.render_bc_input_box.get()
                if str(var) == "LBRACKET":
                    if current != "":
                        if current[-1] == ".":
                            pass
                        else:
                            try:
                                if int(current[-1]) in data['number_list']:
                                    pass
                                else:
                                    rend.render_bc_input_box.delete(0, 'end')             
                                    rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val))
                            except:
                                rend.render_bc_input_box.delete(0, 'end')             
                                rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val))
                    else:
                        rend.render_bc_input_box.delete(0, 'end')             
                        rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val))
                elif str(var) == 'RBRACKET':
                    if current != "" and str(current[-1]) != ".":
                        n = 0
                        lbr_num = 0
                        while n < len(current):
                            if str(current[n]) == "(":
                                lbr_num += 1
                                n += 1
                            else:
                                n += 1
                        n = 0
                        rbr_num = 0
                        while n < len(current):
                            if str(current[n]) == ")":
                                rbr_num += 1
                                n += 1
                            else:
                                n += 1
                        if rbr_num < lbr_num:
                            if str(current[-1]) in data['operators_chars']:
                                pass
                            elif str(current[-1]) == "(":
                                try:
                                    if str(current[-2]) == "^":
                                        current = current[:-2]
                                    else:
                                        current = current[:-1]   
                                except:
                                    current = current[:-1]                             
                                rend.render_bc_input_box.delete(0, 'end')               
                                rend.render_bc_input_box.insert(0, str(current))
                            else:
                                if rbr_num > 0:
                                    rend.render_bc_input_box.delete(0, 'end')             
                                    rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val))                                   
                                else:
                                    rend.render_bc_input_box.delete(0, 'end')             
                                    rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val))
                        else:
                            print(str(lbr_num)+" "+str(rbr_num))
                            print('err')
                    else:
                        pass
            else:
                pass
        elif mode == "dec":
            current = rend.render_bc_input_box.get()
            try:
                if int(current[-1]) in data['number_list']:
                    rend.render_bc_input_box.delete(0, 'end')             
                    rend.render_bc_input_box.insert(0, str(current)+str(var))
                else:
                    pass
            except:
                pass
        elif mode == "equal":
            current = rend.render_bc_input_box.get()
            x = self.BC_number_sort(current)
            rend.render_bc_input_box.delete(0, 'end')             
            rend.render_bc_input_box.insert(0, str(x))            

    def func_calc_shift_down(self):
        rend.render_bc_button_1_0.config(text="x²", padx=9, command= lambda: self.func_calc_input('oper', 'SQ'))
        rend.render_bc_button_2_0.config(text="√", padx=10, command= lambda: self.func_calc_input('oper', 'SQROOT'))
        rend.render_bc_button_3_0.config(text="↑", command=lambda: self.func_calc_shift_up())
        
    def func_calc_shift_up(self):
        rend.render_bc_button_1_0.config(text="x^n ", padx=2, command= lambda: self.func_calc_input('oper', 'NSQ'))
        rend.render_bc_button_2_0.config(text="³√", padx=8, command= lambda: self.func_calc_input('oper', 'NROOT'))
        rend.render_bc_button_3_0.config(text="↓", command=lambda: self.func_calc_shift_down())