#! python3
# -*- coding: utf-8 -*- 

import os
import uuid


studies = {
    "Login": ("id", "condition"),
    "Moralization Control Questions": ("id", "trial", "answer"),
    "Task": ("id", "trial", "menu", "diet", "condition", "time", "energy", "protein", "fat", "sugar",
             "taste_breakfast", "taste_lunch", "taste_dinner",
             "look_breakfast", "look_lunch", "look_dinner",
             "nutrition_breakfast", "nutrition_lunch", "nutrition_dinner"),
    "Ratings1": ("id", "task_difficulty", "task_satisfaction"),
    "Choice": ("id", "trial", "choice", "time"),
    "Ratings2": (
        "id",
        "difficulty",
        "satisfaction",
        "guilt",
        "moral_importance",      # Úkol mi připadal morálně důležitý.
        "money_motivation",      # Dobře si vést v tomto úkolu bylo hlavně o vydělání peněz.
        "concentration_required", # Úkol vyžadoval hodně soustředění.
        "task_interesting",      # Hodnocení pokrmů podle vzhledu a nutričních hodnot mi přišlo zajímavé.
        "usefulness_feeling",    # Během úkolu jsem měl(a) pocit, že dělám něco užitečného.
        "intuition_reliance",    # Při hodnocení pokrmů jsem se řídil(a) hlavně intuicí.
        "pressure_feeling",      # Cítil(a) jsem se během úkolu trochu pod tlakem.
        "task_clarity"          # Úkol byl dobře vysvětlený a srozumitelný.
    ),
    "BDM Control Questions": ("id", "trial", "answer"),
    "BDM": ("id", "bid", "price"),
    "Stereotypes": ("id", "condition", "story1", "story2", "story3", "story4", "story5"),
    "Stereotypes Text": ("id", "text"),
    "Ratings Stereotypes": ("id", "difficulty", "positive_feeling"),
    "Hexaco": ("id", "item", "rating", "question"),
    "PMS": ("id", "item", "rating", "question"),
    "Stereotypes Scale": ("id", "item", "rating", "question"),
    "WorkMorality": ("id", "item", "rating"),
    "WorkMorality2": ("id", "item", "rating"),
    "Motivation": ("id", "item", "rating", "question"),
    "Moralizability": ("id", "item", "rating", "question"),
    "Exposure": ("id", "live_with_65", "health_status", "visit_family", "engage_strangers", "positive_interactions"),
    "Demographics": ("id", "sex", "age", "language", "student", "field"),
    "Comments": ("id", "comment"),
    "Ending": ("id", "reward"),
    "Attention checks": ("id", "study", "correct_answers")
}

frames = ["Initial",
          "Login",
          "Intro",
          "MoralizationInstructions",
          "Task",
          "Ratings1",
          "Choice",
          "Task",
          "Choice",
          "Ratings2",
          "BDM",
          "BDMResult",
          "Task",
          "TimeTask",
          "Stereotypes",
          "RatingsStereotypes",
          "QuestInstructions",
          "Hexaco",
          "PMS",
          "StereotypesScale",
          "WorkMorality",
          "WorkMorality2Instructions",
          "WorkMorality2",
          "Motivation",
          "Moralizability",
          "Exposure",
          "Demographics",
          "Comments",
          "Ending",
          "end"
         ]

read = True
compute = True

if read:
    for study in studies:
        with open("{} results.txt".format(study), mode = "w", encoding = "utf-8") as f:
            f.write("\t".join(studies[study]))

    with open("Time results.txt", mode = "w", encoding = "utf-8") as times:
        times.write("\t".join(["id", "order", "frame", "time"]))

    files = os.listdir()
    for file in files:
        if ".py" in file or "results" in file or "file.txt" in file or ".txt" not in file:
            continue

        with open(file, encoding = "utf-8") as datafile:
            #filecount += 1 #
            count = 1
            for line in datafile:

                study = line.strip()
                if line.startswith("time: "):
                    # with open("Time results.txt", mode = "a") as times:
                        #print(frames[count-1])
                        #print(line.split()[1])
                        #times.write("\n" + "\t".join([file, str(count), frames[count-1], line.split()[1]]))
                    last_time = line.split()[1]
                        #times.write("\n" + "\t".join([file, str(count), study, line.split()[1]]))
                        #count += 1
                    continue
                if study in studies:
                    with open("Time results.txt", mode = "a") as times:
                        times.write("\n" + "\t".join([file, str(count), study, last_time]))
                        count += 1
                    with open("{} results.txt".format(study), mode = "a", encoding = "utf-8") as results:
                        for line in datafile:
                            content = line.strip()
                            if not content or content.startswith("time: "):
                                break
                            elif len(content.split("\t")[0]) == 36:
                                try:
                                    uuid.UUID(content.split("\t")[0])
                                    results.write("\n" + content)
                                except ValueError:
                                    results.write(" " + content)
                            else:
                                results.write(" " + content)
                            

if compute:
    #times = {frame: [] for frame in frames}
    times = {study: [] for study in studies.keys()}
    total = 0
    count = 0
    with open("Time results.txt", mode = "r") as t:
        t.readline()
        for line in t:
            _, num, frame, time = line.split("\t")    
            if int(num) > 1:            
                times[frame0].append(float(time) - t0)                            
            t0 = float(time)
            frame0 = frame
            if frame == "Login":
                t_start = float(time)
            elif frame == "Ending":
                t_end = float(time)
                total += t_end - t_start
                count += 1
    
    print("Total")
    print(round(total / (60*count), 2))


