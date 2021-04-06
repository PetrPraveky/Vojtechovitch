from tkinter import * #Připojení modulu tkinter
from tkinter import font #Připojení modulu tkinter s podmodulem font
from tkinter import ttk #Připojení modulu tkinter s podmudulem ttk
import json #Připojení modulu json
import os #Připojení modulu os

import calculations as calc #Připojení modulu kalkulačky
import unitconver as units #Připojení modulu převodů jednotek
import funcs as funcs #Připojení modulu funkcí

default = 0 #Základní hodnota pro změnu módu kalkulačky
calculator_option = default #Přiřazení základní hodnoty

unit_data_list = ["size", "weight", "time"] #List veličin
unit_conv_list = ['size-conv', "weight-conv", "time-conv"] #List převodů jednotek

#Funkce pro oznámení připojení modulu render
def render_connected():
    print("     render.py")

def main_connected():
    print("\nmain.py has been connected to file:")
    #Připojení modulu kalkulací
    calc.calc_connected() #Připojení modulu kalkulačky
    funcs.func_connected() #Připojení modulu funkcí
    units.unit_conv_connected() #Připojení modulů převodů jednotek
    render_connected() #Připojení modulu render
    print("\n")

class OpenFile():
    #Otevření "data.json" a "locale" souborů
    global locale_file, data, locale, locale_default, unit_conv #Registrování proměnných
    with open(os.path.join('','data.json'), "r") as g: #Otevření dat
        data = json.load(g) #Načtení dat
        g.close() #Zavření původního souboru
    #Otevření souborů jazka
    with open(os.path.join('','locale', data['locale']), "r", encoding="UTF-8") as f: #Otevření lokalizace
        locale = json.load(f) #Načtení lokalizace
        f.close() #Zavření původního souboru
        locale_default = 0
    #Otevření souboru dat s převodama jednotek
    with open(os.path.join('', 'data', 'unit_conv_data.json'), 'r', encoding='UTF-8') as i: #Otevření dat
        unit_conv = json.load(i) #Načtení dat
        i.close() #Zavření původního souboru
    os.system('cls') #Vyčištění konzole
    print(f"DATA: (data.json)\n{data}") #Vypsnání obsahu "data.json"
    print(f"\nLOCALES: ({os.path.join('locale', data['locale'])})\n{locale}") #Vypsání obsahu "locale"
    print("\n")
    print(f"\nUNIT DATA: (data/unit_conv_data.json) \n{unit_conv}") #Vypsání obsahu "unit_conv_data.json"
    mode = data['dark_light_mode'] #Přiřazení správné možnosti pro změnu vzhledu
        
#Třída renderu
class Render(funcs.Func):    
    #Funkce pro vytvoření hlavní stránky
    def render_main(self, mode, option):
        global render_main_frame
        #Funkce pro barvy
        self.render_dark_light_mode(mode)
        #Vytvoření, které pokrývá celou aplikaci
        render_main_frame = Frame(self.main_root, bg=main_background_color)
        render_main_frame.grid_columnconfigure(0, weight=1)
        render_main_frame.grid_rowconfigure(0, weight=0)
        #Zavolání funkce pro vytvožení horní lišty
        self.render_upper_bar()
        #Vykreslení horní lišty
        render_upper_bar_frame.grid(row = 0, column=0, sticky='ew')
        #Výběr vykleslení správného okna
        if option == 0: #Pokud je možnost 0 == kalkulačka
            self.render_basic_calculator() #Funkce renderu kalkulačky
            render_bc_frame.grid(row=1, column=0, sticky='w', padx=50, pady=30) #Render celé kalkulačky
        elif option == 1: #Pokud je možnost 1 == převod jednotek
            self.render_unit_conver() #Funkce renderu převodů jednotek
            render_uc_frame.grid(row=1, column=0, sticky='w', padx=50, pady=30) #Render celých převodů jednotek
        else: 
            pass
        #Vykreslení celého okna
        render_main_frame.pack(fill='both', expand="True")
    
    #Funkce pro určení dark/light módem
    def render_dark_light_mode(self, mode):
        global main_background_color, main_text_color, upper_bar_frame_bg_color, upper_bar_frame_bg_color_hover, upper_bar_frame_submenu_color, upper_bar_frame_submenu_color_hover, mode_window_background_color, mode_window_background_color_hover
        global calc_background_color_1, calc_background_color_2, calc_background_color_2_hover, unit_e_title_background_color_1
        if mode == 1: #Tmavý režim
            main_background_color = '#1c1c1c' #Barva hlavního pozadí
            #Barva pozadí u nastavení
            mode_window_background_color = '#242424' #Barva pozadí okna změny vzhledu
            mode_window_background_color_hover = '#424242' #Aktivní barva pozadí okna změny vzhledu
            #Barva textu
            main_text_color = '#f5f5f5' #Barva textu
            #Horní lišta
            upper_bar_frame_bg_color = '#242424' #Barva pozadí
            upper_bar_frame_bg_color_hover = '#424242' #Barva pozadí, když je na něm myš
            upper_bar_frame_submenu_color = "#595959" #Barva podmenu
            upper_bar_frame_submenu_color_hover = '#808080' #Barva podmenu, když je na něm myš
            #Kalkulačka
            calc_background_color_1 = '#242424' #Barva pozadí kalkulačky 1
            calc_background_color_2 = '#424242' #Barva pozadí kalkulačky 2
            calc_background_color_2_hover = '#595959' #Barva pozadí kalkulačky 2 po přejetí myši
            #Jednotky
            unit_e_title_background_color_1 = '#303030' #Barva pozadí u převodů jednotek
            
        elif mode == 0: #Světlý režim
            main_background_color = '#f5f5f5' #Barva hlavního pozadí
            mode_window_background_color = '#d1d1d1' #Barva pozadí okna změny vzhledu
            mode_window_background_color_hover = 'b3b3b3' #Aktivní barva pozadí okna změny vzhledu
            #Barva textu
            main_text_color = '#0d0d0d' #Barva textu
            #Horní lišta
            upper_bar_frame_bg_color = '#d1d1d1' #Barva pozadí
            upper_bar_frame_bg_color_hover = '#b3b3b3' #Barva pozadí, když je na něm myš
            upper_bar_frame_submenu_color = "#e0e0e0" #Barva podmenu
            upper_bar_frame_submenu_color_hover = '#cccccc' #Barva podmenu, když je na něm myš
            #Kalkulačka
            calc_background_color_1 = '#d1d1d1' #Barva pozadí kalkulačky 1
            calc_background_color_2 = '#b3b3b3' #Barva pozadí kalkulačky 2
            calc_background_color_2_hover = '#e0e0e0' #Barva pozadí kalkulačky 2 po přejetí myši
            #Jednotky
            unit_e_title_background_color_1 = '#dbdbdb' #Barva pozadí u převodů jednotek
            
        else: #Custom
            main_background_color = '#0d0d0d'
    
    #Funkce pro vykreslení základní kalkulačky
    def render_basic_calculator(self):
        global render_bc_frame, render_bc_input_box, render_bc_button_1_0, render_bc_button_1_1, render_bc_button_1_2, render_bc_button_2_0, render_bc_button_3_0, calculator_option
        calculator_option = 0
        #Render paměti kalkulačky
        self.render_BC_memory()
        #Vytovření rámu pro základkní kalkulačku a nastavení listu
        render_bc_frame = Frame(render_main_frame, bg=calc_background_color_1, relief='sunken', borderwidth="2", padx=4, pady=4)
        render_upper_list_submenu.entryconfig("×  "+locale['UB_LSM_option_1'], state="disabled") #Vypnutí zvolení tohoto okna v menu
        #Titulek
        render_bc_title = Label(render_bc_frame, bg=calc_background_color_1, font='bold', fg=main_text_color, text=locale['BC_title'], relief='raised')
        render_bc_title.grid(row=1, column=0, padx=5, pady=5, columnspan=8, sticky='we')
        #Vytvoření vstupu
        render_bc_input_box = Entry(render_bc_frame, width=23, relief='sunken', bg=calc_background_color_2, fg=main_text_color, justify='right', font='bold')
        render_bc_input_box.grid(row=2, column=0, padx=5, pady=5, columnspan=5, ipady=7, ipadx=6)
        #Vytvoření tlačítek
        #0_0 == řádek 0 a sloupec 0
        #Řádek 0
        render_bc_button_0_5 = Button(render_bc_frame, padx=10, pady=6, text="←", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command=lambda: self.func_calc_clear('char'))
        render_bc_button_0_6 = Button(render_bc_frame, padx=10, pady=6, text="C", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command=lambda: self.func_calc_clear('line'))
        render_bc_button_0_7 = Button(render_bc_frame, padx=11, pady=6, text="=", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('equal', ""))
        #Řádek 1
        render_bc_button_1_0 = Button(render_bc_frame, padx=9, pady=6, text="x²", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('oper', 'SQ'))
        render_bc_button_1_1 = Button(render_bc_frame, padx=11, pady=6, text="(", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('add_oper', 'LBRACKET'))
        render_bc_button_1_2 = Button(render_bc_frame, padx=11, pady=6, text=")", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('add_oper', 'RBRACKET'))
        render_bc_button_1_3 = Button(render_bc_frame, padx=10, pady=6, text="×", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('oper', 'MUL'))
        render_bc_button_1_4 = Button(render_bc_frame, padx=11, pady=6, text="/", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('oper', 'DIV'))
        render_bc_button_1_5 = Button(render_bc_frame, padx=4, pady=6, text=" sin ", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', state='disabled')
        render_bc_button_1_6 = Button(render_bc_frame, padx=2, pady=6, text=" log ", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', state='disabled')
        #Řádek 2
        render_bc_button_2_0 = Button(render_bc_frame, padx=10, pady=6, text="√", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('oper', 'SQROOT'))
        render_bc_button_2_1 = Button(render_bc_frame, padx=11, pady=6, text="7", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 7))
        render_bc_button_2_2 = Button(render_bc_frame, padx=11, pady=6, text="8", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 8))
        render_bc_button_2_3 = Button(render_bc_frame, padx=11, pady=6, text="9", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 9))
        render_bc_button_2_4 = Button(render_bc_frame, padx=11, pady=6, text="-", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('oper', 'SUB'))
        render_bc_button_2_5 = Button(render_bc_frame, padx=2, pady=6, text=" cos ", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', state='disabled')
        render_bc_button_2_6 = Button(render_bc_frame, padx=11, pady=6, text="!", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', state='disabled')
        #Řádek 3
        render_bc_button_3_0 = Button(render_bc_frame, padx=11, pady=6, text="↑", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command=lambda: self.func_calc_shift_up())
        render_bc_button_3_1 = Button(render_bc_frame, padx=11, pady=6, text="4", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 4))
        render_bc_button_3_2 = Button(render_bc_frame, padx=11, pady=6, text="5", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 5))
        render_bc_button_3_3 = Button(render_bc_frame, padx=11, pady=6, text="6", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 6))
        render_bc_button_3_4 = Button(render_bc_frame, padx=10, pady=6, text="+", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('oper', 'ADD'))
        render_bc_button_3_5 = Button(render_bc_frame, padx=6, pady=6, text=" tg ", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', state='disabled')
        render_bc_button_3_6 = Button(render_bc_frame, padx=0, pady=6, text="10^x", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 'e'))
        #Řádek 4
        render_bc_button_4_0 = Button(render_bc_frame, padx=11, pady=6, text="0", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 0))
        render_bc_button_4_1 = Button(render_bc_frame, padx=11, pady=6, text="1", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 1))
        render_bc_button_4_2 = Button(render_bc_frame, padx=11, pady=6, text="2", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 2))
        render_bc_button_4_3 = Button(render_bc_frame, padx=11, pady=6, text="3", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('num', 3))
        render_bc_button_4_4 = Button(render_bc_frame, padx=12, pady=6, text=",", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('dec', "."))
        render_bc_button_4_5 = Button(render_bc_frame, padx=8, pady=6, text="%", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', command= lambda: self.func_calc_input('equal', ""))
        render_bc_button_4_6 = Button(render_bc_frame, padx=9, pady=6, text="π", fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, cursor='hand2', state='disabled')
        #Vykreslení tlačítek
        #Řádek 0
        render_bc_button_0_5.grid(row=2, column=5, sticky='W', padx=5, pady=5)
        render_bc_button_0_6.grid(row=2, column=6, sticky='W', padx=5, pady=5)
        render_bc_button_0_7.grid(row=2, column=7, sticky='W', padx=5, pady=5)
        #Řádek 1
        render_bc_button_1_0.grid(row=3, column=0, sticky='W', padx=5, pady=5)
        render_bc_button_1_1.grid(row=3, column=1, sticky='W', padx=5, pady=5)
        render_bc_button_1_2.grid(row=3, column=2, sticky='W', padx=5, pady=5)
        render_bc_button_1_3.grid(row=3, column=3, sticky='W', padx=5, pady=5)
        render_bc_button_1_4.grid(row=3, column=4, sticky='W', padx=5, pady=5)
        render_bc_button_1_5.grid(row=3, column=5, sticky='W', padx=5, pady=5)
        render_bc_button_1_6.grid(row=3, column=6, sticky='W', padx=5, pady=5)
        #Řádek 2
        render_bc_button_2_0.grid(row=4, column=0, sticky='W', padx=5, pady=5)
        render_bc_button_2_1.grid(row=4, column=1, sticky='W', padx=5, pady=5)
        render_bc_button_2_2.grid(row=4, column=2, sticky='W', padx=5, pady=5)
        render_bc_button_2_3.grid(row=4, column=3, sticky='W', padx=5, pady=5)
        render_bc_button_2_4.grid(row=4, column=4, sticky='W', padx=5, pady=5)
        render_bc_button_2_5.grid(row=4, column=5, sticky='W', padx=5, pady=5)
        render_bc_button_2_6.grid(row=4, column=6, sticky='W', padx=5, pady=5)
        #Řádek 3
        render_bc_button_3_0.grid(row=5, column=0, sticky='W', padx=5, pady=5)
        render_bc_button_3_1.grid(row=5, column=1, sticky='W', padx=5, pady=5)
        render_bc_button_3_2.grid(row=5, column=2, sticky='W', padx=5, pady=5)
        render_bc_button_3_3.grid(row=5, column=3, sticky='W', padx=5, pady=5)
        render_bc_button_3_4.grid(row=5, column=4, sticky='W', padx=5, pady=5)
        render_bc_button_3_5.grid(row=5, column=5, sticky='W', padx=5, pady=5)
        render_bc_button_3_6.grid(row=5, column=6, sticky='W', padx=5, pady=5)
        #Řádek 4
        render_bc_button_4_0.grid(row=6, column=0, sticky='W', padx=5, pady=5)
        render_bc_button_4_1.grid(row=6, column=1, sticky='W', padx=5, pady=5)
        render_bc_button_4_2.grid(row=6, column=2, sticky='W', padx=5, pady=5)
        render_bc_button_4_3.grid(row=6, column=3, sticky='W', padx=5, pady=5)
        render_bc_button_4_4.grid(row=6, column=4, sticky='W', padx=5, pady=5)
        render_bc_button_4_5.grid(row=6, column=5, sticky='W', padx=5, pady=5)
        render_bc_button_4_6.grid(row=6, column=6, sticky='W', padx=5, pady=5)
        
    def render_BC_memory(self):
        global render_bc_memory_frame
        #Vytvoření rámu paměti kalkulačky
        render_bc_memory_frame = Frame(render_main_frame, bg=calc_background_color_1, relief='sunken', borderwidth="2", padx=4, pady=4)
        #Titluek paměti kalkulačky
        render_bc_memory_title = Label(render_bc_memory_frame, bg=calc_background_color_1, font='bold', fg=main_text_color, text=locale['BC_memory_title'], relief='raised')
        #Vytvoření renderu samotné paměti
        #Vytvoření číslic
        render_bc_memor_slot_num_1 = Label(render_bc_memory_frame, text='1)', fg=main_text_color, bg=calc_background_color_1)
        render_bc_memor_slot_num_2 = Label(render_bc_memory_frame, text='2)', fg=main_text_color, bg=calc_background_color_1)
        render_bc_memor_slot_num_3 = Label(render_bc_memory_frame, text='3)', fg=main_text_color, bg=calc_background_color_1)
        render_bc_memor_slot_num_4 = Label(render_bc_memory_frame, text='4)', fg=main_text_color, bg=calc_background_color_1)
        render_bc_memor_slot_num_5 = Label(render_bc_memory_frame, text='5)', fg=main_text_color, bg=calc_background_color_1)
        #Vytvoření 5ti míst v paměti
        render_bc_memory_slot_1 = Label(render_bc_memory_frame, text=(str(funcs.BC_num_memory[0])+"  =  "+str(funcs.BC_equal_memory[0])), fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, 
                                        activeforeground=main_text_color, width=28, relief='flat', borderwidth=0, anchor='e', state='disabled', disabledforeground=main_text_color, pady=5, padx=3)
        render_bc_memory_slot_2 = Label(render_bc_memory_frame, text=(str(funcs.BC_num_memory[1])+"  =  "+str(funcs.BC_equal_memory[1])), fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, 
                                        activeforeground=main_text_color, width=28, relief='flat', borderwidth=0, anchor='e', state='disabled', disabledforeground=main_text_color, pady=5, padx=3)
        render_bc_memory_slot_3 = Label(render_bc_memory_frame, text=(str(funcs.BC_num_memory[2])+"  =  "+str(funcs.BC_equal_memory[2])), fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, 
                                        activeforeground=main_text_color, width=28, relief='flat', borderwidth=0, anchor='e', state='disabled', disabledforeground=main_text_color, pady=5, padx=3)
        render_bc_memory_slot_4 = Label(render_bc_memory_frame, text=(str(funcs.BC_num_memory[3])+"  =  "+str(funcs.BC_equal_memory[3])), fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, 
                                        activeforeground=main_text_color, width=28, relief='flat', borderwidth=0, anchor='e', state='disabled', disabledforeground=main_text_color, pady=5, padx=3)
        render_bc_memory_slot_5 = Label(render_bc_memory_frame, text=(str(funcs.BC_num_memory[4])+"  =  "+str(funcs.BC_equal_memory[4])), fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, 
                                        activeforeground=main_text_color, width=28, relief='flat', borderwidth=0, anchor='e', state='disabled', disabledforeground=main_text_color, pady=5, padx=3)
        #Vytvoření 5ti tlačítek "více"
        render_bc_memory_slot_more_1 = Button(render_bc_memory_frame, text="...", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.render_BC_memory_more(0))
        render_bc_memory_slot_more_2 = Button(render_bc_memory_frame, text="...", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.render_BC_memory_more(1))
        render_bc_memory_slot_more_3 = Button(render_bc_memory_frame, text="...", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.render_BC_memory_more(2))
        render_bc_memory_slot_more_4 = Button(render_bc_memory_frame, text="...", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.render_BC_memory_more(3))
        render_bc_memory_slot_more_5 = Button(render_bc_memory_frame, text="...", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.render_BC_memory_more(4))
        #Vytvoření 5ti tlačítek vymazání
        render_bc_memory_slot_del_1 = Button(render_bc_memory_frame, text="X", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.func_calc_memory_delete(0))
        render_bc_memory_slot_del_2 = Button(render_bc_memory_frame, text="X", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.func_calc_memory_delete(1))
        render_bc_memory_slot_del_3 = Button(render_bc_memory_frame, text="X", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.func_calc_memory_delete(2))
        render_bc_memory_slot_del_4 = Button(render_bc_memory_frame, text="X", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.func_calc_memory_delete(3))
        render_bc_memory_slot_del_5 = Button(render_bc_memory_frame, text="X", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, padx=5, command=lambda: self.func_calc_memory_delete(4))
        #Vytvoření 5ti tlačítek načtení
        render_bc_memory_slot_load_1 = Button(render_bc_memory_frame, text=locale['BC_memory_load']+" →", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, command=lambda: self.func_calc_memory_load(0))
        render_bc_memory_slot_load_2 = Button(render_bc_memory_frame, text=locale['BC_memory_load']+" →", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, command=lambda: self.func_calc_memory_load(1))
        render_bc_memory_slot_load_3 = Button(render_bc_memory_frame, text=locale['BC_memory_load']+" →", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, command=lambda: self.func_calc_memory_load(2))
        render_bc_memory_slot_load_4 = Button(render_bc_memory_frame, text=locale['BC_memory_load']+" →", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, command=lambda: self.func_calc_memory_load(3))
        render_bc_memory_slot_load_5 = Button(render_bc_memory_frame, text=locale['BC_memory_load']+" →", cursor='hand2', fg=main_text_color, bg=calc_background_color_2, activebackground=calc_background_color_2_hover, activeforeground=main_text_color, command=lambda: self.func_calc_memory_load(4))
        #Vyrenderování jednotlivých částí
        render_bc_memory_title.grid(row=0, column=0, columnspan=5, sticky='we', padx=5, pady=5)
        #Render 5ti číslic k mezipaměti
        render_bc_memor_slot_num_1.grid(row=1, column=0, padx=5, pady=5) 
        render_bc_memor_slot_num_2.grid(row=2, column=0, padx=5, pady=5) 
        render_bc_memor_slot_num_3.grid(row=3, column=0, padx=5, pady=5) 
        render_bc_memor_slot_num_4.grid(row=4, column=0, padx=5, pady=5)   
        render_bc_memor_slot_num_5.grid(row=5, column=0, padx=5, pady=5) 
        #Render 5ti míst mezipaměti
        render_bc_memory_slot_1.grid(row=1, column=1, padx=5, pady=5)
        render_bc_memory_slot_2.grid(row=2, column=1, padx=5, pady=5)
        render_bc_memory_slot_3.grid(row=3, column=1, padx=5, pady=5)
        render_bc_memory_slot_4.grid(row=4, column=1, padx=5, pady=5)
        render_bc_memory_slot_5.grid(row=5, column=1, padx=5, pady=5)
        #Render 5ti tlačítek "vice"
        render_bc_memory_slot_more_1.grid(row=1, column=2, padx=5, pady=5)
        render_bc_memory_slot_more_2.grid(row=2, column=2, padx=5, pady=5)
        render_bc_memory_slot_more_3.grid(row=3, column=2, padx=5, pady=5)
        render_bc_memory_slot_more_4.grid(row=4, column=2, padx=5, pady=5)
        render_bc_memory_slot_more_5.grid(row=5, column=2, padx=5, pady=5)
        #Render 5ti tlačítek vymazání
        render_bc_memory_slot_del_1.grid(row=1, column=3, padx=5, pady=5)
        render_bc_memory_slot_del_2.grid(row=2, column=3, padx=5, pady=5)
        render_bc_memory_slot_del_3.grid(row=3, column=3, padx=5, pady=5)
        render_bc_memory_slot_del_4.grid(row=4, column=3, padx=5, pady=5)
        render_bc_memory_slot_del_5.grid(row=5, column=3, padx=5, pady=5)
        #Render 5ti tlačítek načtení
        render_bc_memory_slot_load_1.grid(row=1, column=4, padx=5, pady=5)
        render_bc_memory_slot_load_2.grid(row=2, column=4, padx=5, pady=5)
        render_bc_memory_slot_load_3.grid(row=3, column=4, padx=5, pady=5)
        render_bc_memory_slot_load_4.grid(row=4, column=4, padx=5, pady=5)
        render_bc_memory_slot_load_5.grid(row=5, column=4, padx=5, pady=5)
        #Vyrenderování rámu paměti kalkulačky
        render_bc_memory_frame.grid(row=2, column=0, sticky='w', padx=50)
    
    def render_BC_memory_more(self, index):
        render_BC_memory_more_window = Toplevel()
        render_BC_memory_more_window.title(locale['BC_memory_more_window'])
        render_BC_memory_more_window.geometry(str(data['BC_memory_resolution']))
        render_BC_memory_more_window.resizable(0, 0)
        render_BC_memory_more_window.config(bg=mode_window_background_color, relief='flat')
        
        render_BC_memory_more_exit = Button(render_BC_memory_more_window, bg=mode_window_background_color, text='--  '+locale['BC_memory_more_exit']+'  --', fg=main_text_color, padx=20, command=lambda: render_BC_memory_more_window.destroy())
        
        render_BC_memory_more_frame = Frame(render_BC_memory_more_window, bg=calc_background_color_1, relief='sunken', borderwidth=2)
        
        render_BC_label = Label(render_BC_memory_more_frame, text=funcs.BC_num_memory[index], bg=mode_window_background_color, fg=main_text_color)
        render_BC_equal_label = Label(render_BC_memory_more_frame, text="=  "+str(funcs.BC_equal_memory[index]), bg=mode_window_background_color, fg=main_text_color)
        
        render_BC_memory_more_frame.pack(fill='both', expand="True", padx=20, pady=10)
        render_BC_label.pack(padx=5, pady=5)
        render_BC_equal_label.pack(padx=5, pady=5)
        render_BC_memory_more_exit.pack(padx=20, pady=10)
    
    #Funkce pro vykreslení převodů jednotek
    def render_unit_conver(self):
        global calculator_option, render_uc_frame, render_uc_l_menu, ucl_var, uce_var, ucr_var, render_uc_r_menu, render_uc_r_entry, render_uc_l_entry
        calculator_option = 1
        #Vytvoření základního rámu okna
        render_uc_frame = Frame(render_main_frame, bg=calc_background_color_1, relief='sunken', borderwidth="2", padx=4, pady=4)
        render_upper_list_submenu.entryconfig("×  "+locale['UB_LSM_option_3'], state="disabled") #Vypnutí zvolení tohoto okna v menu
        #Render titulu
        render_uc_title = Label(render_uc_frame, bg=calc_background_color_1, font='bold', fg=main_text_color, text=locale['UC_title'], relief='raised')
        #Vytvoření tkinter promněnných
        uce_var = StringVar()
        uce_var.set(locale['unit_data'][0])
        ucl_var = StringVar()
        ucl_var.set(unit_conv[unit_data_list[locale['unit_data'].index(uce_var.get())]][1])
        ucr_var = StringVar()
        ucr_var.set(unit_conv[unit_data_list[locale['unit_data'].index(uce_var.get())]][1])
        #Render druhé řady
        render_uc_e_title = Label(render_uc_frame, bg=calc_background_color_1, font='bold', fg=main_text_color, text=locale['UC_e_title']+" :", relief='flat') #Render titulku
        render_uc_e_menu = OptionMenu(render_uc_frame, uce_var, *locale['unit_data'], command=lambda x:self.func_unit_mode_change(unit_data_list[locale['unit_data'].index(uce_var.get())])) #Render listu možností pro převody jednotek
        render_uc_e_menu.configure(bg=unit_e_title_background_color_1, font='bold', fg=main_text_color, activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, highlightthickness=0, relief='flat', cursor='hand2') #Úprava listu možností pro převod jednotek
        render_uc_e_sep = ttk.Separator(render_uc_frame, orient='horizontal') #Vytvoření separátoru
        #Render třetí řady
        render_uc_l_menu = OptionMenu(render_uc_frame, ucl_var, *unit_conv[unit_data_list[locale['unit_data'].index(uce_var.get())]]) #Render levého listu možností pro jednotky
        render_uc_r_menu = OptionMenu(render_uc_frame, ucr_var, *unit_conv[unit_data_list[locale['unit_data'].index(uce_var.get())]]) #Redner pravého listu možnost pro jednotky
        render_uc_l_menu.configure(width=7, bg=upper_bar_frame_submenu_color, borderwidth=1, relief='sunken', fg=main_text_color, activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, highlightthickness=0, pady=5, state='normal', cursor='hand2') #Úprava levého listu možností pro jednotky
        render_uc_r_menu.configure(width=7, bg=upper_bar_frame_submenu_color, borderwidth=1, relief='sunken', fg=main_text_color, activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, highlightthickness=0, pady=5, state='normal', cursor='hand2') #Úprava pravého listu možností pro jednotky
        render_uc_l_entry = Entry(render_uc_frame, bg=upper_bar_frame_submenu_color, borderwidth=1, relief='sunken', fg=main_text_color, font=('bold', 11), width=10) #Levý vstup hodnoty jednotky
        render_uc_r_entry = Entry(render_uc_frame, bg=upper_bar_frame_submenu_color, borderwidth=1, relief='sunken', fg=main_text_color, font=('bold', 11), width=10, state='disabled', disabledbackground=upper_bar_frame_submenu_color, disabledforeground=main_text_color) #Pravý výstup hodnoky jednotky
        render_uc_equal = Button(render_uc_frame, bg=calc_background_color_1, borderwidth=2, relief='raised', fg=main_text_color, font=('bold', 10), text='=', width=5, activebackground=calc_background_color_2_hover, 
                                 activeforeground=main_text_color, cursor='hand2', command=lambda: self.func_unit_conver(ucl_var.get(), ucr_var.get(), unit_conv_list[locale['unit_data'].index(uce_var.get())], 
                                 unit_data_list[locale['unit_data'].index(uce_var.get())], render_uc_l_entry.get())) #Tlačítko pro převod jednotek
        render_uc_delete = Button(render_uc_frame, bg=calc_background_color_1, borderwidth=2, relief='raised', fg=main_text_color, font=('bold', 10), text='C', activebackground=calc_background_color_2_hover, width=3,
                                 activeforeground=main_text_color, cursor='hand2', command=lambda: self.func_unit_delete()) #Tlačítko pro vymazání textu z vstupů
        render_uc_switch = Button(render_uc_frame, bg=calc_background_color_1, borderwidth=2, relief='raised', fg=main_text_color, font=('bold', 10), text='↔', activebackground=calc_background_color_2_hover, width=3,
                                 activeforeground=main_text_color, cursor='hand2', command=lambda: self.func_unit_swith()) #Tlačítko pro zaměnění textu z vstupů
        #Render prvků
        #Render první řady
        render_uc_title.grid(row=1, column=0, padx=5, pady=5, columnspan=7, sticky='we')
        #Render druhé řady
        render_uc_e_title.grid(row=2, column=0, sticky='we', padx=5, pady=5, columnspan=3)
        render_uc_e_menu.grid(row=2, column=3, sticky='we', padx=5, pady=5, columnspan=2)
        #Render třetí řady/separátoru
        render_uc_e_sep.grid(row=3, column=0, columnspan=7, sticky='we', padx=5, pady=5)
        #Render čtvrté řady
        render_uc_l_entry.grid(row=4, column=0, sticky='we', padx=5, pady=5, ipady=3, ipadx=3)
        render_uc_l_menu.grid(row=4, column=1, sticky='we', padx=5, pady=5)
        render_uc_equal.grid(row=4, column=2, sticky='we', padx=5, pady=5)
        render_uc_r_entry.grid(row=4, column=3, sticky='we', padx=5, pady=5, ipady=3, ipadx=3) 
        render_uc_r_menu.grid(row=4, column=4, sticky='we', padx=5, pady=5)
        render_uc_delete.grid(row=4, column=5, sticky='we', padx=5, pady=5)
        render_uc_switch.grid(row=4, column=6, sticky='we', padx=5, pady=5)      
           
    #Funkce pro vytvoření horní lišty
    def render_upper_bar(self):
        global render_upper_bar_frame, render_upper_list_submenu
        #Vytvoření horní lišty
        render_upper_bar_frame = Frame(render_main_frame, bg=upper_bar_frame_bg_color, relief='raised', borderwidth="2")
        #Vytvoření tlačítek na liště
        render_upper_list_btn = Menubutton(render_upper_bar_frame, text=locale["UB_LB_text"], fg=main_text_color, bg=upper_bar_frame_bg_color, padx=15, activebackground=upper_bar_frame_bg_color_hover, activeforeground=main_text_color, relief='groove', borderwidth="0.5", cursor='hand2')
        render_upper_settings_btn = Menubutton(render_upper_bar_frame, text=locale["UB_SB_text"], fg=main_text_color, bg=upper_bar_frame_bg_color, padx=25, activebackground=upper_bar_frame_bg_color_hover, activeforeground=main_text_color, relief='groove', borderwidth="0.5", cursor='hand2')
        #Vykreslení tlačítek na liště
        render_upper_list_btn.grid(row = 0, column= 0)
        render_upper_settings_btn.grid(row=0, column=1)
        #Vytvoření podlistu pro tlačítka
        render_upper_list_submenu = Menu(render_upper_list_btn, tearoff=0, bg=upper_bar_frame_submenu_color, fg=main_text_color, disabledforeground=main_text_color, cursor='hand2')
        render_upper_settings_submenu = Menu(render_upper_settings_btn, tearoff=0, bg=upper_bar_frame_submenu_color, fg=main_text_color, disabledforeground=main_text_color, cursor='hand2')
        #Přidání položek do podlistu pro 1. tlačítko
        render_upper_list_submenu.add_command(label="×  "+locale['UB_LSM_option_title_1'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='disabled')
        render_upper_list_submenu.add_separator()
        render_upper_list_submenu.add_command(label="×  "+locale['UB_LSM_option_1'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='normal', command=lambda:self.func_render_BC())
        render_upper_list_submenu.add_command(label="×  "+locale['UB_LSM_option_2'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='normal', command=lambda:self.func_render_BC())
        render_upper_list_submenu.add_separator()
        render_upper_list_submenu.add_command(label="×  "+locale['UB_LSM_option_title_2'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='disabled')
        render_upper_list_submenu.add_separator()
        render_upper_list_submenu.add_command(label="×  "+locale['UB_LSM_option_3'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='normal', command=lambda:self.func_render_unit())
        render_upper_list_submenu.add_command(label="×  "+locale['UB_LSM_option_4'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='normal', command=lambda:self.func_render_unit())
        render_upper_list_submenu.add_separator()
        render_upper_list_submenu.add_command(label="×  "+locale['UB_LSM_option_end'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='normal', command=lambda:self.func_quit(self.main_root))
        #Přidání položek do podlistu pro 2. tlačítko
        render_upper_settings_submenu.add_command(label="×  "+locale['UB_SSM_option_1'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='normal', command=self.render_dark_light_mode_window)
        render_upper_settings_submenu.add_command(label="×  "+locale['UB_SSM_option_2'], activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, state='normal', command=self.render_locale_type_window)
        #Zpárování podlistů k tlačítkům
        render_upper_settings_btn.config(menu= render_upper_settings_submenu)
        render_upper_list_btn.config(menu= render_upper_list_submenu)

    #Funkce vytvoření nového okna pro změnu vzhledu
    def render_dark_light_mode_window(self):
        #Vytvoření nového okna
        render_mode_window = Toplevel()
        render_mode_window.title(locale["DL_MW_title"])
        render_mode_window.geometry(str(data['light_dark_mode_resolution']))
        render_mode_window.resizable(0, 0)
        #Vytvoření rámu nového okna
        render_mode_frame = Frame(render_mode_window, bg=mode_window_background_color)
        render_mode_frame.grid_columnconfigure(0, weight=1)
        render_mode_frame.grid_rowconfigure(0, weight=0)
        #Titulek v okně
        render_dl_mode_title = Label(render_mode_frame, text=locale['DL_MC_title'], bg=mode_window_background_color, fg=main_text_color, padx=30, pady=3, font="bold", relief='raised')
        render_dl_mode_title.grid(row=0, column=0, sticky="WE", columnspan=2)
        #Vytvoření promněnné pro více požností
        mode_value = IntVar()
        #Vytvoření možností
        render_dark_mode_toggle = Radiobutton(render_mode_frame, text=locale["dark_mode"], bg=mode_window_background_color, fg=main_text_color, padx=30, pady=5, relief='flat', activebackground=mode_window_background_color, activeforeground=main_text_color, selectcolor=mode_window_background_color, variable=mode_value, value=1, state='normal', command=lambda: self.func_appear_change(mode_value.get()), cursor='hand2')
        render_light_mode_toggle = Radiobutton(render_mode_frame, text=locale["light_mode"], bg=mode_window_background_color, fg=main_text_color, padx=30, pady=5, relief='flat', activebackground=mode_window_background_color, activeforeground=main_text_color, selectcolor=mode_window_background_color, variable=mode_value, value=0, state='normal', command=lambda: self.func_appear_change(mode_value.get()), cursor='hand2')
        render_light_mode_custom = Radiobutton(render_mode_frame, text=locale["custom"], bg=mode_window_background_color, fg=main_text_color, padx=30, pady=5, relief='flat', activebackground=mode_window_background_color, activeforeground=main_text_color, selectcolor=mode_window_background_color, state='disabled')
        render_dark_mode_toggle.grid(row=1, column=0, sticky="W", columnspan=2)
        render_light_mode_toggle.grid(row=2, column=0, sticky="W", columnspan=2)
        render_light_mode_custom.grid(row=3, column=0, columnspan=2, sticky="W")
        #Tlačítka
        render_mode_accept = Button(render_mode_frame, text=locale["DL_MAC_button"], padx=30, command=lambda: self.func_mode_reload(render_mode_window, mode_value.get(), calculator_option), bg=upper_bar_frame_submenu_color, fg=main_text_color, activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, cursor='hand2')
        render_mode_cancel = Button(render_mode_frame, text=locale["DL_MCA_button"], padx=30, command=lambda: self.func_quit(render_mode_window), bg=upper_bar_frame_submenu_color, fg=main_text_color, activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, cursor='hand2')
        render_mode_accept.grid(row=4, column=0, sticky="WS", padx=10, pady=2)
        render_mode_cancel.grid(row=4, column=1, sticky="WS", padx=10, pady=2)
        #Vykreslení rámu nového okna
        render_mode_frame.pack(fill='both', expand="True")
        
    #Funkce na vytvoření nového okna pro zěmu jazyka
    def render_locale_type_window(self):
        #Vytvoření nového okna
        render_locale_window = Toplevel()
        render_locale_window.title(locale['LT_title'])
        render_locale_window.geometry(str(data['locale_type_resolution']))
        render_locale_window.resizable(0, 0)
        #Vytvoření rámu nového okna
        render_locale_frame = Frame(render_locale_window, bg=mode_window_background_color)
        render_locale_frame.grid_columnconfigure(0, weight=1)
        render_locale_frame.grid_rowconfigure(0, weight=0)
        #Titulek v okně
        render_locale_title = Label(render_locale_frame, text=locale['L_title'], bg=mode_window_background_color, fg=main_text_color, padx=30, pady=3, font='bold', relief="raised")
        render_locale_title.grid(column=0, row=0, columnspan=2, sticky="WE")
        #Vytvoření menu možností
        ddm_var = StringVar()
        ddm_var.set(data['locale_list'][locale_default])
        render_locale_ddm = OptionMenu(render_locale_frame, ddm_var, *data['locale_list'])
        render_locale_ddm.config(bg=upper_bar_frame_submenu_color, borderwidth=0, relief='flat', fg=main_text_color, activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color, padx=50)
        render_locale_ddm.grid(row=1, column=0, pady=8, sticky="W", columnspan=2, padx=50)
        #Tlačítka
        render_mode_accept = Button(render_locale_frame, text=locale["DL_MAC_button"], padx=30, command=lambda: self.func_laguage_change(render_locale_window ,ddm_var.get(), calculator_option) , bg=upper_bar_frame_submenu_color, fg=main_text_color, activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color)
        render_mode_cancel = Button(render_locale_frame, text=locale["DL_MCA_button"], padx=30, command=lambda: self.func_quit(render_locale_window), bg=upper_bar_frame_submenu_color, fg=main_text_color, activebackground=upper_bar_frame_submenu_color_hover, activeforeground=main_text_color)
        render_mode_accept.grid(row=4, column=0, sticky="WS", padx=10, pady=37)
        render_mode_cancel.grid(row=4, column=1, sticky="WS", padx=10, pady=37)
        #Vykreslení rámu nového okna
        render_locale_frame.pack(fill='both', expand='true')


class Main(Render, OpenFile):
    def main(self):
        global main_root
        #Hlavní vytvoření GUI
        self.main_root = Tk()
        self.main_root.title("Vojtěchovitch")
        self.main_root.geometry(str(data['main_root_resolution']))
        #Render prvků
        mode = data['dark_light_mode']
        self.render_main(mode, calculator_option)
        #Cyklus aplikace
        self.main_root.mainloop()
        os.system('cls')