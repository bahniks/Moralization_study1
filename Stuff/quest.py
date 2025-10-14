#! python3
# -*- coding: utf-8 -*- 

from tkinter import *
from tkinter import ttk
from collections import defaultdict
from copy import deepcopy

import os
import random

from common import ExperimentFrame, InstructionsFrame, read_all
from gui import GUI

from constants import BONUS, TESTING


################################################################################
# TEXTS
questintro = f"""V následující části studie budete odpovídat na otázky o sobě, Vašich postojích a názorech. Tato část by měla trvat asi 15-20 minut.

Každou otázku si pečlivě přečtěte. Snažte se však na otázky nemyslet příliš dlouho; první odpověď, která Vám přijde na mysl, je obvykle nejlepší.

Za účelem ověření, zda otázkám věnujete pozornost, jsou umístěny tři kontrolní otázky. Pokud odpovíte na všechny kontrolní otázky správně, můžete získat dalších {BONUS} Kč."""

hexacoinstructions = """Na následujících stránkách najdete řadu prohlášení o Vaší osobě.

Přečtěte si prosím každé prohlášení a rozhodněte se, do jaké míry s ním souhlasíte, nebo nesouhlasíte.
"""

bonusGained = f"Protože jste odpověděl(a) správně na všechny kontrolní otázky, získáváte dalších {BONUS} Kč."
bonusNotGained = f"Protože jste neodpověděl(a) správně na všechny kontrolní otázky, nezískáváte dalších {BONUS} Kč."

attentiontext = "Chcete-li prokázat, že zadání věnujete pozornost, vyberte možnost "


pmsIntro = "Ohodnoťte tvrzení níže, jak je sami cítíte, od 1 (rozhodně nesouhlasím) do 5 (rozhodně souhlasím):"


moralizabilityinstructions = """Uveďte prosím svou odpověď na následující tvrzení na škále od 1 (rozhodně nesouhlasím) do 5 (rozhodně souhlasím). Neexistují žádné správné nebo špatné odpovědi, ale každému tvrzení věnujte plnou pozornost."""


motivationInstructions = """Proč jste motivováni k vykonávání své práce?
Uveďte, do jaké míry souhlasíte nebo nesouhlasíte s každým z následujících tvrzení."""
################################################################################



class Quest(ExperimentFrame):
    def __init__(self, root, perpage, file, name, left, right, options = 5, shuffle = True,
                 instructions = "", height = 3, width = 80, center = False, checks = 0, wraplength = "auto"):
        super().__init__(root)

        self.perpage = perpage
        self.left = left
        self.right = right
        self.options = options
        self.checks = checks != 0
        self.checksNumber = checks
        self.name = name
        self.wraplength = wraplength

        self.file.write("{}\n".format(name))

        if instructions:
            self.instructions = Text(self, height = height, relief = "flat", width = width, font = "helvetica 15", wrap = "word")
            self.instructions.grid(row = 1, column = 0, columnspan = 3)
            self.instructions.insert("1.0", instructions, "text")
            if center:
                self.instructions.tag_config("text", justify = "center") 
            self.instructions["state"] = "disabled"

        self.questions = [i for i in read_all(file, comments = True).split("\n")]
        # with open(os.path.join("Stuff", file), encoding = "utf-8") as f:
        #     for line in f:
        #         self.questions.append(line.strip())

        if shuffle:
            random.shuffle(self.questions)

        if checks:
            spread = len(self.questions)//checks
            positions = [random.randint(self.perpage//2 + spread*i, spread*(i+1) - self.perpage//2) for i in range(checks)]
            for i in range(checks):
                self.questions.insert(positions[i], attentiontext + str(random.randint(1, options)) + ".")

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun, state = "disabled")
        self.next.grid(row = self.perpage*2 + 4, column = 1)

        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 2)
        self.rowconfigure(self.perpage*2 + 4, weight = 1)
        self.rowconfigure(self.perpage*2 + 5, weight = 3)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)

        self.mnumber = 0
        
        self.createQuestions()

    def createQuestions(self):
        self.measures = []
        for i in range(self.perpage):
            m = Likert(self, self.questions[self.mnumber], shortText = str(self.mnumber + 1),
                       left = self.left, right = self.right, options = self.options, wraplength=self.wraplength)
            m.grid(column = 0, columnspan = 3, row = i*2 + 3)
            self.rowconfigure(i*2 + 4, weight = 1)
            self.mnumber += 1
            self.measures.append(m)
            if self.mnumber == len(self.questions):
                break

    def nextFun(self):
        for measure in self.measures:
            measure.write()
            measure.grid_forget()
        if self.mnumber == len(self.questions):
            self.file.write("\n")
            if self.checks:
                self.file.write("Attention checks\n")
                correct_checks = str(self.root.status["attention_checks"])
                self.file.write(self.id + "\t" + self.name + "\t" + correct_checks + "\n\n")
                if correct_checks == str(self.checksNumber):
                    self.root.status["results"] += [bonusGained]
                    self.root.status["reward"] += BONUS                    
                else:
                    self.root.status["results"] += [bonusNotGained]
            self.destroy()
            self.root.nextFrame()
        else:
            self.next["state"] = "disabled"
            self.createQuestions()

    def check(self):
        for m in self.measures:
            if not m.answer.get():
                return
        else:
            self.next["state"] = "!disabled"



class Likert(Canvas):
    def __init__(self, root, text, options = 5, shortText = "", left = "strongly disagree", right = "strongly agree", wraplength = "auto"):
        super().__init__(root)

        if wraplength == "auto":
            wraplength = root.root.screenwidth * 0.9

        self.root = root
        self.text = text
        self.short = shortText
        self.answer = StringVar()
        self["background"] = "white"
        self["highlightbackground"] = "white"
        self["highlightcolor"] = "white"

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica 15")

        self.question = ttk.Label(self, text = text, background = "white", anchor = "center", font = "helvetica 15", wraplength=wraplength)
        self.question.grid(column = 0, row = 0, columnspan = options + 2, sticky = S)

        self.left = ttk.Label(self, text = left, background = "white", font = "helvetica 14")
        self.right = ttk.Label(self, text = right, background = "white", font = "helvetica 14")
        self.left.grid(column = 0, row = 1, sticky = E, padx = 5)
        self.right.grid(column = options + 1, row = 1, sticky = W, padx = 5)           

        for value in range(1, options + 1):
            ttk.Radiobutton(self, text = str(value), value = value, variable = self.answer,
                            command = self.check).grid(row = 1, column = value, padx = 4)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(options + 1, weight = 1)
        self.rowconfigure(0, weight = 1)

        if False: #TESTING:
            self.answer.set(str(random.randint(1, options)))


    def write(self):
        if attentiontext in self.text:
            if not "attention_checks" in self.root.root.status:
                self.root.root.status["attention_checks"] = 0
            if self.answer.get() == self.text[-2]:
                self.root.root.status["attention_checks"] += 1
        else:
            ans = "{}\t{}\t{}\n".format(self.short, self.answer.get(), self.text.replace("\t", " "))
            self.root.file.write(self.root.id + "\t" + ans)


    def check(self):
        self.root.check()



class Hexaco(Quest):
    def __init__(self, root):
        super().__init__(root, 9, "hexaco.txt", "Hexaco", instructions = hexacoinstructions, width = 85,
                         left = "silně nesouhlasím", right = "silně souhlasím", checks = 3,
                         height = 3, options = 5, center = True)


class PMS(Quest):
    def __init__(self, root):
        super().__init__(root, 8, "pms.txt", "PMS", instructions = hexacoinstructions, width = 85,
                         left = "rozhodně nesouhlasím", right = "rozhodně souhlasím",
                         height = 3, options = 5, center = True)


class Moralizability(Quest):
    def __init__(self, root):
        super().__init__(root, 7, "moralizability.txt", "Moralizability", instructions = moralizabilityinstructions, width = 85,
                         left = "rozhodně nesouhlasím", right = "rozhodně souhlasím", height = 5, options = 5, center = True, wraplength = "auto")

class Motivation(Quest):
    def __init__(self, root):
        super().__init__(root, 8, "motivation.txt", "Motivation", instructions = motivationInstructions, width = 85,
                         left = "rozhodně nesouhlasím", right = "rozhodně souhlasím", height = 5, options = 5, center = True, wraplength = "auto")


QuestInstructions = (InstructionsFrame, {"text": questintro, "height": 15})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Motivation, Moralizability, Hexaco, QuestInstructions])
