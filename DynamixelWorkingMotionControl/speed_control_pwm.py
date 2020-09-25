import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode (IO.BOARD)
IO.setup(8,IO.OUT)
p = IO.PWM(8 ,50 )
p.start(0)

while 1:  
    for x in range (50,75):              
        p.ChangeDutyCycle(x)          
        time.sleep(0.1)               
      
    for x in range (75,50,-1):        
        p.ChangeDutyCycle(x)
        time.sleep(0.1)    
