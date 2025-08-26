#! python3

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

import os
import random

from common import ExperimentFrame, InstructionsFrame, InstructionsAndUnderstanding, Measure
from gui import GUI
from diets import DIETS


instructions = """Na následujících stránkách najdete stručné popisy jídel podávaných v nemocniční jídelně <b>Fakultní nemocnice Motol</b>. Cílem tohoto úkolu je pro Fakultní nemocnici Motol daná jídla ohodnotit.

Vaším úkolem je:
(a) přepsat čtyři údaje o složení (energie, B - bílkoviny, T - tuky, S - sacharidy (cukry)) přesně tak, jak jsou uvedeny, a 
(b) ohodnotit každý pokrm podle toho, jak chutný, vizuálně přitažlivý a nutričně bohatý Vám osobně připadá. 
Po každém ohodnoceném pokrmu se můžete rozhodnout, zda budete pokračovat dalším pokrmem, nebo úkol zcela ukončíte a přesunete se k další části studie. Záleží pouze na Vás, zda budete v tomto úkolu pokračovat, nebo skončíte. Z předčasného ukončení nevyplývá žádná penalizace.
<b>{}</b>
Úkol bude trvat maximálně 20 minut.

Fakultní Nemocnice Motol Vám tímto děkuje, že jí pomáháte zlepšovat její služby.

Po přečtení instrukcí zodpovězte kontrolní otázky níže."""

neutral = ""

monetary = """
Za každý pokrm, který kompletně vyplníte po prvním pokrmu, získáte k základní odměně navíc bonusovou platbu ve výši 0,50 Kč. 
"""

person_moralization = """
Tím, že se rozhodnete vytrvat co nejdéle, ukážete, že jste starostlivý a morální člověk, který udělá něco navíc, aby pomohl ostatním. Každé další ohodnocené jídlo prokazuje Vaše odhodlání dělat to, co je správné a pomáhat potřebné instituci.
"""

task_moralization = """
Vaše pečlivé hodnocení pokrmů pomůže nemocničním dietologům zvážit nutriční a estetické informace, aby mohli sestavit stravovací plány, které jsou z lékařského hlediska vhodné a zlepšují zdraví pacientů. Pokračováním v tomto úkolu pomůžete dobré věci, protože Vaše hodnocení přímo podporuje zdravější a bezpečnější stravování pro osoby v péči.
"""

Control1 = "Co se stane, když se rozhodnete úkol ukončit dříve než za 20 minut?"
Answers1 = ["Budete penalizováni a přijdete o celou odměnu.", "Musíte zaplatit poplatek a opustit laboratoř.", "Můžete úkol bez jakékoli penalizace ukončit a přesunout se na další část studie.", "Musíte počkat, než vyprší časomíra, jinak se studie zneplatní."]
Feedback1 = ["Špatně. Můžete úkol bez jakékoli penalizace ukončit a přesunout se na další část studie.", "Špatně. Můžete úkol bez jakékoli penalizace ukončit a přesunout se na další část studie.", "Ano, správně.", "Špatně. Můžete úkol bez jakékoli penalizace ukončit a přesunout se na další část studie."]

Control2 = "Které kroky musíte u každého pokrmu provést, než se rozhodnete pokračovat nebo skončit?"
Answers2 = ["Vyfotit jídlo a nahrát fotografii do systému.", "Přesně přepsat údaje o energii, bílkovinách, tucích a cukrech a pak subjektivně ohodnotit\nchutnost, vzhled a nutriční bohatost.", "Přepsat celý text kartičky včetně alergenních látek a poznámek kuchaře.", "Přepisovat celý jídelní lístek do aplikace."]
Feedback2 = ["Špatně. Máte přesně přepsat údaje o energii, bílkovinách, tucích a cukrech a pak subjektivně ohodnotit chutnost, vzhled a nutriční bohatost.", "Ano, správně.", "Špatně. Máte přesně přepsat údaje o energii, bílkovinách, tucích a cukrech a pak subjektivně ohodnotit chutnost, vzhled a nutriční bohatost.", "Špatně. Máte přesně přepsat údaje o energii, bílkovinách, tucích a cukrech a pak subjektivně ohodnotit chutnost, vzhled a nutriční bohatost."]



task = "V záložce Jídelníčky v menu nahoře je seznam všech diet a jejich složení. Prosíme, nejdříve <b>najděte v seznamu dietu označenou jako {} a vyplňte údaje o jejím složení</b>. Následně jídlo ohodnoťte."

tasteText = "Jak chutně toto jídlo působí?"
lookText = "Jak bude jídlo nejspíše vizuálně přitažlivě?"
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

continuation = """Dosud jste dokončili hodnocení {} a strávili na úkolu X minut.

<b>Uveďte, zda chcete pokračovat hodnocení dalších jídel, nebo zda chcete úkol ukončit.</b>
V úkolu je možné pokračovat nejdéle do uplynutí 20 minut od jeho začátku.

Pokud zvolíte „Pokračovat“, zobrazí se Vám další dieta k přepsání a ohodnocení. 
Pokud zvolíte „Ukončit“, úkol skončí a přesunete se na další část studie.

Je to zcela na Vás: můžete kdykoliv přestat bez jakékoli penalizace."""



class Task(ExperimentFrame):
    def __init__(self, root):
        if not "menu_order" in root.status:
            menus = [f for f in os.listdir(os.path.join(os.path.dirname(__file__), 'Menus')) if f.endswith('.png')]
            random.shuffle(menus)
            root.status["menu_order"] = menus

        super().__init__(root)        

        if not "trial" in self.root.status or not self.root.status["trial"]:
            self.root.status["trial"] = 1

        style = ttk.Style()
        style.configure('TNotebook', background='white', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Helvetica', 15), background='white', width=25,
                        foreground='black', borderwidth=1, padding=[10, 5], lightcolor='white', focuscolor='white', labelbackground='white')
        style.map('TNotebook.Tab',
              background=[('selected', 'white'), ('!selected', 'white')],
              font=[('selected', ('Helvetica', 15, 'bold')), ('!selected', ('Helvetica', 15))])
        n = ttk.Notebook(self, style='TNotebook')
        self.moralization = Moralization(root)
        self.menus = Menus(root)
        n.add(self.moralization, text='Hodnocení')
        n.add(self.menus, text='Jídelníčky')
        n.pack(expand=True, fill='both')

        self.newTrial()

    def newTrial(self):
        self.currentDiet = random.choice(DIETS)
        self.moralization.changeText(task.format(self.currentDiet))
        self.menus.changeText(menus_text.format(self.currentDiet))
                
        self.root.status["trial"] += 1


class Moralization(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = task, height = 3, width = 100)

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
            if not info.isdigit() or not info:
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




class Menus(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = menus_text, height = 5, width = 100)

        self.next.grid(column = 1, row = 3)

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

        self.difficulty = Measure(self, difficultyQ1, [i for i in range(1,7)], difficultyL, difficultyR, labelPosition="next", shortText=f"difficultyFirst", questionPosition="above", center=True, function = self.rated)

        self.satisfaction = Measure(self, satisfactionQ1, [i for i in range(1,7)], satisfactionL, satisfactionR, labelPosition="next", shortText=f"satisfactionFirst", questionPosition="above", center=True, function = self.rated)

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



class Choice(InstructionsFrame):
    def __init__(self, root):
        if root.status["trial"] == 1:
            text = continuation.format("jedné diety")
        else:
            text = continuation.format("{} diet".format(root.status["trial"]))

        super().__init__(root, text = text, proceed = False, savedata = True, height = 10, width = 80)

        ttk.Style().configure("TButton", font = "helvetica 15")

        self.buttonFrame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.buttonFrame.grid(row=2, column=1)

        self.continueButton = ttk.Button(self.buttonFrame, text="Pokračovat", command=self.proceed)
        self.continueButton.grid(column=0, row=2, sticky="w", padx=60)

        self.endButton = ttk.Button(self.buttonFrame, text="Ukončit", command=self.end)
        self.endButton.grid(column=2, row=2, sticky="e", padx=60)

    def proceed(self):
        self.nextFun()

    def end(self):
        self.root.count += 2
        self.nextFun()


class Ratings2(InstructionsFrame):
    pass

class BDMInstructions(InstructionsFrame):
    pass

class BDM(InstructionsFrame):
    pass

class BDMResult(InstructionsFrame):
    pass




controlTexts = [[Control1, Answers1, Feedback1], [Control2, Answers2, Feedback2]]
MoralizationInstructions = (InstructionsAndUnderstanding, {"text": instructions, "update": ["condition"], "height": 22, "width": 100, "name": "Moralization Control Questions", "randomize": False, "controlTexts": controlTexts, "fillerheight": 260, "finalButton": "Pokračovat k úkolu"})




if __name__ == "__main__":
    from login import Login
    import os
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login, Choice, Task, Ratings1, MoralizationInstructions, Task])