#! python3

from tkinter import *
from tkinter import ttk
from time import perf_counter, time

import os
import random

from common import ExperimentFrame, InstructionsFrame, TextFrame, read_all
from quest import Quest
from gui import GUI
from constants import TESTING


################################################################################
# TEXTS

storiesIntro = """In this part of the study, you will read three short stories, with one story displayed per page. You decide when to move on to the next story."""

influenceIntro = """In this part of the study, we will ask you to recall and briefly describe a positive influence or role model you have had in your life. Please try to remember a specific person who has had a meaningful impact on you. Provide a brief description (up to 5 sentences) focusing on the key characteristics or actions that made this person a positive influence in your life. Try to keep your response concise and to the point."""

imageryIntro = """In this part of the study, we will ask you to imagine and briefly describe an ideal day in your life at the age of 70. Please try to visualize a specific day that reflects your aspirations and values for that stage of life. Provide a brief description (up to 5 sentences) focusing on how you would spend your time, who you would be with, and how you would feel. Try to keep your response concise and to the point."""

controlIntro = """In this part of the study, we will ask you to read a short newspaper-like story and then provide a brief summary. Please read the story carefully, as you will be asked to summarize it in 2-3 sentences afterwards. Focus on capturing the main points and key details of the story in your summary. Try to keep your response concise and to the point."""


stories = """In the following task, you will read three short stories, with one story displayed per page. You decide when to move on to the next story. 

Please read each story carefully, as at the end you will be asked to indicate what all three stories have in common."""

influence = """Please, think of an older person who has been a positive influence in your life or served as a role model. In the text box below, briefly describe who they were and what they were like. Focus on the characteristics you particularly liked or valued about them. Try to keep your response brief (up to 5 sentences)."""

imagery = """Please imagine yourself at the age of 70. In the textbox below, describe what an ideal day in your life at that age might look like. Think about how you would spend your time, who you might spend it with, and how you would feel. Try to keep your response brief (up to 5 sentences)."""

control = """In the following task, you will read a short newspaper-like story. Please, read it carefully, as you will be asked to provide a 2-3 sentence summary afterwards."""


storiesQuestion = "What do all three stories have in common?"

questionnaireInstructions = "Ohodnoťte tvrzení níže, jak je sami cítíte, od 1 (rozhodně nesouhlasím) do 5 (rozhodně souhlasím):"

################################################################################



class Stereotypes(InstructionsFrame):
    def __init__(self, root):
        self.condition = random.choice(["stories", "imagery", "influence", "control"])
        #self.condition = random.choice(["imagery", "influence", "stories"]) if TESTING else self.condition

        text = eval(self.condition + "Intro")

        super().__init__(root, text, width = 80, height = 10)
        
        self.file.write("Stereotypes\n")
        self.file.write(f"{self.id}\t{self.condition}\n\n")

        self.instructions = True

        if self.condition == "stories":
            self.trial = 0
            storiesTexts = read_all("stories.txt")
            self.storiesList = storiesTexts.split("\n")
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
                self.next.config(state = "disabled")
                self.update()
                self.after(self.wait * 1000, self.next.config(state = "normal"))
            elif self.condition == "imagery":
                self.destroy()  
                self.root.content = Imagery[0](self.root, **Imagery[1])
                self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))
            elif self.condition == "influence":
                self.destroy()  
                self.root.content = Influence[0](self.root, **Influence[1])
                self.root.content.grid(row = 0, column = 0, sticky = (N, S, E, W))
            else:
                pass
                #self.master.nextFrame(Control)
        else:
            super().nextFun()  

        


Stories = (TextFrame, {"text": storiesQuestion, "width": 80, "qlines": 2, "alines": 5, "name": "Stories", "timeDisabled_s": 10, "requiredLength": 10})

Imagery = (TextFrame, {"text": imagery, "width": 80, "qlines": 5, "alines": 15, "name": "Imagery", "timeDisabled_s": 120, "requiredLength": 40})

Influence = (TextFrame, {"text": influence, "width": 80, "qlines": 5, "alines": 15, "name": "Influence", "timeDisabled_s": 120, "requiredLength": 40})


class StereotypesScale(Quest):
    def __init__(self, root):
        super().__init__(root, 8, "stereotypes.txt", "Stereotypes Scale", instructions = questionnaireInstructions, width = 85,
                         left = "rozhodně nesouhlasím", right = "rozhodně souhlasím",
                         height = 3, options = 5, center = True)



if __name__ == "__main__":
    from login import Login
    import os
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Stereotypes, StereotypesScale, Imagery])


