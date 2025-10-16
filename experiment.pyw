#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from intros import Initial, Intro, Ending
from demo import Demographics
from comments import Comments
from login import Login
from moralization import MoralizationInstructions, Task, Ratings1, Choice, Ratings2, BDM, BDMResult, TimeTask
from quest import QuestInstructions, Hexaco, PMS, Moralizability, Motivation
from questionnaire import WorkMorality, WorkMorality2, WorkMorality2Instructions
from stereotypes import Stereotypes, StereotypesScale, Exposure, RatingsStereotypes


# udelat ukladani dat
frames = [Initial,
          Login, 
          Intro,            
          MoralizationInstructions,
          Task, 
          Ratings1,
          Choice,
          Task,
          Choice,
          Ratings2,
          BDM,
          BDMResult,
          Task,
          TimeTask,
          Stereotypes,
          RatingsStereotypes,
          QuestInstructions,
          Hexaco,          
          PMS,
          StereotypesScale,
          WorkMorality,
          WorkMorality2Instructions, 
          WorkMorality2,
          Motivation,  
          Moralizability,    
          Exposure,
          Demographics,
          Comments,
          Ending
         ]


if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))