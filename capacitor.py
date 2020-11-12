import RPi.GPIO as GPIO
import time as t
import numpy as np
import matplotlib.pyplot as plt

D = [10, 9, 11, 5, 6, 13, 19, 26]
L = [24, 25, 8, 7, 12, 16, 20, 21]

for i in range(0, 8, 1):
    GPIO.setmode(GPIO.BCM)
    n = D[i]
    GPIO.setup(n, GPIO.OUT)
    GPIO.output(n, 0)

for k in range (0, 8, 1):
    n = L[k]
    GPIO.setup(n, GPIO.OUT)
    GPIO.output(n, 0)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(4, GPIO.IN)

def decToBin(decNumber):
    b = [0, 0, 0, 0, 0, 0, 0, 0]
    k = 7
    while decNumber > 0:
        b[k] = int(decNumber % 2)
        decNumber = decNumber // 2
        k -= 1 
    return b

def num2pins(pins, value):
    GPIO.output(list(reversed(pins)), decToBin(value))
            
def adc():
    x=0
    y=256
    while (y-x) > 1:
        p = int((x+y) / 2)
        num2pins(D, p)
        t.sleep(0.005)
        if GPIO.input(4) == 0:
            y = p
        else:
            x = p
    return x 

try:
    t_start = t.time()
    measure = []
    listT = []
    GPIO.output(17, 1)
    v = adc()
    while v < 245:
        t_start_m = t.time()
        measure.append(round(v/255*3.2, 4))
        listT.append(t.time() - t_start)
        v = adc()
        t.sleep(0.005)

    GPIO.output(17, 0)
    v = adc()
    while v > 10:
        t_start_m = t.time()
        measure.append(round(v/255*3.2, 4))
        listT.append(t.time() - t_start)
        v = adc()
        t.sleep(0.005)

    plt.title("V(t)")
    plt.xlabel("Time, s")
    plt.ylabel("Voltage, V")
    plt.plot(listT, measure, 'r.')
    plt.show()

    for i in range (0, len(measure), 1):
        measure[i] = int(measure[i]*255/3.2)
    
    path = str('/home/gr006/Desktop/Scripts/Panasik_Ermakov') + '/data.txt'
    open(path, 'w')
    for i in range(0, len(measure), 1):
        open(path, 'a').write(str(measure[i]) + '\n')
    
    dT = round(listT[len(listT)-1]/len(listT), 3)
    path = str('/home/gr006/Desktop/Scripts/Panasik_Ermakov') + '/settings.txt'
    open(path, 'w').write("dT = " + str(dT) + "\n" + "dV = " + str(round(3.2/255, 4)))
        
except KeyboardInterrupt:
    print("You killed the function")
finally:
    for i in range(0, 8, 1):
        n = D[i]
        GPIO.output(n, 0)
        n = L[i]
        GPIO.output(n, 0)
    GPIO.cleanup()
