import RPi.GPIO as GPIO
import time

# inversione
spento=GPIO.HIGH
acceso=GPIO.LOW

#dizionario delle stanze e dei pin
pinStanza={
    "s":(23,5),
    "c":(7,11),
    "cs":(13,15),
    "cf":(19,21),
}

#Imposto i tempi delle tapparelle
tempo = 2
Htempo = 1

#Imposto il pinMode
def initialize():
    for k, pin in pinStanza.iteritems():
        GPIO.setup(pin[0], GPIO.OUT)
        GPIO.output(pin[0], spento)

        GPIO.setup(pin[1], GPIO.OUT)
        GPIO.output(pin[1], spento)

def getStanzaPin(stanza):
    return pinStanza[stanza]

def movimento(stanza,verso):
    GPIO.setmode(GPIO.BOARD)
    initialize()

    # gestisco separatamente il caso "t"
    if stanza=="t":
        # accendo tutti i pin

        if verso=="u":
            for k, pin in pinStanza.iteritems():
                GPIO.output(pin[0],acceso)
            time.sleep(tempo)
            for k, pin in pinStanza.iteritems():
                GPIO.output(pin[0],spento)
        elif verso=="m":
            # salgono tutti
            for k, pin in pinStanza.iteritems():
                GPIO.output(pin[0], acceso)
            time.sleep(tempo)
            for k, pin in pinStanza.iteritems():
                GPIO.output(pin[0], spento)

            # scendonmo tutti
            for k, pin in pinStanza.iteritems():
                GPIO.output(pin[1],acceso)
            time.sleep(Htempo)
            for k, pin in pinStanza.iteritems():
                GPIO.output(pin[1],spento)
        elif verso=="d":
            for k, pin in pinStanza.iteritems():
                GPIO.output(pin[1],acceso)
            time.sleep(tempo)
            for k, pin in pinStanza.iteritems():
                print(pin[1])
                GPIO.output(pin[1],spento)

		GPIO.cleanup()
        return 87

    pUp=getStanzaPin(stanza)[0]
    pDown=getStanzaPin(stanza)[1]

    if (verso == "u"):
        #Alzo completamente
        GPIO.output(pUp,acceso)
        time.sleep(tempo)
        GPIO.output(pUp,spento)

    elif (verso == "m"):
        #Alzo completamente la tapparella
        GPIO.output(pUp,acceso)
        time.sleep(tempo)
        GPIO.output(pUp,spento)
        #Abbasso di meta la tepparella
        GPIO.output(pDown,acceso)
        time.sleep(Htempo)
        GPIO.output(pDown,spento)

    elif (verso == "d"):
        #Abbasso completamente
        GPIO.output(pDown,acceso)
        time.sleep(tempo)
        GPIO.output(pDown,spento)
	GPIO.cleanup()
    return 87
