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

storiesIntro = """In this part of the study, you will read three short, real-life stories, each presented on a separate page. You decide when to move on to the next story. 

Please read each story carefully, as at the end you will be asked to indicate what all three stories have in common."""

influenceIntro = """In this part of the study, please think of an older person who has positively influenced your life or served as a role model. In the text box below, briefly describe who they were and what they were like. Focus on the characteristics you particularly liked or valued about them. Try to keep your response concise - up to 5 sentences."""

imageryIntro = """In this part of the study, please imagine yourself at the age of 70. In the textbox below, briefly describe what an ideal day in your life at that age might look like. Think about how you would spend your time, who you would be with, and how you would feel. Feel free to be creative in your description. Try to keep your response concise - up to 5 sentences."""

controlIntro = """In this part of the study, you will read three short articles, each presented on a separate page. You decide when to move on to the next article. Please read each article carefully, as you will be asked to provide a short summary (up to 2 sentences) of the main points presented in each of them."""


# stories = """In the following task, you will read three short stories, with one story displayed per page. You decide when to move on to the next story. 

# Please read each story carefully, as at the end you will be asked to indicate what all three stories have in common."""

influence = """Please, think of an older person who has been a positive influence in your life or served as a role model. In the text box below, briefly describe who they were and what they were like. Focus on the characteristics you particularly liked or valued about them. Try to keep your response brief (up to 5 sentences)."""

imagery = """Please imagine yourself at the age of 70. In the textbox below, describe what an ideal day in your life at that age might look like. Think about how you would spend your time, who you might spend it with, and how you would feel. Try to keep your response brief (up to 5 sentences)."""

control = """In the following task, you will read a short newspaper-like story. Please, read it carefully, as you will be asked to provide a 2-3 sentence summary afterwards."""


storiesQuestion = "Co měly všechny tři příběhy společného?"

questionnaireInstructions = "Ohodnoťte tvrzení níže, jak je sami cítíte, od 1 (rozhodně nesouhlasím) do 5 (rozhodně souhlasím):"

exposureText = """<center>Následující otázky se týkají Vašich názorů na starší dospělé.
<b>Tímto jsou myšleny všechny osoby ve věku 65 let a více.</b></center>"""

################################################################################

SHORT_LIMIT = 10 if TESTING else 1


class Stereotypes(InstructionsFrame):
    def __init__(self, root):
        self.condition = random.choice(["stories", "imagery", "influence", "control"])
        #self.condition = random.choice(["control"]) if TESTING else self.condition

        text = eval(self.condition + "Intro")

        super().__init__(root, text, width = 80, height = 10)
        
        self.file.write("Stereotypes\n")
        self.file.write(f"{self.id}\t{self.condition}\n\n")

        self.instructions = True

        if self.condition == "stories" or self.condition == "control":
            self.trial = 0
            storiesTexts = read_all(f"{self.condition}.txt")
            self.storiesList = storiesTexts.split("\n\n\n")
            random.shuffle(self.storiesList)
            self.wait = 2 if TESTING else 20

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
                story = self.storiesList[self.trial]
                self.trial += 1
                story = story.split("|")
                storyText = f"<center><b>{story[0]}</b></center>\n\n{story[1]}"
                self.changeText(storyText)
                self.next.config(state="disabled")
                self.next.unbind("<Button-1>")
                self.update()
                self.after(self.wait * int(10000 / SHORT_LIMIT), lambda: [self.next.config(state="normal"), self.next.bind("<Button-1>", lambda e: self.next.invoke())])
            elif self.condition == "imagery":
                self.destroy()  
                self.root.content = Imagery[0](self.root, **Imagery[1])
                self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))
            elif self.condition == "influence":
                self.destroy()  
                self.root.content = Influence[0](self.root, **Influence[1])
                self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))
            elif self.condition == "control":
                # add a summary afterward
                if self.trial == 3:
                    self.destroy()  
                    self.root.content = Control[0](self.root, **Control[1])
                    self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))
                    return
                story = self.storiesList[self.trial]
                self.trial += 1
                story = story.split("|")
                storyText = f"<center><b>{story[0]}</b></center>\n\n{story[1]}"
                self.changeText(storyText)
                self.next.config(state="disabled")
                self.next.unbind("<Button-1>")
                self.update()
                self.after(self.wait * int(10000 / SHORT_LIMIT), lambda: [self.next.config(state="normal"), self.next.bind("<Button-1>", lambda e: self.next.invoke())])
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
        #self.lab6 = Likert(self, , options = 5, shortText = "Positivity", left = "velmi negativní", right = "velmi pozitivní")
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

        




        
Stories = (TextFrame, {"text": storiesQuestion, "width": 80, "qlines": 2, "alines": 5, "name": "Stories", "timeDisabled_s": int(10/SHORT_LIMIT), "requiredLength": 10})

Imagery = (TextFrame, {"text": imagery, "width": 80, "qlines": 5, "alines": 10, "name": "Imagery", "timeDisabled_s": int(90/SHORT_LIMIT), "requiredLength": 120})

Influence = (TextFrame, {"text": influence, "width": 80, "qlines": 5, "alines": 10, "name": "Influence", "timeDisabled_s": int(90/SHORT_LIMIT), "requiredLength": 120})

Control = (TextFrame, {"text": control, "width": 80, "qlines": 5, "alines": 5, "name": "Control", "timeDisabled_s": int(10/SHORT_LIMIT), "requiredLength": 10})


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


