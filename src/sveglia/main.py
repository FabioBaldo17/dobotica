import time, pytz, os, sys
from datetime import datetime
sys.path.insert(0, os.path.abspath(".."))
import f_gpio

tempoSveglia="08:15"
tempoDormita="23:50"
alzata=0
abbassata=1

while True:

    adesso=datetime.now(pytz.timezone('Europe/Rome'))
    tempo=adesso.strftime("%H:%M")

    if (tempo>=tempoSveglia and alzata==0):
        print("Sto alzando la tapparella...")
        movimento("cf", "u")
        alzata=1
        abbassata=0

    if (tempo>=tempoDormita and abbassata==0):
        print("Sto abbassando la tapparella...")
        movimento("cf", "d")
        alzata=0
        abbassata=1

    time.sleep(60)
