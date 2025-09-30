#! python3

from tkinter import *
from tkinter import ttk
from time import perf_counter, time

import os
import random

from common import ExperimentFrame, InstructionsFrame, TextFrame, read_all, Measure
from quest import Quest, Likert
from gui import GUI
from constants import TESTING


################################################################################
# TEXTS

storiesIntro = """V další části studie si přečtete tři krátké skutečné příběhy, z nichž každý bude zobrazen na samostatné stránce. Sami rozhodnete, kdy přejdete na další příběh.

Každý příběh si prosím pečlivě přečtěte. Poté budete požádáni, abyste uvedli, co měly všechny tři příběhy společného."""

influenceIntro = """V další části studie budete požádáni o krátký písemný úkol."""

imageryIntro = """V další části studie budete požádáni o krátký písemný úkol."""

controlIntro = """V další části studie si přečtete tři krátké články, z nichž každý bude zobrazen na samostatné stránce. Sami rozhodnete, kdy přejdete na další článek. Každý článek si prosím pečlivě přečtěte, protože budete požádáni o krátké shrnutí jeho obsahu."""


# stories = """In the following task, you will read three short stories, with one story displayed per page. You decide when to move on to the next story. 

# Please read each story carefully, as at the end you will be asked to indicate what all three stories have in common."""

influence = """Prosím, vzpomeňte si na starší osobu, která měla ve vašem životě pozitivní vliv nebo vám byla vzorem. Do textového pole níže stručně popište, kdo to byl a jaký byl. Zaměřte se na vlastnosti, které jste na této osobě obzvlášť oceňovali nebo měli rádi.
(musíte napsat alespoň 120 znaků)"""

imagery = """Představte si sami sebe ve věku 70 let. Do textového pole níže stručně popište, jak by mohl vypadat ideální den ve vašem životě v tomto věku. Zamyslete se nad tím, jak byste trávili čas, s kým byste byli a jak byste se cítili. Nebojte se být kreativní.
(musíte napsat alespoň 120 znaků)"""

control = """V následujícím úkolu si přečtete krátký novinový článek. Prosím, přečtěte si jej pečlivě, protože budete požádáni o krátké shrnutí jeho obsahu."""


storiesQuestion = """Co měly všechny tři příběhy společného?
(musíte napsat alespoň 10 znaků)"""

controlQuestion = """Níže napište krátké shrnutí článku, který jste právě četl(a).
(musíte napsat alespoň 10 znaků)"""

questionnaireInstructions = "Ohodnoťte tvrzení níže, jak je sami cítíte, od 1 (rozhodně nesouhlasím) do 5 (rozhodně souhlasím):"

exposureText = """<center>Následující otázky se týkají Vašich názorů na starší dospělé.
<b>Tímto jsou myšleny všechny osoby ve věku 65 let a více.</b></center>"""

################################################################################

SHORT_LIMIT = 50 if TESTING else 1


class Stereotypes(InstructionsFrame):
    def __init__(self, root):
        if "storiesSeen" in root.status:
            if root.status["storiesSeen"] > 0:
                self.instructions = True
                self.condition = "control"
                self.trial = 0
                self.waitTime = 12                
                super().__init__(root, "", width = 80, height = 10)     
                self.nextFun()                
                return

        self.condition = random.choice(["stories", "imagery", "influence", "control"])
        #self.condition = random.choice(["control"]) if TESTING else self.condition

        text = eval(self.condition + "Intro")

        super().__init__(root, text, width = 80, height = 10)

        self.instructions = True
       
        self.file.write("Stereotypes\n")
        self.file.write(f"{self.id}\t{self.condition}")

        if self.condition == "stories" or self.condition == "control":
            self.trial = 0
            storiesTexts = read_all(f"{self.condition}.txt")
            self.root.status["storiesList"] = storiesTexts.split("\n\n\n")
            random.shuffle(self.root.status["storiesList"])
            for i in range(5):
                self.file.write("\t" + self.root.status["storiesList"][i].split("|")[0])
            self.waitTime = 12
            self.root.status["storiesSeen"] = 0
        else:
            self.file.write("\tNA\tNA\tNA\tNA\tNA")

        self.file.write("\n\n")

    def nextFun(self):
        if self.instructions:
            self.instructions = False
            if self.condition == "stories":
                if self.trial == 4:
                    self.destroy()  
                    self.root.content = Stories[0](self.root, **Stories[1])
                    self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))
                    return
                self.instructions = True
                story = self.root.status["storiesList"][self.trial]
                self.trial += 1
                story = story.split("|")
                storyText = f"<center><b>{story[0]}</b></center>\n\n{story[1]}"
                self.changeText(storyText)
                self.next.config(state="disabled")
                self.next.unbind("<Button-1>")
                self.update()
                self.after(self.waitTime * int(1000 / SHORT_LIMIT), lambda: [self.next.config(state="normal"), self.next.bind("<Button-1>", lambda e: self.next.invoke())])
            elif self.condition == "imagery":
                self.destroy()  
                self.root.content = Imagery[0](self.root, **Imagery[1])
                self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))
            elif self.condition == "influence":
                self.destroy()  
                self.root.content = Influence[0](self.root, **Influence[1])
                self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))
            elif self.condition == "control":
                if self.trial == 1:
                    if self.root.status["storiesSeen"] < 3:
                        self.root.count -= 1  
                    self.destroy()  
                    self.root.content = Control[0](self.root, **Control[1])
                    self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))                 
                    return                      
                self.instructions = True  
                story = self.root.status["storiesList"][self.root.status["storiesSeen"]]
                self.trial += 1
                story = story.split("|")
                storyText = f"<center><b>{story[0]}</b></center>\n\n{story[1]}"
                self.text.config(height = 20)
                self.changeText(storyText)
                self.root.status["storiesSeen"] += 1
                self.next.config(state="disabled")
                self.next.unbind("<Button-1>")
                self.update()
                self.after(self.waitTime * int(1000 / SHORT_LIMIT), lambda: [self.next.config(state="normal"), self.next.bind("<Button-1>", lambda e: self.next.invoke())])
        else:
            super().nextFun()


class Exposure(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = exposureText, width = 80, height = 2, savedata=True)
        self.file.write("Exposure\n")

        # self.ageVar = StringVar()
        # self.lab1 = ttk.Label(self, text = "At what age is a person considered old?", background = "white", font = "helvetica 15")
        # self.lab1.grid(column = 1, row = 2, pady = 2, padx = 2)        
        # self.age = ttk.Entry(self, width = 5, font = "helvetica 15", textvariable=self.ageVar)
        # self.age.grid(column = 2, row = 2, pady = 2, padx = 2)

        self.text.grid(column = 1, row = 1, pady = 10, padx = 10, columnspan=2)

        self.lab2 = Measure(self, "Žijete nebo jste někdy žili s osobou starší 65 let?", values = ["ano, aktuálně", "ano, v minulosti", "ne, nikdy"], shortText = "Live with 65+", left = "", right = "", questionPosition="above", labelPosition="none", function=self.enable)
        self.lab2.grid(column = 1, row = 3, pady = 2, padx = 2, columnspan=2)

        self.lab3 = Measure(self, "Jak byste popsali zdravotní stav této osoby během doby, kdy jste s ní žili?", values = ["většinou zdravý/v kondici", "většinou nemocný/křehký", "nevyléčitelně nemocný"], filler = 700, shortText = "Health status", left = "", right = "", questionPosition="above", labelPosition="none", function=self.enable)
        self.lab3.grid(column = 1, row = 4, pady = 2, padx = 2, columnspan=2)
        self.lab3.grid_remove()
        self.filler = Canvas(self, width=1, height=68, background="white", highlightbackground="white", highlightcolor="white")
        self.filler.grid(column = 0, row = 4, pady = 2)

        self.lab4 = Measure(self, "Jak často v současnosti navštěvujete nebo mluvíte (včetně telefonních/videohovorů)\nse staršími dospělými ve vaší rodině nebo blízkém okruhu (např. prarodiče, jiní příbuzní)?", values = ["každý den", "několikrát týdně", "několikrát měsíčně", "několikrát ročně", "vůbec ne"], shortText = "Visit family", left = "", right = "", questionPosition="above", labelPosition="none", function=self.enable)
        self.lab4.grid(column = 1, row = 5, pady = 2, padx = 2, columnspan=2)

        self.lab5 = Measure(self, "Jak často se zapojujete do konverzací se staršími dospělými,\nse kterými nejste blízce seznámeni (např. v hromadné dopravě, obchodě)?", values = ["každý den", "několikrát týdně", "několikrát měsíčně", "několikrát ročně", "vůbec ne"], shortText = "Engage with strangers", left = "", right = "", questionPosition="above", labelPosition="none", function=self.enable)
        self.lab5.grid(column = 1, row = 6, pady = 2, padx = 2, columnspan=2)

        self.lab6 = Measure(self, "Jak pozitivní nebo negativní jsou vaše interakce se staršími dospělými?", values = [i for i in range(1,8)], shortText = "Positive interactions", left = "velmi negativní", right = "velmi pozitivní", questionPosition="above", labelPosition="next", function=self.enable)        
        self.lab6.grid(column = 1, row = 7, pady = 2, padx = 2, columnspan=2)

        self.next.config(state="disabled")
        self.next.grid(column = 1, row = 8, pady = 10, columnspan=2)

        for i in range(1, 9):
            self.rowconfigure(i, weight = 1)
        self.rowconfigure(10, weight = 2)
        self.columnconfigure(1, weight = 0) 
        self.columnconfigure(2, weight = 0)
        self.columnconfigure(3, weight = 1)

    def write(self):
        # ans = [self.ageVar.get(), self.lab2.answer.get(), self.lab3.answer.get(), self.lab4.answer.get(), self.lab5.answer.get(), self.lab6.answer.get()]        
        ans = [self.lab2.answer.get(), self.lab3.answer.get(), self.lab4.answer.get(), self.lab5.answer.get(), self.lab6.answer.get()]        
        self.file.write(self.id + "\t" + "\t".join(ans) + "\n\n")

    def enable(self):
        self.saved3 = ""        
        if self.lab2.answer.get() in ["ano, aktuálně", "ano, v minulosti"]:
            self.lab3.grid()
            if self.saved3:
                self.lab3.answer.set(self.saved3)
        else:
            self.lab3.grid_remove()
            self.saved3 = self.lab3.answer.get()
        if all([self.lab2.answer.get(), self.lab4.answer.get(), self.lab5.answer.get(), self.lab6.answer.get()]):
            if self.lab2.answer.get() in ["ano, aktuálně", "ano, v minulosti"]:
                if self.lab3.answer.get():
                    self.next["state"] = "!disabled"
                    return
            else:
                self.next["state"] = "!disabled"
                return
        self.next["state"] = "disabled"

        




        
Stories = (TextFrame, {"text": storiesQuestion, "width": 80, "qlines": 2, "alines": 5, "name": "Stereotypes Text", "timeDisabled_s": int(8/SHORT_LIMIT), "requiredLength": 10})

Imagery = (TextFrame, {"text": imagery, "width": 80, "qlines": 5, "alines": 10, "name": "Stereotypes Text", "timeDisabled_s": int(90/SHORT_LIMIT), "requiredLength": 120})

Influence = (TextFrame, {"text": influence, "width": 80, "qlines": 5, "alines": 10, "name": "Stereotypes Text", "timeDisabled_s": int(90/SHORT_LIMIT), "requiredLength": 120})

Control = (TextFrame, {"text": controlQuestion, "width": 80, "qlines": 5, "alines": 5, "name": "Stereotypes Text", "timeDisabled_s": int(8/SHORT_LIMIT), "requiredLength": 10})


class StereotypesScale(Quest):
    def __init__(self, root):
        super().__init__(root, 8, "stereotypes.txt", "Stereotypes Scale", instructions = questionnaireInstructions, width = 85,
                         left = "rozhodně nesouhlasím", right = "rozhodně souhlasím",
                         height = 3, options = 5, center = True)



if __name__ == "__main__":
    from login import Login
    import os
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Stereotypes, StereotypesScale, Exposure])


