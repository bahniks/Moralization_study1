#! python3

import os
import urllib.request
import urllib.parse

from math import ceil
from time import sleep

from common import InstructionsFrame
from gui import GUI

from constants import PARTICIPATION_FEE, URL, BONUS
from login import Login
from tkinter import *


################################################################################
# TEXTS
login = """Vítejte na výzkumné studii pořádané Fakultou podnikohospodářskou Vysoké školy ekonomické v Praze! Na tomto výzkumu se podílíme spolu s  <b>Fakultní nemocnicí v Motole (FN Motol)</b>. Ve spolupráci s Mgr. Marietou Balikovou, vedoucí nutriční terapeutkou, Vás požádáme, abyste hodnotili jídelní lístky (vizte její poděkování níže). Toto Vaše hodnocení je důležité, protože dá nemocnici informace, jak pacienti mohou různá jídla a diety vnímat.

Za účast na studii obdržíte paušálně {} Kč. Kromě toho můžete vydělat další peníze v průběhu studie. 

Studie bude trvat cca 35-70 minut.

<b>Všechny informace uvedené v této studii jsou pravdivé</b>, nikdy nebudete klamáni či vystavováni zavádějícím informacím. Pakliže Vám cokoliv v průběhu studie nebude jasné a ověříte, že daná informace není uvedena v instrukcích, přihlašte se. Přijde k Vám výzkumný asistent a pomůže Vám.

Děkujeme, že jste vypnuli své mobilní telefony, a že nebudete s nikým komunikovat v průběhu studie. Pokud s někým budete komunikovat, nebo pokud budete nějakým jiným způsobem narušovat průběh studie, budete požádáni, abyste opustili laboratoř, bez nároku na vyplacení peněz. <b>Používání telefonů či psaní poznámek je během studie zakázáno</b>, pokud budete používat telefon či si budete psát poznámky, budete požádáni, abyste opustili laboratoř bez nároku na vyplacení peněz. Prosíme, dodržujte tato pravidla, aby průběh studie byl pro všechny zúčastněné příjemný.

Pokud jste již tak neučinili, přečtěte si informovaný souhlas a podepište ho.""".format(PARTICIPATION_FEE)


intro = f"""Tímto začíná naše studie, jejíž krátké shrnutí zde uvádíme:

1) Hlavním úkolem je hodnocení nemocničních jídel.
    a. Budou Vám prezentovány denní jídelníčky s popisem jídel z nemocniční jídelny FN Motol. 
    b. Vaším úkolem bude přepsat některé údaje a ohodnotit pokrmy. 
    c. Po každém hodnoceném dnu si můžete zvolit, zda chcete pokračovat, nebo úkol ukončit. Za předčasné ukončení nejste nijak penalizováni.
2) Budete odpovídat na otázky o tom, jak se Vám úkol dělal.
3) Budete plnit krátký úkol, kde můžete číst krátké příběhy nebo popisovat různé situace.
4) Na závěr vyplníte dotazník s několika demografickými údaji a dalšími otázkami zaměřenými na to, jak smýšlíte o práci a světě kolem sebe. 
    a. Součástí jsou také tři kontrolní otázky pozornosti – pokud odpovíte na všechny tři správně, získáte dodatečnou odměnu {BONUS} Kč.
5) Vyplacení celkové odměny a rozloučení.

V případě, že máte otázky nebo narazíte na technický problém během úkolů, prosíme, zvedněte ruku a tiše vyčkejte příchodu výzkumného asistenta.

Po přečtení stiskněte tlačítko “Pokračovat”."""


ending = """Děkujeme za Vaši účast ve výzkumu!
{}
Za účast na studii dostáváte {} Kč. 

Celkově jste tedy získal(a) {} Kč. Tuto částku jsme zaokrouhlili na desítky korun směrem nahoru – prosíme, <b>zapište konečnou výši odměny {} Kč do příjmového dokladu, který máte před sebou na stole</b>.

Studie, která vychází z tohoto experimentu, bude po zpracování dat a publikaci výsledků volně dostupná na webových stránkách Centra laboratorního a experimentálního výzkumu FPH VŠE.

Abychom zajistili objektivitu výsledků, žádáme Vás, abyste nesdílel(a) žádné detaily o průběhu studie s dalšími možnými účastníky. I drobné informace by mohly ovlivnit jejich odpovědi a tím znehodnotit celý výzkum.

Až budete mít vše vyplněno, vezměte si své osobní věci, příjmový doklad a záznamový arch, a v tichosti přejděte do vedlejší místnosti za výzkumným asistentem, který Vám předá odměnu.

Tímto je experiment u konce.
Děkujeme Vám ještě jednou za spolupráci a čas!

Centrum laboratorního a experimentálního výzkumu FPH VŠE""" 

# add contact info, update the website name


################################################################################





class Ending(InstructionsFrame):
    def __init__(self, root):
        root.texts["results"] = "\n" + "\n\n".join(root.status["results"]) + "\n"
        root.texts["reward"] = str(root.status["reward"])
        root.texts["rounded_reward"] = ceil(root.status["reward"] / 10) * 10
        root.texts["participation_fee"] = PARTICIPATION_FEE
        updates = ["results", "participation_fee", "reward", "rounded_reward"]
        super().__init__(root, text = ending, keys = ["g", "G"], proceed = False, height = 38, update = updates, width = 100)
        self.file.write("Ending\n")
        self.file.write(self.id + "\t" + str(root.texts["rounded_reward"]) + "\n\n")

    def run(self):
        self.sendInfo()

    def sendInfo(self):
        while True:
            self.update()    
            data = urllib.parse.urlencode({'id': self.root.id, 'round': -99, 'offer': self.root.texts["rounded_reward"]})
            data = data.encode('ascii')
            if URL == "TEST":
                response = "ok"
            else:
                try:
                    with urllib.request.urlopen(URL, data = data) as f:
                        response = f.read().decode("utf-8") 
                except Exception:
                    pass
            if "ok" in response:                     
                break              
            sleep(5)




class Initial(InstructionsFrame):
    def __init__(self, root):
        super().__init__(root, text = login, proceed = False, height = 25, keys = ["g", "G"])
        
        img_path = os.path.join(os.path.dirname(__file__), "letter.png")
        self.image = PhotoImage(file=img_path)
        self.image = self.image.subsample(2, 2)
        self.img_label = Label(self, image=self.image)
        self.img_label.grid(row=2, column=0, columnspan=3)



Intro = (InstructionsFrame, {"text": intro, "proceed": True, "height": 21})


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.getcwd()))
    GUI([Login,
         Initial, 
         Intro,
         Ending])
