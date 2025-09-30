#! python3

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from time import perf_counter
from math import floor

import os
import random

from common import ExperimentFrame, InstructionsFrame, InstructionsAndUnderstanding, Measure, MultipleChoice
from questionnaire import Questionnaire
from gui import GUI
from diets import DIETS, DIETS_KIDS
from constants import MAX_BDM_PRIZE, MINUTEBONUS, TESTING


################################################################################
# TEXTS

instructions = """Na následujících stránkách najdete stručné popisy jídel podávaných v nemocniční jídelně <b>Fakultní nemocnice Motol</b>. Cílem tohoto úkolu je pro Fakultní nemocnici Motol daná jídla ohodnotit.

Vaším úkolem je:
(a) přepsat čtyři údaje o složení (energie, B - bílkoviny, T - tuky, S - sacharidy (cukry)) přesně tak, jak jsou uvedeny pro vybraný jídelníček, a 
(b) po přečtení podávaného pokrmu ohodnotit každé jídlo (snídani, oběd, večeři) ve vybraném jídelníčku podle toho, jak Vám osobně připadá chutné, vizuálně přitažlivé a nutričně bohaté.
Po každém ohodnoceném jídelníčku se můžete rozhodnout, zda budete pokračovat dalším jídelníčkem, nebo úkol zcela ukončíte a přesunete se k další části studie. Záleží pouze na Vás, zda budete v tomto úkolu pokračovat, nebo skončíte. Z předčasného ukončení nevyplývá žádná penalizace.
<b>{}</b>
Úkol bude trvat maximálně 30 minut.

Po přečtení instrukcí zodpovězte kontrolní otázky níže."""

neutral = ""

monetary = f"""
Za každou minutu, kterou na úkolu strávíte, získáte k základní odměně navíc bonusovou platbu ve výši {MINUTEBONUS} Kč.
"""

person_moralization = """
Tím, že se rozhodnete vytrvat co nejdéle, ukážete, že jste starostlivý a morální člověk, který udělá něco navíc, aby pomohl ostatním. Každý další ohodnocený jídelníček prokazuje Vaše odhodlání dělat to, co je správné a pomáhat potřebné instituci.
"""

task_moralization = """
Vaše pečlivé hodnocení jídelníčků pomůže nemocničním dietologům zvážit nutriční a estetické informace, aby mohli sestavit stravovací plány, které jsou z lékařského hlediska vhodné a zlepšují zdraví pacientů. Pokračováním v tomto úkolu pomůžete dobré věci, protože Vaše hodnocení přímo podporuje zdravější a bezpečnější stravování pro osoby v péči.
"""

monetary_end = "Za hodnocení jídelníčků jste obdržel(a) navíc odměnu {} Kč."

Control1 = "Co se stane, když se rozhodnete úkol ukončit dříve než za 30 minut?"
Answers1 = ["Budete penalizováni a přijdete o celou odměnu.", "Musíte zaplatit poplatek a opustit laboratoř.", "Můžete úkol bez jakékoli penalizace ukončit a přesunout se na další část studie.", "Musíte počkat, než vyprší časomíra, jinak se studie zneplatní."]
Feedback1 = ["Špatně. Můžete úkol bez jakékoli penalizace ukončit a přesunout se na další část studie.", "Špatně. Můžete úkol bez jakékoli penalizace ukončit a přesunout se na další část studie.", "Ano, správně.", "Špatně. Můžete úkol bez jakékoli penalizace ukončit a přesunout se na další část studie."]

Control2 = "Které kroky musíte u každého jídelníčku provést, než se rozhodnete pokračovat nebo skončit?"
Answers2 = ["Vyfotit jídlo a nahrát fotografii do systému.", "Přesně přepsat údaje o energii, bílkovinách, tucích a cukrech a pak subjektivně ohodnotit\nchutnost, vzhled a nutriční bohatost.", "Přepsat celý text kartičky včetně alergenních látek a poznámek kuchaře.", "Přepisovat celý jídelní lístek do aplikace."]
Feedback2 = ["Špatně. Máte přesně přepsat údaje o energii, bílkovinách, tucích a cukrech a pak subjektivně ohodnotit chutnost, vzhled a nutriční bohatost jednotlivých jídel.", "Ano, správně.", "Špatně. Máte přesně přepsat údaje o energii, bílkovinách, tucích a cukrech a pak subjektivně ohodnotit chutnost, vzhled a nutriční bohatost jednotlivých jídel.", "Špatně. Máte přesně přepsat údaje o energii, bílkovinách, tucích a cukrech a pak subjektivně ohodnotit chutnost, vzhled a nutriční bohatost jednotlivých jídel."]


task = "V záložce Jídelníčky v menu nahoře je seznam všech diet a jejich složení. Prosíme, nejdříve <b>ve sloupci <color: red4>“Dieta”</color> najděte v seznamu dietu označenou jako {} a vyplňte údaje o jejím složení</b>. Následně jídla v dané dietě ohodnoťte."

tasteText = "Jak chutně toto jídlo působí?"
lookText = "Jak bude jídlo nejspíše vizuálně přitažlivé?"
nutritionText = "Jak nutričně bohaté se Vám toto jídlo zdá?"


menus_text = """V seznamu níže najděte <b>dietu označenou jako {}</b> a v záložce Hodnocení vyplňte údaje o jejím nutričním složení.
Označení diet naleznete v levém horním rohu v prvním sloupci. Každý řádek odpovídá jídelníčku pro danou dietu ve vybraný den.  
Jídla, která budete posléze hodnotit naleznete ve sloupcích Snídaně, Oběd a Večeře v řádku s Vámi nalezenou dietou."""

difficultyQ1 = "Jak obtížný se Vám úkol zdá?"
satisfactionQ1 = "Jak moc jste spokojen(a) s úsilím, které jste do úkolu zatím vložil(a)?"

proceedText = "<center>Ohodnoťte právě dokončený úkol a poté stiskněte tlačítko “Pokračovat”.</center>"

difficultyQ2 = "Jak obtížný se Vám celý úkol zdál?"
difficultyL = "Velmi snadný"
difficultyR = "Velmi obtížný"

satisfactionQ2= "Jak moc jste spokojen(a) s úsilím, které jste do celého úkolu vložil(a)?"
satisfactionL = "Velmi nespokojen(a)"
satisfactionR = "Velmi spokojen(a)"

guiltQ2 = "Do jaké míry cítíte vinu za to, jak jste celý úkol zvládl(a)?"
guiltL = "Necítím žádnou vinu"
guiltR = "Cítím velkou vinu"

ratingsText = "Nyní odpovězte na následující otázky ohledně právě dokončeného úkolu:"
ratingsText2 = "Tvrzení níže ohodnoťte na základě toho, nakolik s nimi souhlasíte."

continuation = """Dosud jste dokončili hodnocení {} a strávili na úkolu {} minut.
{}
<b>Uveďte, zda chcete pokračovat hodnocení dalších jídelníčků, nebo zda chcete úkol ukončit.</b>
V úkolu je možné pokračovat nejdéle do uplynutí 30 minut od jeho začátku.

Pokud zvolíte „Pokračovat“, zobrazí se Vám další jídelníček k přepsání nutričních hodnot a ohodnocení jídel. 
Pokud zvolíte „Ukončit“, úkol skončí a přesunete se na další část studie.

Je to zcela na Vás: můžete kdykoliv přestat bez jakékoli penalizace."""

reminder_neutral = ""

reminder_monetary = f"""
Za každou minutu, kterou na úkolu strávíte, získáte k základní odměně navíc bonusovou platbu ve výši {MINUTEBONUS} Kč. 
"""

reminder_person_moralization = """
Tím, že se rozhodnete vytrvat co nejdéle, ukážete, že jste starostlivý a morální člověk, který udělá něco navíc, aby pomohl ostatním. Každý další ohodnocený jídelníček prokazuje Vaše odhodlání dělat to, co je správné a pomáhat potřebné instituci.
"""

reminder_task_moralization = """
Vaše pečlivé hodnocení jídelníčků pomůže nemocničním dietologům zvážit nutriční a estetické informace, aby mohli sestavit stravovací plány, které jsou z lékařského hlediska vhodné a zlepšují zdraví pacientů. Pokračováním v tomto úkolu pomůžete dobré věci, protože Vaše hodnocení přímo podporuje zdravější a bezpečnější stravování pro osoby v péči.
""" 

endtime = """Dosud jste dokončili hodnocení {} a strávili na úkolu {} minut.

Jelikož již uplynulo více než 30 minut od začátku úkolu, hodnocení dalších jídelníčků již není možné."""


continuation2 = """Dosud jste dokončili hodnocení {} a strávili na úkolu {} minut.

V úkolu budete pokračovat, dokud neuplyne 10 minut.

Klikněte na tlačítko „Pokračovat“."""

endtime2 = """Dokončili jste hodnocení {} a strávili na úkolu {} minut.

Jelikož již uplynulo více než 10 minut od začátku úkolu, úkol je ukončen."""


BDMtext = """Nyní můžete uvést, kolik peněz vyžadujete jako bonus navíc, abyste na úkolu ještě 10 minut pracovali. Pomocí mechanismu popsaného níže bude určeno, zda na úkolu budete pracovat či ne a tedy zda požadovaný bonus navíc získáte či nikoliv.

Vysvětleme si pravidla:

Níže uvidíte pole, kam zadáte nejnižší částku (v Kč), za kterou byste byli ochotni strávit dalších 10 minut stejným úkolem (bez možnosti skončit dříve), mezi 0 Kč a 100 Kč.

Po odeslání této částky generátor náhodných čísel vylosuje náhodné číslo mezi 0 a 100 (tj. všechny čísla od 0 do 100 mají stejnou pravděpodobnost, že budou vylosována).

Pokud bude náhodné číslo větší či rovné (≥) Vámi minimálně požadované částce, obdržíte částku ve velikosti vylosovaného náhodného čísla jako bonus a budete 10 minut dále pracovat na úkolu. Například, uvedete-li 20 Kč a bude vylosováno 50 Kč, získáte bonus 50 Kč navíc a budete pokračovat v úkolu.

Pokud je náhodné číslo menší než (<) Vámi minimálně požadovaná částka, nezískáte dodatečný bonus a na úkolu už pracovat nebudete. Například, uvedete-li 50 Kč a bude vylosováno 20 Kč, nezískáte nic navíc, nebudete pokračovat v úkolu a přesunete se k další částí studie.

Tento proces zajišťuje, že nejvýhodnější je zadat skutečné minimum, za které byste na úkolu pracovali. Když uvedete moc vysokou požadovanou částku, je nízká pravděpodobnost, že bude vylosované číslo stejné nebo vyšší a nezískáte tedy nic. Pakliže uvedete příliš nízkou částku, může se stát, že za úkol dostanete méně, než byste chtěli. Přeplacení ani podstřelení se tedy nevyplácí.

Než uvedete nejnižší částku (v Kč), za kterou byste byli ochotni strávit dalších 10 minut stejným úkolem, zkontrolujeme si porozumění popsaného mechanismu."""


BDMcontrol1 = "Co se stane, pokud zadáte částku 20 Kč a generátor vylosuje náhodné číslo 30 Kč?"
BDManswers1 = ["Na úkolu už nebudete pracovat.", "Dostanete 30 Kč a budete pokračovat v úkolu, jak dlouho budete chtít.", 
               "Dostanete 30 Kč a budete 10 minut pracovat na úkolu.", "Dostanete 20 Kč a budete 10 minut pracovat na úkolu."]
BDMfeedback1 = ["Špatně. Dostanete 30 Kč navíc a budete 10 minut pracovat na úkolu.",
                "Špatně. Dostanete 30 Kč navíc a budete 10 minut pracovat na úkolu.",
                "Ano, správně.",
                "Špatně. Dostanete 30 Kč navíc a budete 10 minut pracovat na úkolu."]


BDMcontrol2 = "Proč není výhodné uvést vyšší částku, než za kterou byste byli ochotni úkol vykonat?"
BDManswers2 = [
    "Protože by to mohlo narušit studii.",
    "Protože se může stát, že nebudete úkol vykonávat za částku, za kterou byste byli ochotni pracovat.",
    "Protože je větší pravděpodobnost, že vyhraje někdo jiný.",
    "Protože budete automaticky penalizováni."
]
BDMfeedback2 = [
    "Špatně. Správná odpověď je, že se může stát, že nebudete úkol vykonávat za částku, za kterou byste byli ochotni pracovat.",
    "Ano, správně.",
    "Špatně. Správná odpověď je, že se může stát, že nebudete úkol vykonávat za částku, za kterou byste byli ochotni pracovat.",
    "Špatně. Správná odpověď je, že se může stát, že nebudete úkol vykonávat za částku, za kterou byste byli ochotni pracovat."
]

BDMproceed = "Po dokončení stiskněte tlačítko “Pokračovat”."

decisionText = "Nyní, prosíme, uveďte nejnižší částku (v Kč), za kterou byste byli ochotni strávit dalších 10 minut\nstejným úkolem (bez možnosti dříve skončit), mezi 0 Kč a 100 Kč (v celých korunách)."

BDMresult = """Uvedli jste: {}
Generátor náhodných čísel vylosoval: {}

{}

Po dokončení stiskněte tlačítko “Pokračovat”."""

BDMwon = "Náhodné číslo je větší či rovné (≥) než Vámi minimálně požadovaná částka. Obdržíte tedy částku {} Kč a budete 10 minut pracovat na úkolu." 

BDMlost = "Náhodné číslo je menší než (<) Vámi minimálně požadovaná částka. Nezískáte dodatečný bonus a na úkolu už pracovat nebudete."

bmdRewardText = "Za dodatečné plnění úkolu s jídelníčky dostáváte {} Kč."

labels = ["rozhodně nesouhlasím", "nesouhlasím", "spíše nesouhlasím", "neutrální", "spíše souhlasím", "souhlasím","rozhodně souhlasím"]

################################################################################


class Task(ExperimentFrame):
    def __init__(self, root):
        if not "menu_order" in root.status:
            menus = [f for f in os.listdir(os.path.join(os.path.dirname(__file__), 'Menus')) if f.endswith('.png')]
            kidsMenus = [f for f in os.listdir(os.path.join(os.path.dirname(__file__), 'Menus2')) if f.endswith('.png')]
            random.shuffle(menus)
            random.shuffle(kidsMenus)
            root.status["menu_length"] = len(menus)
            root.status["menu_order"] = menus + kidsMenus

        super().__init__(root)        

        if not "trial" in self.root.status or not self.root.status["trial"]:
            self.root.status["trial"] = 0

        style = ttk.Style()
        style.configure('TNotebook', background='white', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Helvetica', 15), background='white', width=25,
                        foreground='black', borderwidth=1, padding=[10, 5], lightcolor='white', focuscolor='white', labelbackground='white')
        style.map('TNotebook.Tab',
              background=[('selected', 'white'), ('!selected', 'white')],
              font=[('selected', ('Helvetica', 15, 'bold')), ('!selected', ('Helvetica', 15))])
        n = ttk.Notebook(self, style='TNotebook')
        
        self.newTrial()

        self.moralization = Moralization(root, self)
        self.menus = Menus(root, self)
        n.add(self.moralization, text='Hodnocení')
        n.add(self.menus, text='Jídelníčky')
        n.pack(expand=True, fill='both')

    def write(self):
        self.file.write("Task\n")
        self.file.write(self.id + "\t" + str(self.root.status["trial"]) + "\t" + self.root.status["menu_order"][self.root.status["trial"] - 1] + "\t" + self.currentDiet + "\t" + self.root.status["condition"] + "\t")
        self.file.write(str(perf_counter() - self.root.status["startTime"]))
        self.moralization.write()        

    def newTrial(self):
        self.root.status["trial"] += 1

        if self.root.status["trial"] <= self.root.status["menu_length"]:
            self.currentDiet = random.choice(DIETS)
        else:
            self.currentDiet = random.choice(DIETS_KIDS)

        if self.root.status["trial"] == 1:
            self.root.status["startTime"] = perf_counter()

    def nextFun(self):
        super().nextFun()
        


class Moralization(InstructionsFrame):
    def __init__(self, root, taskFrame):
        super().__init__(root, text = task.format(taskFrame.currentDiet), height = 3, width = 100)

        self.taskFrame = taskFrame

        self.ratingFrame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.ratingFrame.grid(row=3, column=1)
        self.ratingFrame.columnconfigure(0, weight=1)
        self.ratingFrame.columnconfigure(3, weight=1)

        # Label for instruction
        self.label_intro = ttk.Label(self.ratingFrame, text="Nutriční údaje z prvního sloupce", font="helvetica 15 bold", background="white")
        self.label_intro.grid(row=3, column=1, columnspan=2, padx=10, pady=(20, 5))

        # Energie (kJ)
        self.label_energy = ttk.Label(self.ratingFrame, text="Energie (kJ):", font="helvetica 15", background="white")
        self.label_energy.grid(row=4, column=1, sticky="e", padx=10, pady=2)        
        self.vcmdEnergy = (self.root.register(self.checkNutrition), '%P', "energy")
        self.entry_energy = ttk.Entry(self.ratingFrame, width=20, font="helvetica 15", validatecommand=self.vcmdEnergy, validate = "key")
        self.entry_energy.grid(row=4, column=2, sticky="w", padx=10, pady=2)

        # Obsah bílkovin (B)
        self.label_protein = ttk.Label(self.ratingFrame, text="Obsah bílkovin (B):", font="helvetica 15", background="white")
        self.label_protein.grid(row=5, column=1, sticky="e", padx=10, pady=2)
        self.vcmdProtein = (self.root.register(self.checkNutrition), '%P', "protein")
        self.entry_protein = ttk.Entry(self.ratingFrame, width=20, font="helvetica 15", validatecommand=self.vcmdProtein, validate = "key")
        self.entry_protein.grid(row=5, column=2, sticky="w", padx=10, pady=2)

        # Obsah tuků (T)
        self.label_fat = ttk.Label(self.ratingFrame, text="Obsah tuků (T):", font="helvetica 15", background="white")
        self.label_fat.grid(row=6, column=1, sticky="e", padx=10, pady=2)
        self.vcmdFat = (self.root.register(self.checkNutrition), '%P', "fat")
        self.entry_fat = ttk.Entry(self.ratingFrame, width=20, font="helvetica 15", validatecommand=self.vcmdFat, validate = "key")
        self.entry_fat.grid(row=6, column=2, sticky="w", padx=10, pady=2)

        # Obsah cukrů (S)
        self.label_sugar = ttk.Label(self.ratingFrame, text="Obsah cukrů (S):", font="helvetica 15", background="white")
        self.label_sugar.grid(row=7, column=1, sticky="e", padx=10, pady=2)
        self.vcmdSugar = (self.root.register(self.checkNutrition), '%P', "sugar")
        self.entry_sugar = ttk.Entry(self.ratingFrame, width=20, font="helvetica 15", validatecommand=self.vcmdSugar, validate = "key")
        self.entry_sugar.grid(row=7, column=2, sticky="w", padx=10, pady=2)

        qs = [tasteText, lookText, nutritionText]
        chars = ["taste", "look", "nutrition"]
        widgets = {"canvases":[], "separators": [], "labels": [], "measures": {"taste":[], "look":[], "nutrition":[]}, "questions": {"taste":[], "look":[], "nutrition":[]}}
        for i, food in enumerate(["Snídaně", "Oběd", "Večeře"]):
            canvas = Canvas(self, background="white", highlightbackground="white", highlightcolor="white")
            canvas.grid(row= + i + 4, column=0, columnspan=3, pady=(10, 0))
            canvas.columnconfigure(2, weight=1)
            widgets["canvases"].append(canvas)
            widgets["separators"].append(ttk.Separator(canvas, orient="horizontal"))
            widgets["separators"][i].grid(row=1, column=0, columnspan=3, sticky="ew", pady=(20,0))
            widgets["labels"].append(ttk.Label(canvas, text=food, font="helvetica 15 bold", background="white"))
            widgets["labels"][i].grid(row=2, column=0, columnspan=3, sticky="n", pady=(10, 0), padx=20)
            for j, question in enumerate(qs):
                widgets["questions"][chars[j]].append(ttk.Label(canvas, text=question, font="helvetica 15", background="white"))
                widgets["questions"][chars[j]][i].grid(row= + j + 3, column=0, sticky="e", padx=10, pady=2)
            widgets["measures"]["taste"].append(Measure(canvas, "", [i for i in range(1,8)], "Zcela nechutně", "Velmi chutně", labelPosition="next", shortText=f"taste{i+1}", questionPosition="next", center=True, function = self.rated))
            widgets["measures"]["look"].append(Measure(canvas, "", [i for i in range(1,8)], "Zcela nevzhledné", "Velmi přitažlivé", labelPosition="next", shortText=f"look{i+1}", questionPosition="next", center=True, function = self.rated))
            widgets["measures"]["nutrition"].append(Measure(canvas, "", [i for i in range(1,8)], "Zcela chudé na živiny", "Velmi bohaté na živiny", labelPosition="next", shortText=f"nutrition{i+1}", questionPosition="next", center=True, function = self.rated))
            widgets["measures"]["taste"][i].grid(row=3, column=2, pady=2, sticky="ew")
            widgets["measures"]["look"][i].grid(row=4, column=2, pady=2, sticky="ew")
            widgets["measures"]["nutrition"][i].grid(row=5, column=2, pady=2, sticky="ew")            
        self.widgets = widgets
        for measures in self.widgets["measures"].values():
            for measure in measures:
                measure.disable()

        self.next.grid(row = 20, column=1, pady=10)
        self.next["state"] = "disabled"

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        # self.rowconfigure(8, weight=1)
        # self.rowconfigure(9, weight=1)
        # self.rowconfigure(10, weight=1)
        #self.rowconfigure(11, weight=1)
        self.rowconfigure(19, weight=1)
        self.rowconfigure(20, weight=1)
        self.rowconfigure(21, weight=1)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def checkNutrition(self, value, what):
        for entry in ["self.entry_energy", "self.entry_protein", "self.entry_fat", "self.entry_sugar"]:
            if not what in entry:                
                val = eval(entry).get()
            else:
                val = value
            info = val.strip().replace(",", ".")      
            try:
                float(info)
                notfloat = False 
            except ValueError:
                notfloat = True                   
            if notfloat or not info:
                self.next["state"] = "disabled"
                for measures in self.widgets["measures"].values():
                    for measure in measures:
                        measure.disable()
                break
        else:                        
            all_rated = True            
            for measures in self.widgets["measures"].values():                
                for measure in measures:
                    if not measure.answer.get():
                        all_rated = False
                    measure.enable()
            if all_rated:
                self.next["state"] = "normal"
        return True
    
    def rated(self):
        self.checkNutrition("", "XYZ")

    def nextFun(self):
        self.taskFrame.nextFun()

    def write(self):
        self.file.write("\t" + self.entry_energy.get().strip().replace(",", ".") + "\t" + self.entry_protein.get().strip().replace(",", ".") + "\t" + self.entry_fat.get().strip().replace(",", ".") + "\t" + self.entry_sugar.get().strip().replace(",", "."))
        for measures in self.widgets["measures"].values():
            for measure in measures:
                self.file.write("\t" + str(measure.answer.get())) # saves first taste for all three foods, then look, then nutrition
        self.file.write("\n")



class Menus(InstructionsFrame):
    def __init__(self, root, taskFrame):
        super().__init__(root, text = menus_text.format(taskFrame.currentDiet), height = 5, width = 100, proceed=False)

        self.taskFrame = taskFrame

        # Create a frame for the image and scrollbar
        img_frame = Frame(self)
        img_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=10)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=0)

        # Create canvas and scrollbar
        canvas = Canvas(img_frame, bg="white", highlightthickness=0)
        v_scroll = ttk.Scrollbar(img_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scroll.set)

        v_scroll.pack(side="right", fill="y")

        # Enable mouse wheel scrolling when cursor is over the canvas
        def _on_mousewheel(event):
            if event.num == 5 or event.delta == -120:
                canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta == 120:
                canvas.yview_scroll(-1, "units")
            elif event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.focus_set())
        canvas.bind("<Leave>", lambda e: canvas.master.focus_set())
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)

        # Load image
        img_path = os.path.join(os.path.dirname(__file__), 'Menus', root.status["menu_order"][root.status["trial"] - 1])

        try:
            pil_img = Image.open(img_path)
            max_width = 1200
            img_w, img_h = pil_img.size
            scale = min(max_width / img_w, 1.0)
            if scale < 1.0:
                new_size = (int(img_w * scale), int(img_h * scale))
                pil_img = pil_img.resize(new_size, Image.LANCZOS)
            photo_img = ImageTk.PhotoImage(pil_img)
            img_id = canvas.create_image(0, 0, anchor="nw", image=photo_img)
            canvas.image = photo_img  # Keep reference
            canvas.config(scrollregion=canvas.bbox(img_id))
        except Exception as e:
            canvas.create_text(10, 10, anchor="nw", text=f"Error loading image: {e}", fill="red")



class Ratings1(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = proceedText, proceed = True, savedata = True, height = 2, width = 80)

        self.difficulty = Measure(self, difficultyQ1, [i for i in range(1,8)], difficultyL, difficultyR, labelPosition="next", shortText=f"difficultyFirst", questionPosition="above", center=True, function = self.rated)

        self.satisfaction = Measure(self, satisfactionQ1, [i for i in range(1,8)], satisfactionL, satisfactionR, labelPosition="next", shortText=f"satisfactionFirst", questionPosition="above", center=True, function = self.rated)

        self.difficulty.grid(column = 1, row = 2)
        self.satisfaction.grid(column = 1, row = 3)

        self.next.grid(column = 1, row = 5)

        self.next["state"] = "disabled"

        for i in range(1, 5):
            self.rowconfigure(i, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(6, weight=3)

    def rated(self):
        if self.difficulty.answer.get() and self.satisfaction.answer.get():
            self.next["state"] = "normal"

    def write(self):
        self.file.write("Ratings1\n")
        self.file.write(self.id + "\t" + str(self.difficulty.answer.get()) + "\t" + str(self.satisfaction.answer.get()) + "\n\n")


class Choice(InstructionsFrame):
    def __init__(self, root):
        self.elapsedTime_s = perf_counter() - root.status["startTime"]
        self.elapsedTime = floor(self.elapsedTime_s / 60)
        baseText = continuation if self.elapsedTime < 30 else endtime
        reminderText = "" if self.elapsedTime > 30 else eval("reminder_" + root.status["condition"])
        if root.status["trial"] == 1:
            text = baseText.format("jednoho jídelníčku", str(self.elapsedTime), reminderText)
        else:
            text = baseText.format("{} jídelníčků".format(root.status["trial"]), str(self.elapsedTime), reminderText)

        super().__init__(root, text = text, proceed = False, savedata = True, height = 15, width = 80)

        ttk.Style().configure("TButton", font = "helvetica 15")

        self.buttonFrame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.buttonFrame.grid(row=2, column=1)

        self.continueButton = ttk.Button(self.buttonFrame, text="Pokračovat", command=self.proceed)
        if self.elapsedTime < 30:
            self.continueButton.grid(column=0, row=2, sticky="w", padx=60)

            self.endButton = ttk.Button(self.buttonFrame, text="Ukončit", command=self.end)
            self.endButton.grid(column=2, row=2, sticky="e", padx=60)
        else:
            self.continueButton.grid(column=1, row=2, padx=60, command = self.end)            

    def proceed(self):
        self.response = "continue"
        if self.root.status["trial"] != 1:
            self.root.count -= 2
        self.nextFun()

    def end(self):
        self.response = "end"
        if self.root.status["trial"] == 1:
            self.root.count += 2
        if self.root.status["condition"] == "monetary":
            self.root.status["reward"] += self.elapsedTime * MINUTEBONUS
            self.root.status["results"] += [monetary_end.format(self.elapsedTime * MINUTEBONUS)]
        self.nextFun()

    def write(self):
        self.file.write("Choice\n")
        self.file.write(self.id + "\t" + str(self.root.status["trial"]) + "\t" + self.response + "\t" + str(self.elapsedTime_s) + "\n\n")


class Ratings2(Questionnaire):
    def __init__(self, root):
        super().__init__(root, words = "ratings.txt", blocksize = 8, fontsize = 15, labelwidth=10, filetext = "Ratings2", labels = labels, wraplength = 370, fixedlines=2)

        self.difficulty = Measure(self, difficultyQ2, [i for i in range(1,8)], difficultyL, difficultyR, labelPosition="next", shortText=f"difficultySecond", questionPosition="above", center=True, function = self.clicked)

        self.satisfaction = Measure(self, satisfactionQ2, [i for i in range(1,8)], satisfactionL, satisfactionR, labelPosition="next", shortText=f"satisfactionSecond", questionPosition="above", center=True, function = self.clicked)

        self.guilt = Measure(self, guiltQ2, [i for i in range(1,8)], guiltL, guiltR, labelPosition="next", shortText=f"guiltSecond", questionPosition="above", center=True, function = self.clicked)

        self.instructions = ttk.Label(self, text = ratingsText, font = "helvetica 15 bold", background = "white")
        self.instructions2 = ttk.Label(self, text = ratingsText2, font = "helvetica 15 bold", background = "white")
        self.instructions.grid(column = 0, columnspan=3, row = 1)
        self.instructions2.grid(column = 0, columnspan=3, row = 6)

        self.difficulty.grid(column = 1, row = 2)
        self.satisfaction.grid(column = 1, row = 3)
        self.guilt.grid(column = 1, row = 4)

        self.frame.grid(column = 1, row = 7, sticky = NSEW, pady = 10)

        self.next.grid(column = 1, row = 8)

        self.next["state"] = "disabled"

        for i in range(0, 9):
            self.rowconfigure(i, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(5, weight=3)
        self.rowconfigure(9, weight=2)

    def clicked(self):
        super().clicked()
        if not self.checkRatings():
            self.next["state"] = "disabled" 

    def checkRatings(self):
        return self.difficulty.answer.get() and self.satisfaction.answer.get() and self.guilt.answer.get()
    
    def write(self):        
        self.file.write(self.id + "\t" + str(self.difficulty.answer.get()) + "\t" + str(self.satisfaction.answer.get()) + "\t" + str(self.guilt.answer.get()))
        for word in self.words:
            self.file.write("\t" + self.variables[word].get())
        self.file.write("\n")




class BDM(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = BDMtext, height = 25, font = 15, width = 105)

        self.name = "BDM"

        # offer frame
        self.offerVar = StringVar()
        self.vcmd = (self.register(self.onValidate), '%P')
        self.offerFrame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.filler1 = Canvas(self.offerFrame, background = "white", width = 1, height = 255,
                                highlightbackground = "white", highlightcolor = "white")
        self.filler1.grid(column = 1, row = 0, rowspan = 10, sticky = NS)
        self.decisionTextLab = ttk.Label(self.offerFrame, text = decisionText, font = "helvetica 15 bold", background = "white")
        self.decisionTextLab.grid(row = 1, column = 0, columnspan = 3, pady = 10)        
        self.offerInnerFrame = Canvas(self.offerFrame, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.offerInnerFrame.grid(row = 2, column = 0, columnspan = 3, sticky = EW)
        # self.offerTextLab = ttk.Label(self.offerInnerFrame, text = offerText, font = "helvetica 15", background = "white")
        # self.offerTextLab.grid(row = 2, column = 1, padx = 6, sticky = E)
        self.entry = ttk.Entry(self.offerInnerFrame, textvariable = self.offerVar, width = 10, justify = "right",
                               font = "helvetica 15", validate = "key", validatecommand = self.vcmd)
        self.entry.grid(row = 2, column = 2, sticky = E, padx = 5)
        self.currencyLabel = ttk.Label(self.offerInnerFrame, text = "Kč", font = "helvetica 15", background = "white")
        self.currencyLabel.grid(row = 2, column = 3, sticky = W)
        self.offerInnerFrame.columnconfigure(0, weight = 1)
        self.offerInnerFrame.columnconfigure(4, weight = 1)
        
        self.problem = ttk.Label(self.offerFrame, text = "", font = "helvetica 15", background = "white", foreground = "red")
        self.problem.grid(row = 4, column = 0, columnspan = 3, pady = 10)

        # control question frame
        self.controlTexts = [[BDMcontrol1, BDManswers1, BDMfeedback1], [BDMcontrol2, BDManswers2, BDMfeedback2]]

        self.controlFrame = Canvas(self, background = "white", highlightbackground = "white",
                                 highlightcolor = "white")
        self.filler2 = Canvas(self.controlFrame, background = "white", width = 1, height = 255,
                                highlightbackground = "white", highlightcolor = "white")
        self.filler2.grid(column = 1, row = 0, rowspan = 10, sticky = NS)
                     
        self.next.grid(row = 5, column = 1, sticky = N)
   
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        self.rowconfigure(6, weight = 2)        

        self.controlNum = 0
        self.file.write("BDM Control Questions\n")
        self.createQuestion()


    def createQuestion(self):
        self.next["state"] = "disabled"     
        if self.controlNum < len(self.controlTexts):            
            self.createControlQuestion()            
            self.controlFrame.grid(row = 2, column = 1)
        else:
            self.file.write("\n")
            self.controlFrame.grid_forget()
            self.offerFrame.grid(row = 2, column = 1)

    def createControlQuestion(self):
        if self.controlNum:
            self.controlQuestion.grid_forget()
        texts = self.controlTexts[self.controlNum]
        self.controlQuestion = MultipleChoice(self.controlFrame, text = texts[0], answers = texts[1], feedback = texts[2])
        self.controlQuestion.grid(row = 0, column = 0)
        self.controlNum += 1
        self.controlstate = "answer"

    def onValidate(self, P):
        try:
            if "," in P or "." in P:
                raise ValueError()            
            if "-" in P:
                raise Exception("Nabídka musí být vyšší než 0 Kč.")
            offer = int(P)
            if offer < 0:
                raise Exception("Nabídka musí být vyšší než 0 Kč.")
            elif offer > MAX_BDM_PRIZE:
                raise Exception("Nabídka nesmí být vyšší než {} Kč.".format(MAX_BDM_PRIZE))
            else:
                self.next["state"] = "!disabled"
                self.problem["text"] = ""
        except ValueError:
            self.next["state"] = "disabled"
            self.problem["text"] = "Do textového pole je potřeba uvést celé číslo."
        except Exception as e:
            self.next["state"] = "disabled"
            self.problem["text"] = e
        return True

    def write(self):        
        fee = random.randint(0, MAX_BDM_PRIZE)
        offer = int(self.offerVar.get())
        if offer < fee:
            self.root.status["BDMwin"] = True
            self.root.texts["bdmResults"] = BDMresult.format(offer, fee, BDMwon.format(fee))
            self.root.status["reward"] += fee
            self.root.status["results"] += [bmdRewardText.format(fee)]
        else:
            self.root.status["BDMwin"] = False
            self.root.texts["bdmResults"] = BDMresult.format(offer, fee, BDMlost)

        self.file.write("BDM\n")
        self.file.write(self.id + "\t" + self.offerVar.get() + "\t" + str(fee) + "\n\n")

    def nextFun(self):        
        if (self.controlNum == len(self.controlTexts) and self.offerVar.get()):
            self.write()
            if self.root.status["BDMwin"]:
                self.root.status["startTime"] = perf_counter()
            super().nextFun()   
        else:
            if self.controlstate == "answer":
                self.controlQuestion.showFeedback()
                self.controlstate = "feedback"
            else:                
                self.file.write(self.id + "\t" + str(self.controlNum) + "\t" + self.controlQuestion.getAnswer() + "\n")
                self.createQuestion()


class TimeTask(InstructionsFrame):
    def __init__(self, root):
        elapsedTime = floor((perf_counter() - root.status["startTime"]) / 60)
        limit = 10 if not TESTING else 1
        if elapsedTime < limit:
            baseText = continuation2
            root.count -= 2
        else:
            baseText = endtime2
        if root.status["trial"] == 1:
            text = baseText.format("jednoho jídelníčku", str(elapsedTime))
        else:
            text = baseText.format("{} jídelníčků".format(root.status["trial"]), str(elapsedTime))

        super().__init__(root, text = text, proceed = True, height = 10, width = 80)

  
class BDMResult(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = "{}", update = ["bdmResults"], height = 15, width = 80, proceed = True)

        if not self.root.status["BDMwin"]:
            self.root.count += 2


controlTexts = [[Control1, Answers1, Feedback1], [Control2, Answers2, Feedback2]]
MoralizationInstructions = (InstructionsAndUnderstanding, {"text": instructions, "update": ["condition"], "height": 22, "width": 100, "name": "Moralization Control Questions", "randomize": False, "controlTexts": controlTexts, "fillerheight": 260, "finalButton": "Pokračovat k úkolu"})




if __name__ == "__main__":
    from login import Login
    import os
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Task, BDM, BDMResult, Task, TimeTask, Login, Task, Ratings1, Choice, Task, Choice, Ratings2, MoralizationInstructions])