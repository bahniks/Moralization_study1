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



task = "V záložce Jídelníčky v menu nahoře je seznam všech diet a jejich složení. Prosíme, <b>najděte v seznamu dietu označenou jako {} a vyplňte nejdříve údaje o jejím složení</b>. Následně jídlo ohodnoťte."

tasteText = "Jak chutně toto jídlo může působit?"
lookText = "Jak vizuálně přitažlivě jídlo může působit?"
nutritionText = "Jak nutričně bohaté se Vám toto jídlo zdá?"


menus_text = """V seznamu níže najděte <b>dietu označenou jako {}</b> a v záložce Hodnocení vyplňte údaje o jejím nutričním složení.
Každý řádek odpovídá jídelníčku pro daný den pro danou dietu. Označení diety naleznete v levém horním rohu v prvním sloupci. 
Jídla, která budete hodnotit naleznete ve sloupcích Snídaně, Oběd a Večeře v daném řádku."""



class Task(ExperimentFrame):
    def __init__(self, root):
        #if not "diet_order" in root.status:
            #alldiets = DIETS
            #random.shuffle(alldiets)
            #root.status["diet_order"] = alldiets

        super().__init__(root)        

        style = ttk.Style()
        style.configure('TNotebook', background='white', borderwidth=0)
        style.configure('TNotebook.Tab', font=('Helvetica', 15), background='white', width=25,
                        foreground='black', borderwidth=1, padding=[10, 5], lightcolor='white', focuscolor='white', labelbackground='white')
        style.map('TNotebook.Tab',
              background=[('selected', 'white'), ('!selected', 'white')],
              font=[('selected', ('Helvetica', 15, 'bold')), ('!selected', ('Helvetica', 15))])
        n = ttk.Notebook(self, style='TNotebook')
        self.moralization = Moralization(self)
        self.menus = Menus(self)
        n.add(self.moralization, text='Hodnocení')
        n.add(self.menus, text='Jídelníčky')
        n.pack(expand=True, fill='both')

        if not "trial" in self.root.status:
            self.root.status["trial"] = 1

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
        self.ratingFrame.grid(row=3, column=1, sticky="nsew")
        self.ratingFrame.columnconfigure(0, weight=1)
        self.ratingFrame.columnconfigure(3, weight=1)

        # Label for instruction
        self.label_intro = ttk.Label(self.ratingFrame, text="Nutriční údaje z prvního sloupce", font="helvetica 15 bold", background="white")
        self.label_intro.grid(row=3, column=1, columnspan=2, padx=10, pady=(20, 5))

        # Energie (kJ)
        self.label_energy = ttk.Label(self.ratingFrame, text="Energie (kJ):", font="helvetica 15", background="white")
        self.label_energy.grid(row=4, column=1, sticky="e", padx=10, pady=2)
        self.entry_energy = ttk.Entry(self.ratingFrame, width=20, font="helvetica 15")
        self.entry_energy.grid(row=4, column=2, sticky="w", padx=10, pady=2)

        # Obsah bílkovin (B)
        self.label_protein = ttk.Label(self.ratingFrame, text="Obsah bílkovin (B):", font="helvetica 15", background="white")
        self.label_protein.grid(row=5, column=1, sticky="e", padx=10, pady=2)
        self.entry_protein = ttk.Entry(self.ratingFrame, width=20, font="helvetica 15")
        self.entry_protein.grid(row=5, column=2, sticky="w", padx=10, pady=2)

        # Obsah tuků (T)
        self.label_fat = ttk.Label(self.ratingFrame, text="Obsah tuků (T):", font="helvetica 15", background="white")
        self.label_fat.grid(row=6, column=1, sticky="e", padx=10, pady=2)
        self.entry_fat = ttk.Entry(self.ratingFrame, width=20, font="helvetica 15")
        self.entry_fat.grid(row=6, column=2, sticky="w", padx=10, pady=2)

        # Obsah cukrů (S)
        self.label_sugar = ttk.Label(self.ratingFrame, text="Obsah cukrů (S):", font="helvetica 15", background="white")
        self.label_sugar.grid(row=7, column=1, sticky="e", padx=10, pady=2)
        self.entry_sugar = ttk.Entry(self.ratingFrame, width=20, font="helvetica 15")
        self.entry_sugar.grid(row=7, column=2, sticky="w", padx=10, pady=2)

        # First set of measures in its own canvas
        sep1 = ttk.Separator(self, orient="horizontal")
        sep1.grid(row=7, column=0, columnspan=3, sticky="ew", pady=(20,0))
        breakfast = ttk.Label(self, text="Snídaně", font="helvetica 15 bold", background="white")
        breakfast.grid(row=8, column=0, sticky="ne", pady=(10, 0), padx=20)
        canvas1 = Canvas(self, background="white", highlightbackground="white", highlightcolor="white")
        canvas1.grid(row=8, column=1, sticky="nsew", pady=(10, 0))
        taste1 = Measure(canvas1, tasteText, [i for i in range(1,8)], "Zcela nechutně", "Velmi chutně", labelPosition="next", shortText="taste1", questionPosition="next")
        look1 = Measure(canvas1, lookText, [i for i in range(1,8)], "Zcela nevzhledné", "Velmi přitažlivé", labelPosition="next", shortText="look1", questionPosition="next")
        nutrition1 = Measure(canvas1, nutritionText, [i for i in range(1,8)], "Zcela chudé na živiny", "Velmi bohaté na živiny", labelPosition="next", shortText="nutrition1", questionPosition="next")
        taste1.grid(row=0, column=0, pady=2, sticky="ew")
        look1.grid(row=1, column=0, pady=2, sticky="ew")
        nutrition1.grid(row=2, column=0, pady=2, sticky="ew")

        # Second set of measures in its own canvas
        sep2 = ttk.Separator(self, orient="horizontal")
        sep2.grid(row=9, column=0, columnspan=3, sticky="ew", pady=(20,0))
        lunch = ttk.Label(self, text="Oběd", font="helvetica 15 bold", background="white")
        lunch.grid(row=10, column=0, sticky="ne", pady=(10, 0), padx=20)
        canvas2 = Canvas(self, background="white", highlightbackground="white", highlightcolor="white")
        canvas2.grid(row=10, column=1, sticky="nsew", pady=(10, 0))
        taste2 = Measure(canvas2, tasteText, [i for i in range(1,8)], "Zcela nechutně", "Velmi chutně", labelPosition="next", shortText="taste2", questionPosition="above")
        look2 = Measure(canvas2, lookText, [i for i in range(1,8)], "Zcela nevzhledné", "Velmi přitažlivé", labelPosition="next", shortText="look2", questionPosition="above")
        nutrition2 = Measure(canvas2, nutritionText, [i for i in range(1,8)], "Zcela chudé na živiny", "Velmi bohaté na živiny", labelPosition="next", shortText="nutrition2", questionPosition="above")
        taste2.grid(row=0, column=0, pady=2, sticky="ew")
        look2.grid(row=1, column=0, pady=2, sticky="ew")
        nutrition2.grid(row=2, column=0, pady=2, sticky="ew")

        # Third set of measures in its own canvas
        sep3 = ttk.Separator(self, orient="horizontal")
        sep3.grid(row=11, column=0, columnspan=3, sticky="ew", pady=(20,0))
        dinner = ttk.Label(self, text="Večeře", font="helvetica 15 bold", background="white")
        dinner.grid(row=12, column=0, sticky="ne", pady=(10, 0), padx=20)
        canvas3 = Canvas(self, background="white", highlightbackground="white", highlightcolor="white")
        canvas3.grid(row=12, column=1, sticky="nsew", pady=(10, 0))
        taste3 = Measure(canvas3, tasteText, [i for i in range(1,8)], "Zcela nechutně", "Velmi chutně", labelPosition="next", shortText="taste3", questionPosition="above")
        look3 = Measure(canvas3, lookText, [i for i in range(1,8)], "Zcela nevzhledné", "Velmi přitažlivé", labelPosition="next", shortText="look3", questionPosition="above")
        nutrition3 = Measure(canvas3, nutritionText, [i for i in range(1,8)], "Zcela chudé na živiny", "Velmi bohaté na živiny", labelPosition="next", shortText="nutrition3", questionPosition="above")
        taste3.grid(row=0, column=0, pady=2, sticky="ew")
        look3.grid(row=1, column=0, pady=2, sticky="ew")
        nutrition3.grid(row=2, column=0, pady=2, sticky="ew")

        self.next.grid(row = 20, column=1, pady=10)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        #self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        #self.rowconfigure(11, weight=1)
        self.rowconfigure(20, weight=1)
        self.rowconfigure(21, weight=1)
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

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
        img_path = os.path.join(os.path.dirname(__file__), 'Dosp_vše_190513.png')

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













controlTexts = [[Control1, Answers1, Feedback1], [Control2, Answers2, Feedback2]]
MoralizationInstructions = (InstructionsAndUnderstanding, {"text": instructions, "update": ["condition"], "height": 22, "width": 80, "name": "Moralization Control Questions", "randomize": False, "controlTexts": controlTexts, "fillerheight": 260, "finalButton": "Pokračovat k úkolu"})




if __name__ == "__main__":
    from login import Login
    import os
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login, Task, Moralization, MoralizationInstructions])