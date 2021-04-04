import os
import json
from tkinter import *

import render as rend

def unit_conv_connected():
    print("     unitconver.py")

class OpenFile():
    #Otevření "data.json" a "locale" souborů
    global locale_file, data, locale, locale_default, unit_conv #Registrování proměnných
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
    os.system('cls') #Vyčištění konzole
    print(f"DATA: (data.json)\n{data}") #Vypsnání obsahu "data.json"
    print(f"\nLOCALES: ({os.path.join('locale', data['locale'])})\n{locale}") #Vypsání obsahu "locale"
    print("\n")
    print(f"\nUNIT DATA: (data/unit_conv_data.json) \n{unit_conv}")
    mode = data['dark_light_mode'] #Přiřazení správné možnosti pro změnu vzhledu
    
class UnitConverter():
    
    def UC_convert(self, l_val, r_val, val, val_list, conv_val):
        if r_val == l_val:
            try:
                return float(conv_val)
            except:
                return 'Err'
        else:
            pass
        if r_val in unit_conv['basic-unit']:
            if l_val in unit_conv['basic-unit']:
                pass
            else:
                if int(unit_conv[val_list].index(l_val)) > int(unit_conv[val_list].index(r_val)):
                    y = int(conv_val)/int(unit_conv[val][unit_conv[val_list].index(l_val)])
                    return float(y)
                else:
                    y = int(conv_val)*int(unit_conv[val][unit_conv[val_list].index(l_val)])
                    return float(y)
        elif r_val not in unit_conv['basic-unit']:
            if l_val in unit_conv['basic-unit']:
                if int(unit_conv[val_list].index(l_val)) < int(unit_conv[val_list].index(r_val)):
                    y = int(conv_val)*int(unit_conv[val][unit_conv[val_list].index(r_val)])
                    return float(y)
                elif int(unit_conv[val_list].index(l_val)) > int(unit_conv[val_list].index(r_val)):
                    y = int(conv_val)/int(unit_conv[val][unit_conv[val_list].index(r_val)])
                    return float(y)                        
            if l_val not in unit_conv['basic-unit']:
                if int(unit_conv[val_list].index(l_val)) > int(unit_conv[val_list].index(unit_conv['basic-unit'][rend.unit_data_list.index(val_list)])):
                    x = int(conv_val)/int(unit_conv[val][unit_conv[val_list].index(l_val)])
                    if int(unit_conv[val_list].index(r_val)) > int(unit_conv[val_list].index(unit_conv['basic-unit'][rend.unit_data_list.index(val_list)])):
                        y = x*int(unit_conv[val][unit_conv[val_list].index(r_val)])
                        return float(y)
                    elif int(unit_conv[val_list].index(r_val)) < int(unit_conv[val_list].index(unit_conv['basic-unit'][rend.unit_data_list.index(val_list)])):
                        y = x/int(unit_conv[val][unit_conv[val_list].index(r_val)])
                        return float(y)          
                elif int(unit_conv[val_list].index(l_val)) < int(unit_conv[val_list].index(unit_conv['basic-unit'][rend.unit_data_list.index(val_list)])):
                    x = int(conv_val)*int(unit_conv[val][unit_conv[val_list].index(l_val)])
                    if int(unit_conv[val_list].index(r_val)) > int(unit_conv[val_list].index(unit_conv['basic-unit'][rend.unit_data_list.index(val_list)])):
                        y = x*int(unit_conv[val][unit_conv[val_list].index(r_val)])
                        return float(y)
                    elif int(unit_conv[val_list].index(r_val)) < int(unit_conv[val_list].index(unit_conv['basic-unit'][rend.unit_data_list.index(val_list)])):
                        y = x/int(unit_conv[val][unit_conv[val_list].index(r_val)])
                        return float(y)
                else:
                    return 'Err'