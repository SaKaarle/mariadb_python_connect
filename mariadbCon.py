import json
from logging import exception
from math import prod
from signal import alarm
#from sqlite3 import InterfaceError
import sys
from typing import final
import mariadb
from pprint3x import pprint
import RPi.GPIO as GPIO
from datetime import datetime
import time
from subprocess import Popen, PIPE
import schedule

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

# program started
print("Program running...")
# constants
MACHINE_STATE_POWER_OFF = 0
MACHINE_STATE_IDLE =1
MACHINE_STATE_RUNNING = 2
MACHINE_STATE_PART_READY = 3
MACHINE_STATE_ALARM = 4

# variables
machine_id ="Byfib8025"
measuring_started = False
start_time = None
end_time = None
duration = None
isFault = False
fault_detect_time = None
machine_state = 0
# Data
production_times = []
alarms = []
idletimes = []

#File
jsonBackupFile = '/home/pi/Desktop/sshVSC/jsonBackupMachine.json'
try:
    jsonBackupFile = '/home/pi/Desktop/sshVSC/jsonBackupMachine.json'
    with open(jsonBackupFile) as jsonData:
        jsonData.seek(0)
        production_times = json.load(jsonData)

        #print(production_times)
except json.JSONDecodeError as e:
    print(e)
    pass

class mainClass():

    
            

    #return production_times,jsonBackupFile

#production_times, jsonBackupFile = jsonBackup()


    def dataSendDb(self,machine_id, start_time, end_time, duration,isFault):
        query = "INSERT INTO laserdata (machine_id, start_time, end_time, duration, isFault) " \
            "VALUES (%s,%s,%s,%s,%s)"
        args = (machine_id, start_time, end_time, duration, isFault)
        try:

            #self.cursor = self.conn.cursor()
            #print(query, args)

            self.cursor = self.conn.cursor()
            self.cursor.execute(query,args)
            self.conn.commit()
            
            time.sleep(0.1)

        except mariadb.Error as e:
            print(f"Error connectiong to MariaDB Platform: {e}")
            time.sleep(0.1)
            
            
            
        finally:
            with open(jsonBackupFile,'w') as jsonData:
                #production_times.append(data)
                jsonData.seek(0)
                json.dump(production_times,jsonData,indent=5)
            print("Cursor Closed. None = Closed:",self.cursor.close(),)
            
    def tryConnection(self):

        try:
            with open('/home/pi/Desktop/sshVSC/userconf24.json','r') as loginData:
                self.loginSettings = json.load(loginData)
                try:
                    print("Testing connection to Local MariaDB...")
                    
                    self.connParams = {
                        "user":self.loginSettings["user"],
                        "password":self.loginSettings["password"],
                        "host":self.loginSettings["host"],
                        "port":self.loginSettings["port"],
                        "database":self.loginSettings["database"]}

                    self.conn = mariadb.connect(**self.connParams)
                    
                    #ALKUPERÄINEN CONNECTING
                    # self.conn = mariadb.connect(
                    # user=self.loginSettings["user"],
                    # password=self.loginSettings["password"],
                    # host=self.loginSettings["host"],
                    # port=self.loginSettings["port"],
                    # database=self.loginSettings["database"])

                    self.cursor = self.conn.cursor()


                    print("Connection mariadb.connect(): ",self.conn,"\nAuto_reconnect :",self.conn.auto_reconnect)
                    print("Server open:",self.conn)
                    print("Server cursor ping: ", self.cursor)
                    
                    
                except mariadb.Error as e:
                    raise ConnectionError(f"Error occurred... '{e}' Couldn't connect to MariaDB server. Check connection.\nPing: ",self.conn.ping)

        except IOError as ose:
            print("Virhe, ei pystytä lukemaan tiedostoa...")
            raise FileNotFoundError(f"{ose}, can't read file: \n")

        self.laserDataRead(machine_id, start_time,end_time,duration, isFault)

    ### BACKUPSQL COMMAND ###
    def backupSQL(self):

        dateTimeNowCall = datetime.now()
        print("SQL Backup Created:", dateTimeNowCall) 
        buDate = dateTimeNowCall.strftime("%Y-%m-%d_%H%M%S")
        #Backup komento. 
        Popen([f"mysqldump -u SaKa -p{self.loginSettings['password']} esimDB > /home/pi/Desktop/SQLBU/testidbbackup{buDate}.sql"], stdout=PIPE,shell=True)
        time.sleep(0.1)

    def servuPing(self):

        self.dateTimeNowString = datetime.now()
        self.dateTimePing =self.dateTimeNowString.strftime("%Y-%m-%d %H:%M:%S")
        #pinggaus = self.conn.reconnect()
        print(f"\nAutomatic ping to server...\nTime: {self.dateTimePing} \n")
        try:
            self.connParams = {
                "user":self.loginSettings["user"],
                "password":self.loginSettings["password"],
                "host":self.loginSettings["host"],
                "port":self.loginSettings["port"],
                "database":self.loginSettings["database"]}

            self.conn = mariadb.connect(**self.connParams)
            self.cursor = self.conn.cursor()
            self.conn.commit()
            print("Cursor Check:",self.cursor,"\nConn Commit:",self.conn.commit())
        except mariadb.Error as er:
            print('Unable to ping: ',er)
        return print(self.conn)
        
        #print(self.conn.ping(True))
    def laserDataRead(self, machine_id, start_time,end_time,duration, isFault):

        global machine_state
        global measuring_started
        
        #Määritetty backup tiedoston ajankohdat
        schedule.every().day.at("14:30").do(self.backupSQL).run
        schedule.every().day.at("14:30").do(self.servuPing).run
        schedule.every(2).hours.do(self.servuPing).run
        schedule.every(30).minutes.do(self.servuPing).run
        #schedule.every(1).minutes.do(self.servuPing).run
        

        try:
            while True:

                laser = GPIO.input(LASER_ON_SIGNAL)
                alarm = GPIO.input(FAULT_SIGNAL)
                power_on = GPIO.input(MACHINE_POWER_ON_SIGNAL)

                # machine state OFF  
                if power_on == False and alarm == False and laser == False and machine_state != MACHINE_STATE_POWER_OFF:
                    machine_state = MACHINE_STATE_POWER_OFF
                    print("Machine state: Power OFF")
                    #Power OFF timer?

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
                    isFault = False
                    data = {
                        "Machine ID":machine_id,
                        "Start":str(start_time) ,
                        "End": str(end_time),
                        "Duration": str(duration),
                        "isFault" : str(isFault)
                        }
                    production_times.append(data)
                    measuring_started = False
                    
                    print("\nMachine data:")
                    pprint(data)
                    time.sleep(0.1)

                    self.dataSendDb(machine_id, start_time, end_time, duration, isFault)                   

                # machine state ALARM
                elif laser == True and measuring_started == True  and alarm == True and machine_state != MACHINE_STATE_ALARM  :
                    print("Machine state: Alarm")
                    machine_state = MACHINE_STATE_ALARM  
                    end_time = datetime.now()
                    duration = end_time- start_time
                    print("Fault detected", end_time)
                    print("Cutting interrupted! timestamp: ", end_time)
                    print("last laser on time:", start_time)
                    print("Duration: ",duration)
                    measuring_started = False
                    isFault = True

                    data = {
                        "Machine ID":machine_id,
                        "Start":str(start_time) ,
                        "End": str(end_time),
                        "Duration": str(duration),
                        "isFault" : str(isFault)
                    }
                    production_times.append(data)
                    print("\nMachine Data:")
                    pprint(data)
                    time.sleep(0.1)

                    self.dataSendDb(machine_id, start_time, end_time, duration, isFault)

                schedule.run_pending()
                time.sleep(0.3)
                


        except KeyboardInterrupt:
            print("------------------")
            print("Production times:")
            #print(type(production_times))
            for DataItem in production_times:
                print(DataItem)
            
            
            print(json.dumps(production_times,indent=5))


    def main(self):
        
        #Reading Login JSON
        #Trying to connect MariaDB using .JSON file
        #self.jsonBackupRead(production_times)
        self.tryConnection()
    
if __name__ == '__main__':
    paa = mainClass()
    paa.main()
    #paa.kaikkiAsiakkaat()
