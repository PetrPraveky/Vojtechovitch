import json
import os
from math import floor
from tkinter import OptionMenu
from itertools import cycle

import calculations as calc
import render as rend
import unitconver as units
from render import *

BC_num_memory = ["", "", "", "", ""]
BC_equal_memory = ["", "", "", "", ""]

def func_connected():
    print("     funcs.py")

class OpenFile():
    #Otevření "data.json" a "locale" souborů
    def file_opener(self):
        global locale_file, data, locale, locale_default, unit_data, unit_conv #Registrování proměnných
        with open(os.path.join('','data.json'), "r") as g: #Otevření dat
            data = json.load(g) #Načtení dat
            g.close() #Zavření původního souboru
        #Otevření souborů jazka
        with open(os.path.join('','locale', data['locale']), "r", encoding="UTF-8") as f: #Otevření lkkalizace
            locale = json.load(f) #Načtení lokalizace
            f.close() #Zavření původního souboru
            locale_default = 0
        with open(os.path.join('', 'data', 'unit_conv_data.json'), 'r', encoding='UTF-8') as i:
            unit_conv = json.load(i)
            i.close()
    file_opener(0)

class Func(OpenFile, calc.BasicCalculator, units.UnitConverter):
    #Proměnná pro změnu jazyka
    global new_locale
    new_locale = data['locale']
    #Funkce zavření okna
    def func_quit(self, root):
        root.destroy()
    #Funkce pro vykreslení základní kalkulačky
    def func_render_BC(self):
        rend.render_main_frame.pack_forget() #Vypnutí případné otevřené jiné aplikace
        self.file_opener() #Zavolání funkce na otevírání souborů
        self.render_main(data['dark_light_mode'], 0) #Vykreslení okna
    #FUnkce pro vykreslení převodů jednotek
    def func_render_unit(self):
        rend.render_main_frame.pack_forget() #Vypnutí případné otevřené jiné aplikace
        self.file_opener() #Zavolání funkce na otevírání souborl
        self.render_main(data['dark_light_mode'], 1) #Vykreslení okna
    def func_render_GF(self):
        rend.render_main_frame.pack_forget()
        self.file_opener()
        self.render_main(data['dark_light_mode'], 2)
    #Funkce obnovení okna díky oknu možností
    def func_mode_reload(self, root, val, option):
        self.func_quit(root) #Zavření okna možnosti
        rend.render_main_frame.pack_forget() #"Zapomenutí" hlavního rámu
        self.func_settings_change(val) #Zapsání nové hodnoty do souboru
        self.render_main(val, option) #Znovu vytvoření hlavního rámu
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
    def func_laguage_change(self, root, value, option):
        print("\nlocalisation file set to: "+value) #Vypsní změny jazky do koncole pro debug
        self.new_locale = value #Přiřazení nové hodnoty
        self.func_locale_save() #Zavolání funkce pro uložení změny jazyka
        self.func_quit(root) #Zavření okna
        rend.render_main_frame.pack_forget() #Resetování hlavního rámu
        self.file_opener() #Znovu načtení dat se změnou
        self.render_main(data['dark_light_mode'], option) #Znovu vykreslení rámu   
    #Funkce pro vyčištění kalkulátoru
    def func_calc_clear(self, mode):
        if mode == 'line': #Vyčištění řádku
            rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku 
        else: #Vyčištění poslední hodnoty/znaku
            current = rend.render_bc_input_box.get() #Získání dat z řádku
            if current != "": #Testuje, zda-li je řádek prázdný
                if str(current[-1]) in data['char_list']: #Pokud poslední znak je v listu povolených písmen:
                    m = -1 #Vytvoření hodnory
                    for n in cycle(range(0, 1)): #Nekonečný cyklus
                        try: #Pokus
                            if str(current[m]) in data['char_list']: #Pokud je další znak v listu:
                                m -= 1 #Odečte 1 od hodnoty
                                continue
                            else: #Jinak
                                break #Zlomí cylkus
                        except: #Pokud naskytne chyba (hodnota "m" již není v listu)
                            break #Zlomí cyklus
                    current = current[:(m+1)] #Odebrání znaku hodnory "m" od řádku
                    rend.render_bc_input_box.delete(0, 'end') #Vymazní řádku
                    rend.render_bc_input_box.insert(0, str(current)) #Vypsání nového řádku
                else:
                    current = current[:-1] #Vymaže poslední znak
                    rend.render_bc_input_box.delete(0, 'end') #Vymazní řádku
                    rend.render_bc_input_box.insert(0, str(current)) #Vypsání nového řádku
            else: #Jinak přeskočit příkaz
                pass
    def func_calc_input(self, mode, var):        
        if mode == "num": #Testuje, zda-li je zadané číslo
            try:
                if int(var) in data['number_list']: #Testuje, zda-li je číslo platné
                    current = rend.render_bc_input_box.get() #Záskání dat z řádku
                    if current == "0" and int(var) == 0: #Pokud-li jediné, co řádek obsahuje je 0, nenapíše další nulu
                        pass #Překosčí příkaz
                    else: #Ostatní možnosti
                        try: #Testování errorů
                            if current == "0": #Pokud-li jediné, co řádek obsahuje je 0, číslo nulu přepíše
                                rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                rend.render_bc_input_box.insert(0, str(var)) #Vypsání nového řádku
                            else: #Ostatní možnosti
                                try:
                                    if current[-1] == 'π' or current[-1] == 'e' or current[-1] == 'τ': #Pokud je poslendí číslo nějaké ze speciálních
                                        pass #Přeskoží příkat
                                    else:
                                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                        rend.render_bc_input_box.insert(0, str(current)+str(var)) #Vypsání nového řádku
                                except:
                                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                    rend.render_bc_input_box.insert(0, str(current)+str(var)) #Vypsání nového řádku
                        except: #Pokud-li přijde error, přeskočí příkaz
                            pass
            except: #Pokud hodnota není číslo
                if var == "E": #Pokud je "E" jako číslo
                    current = rend.render_bc_input_box.get() #Získání dat z řádku
                    try: #Pokus
                        int(current[-1]) #Pokud je poslední znak číslo
                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                        rend.render_bc_input_box.insert(0, str(current)+str(var)) #Vypsání nového řádku
                    except: #Pokud poslední znak není číslo
                        pass #Překočí příkaz
        elif mode == "snum": #Testuje, zda-li je zadané speciální číslo
            current = rend.render_bc_input_box.get() #Získání dat  zřádku
            if str(var) == 'pi': #Pokud je zadané číslo pí
                if current == "": #Pokud je řádek prázdný
                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                    rend.render_bc_input_box.insert(0, str(current)+'π') #Vypsání nového řádku
                else: #Jinak
                    #Pokud je poslední hodnota znaménko, otevřená závorka nebo absolutní hodnota
                    if str(current[-1]) in data['operators_chars'] or str(current[-1]) == "(" or str(current[-1]) == "" or str(current[-1]) == "|":
                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                        rend.render_bc_input_box.insert(0, str(current)+'π') #Vypsnání nového řádku
                    else: #Jinak
                        pass #Přeskočit příkaz
            elif str(var) == 'e': #Pokud je zadané číslo eulerovo číslo
                if current == "": #Pokud je řádek prázdný
                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                    rend.render_bc_input_box.insert(0, str(current)+'e') #Vypsnání nového řádku
                else:
                    #Pokud je poslední hodnota znaménko, otevřená závorka nebo absolutní hodnota
                    if str(current[-1]) in data['operators_chars'] or str(current[-1]) == "(" or str(current[-1]) == "" or str(current[-1]) == "|":
                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                        rend.render_bc_input_box.insert(0, str(current)+'e') #Vypsání nového řádku
                    else: #Jinak
                        pass #Přeskočit
            elif str(var) == 't': #Testuje, zda-li zadané číslo je tau
                if current == "": #Pokud je řádek prázdný
                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                    rend.render_bc_input_box.insert(0, str(current)+'τ') #Vypsání nového řádku
                else: #Jinak
                    #Pokud je poslední hodnota znaménko, otevřená závorka nebo absolutní hodnota
                    if str(current[-1]) in data['operators_chars'] or str(current[-1]) == "(" or str(current[-1]) == "" or str(current[-1]) == "|":
                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                        rend.render_bc_input_box.insert(0, str(current)+'τ') #Vypsání nového řádku
                    else: #Jinak
                        pass #Přeskočit
        elif mode == "oper": #Testuje, zda-li je zadaná operace
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
                        rend.render_bc_input_box.insert(0, "0"+'-') #Vypsání nového řádku
                    elif current[-1] == "E" and str(var) == "SUB":
                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                        rend.render_bc_input_box.insert(0, str(current)+'-')                        
                    elif current != "" and current[-1] != "E": #Pokud-li řádek není prázdný
                        if current[-1] == ".": #Pokud-li je poslední znak desetinná čárka, přeskočí
                            pass
                        else:
                            if str(current[-1]) == "(" and var == 'SUB' or str(current[-1]) == "|" and var == "SUB": #Pokudli je poslední znak otevřená závorka a operace je odčítání, vypíše se "0-"
                                rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                rend.render_bc_input_box.insert(0, str(current)+"0"+'-') #Vypsání nového řádku                           
                            else:
                                if str(current[-1]) == "(" and var != 'SUB' or str(current[-1]) == "|" and var != "SUB": #Pokud je poseldní znak optevřená závorka a operace není odčítání, přeskočí příkaz
                                    pass
                                else:
                                    if str(current[-1]) in data["operators_chars"] and str(current[-1]) != '!': #Testuje, jestli je poslední znak mezi znakama operací
                                        try: #Pokus
                                            #Pokud je poslední znak E, tj 10^x, tak příkaz přeskočí
                                            if current[-2] == "E" and current[-1] == "-":
                                                pass
                                            #Pokud-li jsou poslední třy znaky "(0-", příkaz přeskočí
                                            elif current[-3] == "(" and current[-1] == "-" and current[-2] == "0":
                                                pass
                                            else: #Jinak
                                                current = str(current[:-1])+str(oper_val) #Přepsání starého znaku operace za nový
                                                rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                                rend.render_bc_input_box.insert(0, str(current)) #Vypsání nového řádku
                                        except: #Pokud index již není součástí listu
                                            current = str(current[:-1])+str(oper_val) #Přepsání starého znaku operace za nový
                                            rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                            rend.render_bc_input_box.insert(0, str(current)) #Vypsání nového řádku 
                                    else: #Jinak
                                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku             
                                        rend.render_bc_input_box.insert(0, str(current)+str(oper_val)) #Vypsání nového řádku
                elif str(var) in data['operators_list'][8]: #Pokud je oprátr "faktoriál"
                    current = rend.render_bc_input_box.get() #Získání dat z řdku
                    try: #Pokus
                        #Pokud-li je poslední znak číslo, konec závorky nebo absolutní hodnota
                        if str(current[-1]) in str(data['number_list']) or str(current[-1]) == ")"  or str(current[-1]) == "|":
                            rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku             
                            rend.render_bc_input_box.insert(0, str(current)+"!") #Vypsání nového řádku
                        else: #Jinak
                            pass #Přeskočí překlad
                    except ValueError as err: #Chyba
                        print(err) #Vypsání erroru do konzole
                        pass #Přeskočení příkazu
                elif str(var) in data['operators_list'][3:] and str(var) not in data['operators_list'][8:]: #Testuje, zda-li jsou operace mezi pokročilými
                    current = rend.render_bc_input_box.get() #Zíkání dat z řádku
                    if current == "": #Pokud je řádek prázdný, příkaz se přeskočí
                        pass #Přeskočení příkazu
                    else: #Jinak
                        if current[-1] in data['operators_chars']: #Pokud je poslední znak jiný operátor, příkaz se přeskočí
                            pass #Přeskočí příkaz
                        else: #Jinak
                            if current[-1] == "(": #Pokud je poslední znak otevřená závorka, příkaz se přeskočí
                                pass #Přeskočí příkat
                            else: #Jinak
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
                                else: #Jinak
                                    pass #Přeskočí příkaz
                else: #Jinak
                    pass #Přeskočí příkaz
        elif mode == "add_oper": #Testuje, zda-li je mód závorky nebo absolutní hodnota
            if str(var) in data['add_operators_list']: #Pokud je to v listu těchto hodnot
                if str(var) == 'LBRACKET': #Připsání hodnoty k levé závorce
                    add_oper_val = "("
                elif str(var) == 'RBRACKET': #Připsání hodnoty k pravé závorce
                    add_oper_val = ")"
                elif str(var) == 'ABSVAL': #Připsání hodnoty k absolutní hodnotě
                    add_oper_val = "|"
                current = rend.render_bc_input_box.get() #Získání dat z řádku
                if str(var) == "LBRACKET": #Pokud je příkaz levá závorka
                    if current != "": #Pokud řádek není prázdný
                        if current[-1] == ".": #Pokud poslední znak je desetinná čárka
                            pass #Přeskočí
                        elif current[-1] == 'π' or current[-1] == 'e' or current[-1] == 'τ': #Pokud poslednáí znak je speciální číslo
                            pass  #Přeskočí
                        else: #Jinak
                            try: #Pokus
                                if int(current[-1]) in data['number_list']: #Je li poslední znak v listu čísel
                                    pass #Přeskočí
                                else: #Jinak
                                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                    rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val)) #Vypsání nového řádku
                            except: #Pokud-li nastane chyba
                                rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                                rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val)) #Vypsání nového řádku
                    else: #Jinak
                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku            
                        rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val)) #Vypsání nového řádku
                elif str(var) == 'RBRACKET': #Pokud je příkaz pravá závorka
                    if current != "" and str(current[-1]) != ".": #Pokud poslední znak není desetinná čárka nebo řádek není prázdny
                        n = 0 #Vytvoření proměnné
                        lbr_num = 0 #Vytvoření proměnné
                        while n < len(current): #Cyklus dokud je "n" menší jak délka řádku
                            if str(current[n]) == "(": #Pokud li je v řádku závorka
                                lbr_num += 1 #Přičte k hodnotě 1
                                n += 1 #Přičte k hodnotě 1
                            else: #Jinak
                                n += 1 #Přičte k hodnotě 1
                        n = 0 #Resetování proměnné
                        rbr_num = 0 #Vytvoření proměnné
                        while n < len(current): #Cyklus dokud je "n" menší jak dílka řádku
                            if str(current[n]) == ")": #Pokud li je v řádku uzavírací závorka
                                rbr_num += 1 #Přičte k hodnotě 1
                                n += 1 #Přičte k hodnotě 1
                            else: #Jinak
                                n += 1 #Přičte k hodnotě 1
                        if rbr_num < lbr_num: #Pokud si hodnoty nejsou rovny
                            if str(current[-1]) in data['operators_chars']: #Pokud je poslendní znak v řádku operátor
                                pass #Přeskočí příkaz
                            elif str(current[-1]) == "(": #Pokudd-li je poslední znak v řádku závorka
                                try: #Zkusí
                                    if str(current[-2]) == "^": #Pokud je předposlendí znak "^"
                                        current = current[:-2] #Vymaže závorku i znak "^"
                                    else: #Jinak
                                        current = current[:-1] #Vymaže závorku
                                except: #Pokud-li nastane chyba délky listu
                                    current = current[:-1] #Vymaže závorku            
                                rend.render_bc_input_box.delete(0, 'end') #Vymaže řádek              
                                rend.render_bc_input_box.insert(0, str(current)) #Vypíše nový řádek
                            else: #Jinak
                                rend.render_bc_input_box.delete(0, 'end') #Vymaže řádek            
                                rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val)) #Vypíše nový řádek
                        else: #Jinak
                            pass #Přeskočí příkaz
                    else: #Jinak
                        pass #Přeskočí příkaz
                elif str(var) == 'ABSVAL': #Pokud je příkaz absolutní hodnota
                    rend.render_bc_input_box.delete(0, 'end') #Vymaže řádek
                    rend.render_bc_input_box.insert(0, str(current)+str(add_oper_val)) #Vypíše nový řádek
            else: #Jinak
                pass #Přeskočí pžíkaz
        elif mode == "geom": #Testuje, zda-li je mód goniometrických funkcí
            if str(var) == 'SIN': #Připíše k hodně "sin"
                geo_val = 'sin('
            elif str(var) == 'COS': #Připíše k hodnotě "cos"
                geo_val = 'cos('
            elif str(var) == 'TG': #Připíše k hodnotě "tg"
                geo_val = 'tg('
            elif str(var) == 'ASIN': #Připíše k hodnotě "asin"
                geo_val = 'asin('
            elif str(var) == 'ACOS': #Připíše k hodnotě "acos"
                geo_val = 'acos('
            elif str(var) == 'ATG': #Připíše k hodnotě "atg"
                geo_val = 'atg('            
            current = rend.render_bc_input_box.get() #Získání dat z řádku
            try: #Pokus
                if current[-1] in data['operators_chars'] and current[-1] != '!': #Je-li jako poslední znak opěráter bez faktoriálnu
                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                    rend.render_bc_input_box.insert(0, str(current)+str(geo_val)) #Vypsání nového řádku
                else: #Jinak
                    if str(current[-1]) == '(' or str(current[-1]) == "|": #Pokud je jako poslední znak otevírací závorka neob absolutní hodnota
                        rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                        rend.render_bc_input_box.insert(0, str(current)+str(geo_val)) #Vypsání nového řádku
                    else: #Jinak
                        pass #Přeskočí příkaz
            except: #Je-li chyba v délce řádku
                rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku          
                rend.render_bc_input_box.insert(0, str(current)+str(geo_val)) #Vypsání nového řádku          
        elif mode == "dec": #Testuje, zda-li je mód desetinné čárky
            current = rend.render_bc_input_box.get() #Získání dat z řádku
            try: #Pokus
                if int(current[-1]) in data['number_list']: #Je-li poslední znak číslo
                    rend.render_bc_input_box.delete(0, 'end') #Vymazání řádku
                    rend.render_bc_input_box.insert(0, str(current)+str(var)) #Vypsání nového řádku
                else: #Jinak
                    pass #Přeskočí příkaz
            except: #V chybě hodnoty
                pass #Přeskočí příkaz
        elif mode == "func":
            current = rend.render_bc_input_box.get()
            if str(var) == "LOG":
                func_val = "log("
            elif str(var) == "LN":
                func_val = "ln("
            try:
                if current[-1] in data['operators_chars'] and current[-1] != "!" or str(current[-1]) == "(" or str(current[-1]) == "|":
                    rend.render_bc_input_box.delete(0, 'end')             
                    rend.render_bc_input_box.insert(0, str(current)+str(func_val))
                else:
                    pass
            except:
                rend.render_bc_input_box.delete(0, 'end')             
                rend.render_bc_input_box.insert(0, str(current)+str(func_val))
        elif mode == "equal":
            current = rend.render_bc_input_box.get()
            if var == 'eq':
                x = self.BC_number_sort(current)
                if str(x) == "∞":
                    pass
                elif str(x) == "Math Err":
                    pass
                else:
                    BC_num_memory.insert(0, current)
                    BC_equal_memory.insert(0, x)
                    try:
                        BC_num_memory.pop(10)
                        BC_equal_memory.pop(10)
                    except:
                        pass
                self.func_calc_memory_reload()
                rend.render_bc_input_box.delete(0, 'end')             
                rend.render_bc_input_box.insert(0, str(x))
            elif var == 'deg':
                try:
                    float(current)
                    x = floor(float(current))
                    print(x)
                    y = floor((float(current)-x)*60)
                    print(y)
                    z = floor((float(current)-x-(y/60))*6000)
                    print(z)
                    rend.render_bc_input_box.delete(0, 'end')             
                    rend.render_bc_input_box.insert(0, "~ "+str(x)+'°'+str(y)+"'"+str(z)+"''")                 
                except:
                    pass

    def func_calc_memory_reload(self):
        rend.render_bc_memory_frame.grid_forget()
        self.render_BC_memory()
        
    def func_calc_memory_delete(self, index):
        BC_num_memory.pop(index)
        BC_equal_memory.pop(index)
        if len(BC_num_memory) == 4:
            BC_num_memory.append('')
            BC_equal_memory.append('')
        self.func_calc_memory_reload()
        
    def func_calc_memory_load(self, index):
        current = rend.render_bc_input_box.get()
        if current != 0:
            try:
                if int(current[-1]):
                    rend.render_bc_input_box.delete(0, 'end')             
                    rend.render_bc_input_box.insert(0, str(BC_equal_memory[index]))
            except:
                try:
                    if str(current[-1]) == "π" or str(current[-1]) == "e" or str(current[-1]) == "τ" or str(current[-1]) == ")" or str(current[-1]) == ".":
                        rend.render_bc_input_box.delete(0, 'end')             
                        rend.render_bc_input_box.insert(0, str(BC_equal_memory[index]))
                    else:
                        rend.render_bc_input_box.delete(0, 'end')             
                        rend.render_bc_input_box.insert(0, current + str(BC_equal_memory[index]))
                except:
                    rend.render_bc_input_box.delete(0, 'end')             
                    rend.render_bc_input_box.insert(0, str(BC_equal_memory[index]))                    
        else:
            rend.render_bc_input_box.delete(0, 'end')             
            rend.render_bc_input_box.insert(0, str(BC_equal_memory[index]))

    def func_calc_shift_down(self):
        rend.render_bc_button_1_0.config(text="x²", padx=9, command= lambda: self.func_calc_input('oper', 'SQ'))
        rend.render_bc_button_2_0.config(text="√", padx=10, command= lambda: self.func_calc_input('oper', 'SQROOT'))
        rend.render_bc_button_3_0.config(text="↑", command=lambda: self.func_calc_shift_up())
        
        rend.render_bc_button_1_5.config(padx=4, text=" sin ", command= lambda: self.func_calc_input('geom', 'SIN'))
        rend.render_bc_button_2_5.config(padx=2, text=" cos ", command= lambda: self.func_calc_input('geom', 'COS'))
        rend.render_bc_button_3_5.config(padx=6, text=" tg ", command= lambda: self.func_calc_input('geom', 'TG'))

        rend.render_bc_button_4_7.config(padx=9, text='π', command= lambda: self.func_calc_input('snum', 'pi'))
        
    def func_calc_shift_up(self):
        rend.render_bc_button_1_0.config(text="x^n ", padx=2, command= lambda: self.func_calc_input('oper', 'NSQ'))
        rend.render_bc_button_2_0.config(text="³√", padx=8, command= lambda: self.func_calc_input('oper', 'NROOT'))
        rend.render_bc_button_3_0.config(text="↓", command=lambda: self.func_calc_shift_down())

        rend.render_bc_button_1_5.config(padx=1, text=" asin ", command= lambda: self.func_calc_input('geom', 'ASIN'))
        rend.render_bc_button_2_5.config(padx=2, text="acos", command= lambda: self.func_calc_input('geom', 'ACOS'))
        rend.render_bc_button_3_5.config(padx=3, text=" atg ", command= lambda: self.func_calc_input('geom', 'ATG'))

        rend.render_bc_button_4_7.config(padx=10, text='τ', command= lambda: self.func_calc_input('snum', 't'))
        
    
    def func_gf_clear(self, mode):
        if mode == "C":
            rend.render_gf_entry_1_2_6.delete(0, 'end')
        if mode == "back":
            current = rend.render_gf_entry_1_2_6.get()
            if current[-1] in data['char_list']:
                m = -1
                for n in range(len(current)):
                    if str(current[m]) in data['char_list']:
                        m -= 1
                        print(1)
                    else:
                        m += 1
                        break
                    print(m)
                current = current[:(m)]
                rend.render_gf_entry_1_2_6.delete(0, 'end')
                rend.render_gf_entry_1_2_6.insert(0, str(current))
            else:
                current = current[:-1]
                rend.render_gf_entry_1_2_6.delete(0, 'end')
                rend.render_gf_entry_1_2_6.insert(0, str(current))
    
    def func_gf_input(self, mode, val):
        current = rend.render_gf_entry_1_2_6.get()
        if mode == "var":
            if val == "y" or val == "x":
                if current == "":
                    rend.render_gf_entry_1_2_6.delete(0, 'end')
                    rend.render_gf_entry_1_2_6.insert(0, str(current)+str(val))
                else:
                    if current[-1] in data['operators_chars'] or current[-1] == "(" or current[-1] == "|":
                        rend.render_gf_entry_1_2_6.delete(0, 'end')
                        rend.render_gf_entry_1_2_6.insert(0, str(current)+str(val))
                    try:
                        if int(current[-1]) in data['number_list']:
                            rend.render_gf_entry_1_2_6.delete(0, 'end')
                            rend.render_gf_entry_1_2_6.insert(0, str(current)+str(val))
                        else:
                            pass
                    except:
                        if  str(current[-1]) == "π" or str(current[-1]) == "e" or str(current[-1]) == "τ":
                            rend.render_gf_entry_1_2_6.delete(0, 'end')
                            rend.render_gf_entry_1_2_6.insert(0, str(current)+str(val))   
                        else:
                            pass
                    
            else:
                pass
        elif mode == "num":
            try:
                int(val)
                if str(current) == "0" and val == 0:
                    pass
                elif str(current) == "0" and val != 0:
                    rend.render_gf_entry_1_2_6.delete(0, 'end')
                    rend.render_gf_entry_1_2_6.insert(0, str(val))
                else:
                    try:
                        if str(current[-1]) in data['char_list'] or str(current[-1]) == "e" or str(current[-1]) == "π" or str(current[-1]) == "τ":
                            pass
                        else:
                            rend.render_gf_entry_1_2_6.delete(0, 'end')
                            rend.render_gf_entry_1_2_6.insert(0, str(current)+str(val))
                    except:
                        if current == "":
                            rend.render_gf_entry_1_2_6.delete(0, 'end')
                            rend.render_gf_entry_1_2_6.insert(0, str(current)+str(val))
            except:
                if str(val) == "E":
                    try:
                        if int(current[-1]) in data["number_list"]:
                            rend.render_gf_entry_1_2_6.delete(0, 'end')
                            rend.render_gf_entry_1_2_6.insert(0, str(current)+str(val))
                        else:
                            pass
                    except:
                        if current == "":
                            pass
                        else:
                            if str(current[-1]) == "e" or str(current[-1]) == "π" or str(current[-1]) == "τ" or str(current[-1]) == "x" or str(current[-1]) == "y":
                                rend.render_gf_entry_1_2_6.delete(0, 'end')
                                rend.render_gf_entry_1_2_6.insert(0, str(current)+str(val))
                            else:
                                pass
        elif mode == "snum":
            if str(val) == "pi":
                num = "π"
            elif str(val) == "e":
                num = "e"
            elif str(val) == "t":
                num = "τ"
            if current == "":
                rend.render_gf_entry_1_2_6.delete(0, 'end')
                rend.render_gf_entry_1_2_6.insert(0, str(current)+str(num))
            else:
                if str(current[-1]) in data['operators_chars'] or str(current[-1]) == "(" or str(current[-1]) == "|" or str(current[-1]) == "E":
                    rend.render_gf_entry_1_2_6.delete(0, 'end')
                    rend.render_gf_entry_1_2_6.insert(0, str(current)+str(num))                    
        elif mode == "oper":
            if str(val) == "ADD":
                oper = "+"
            elif str(val) == "SUB":
                oper = "-"
            elif str(val) == "MUL":
                oper = "*"
            elif str(val) == "DIV":
                oper = "/"
            if str(val) in data['operators_list'][:4]:
                if current == "" and str(val) == "SUB":
                    rend.render_gf_entry_1_2_6.delete(0, 'end')
                    rend.render_gf_entry_1_2_6.insert(0, str(current)+"0-")
                elif current != "":
                    if str(current[-1]) in data['operators_chars'] and str(current[-1]) != "!":
                        if str(current) == "0-":
                            pass
                        else:
                            try:
                                if str(current[-1]) == "-" and str(current[-2]) == "E" or str(current[-1]) == "-" and str(current[-2]) == "0" and str(current[-3]) == "(":
                                    pass
                                else:
                                    current = current[:-1]
                                    rend.render_gf_entry_1_2_6.delete(0, 'end')
                                    rend.render_gf_entry_1_2_6.insert(0, str(current)+str(oper))
                            except:
                                current = current[:-1]
                                rend.render_gf_entry_1_2_6.delete(0, 'end')
                                rend.render_gf_entry_1_2_6.insert(0, str(current)+str(oper))
                    else:
                        try:
                            int(current[-1])
                            rend.render_gf_entry_1_2_6.delete(0, 'end')
                            rend.render_gf_entry_1_2_6.insert(0, str(current)+str(oper))
                        except:
                            if current[-1] == "e" or current[-1] == ")" or current[-1] == "|" or current[-1] == "τ" or current[-1] == "π":
                                rend.render_gf_entry_1_2_6.delete(0, 'end')
                                rend.render_gf_entry_1_2_6.insert(0, str(current)+str(oper))
                            elif current[-1] == "x" or current[-1] == "y":
                                rend.render_gf_entry_1_2_6.delete(0, 'end')
                                rend.render_gf_entry_1_2_6.insert(0, str(current)+str(oper))
                            elif current[-1] == "E" and str(val) == "SUB":
                                rend.render_gf_entry_1_2_6.delete(0, 'end')
                                rend.render_gf_entry_1_2_6.insert(0, str(current)+str(oper))
                            elif current[-1] == "(" and str(val) == "SUB":
                                rend.render_gf_entry_1_2_6.delete(0, 'end')
                                rend.render_gf_entry_1_2_6.insert(0, str(current)+'0-')
                            else:
                                pass   
                            try:
                                if current[-2] == "E" and current[-1] == "-":
                                    pass
                            except:
                                pass
                else:
                    pass
            elif str(val) == "FAC":
                try:
                    int(current[-1])
                    rend.render_gf_entry_1_2_6.delete(0, 'end')
                    rend.render_gf_entry_1_2_6.insert(0, str(current)+'!')
                except:
                    if str(current[-1]) == "e" or str(current[-1]) == "π" or str(current[-1]) == "τ" or current[-1] == ")" or current[-1] == "|":
                        rend.render_gf_entry_1_2_6.delete(0, 'end')
                        rend.render_gf_entry_1_2_6.insert(0, str(current)+'!')
                    elif str(current[-1]) == "x" or str(current[-1]) == "y":
                        rend.render_gf_entry_1_2_6.delete(0, 'end')
                        rend.render_gf_entry_1_2_6.insert(0, str(current)+'!')
                    else:
                        pass
            else:
                pass
        elif mode == "add_oper":
            return
        elif mode == "equal":
            return
        
    
    
    def func_unit_mode_change(self, val):  
        if val == "time":
            rend.ucl_var.set(unit_conv[rend.unit_data_list[locale['unit_data'].index(rend.uce_var.get())]][5])
            rend.ucr_var.set(unit_conv[rend.unit_data_list[locale['unit_data'].index(rend.uce_var.get())]][5])
        else:
            rend.ucl_var.set(unit_conv[rend.unit_data_list[locale['unit_data'].index(rend.uce_var.get())]][1])
            rend.ucr_var.set(unit_conv[rend.unit_data_list[locale['unit_data'].index(rend.uce_var.get())]][1])
        
        rend.render_uc_r_entry.delete(0, 'end') 
        rend.render_uc_r_entry.config(state='disabled')
        
        rend.render_uc_l_menu.grid_forget()
        rend.render_uc_l_menu = OptionMenu(rend.render_uc_frame, rend.ucl_var, *unit_conv[val])
        rend.render_uc_l_menu.configure(width=7, bg=rend.upper_bar_frame_submenu_color, borderwidth=1, relief='sunken', fg=rend.main_text_color, activebackground=rend.upper_bar_frame_submenu_color_hover, activeforeground=rend.main_text_color, highlightthickness=0, pady=5, state='normal', cursor='hand2')
        
        rend.render_uc_r_menu.grid_forget()
        rend.render_uc_r_menu = OptionMenu(rend.render_uc_frame, rend.ucr_var, *unit_conv[val])
        rend.render_uc_r_menu.configure(width=7, bg=rend.upper_bar_frame_submenu_color, borderwidth=1, relief='sunken', fg=rend.main_text_color, activebackground=rend.upper_bar_frame_submenu_color_hover, activeforeground=rend.main_text_color, highlightthickness=0, pady=5, state='normal', cursor='hand2')
        
        rend.render_uc_l_menu.grid(row=4, column=1, sticky='we', padx=5, pady=5)
        rend.render_uc_r_menu.grid(row=4, column=4, sticky='we', padx=5, pady=5) 
        return
    
    def func_unit_conver(self, l_val, r_val, val, val_list, conv_val):
        rend.render_uc_r_entry.delete(0, 'end') 
        
        y = self.UC_convert(l_val, r_val, val, val_list, conv_val)
        
        rend.render_uc_r_entry.config(state='normal')
        rend.render_uc_r_entry.insert(0, y)
        return
    
    def func_unit_delete(self):
        rend.render_uc_l_entry.delete(0, 'end') 
        
        rend.render_uc_r_entry.delete(0, 'end') 
        rend.render_uc_r_entry.config(state='disabled')
        
    def func_unit_swith(self):
        try:
            x = float(rend.render_uc_l_entry.get())
            y = float(rend.render_uc_r_entry.get())
            
            rend.render_uc_l_entry.delete(0, 'end')
            rend.render_uc_l_entry.insert(0, y)
            
            rend.render_uc_r_entry.delete(0, 'end') 
            rend.render_uc_r_entry.insert(0, x)
        except:
            pass