import RPi.GPIO as GPIO
import time
import math as m
import csv

# CSV File name to pull angle values from
fileName = '/home/pi/Documents/Senior Design/Hip Curves/03032021.csv'
#fileName = '/home/pi/Documents/Motor Control/Standing Positions/02242021.csv'

# Set GPIO Numbering
GPIO.setmode(GPIO.BOARD)

# List of lengths for both sets of actuators
actuator1Points = []
actuator2Points = []

# Both lists include the pair of two actuators
actuator1s = []
actuator2s = []

actuators = []

# Actuator initial lengths
actuator1_initialLength = 8
actuator2_initialLength = 16

# Model Scale adjusts change in lengths (our specific prototype was 1/2, normal scale would be 1)
modelScale = 0.5

# Open csv fil and take all angle values from three rows and append them to appropriate theta lists
with open(fileName, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    for line in csv_reader:
        actuator1Points.append(float(line[0]) * (12 * modelScale) - actuator1_initialLength)
        actuator2Points.append(float(line[1]) * (12 * modelScale) - actuator2_initialLength)


print("Actuator1: " + str(actuator1Points))
print("Actuator2 " + str(actuator2Points))


#Creating Servo Class
class Actuator:
    def __init__(self, pin, lengths, pair):
        #Set Servo Pin to OUTPUT, Freq to 50HZ
        self.pin = pin
        self.lengths = lengths
        self.pair = pair
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwmPin = GPIO.PWM(self.pin,50)
        self.length = 0
        self.index = 0
        
        #Initilize PWM Pin
        self.pwmPin.start(4.5)
        
        #Append Servo to Servo Lists
        self.pair.append(self)
        actuators.append(self)
        time.sleep(0.2)
    
    # Convert Angle value to Duty and sets the servo angle
    def setLength(self, length):
        duty = 4.5 + length
        self.pwmPin.ChangeDutyCycle(duty)
        
    # Calculates the angle the servo should be set to using linear interpolation between two adjacent angle values in theta list
    # self.index is the index the servo should be referencing from theta list
    # when self.index is not a whole number, it linear interpolates between list element before and after current index value
    # Ex: index = 2.5 -> indexLow = 2, indexHigh = 3, if thetas[2] = 10 and thetas[3] = 20, self.theta = 15
    def calculateLength(self, speed):
        self.index += speed
        if self.index > len(self.lengths) - 1:
            self.index -= len(self.lengths) - 1
               
        # If index is a whole number, indexHigh still has to be next number, hence the +0.0001 so it rounds up
        indexLow = m.floor(self.index)
        indexHigh = m.ceil(self.index + 0.0001)
 
        if indexHigh > len(self.lengths) - 1:
            indexHigh -= len(self.lengths) - 1
            
        lengthLow = self.lengths[indexLow]
        lengthHigh = self.lengths[indexHigh]
        
        # Linear interpolation
        self.length = lengthLow + (((self.index - indexLow) * (lengthHigh - lengthLow)) / (indexHigh - indexLow))


# Take away jitter 
def deJitter(delay):
    time.sleep(delay)
    
    for actuator in actuators:
        actuator.pwmPin.ChangeDutyCycle(0)
        
    time.sleep(delay*2)

#Calculates anlgle values for each servo and adjusts them using setAngle method
def iterateActuators(speed):
    for actuator in actuator1s:
        actuator.calculateLength(speed)
        actuator.setLength(actuator.length)
    for actuator in actuator2s:
        actuator.calculateLength(speed)
        actuator.setLength(actuator.length)
    deJitter(0.2)

# Should be used after a walking method is used (trot, saunter) in order to set the legs to a proper initial configuration
def initiateServos():
    index = 0
    for actuator in actuators:
        actuator.index = 0
    for actuator in actuators:
        actuator.calculateLength(0)
        actuator.setLength(actuator.length)
    time.sleep(20)
    deJitter(0.1)
 
# Set Up Servo
actuatorBL = Actuator(8, actuator1Points, actuator1s)
actuatorBR = Actuator(10, actuator1Points, actuator1s)

actuatorTL = Actuator(11, actuator2Points, actuator1s)
actuatorTR = Actuator(13, actuator2Points, actuator1s)

speed = 0.2
while True:
    initiateServos()
    while actuatorBL.index < len(actuator1Points) - speed:
        iterateActuators(speed)
        percentComplete = 100 - ((len(actuator1Points) - actuatorBL.index) / len(actuator1Points)) * 100
        print("Percent Complete: " + str(percentComplete) + '%')
        currentTime = time.time()
    print('Reset')

actuatorBL.pwmPin.stop()
actuatorBR.pwmPin.stop()
actuatorTL.pwmPin.stop()
actuatorTR.pwmPin.stop()

print('Done')

GPIO.cleanup()




  


