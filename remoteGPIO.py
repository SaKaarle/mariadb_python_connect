import RPi.GPIO as GPIO
from datetime import datetime
import time

# Signals from machine
LASER_ON_SIGNAL = 23
FAULT_SIGNAL = 24
MACHINE_POWER_ON_SIGNAL= 25
# GPIO setup
# input connected to 3,3v
# Pull down resistor mode activated to get solid 0 reading
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_ON_SIGNAL,GPIO.IN, pull_up_down =GPIO.PUD_DOWN)
GPIO.setup(FAULT_SIGNAL,GPIO.IN, pull_up_down =GPIO.PUD_DOWN)
GPIO.setup(MACHINE_POWER_ON_SIGNAL,GPIO.IN, pull_up_down =GPIO.PUD_DOWN)
# constants
MACHINE_STATE_POWER_OFF = 0
MACHINE_STATE_IDLE =1
MACHINE_STATE_RUNNING = 2
MACHINE_STATE_PART_READY = 3
MACHINE_STATE_ALARM = 4
# program started
print("Program running..")
# variables
machine_id ="Byfib8025"
measuring_started = False
start_time = None
end_time = None
duration = None
fault_detect_time = None
machine_state = 0
# Data
production_times = []
alarms = []
idletimes = []
try:
    while True:
        laser = GPIO.input(LASER_ON_SIGNAL)
        alarm = GPIO.input(FAULT_SIGNAL)
        power_on = GPIO.input(MACHINE_POWER_ON_SIGNAL)

        # machine state OFF  
        if power_on == False and alarm == False and laser == False and machine_state != MACHINE_STATE_POWER_OFF:
            machine_state = MACHINE_STATE_POWER_OFF
            print("Machine state: Power OFF")

        # machine state IDLE
        elif power_on == True and alarm == False and laser == False and machine_state != MACHINE_STATE_IDLE :
            print("Machine state: idle")
            machine_state = MACHINE_STATE_IDLE
        # machine state laser on, production running  
        elif laser == True and power_on == True and alarm == False and  measuring_started == False and machine_state != MACHINE_STATE_RUNNING:
            print("Laser ON")
            print("Machine state: Running")
            machine_state = MACHINE_STATE_RUNNING
            start_time = datetime.now()
            measuring_started = True
        # machine state production end  
        elif laser == False and measuring_started == True and machine_state !=MACHINE_STATE_PART_READY:
            print("Laser OFF")
            print("Machine state: Part ready")
            machine_state = MACHINE_STATE_PART_READY
            end_time = datetime.now()
            duration = end_time- start_time
            print("start time: ", start_time)
            print("duration: ", duration)
            data = {
                "machine ID":machine_id,
                "Start":str(start_time) ,
                "End": str(end_time),
                "duration": str(duration)
                }
            production_times.append(data)
            measuring_started = False
        # machine state ALARM
        elif laser == True and measuring_started == True  and alarm == True and machine_state != MACHINE_STATE_ALARM  :
            print("Machine state: Alarm")
            machine_state = MACHINE_STATE_ALARM  
            fault_detect_time = datetime.now()
            print("Fault detected",fault_detect_time)
            print("Cutting interrupted! timestamp: ",fault_detect_time)
            print("last laser on time:", start_time)
            measuring_started = False
        time.sleep(0.3)
except KeyboardInterrupt:
    print("------------------")
    print("Production times:")
    print(production_times)