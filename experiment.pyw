#! python3

import sys
import os

sys.path.append(os.path.join(os.getcwd(), "Stuff"))


from gui import GUI

from intros import Initial, Intro, Ending
from demo import Demographics
from comments import Comments
from login import Login
#from videointros import VideoIntro1, VideoIntro2, Sound, VideoIntro4, VideoIntro5, Selection, VideoIntro6
#from videos import Videos, JOL, IMI1, Quiz1, Quiz2, IMI2, Quiz3, IMI3
from moralization import MoralizationInstructions, Task, Ratings1, Choice, Ratings2, BDM, BDMResult, TimeTask
from quest import QuestInstructions, Hexaco, PMS
#from questionnaire import NFC, Boredom, Social



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
          QuestInstructions,
          PMS,
          Hexaco,
          Demographics,
          Comments,
          Ending
         ]

#frames = [VideoIntro1,
        #   VideoIntro2,
        #   Sound,
        #   Videos, JOL, IMI1, Quiz1,
        #   VideoIntro4,
        #   Videos, JOL, IMI2, Quiz2,
        #   VideoIntro5,
        #   Selection,
        #   VideoIntro6,
        #   Videos, Videos, Videos, Videos, Videos,
        #   IMI3,
        #   Quiz3
        #NFC,
        #Boredom,
        #Social,]

if __name__ == "__main__":
    GUI(frames, load = os.path.exists("temp.json"))