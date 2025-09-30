from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont
from collections import deque
from time import perf_counter, sleep
from math import ceil

import random
import os

from common import ExperimentFrame, InstructionsFrame, Question, Measure, read_all
from gui import GUI
from constants import TESTING, AUTOFILL




intro = "Označte, do jaké míry souhlasíte s následujícímí tvrzeními, na poskytnuté škále."

mwbfIntro = """Think about the last 30 days (or since returning to work). Indicate how often each happened in a job-related situation. 
If an item truly didn't apply to your role, choose N/A."""

boredomIntro = """Přečtěte si prosíme každé tvrzení a označte, nakolik s ním souhlasíte.
Vaším úkolem je odpovídat co nejupřímněji podle toho, co nejlépe vystihuje Vaše běžné prožívání a chování."""

socialIntro = """Níže naleznete několik otázek týkajících se Vašeho vztahu k sociálním médiím (Facebook, Twitter, Instagram, TikTok apod.) a jejich používání. 
U každé otázky vyberte tu variantu odpovědi, která vás nejlépe vystihuje."""



class Questionnaire(ExperimentFrame):
    def __init__(self, root, words, question = "", labels = None, blocksize = 4, values = 7, text = True,
                 filetext = "", fontsize = 13, labelwidth = None, wraplength = 0, pady = 0, fixedlines = 0):
        super().__init__(root)

        self.fontsize = fontsize

        if filetext:
            self.file.write(filetext + "\n")

        if type(words) == str and os.path.exists(os.path.join(os.path.dirname(__file__), words)):
            self.words = read_all(os.path.join(os.path.dirname(__file__), words)).split("\n")
        else:
            self.words = words

        self.buttons = {}
        self.variables = {}
        self.labels = {}

        self.frame = Canvas(self, background = "white", highlightbackground = "white", highlightcolor = "white")
        self.frame.grid(column = 1, row = 1, sticky = NSEW, pady = 10)

        maxwidth = max(map(len, self.words))

        for count, word in enumerate(self.words, 1):
            self.variables[word] = StringVar()
            if AUTOFILL:
                self.variables[word].set(random.randint(1, values))
            for i in range(1, values+1):
                if word not in self.buttons:
                    self.buttons[word] = {}
                valuetext = str(i) if text else ""
                self.buttons[word][i] = ttk.Radiobutton(self.frame, text = valuetext, value = i,
                                                        command = self.clicked,
                                                        variable = self.variables[word])
                self.buttons[word][i].grid(column = i+1, row = count + (count-1)//blocksize, padx = 15)

            if fixedlines:
                fillerlabel = ttk.Label(self.frame, text = "l" + "\nl"*int(fixedlines - 1), background = "white", foreground = "white", font = "helvetica {}".format(fontsize+1))
                fillerlabel.grid(column = 0, row = count + (count-1)//blocksize, pady = pady)

            self.labels[word] = ttk.Label(self.frame, text = word, background = "white",
                                          font = "helvetica {}".format(fontsize+1), justify = "left",
                                          width = maxwidth/1.2, wraplength = wraplength)
            self.labels[word].grid(column = 1, row = count + (count-1)//blocksize, padx = 15, sticky = W, pady = pady)
            if not count % blocksize:
                self.frame.rowconfigure(count + count//blocksize, weight = 1)

        avg_char_width = tkfont.Font(family="helvetica", size=fontsize+1).measure("s")
        if wraplength:
            fillerSize = min([int(ceil(maxwidth/(1+maxwidth/1000))), wraplength//avg_char_width])
        else:
            fillerSize = int(ceil(maxwidth/(1+maxwidth/1000)))
        fillerLabel = ttk.Label(self.frame, text = "s"*fillerSize, background = "white", font = "helvetica {}".format(fontsize+1), foreground = "white", justify = "left", width = maxwidth/1.2, wraplength = wraplength)
        fillerLabel.grid(column = 1, padx = 15, sticky = W, row = count + 1 + (count-1)//blocksize)

        self.texts = []
        if not labels:
            labels = [""]*values
        elif len(labels) != values:
            labels = [labels[0]] + [""]*(values - 2) + [labels[-1]]
      
        for count, label in enumerate(labels):
            self.texts.append(ttk.Label(self.frame, text = labels[count], background = "white",
                                        font = "helvetica {}".format(fontsize), anchor = "center",
                                        justify = "center", wraplength = labelwidth * tkfont.Font(family="helvetica", size=fontsize, weight="normal").measure("0")))
            if labelwidth:
               self.texts[count]["width"] = labelwidth,
            self.texts[count].grid(column = count+2, row = 0, sticky = W, pady = 4, padx = 3)

        ttk.Style().configure("TRadiobutton", background = "white", font = "helvetica {}".format(fontsize))

        ttk.Style().configure("TButton", font = "helvetica 15")
        self.next = ttk.Button(self, text = "Pokračovat", command = self.nextFun,
                               state = "disabled")
        self.next.grid(column = 1, row = 2)

        self.question = ttk.Label(self, text = question, background = "white", font = "helvetica 15")
        self.question.grid(column = 1, row = 0, sticky = S, pady = 10)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 2)
        self.rowconfigure(3, weight = 1)


    def clicked(self):
        end = True
        for word in self.words:
            if not self.variables[word].get():
                end = False
            else:
                self.labels[word]["foreground"] = "grey"
        if end:
            self.next["state"] = "!disabled"

    def write(self):
        for word in self.words:
            self.file.write(self.id + "\t" + word + "\t" + self.variables[word].get() + "\n")



MWBF = (Questionnaire,
                {"words": "mwbf.txt",
                 "question": mwbfIntro,
                 "labels": ["Never\n(0×)",
                            "Once\n(1×)",
                            "Occasionally\n(2–3×)",
                            "Often\n(4–5×)",
                            "Very often\n(6+×)",
                            "N/A"],
                 "values": 6,
                 "labelwidth": 11,
                 "text": False,
                 "fontsize": 15,
                 "blocksize": 9,
                 "wraplength": 400,
                 "filetext": "MWBF",
                 "fixedlines": 3,
                 "pady": 3})





if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([MWBF])