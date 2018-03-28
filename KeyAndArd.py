import thread
import time
import serial
import pygame

state = '_'

def keyboardRead(threadName, delay):
    global state
    pygame.init()
    time.sleep(5)
    screen = pygame.display.set_mode((50, 50))
    while state != 'm':
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                     state = 'a'
                elif event.key == pygame.K_m:
                    state = 'm'
            else:
                state = '_'

    pygame.quit()
    
def arduinoRead( threadName, start):
    global state
    data=[]
    start=time.time()
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    while state != 'm':
        dataSer=ser.readline() 
        data.append(dataSer.strip() + ', ' + str(state) + ', ' +str("%.2f"%(time.time()-start)) +'\n')  

    ser.close()
    saveData(data)

def saveData(data):
    textFile = open('test.txt','w')
    textFile.writelines(data)
    textFile.close()


try:
   thread.start_new_thread( arduinoRead, ("Thread-1", 2, ) )
   thread.start_new_thread( keyboardRead, ("Thread-2", 4, ) )
except:
   print "Error: unable to start thread"

while 1:
    pass


