import json
from logging import exception
from math import prod
from signal import alarm
#from sqlite3 import InterfaceError
import sys
from typing import final
import mariadb
#from pprint3x import pprint
import RPi.GPIO as GPIO
from datetime import datetime
import time
from subprocess import Popen, PIPE
import schedule

# Signals from machine
LASER_ON_SIGNAL = 23
MACHINE_STANDBY = 24
MACHINE_POWER_ON_SIGNAL= 25
# GPIO setup
# input connected to 3,3v
# Pull down resistor mode activated to get solid 0 reading
GPIO.setmode(GPIO.BCM)
GPIO.setup(LASER_ON_SIGNAL,GPIO.IN, pull_up_down =GPIO.PUD_DOWN)
GPIO.setup(MACHINE_STANDBY,GPIO.IN, pull_up_down =GPIO.PUD_DOWN)
GPIO.setup(MACHINE_POWER_ON_SIGNAL,GPIO.IN, pull_up_down =GPIO.PUD_DOWN)

# program started
print("Program running...")
# constants
MACHINE_STATE_POWER_OFF = 0
MACHINE_STATE_IDLE = 1
MACHINE_STATE_IDLE_MEASURE = 2
MACHINE_STATE_STANDBY = 3
MACHINE_STATE_STANDBY_MEASURE = 4
MACHINE_STATE_RUNNING = 5
MACHINE_STATE_PART_READY = 6


# variables
machine_id ="Byfib8025"
connection_succ = False
measuring_started = False
standby_measuring_started = False
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
jsonPath = '/home/pi/Desktop/sshVSC/'
jsonBackupFile = f"{jsonPath}jsonBackupMachine1.json"
print(jsonBackupFile)
try:
    with open(jsonBackupFile,'a+') as jsonData:
        jsonData.seek(0)
        production_times = json.load(jsonData)
except json.JSONDecodeError as e:
    print(e)
    pass

class mainClass():

#================================================================
# Datan lähetys MariaDB -serveriin #
#================================================================
    def dataSendDb(self,machine_id, start_time, end_time, duration,isFault):
        query = "INSERT INTO laserdata (machine_id, start_time, end_time, duration, isFault) " \
            "VALUES (%s,%s,%s,%s,%s)"
        args = (machine_id, start_time, end_time, duration, isFault)
        try:
            
            print(self.conn.reconnect())
            print(self.conn.ping())

            self.cursor = self.conn.cursor()
            self.cursor.execute(query,args)
            self.conn.commit()

            time.sleep(0.1)

        except mariadb.Error as e:
            print(f"Error connectiong to MariaDB Platform: {e}")
            time.sleep(0.1)

        finally:
            
            self.conn.commit()
            self.cursor.close()
            print("Cursor Closed:",self.cursor.closed)
            with open(jsonBackupFile,'w') as jsonData:
                #production_times.append(data)
                jsonData.seek(0)
                json.dump(production_times,jsonData,indent=5)

##==================================================
## Connect To MariaDB using JSON -file
##==================================================
##
## Koodi virheellinen, keksittävä "Jos Virhe, Ota yhteys lokaaliin" jne...
##
## Tämä osio on turha. Yritetty luoda lukua JSON tiedostosta ja sen epäonnistutta, ottaa yhteys localhost:iin
    def ConnectMariaDBJSON(self):
        try:
            with open('/home/pi/Desktop/sshVSC/userconf24.json','r') as loginData:
                self.loginSettings = json.load(loginData)
                try:
                    print("Testing connection to Server MariaDB...")

                    self.connParams = {
                        "user":self.loginSettings["user"],
                        "password":self.loginSettings["password"],
                        "host":"localhost",
                        "port":self.loginSettings["port"],
                        "database":self.loginSettings["database"]}

                    self.conn = mariadb.connect(**self.connParams)
                    self.conn.auto_reconnect = True
                    print(self.conn.auto_reconnect)
                    self.cursor = self.conn.cursor()
                    self.cursor.close()
                    print("Cursor closed...",self.cursor.closed)

                    #ALKUPERÄINEN CONNECTING
                    # self.conn = mariadb.connect(
                    #     user=self.loginSettings["user"],
                    #     password=self.loginSettings["password"],
                    #     host=self.loginSettings["host"],
                    #     port=self.loginSettings["port"],
                    # print(self.conn)



                except Exception as e:
                    print(f"Error occurred... '{e}' Couldn't connect to MariaDB server")#Check connection.\nPing: ",self.conn.ping
                finally:
                    return connection_succ == False


        except IOError as ose:
            print("Virhe, ei pystytä lukemaan tiedostoa...")
            raise FileNotFoundError(f"{ose}, can't read file: \n")

##==================================================
## Connect To MariaDB using JSON -file + localhost
##==================================================

    def ConnectLocalMariaDB(self):
        try:
            with open('/home/pi/Desktop/sshVSC/userconf24.json','r') as loginData:
                self.loginSettings = json.load(loginData)
                try:
                    print("Testing connection to Localhost MariaDB...")
                    self.connParams = {
                        "user":self.loginSettings["user"],
                        "password":self.loginSettings["password"],
                        "host":"192.168.178.2",
                        "port":self.loginSettings["port"],
                        "database":self.loginSettings["database"]}
                    self.conn = mariadb.connect(**self.connParams)

                            #ALKUPERÄINEN CONNECTING
                            # self.conn = mariadb.connect(
                            #     user=self.loginSettings["user"],
                            #     password=self.loginSettings["password"],
                            #     host=self.loginSettings["host"],
                            #     port=self.loginSettings["port"],
                            #     database=self.loginSettings["database"])
                    self.conn = mariadb.connect(**self.connParams)
                    print(self.conn)
                    self.conn.auto_reconnect = True
                    print(self.conn.auto_reconnect)
                    self.cursor = self.conn.cursor()
                    self.cursor.close()
                    print("Cursor closed...",self.cursor.closed)

                except Exception as e:
                    print(f"Error occurred... '{e}' Couldn't connect to MariaDB server")#Check connection.\nPing: ",self.conn.ping
                    
                finally:

                    return connection_succ == True

        except IOError as ose:
            print("Virhe, ei pystytä lukemaan tiedostoa...")
            raise FileNotFoundError(f"{ose}, can't read file: \n")

#================================================================
# Kirjautumistiedoston luku ja kirjautuminen MariaDB serveriin #
#================================================================

    def tryConnection(self):
        #if ConnectionSucc == True:
            #self.ConnectMariaDBJSON()
            #self.laserDataRead(machine_id, start_time,end_time,duration, isFault)
        #el
        if connection_succ == False:
            self.ConnectLocalMariaDB()
            self.laserDataRead(machine_id, start_time,end_time,duration, isFault)
        else:
            print("error:",mariadb.Error)
            sys.exit()
#================================================================
##### BACKUPSQL COMMAND #####
#================================================================
    def backupSQL(self):

        dateTimeNowCall = datetime.now()
        print("SQL Backup Created:", dateTimeNowCall)
        buDate = dateTimeNowCall.strftime("%Y-%m-%d_%H%M%S")
        #Backup komento.
        Popen([f"mysqldump -u SaKa -p{self.loginSettings['password']} esimDB > /home/pi/Desktop/SQLBU/testidbbackup{buDate}.sql"], stdout=PIPE,shell=True)
        time.sleep(0.1)

#================================================================
#Ping -komento
#================================================================
    def servuPing(self):

        self.dateTimeNowString = datetime.now()
        self.dateTimePing =self.dateTimeNowString.strftime("%Y-%m-%d %H:%M:%S")

        print(f"\nAutomatic ping to server...\nTime: {self.dateTimePing} \n")
        try:
            self.conn.cursor()
            self.conn
            self.cursor
            self.conn.commit()

        except mariadb.Error as er:
            print('Unable to ping: ',er)
        finally:
            self.cursor.close()

#================================================================
# Laser logiikka
#================================================================

    def laserDataRead(self, machine_id, start_time, end_time, duration, isFault):

        global machine_state
        global measuring_started
        global standby_measuring_started

        #Määritetty backup tiedoston ajankohdat
        schedule.every().day.at("12:00").do(self.backupSQL).run
        schedule.every().day.at("12:00").do(self.servuPing).run
        schedule.every().sunday.at("12:00").do(self.backupSQL).run
        schedule.every(4).hours.do(self.servuPing).run
        schedule.every(30).minutes.do(self.servuPing).run
        #schedule.every(30).minutes.do(self.backupSQL).run
        #schedule.every(1).minutes.do(self.servuPing).run

        try:
            while True:

                laser = GPIO.input(LASER_ON_SIGNAL)
                standby = GPIO.input(MACHINE_STANDBY)
                power_on = GPIO.input(MACHINE_POWER_ON_SIGNAL)

                # machine state OFF
                if power_on == False and standby == False and laser == False and machine_state != MACHINE_STATE_POWER_OFF:
                    machine_state = MACHINE_STATE_POWER_OFF
                    print("Machine state: Power OFF")
                    #Power OFF timer?

                # machine state IDLE
                elif power_on == True and standby == False and laser == False and measuring_started == False and machine_state != MACHINE_STATE_IDLE:
                    print("\nMachine state: idle")
                    machine_state = MACHINE_STATE_IDLE

                elif power_on == True and standby == False and laser == False and standby_measuring_started == True and machine_state != MACHINE_STATE_IDLE_MEASURE:
                    print("\nMachine state: idle")

                    machine_state = MACHINE_STATE_IDLE_MEASURE
                    print("\nMachine standby duration:")
                    end_time = datetime.now()
                    duration = end_time - start_time
                    print("\nStandby time :",duration)

                    data = {
                        "Machine ID":machine_id,
                        "Start":str(start_time) ,
                        "End": str(end_time),
                        "Duration": str(duration),
                        "isFault" : str(isFault)
                        }

                    production_times.append(data)

                    print("\nMachine data:")
                    for datakey, datavalue in data.items():
                        print(datakey,":",datavalue)

                    self.dataSendDb(machine_id, start_time, end_time, duration, isFault)
                    
                    standby_measuring_started = False

                # machine standby and waiting for commmand
                elif power_on == True and standby == True and laser == False and measuring_started == False and machine_state != MACHINE_STATE_STANDBY:
                    print("\nMachine is standby and waiting...")
                    machine_state = MACHINE_STATE_STANDBY
                    start_time = datetime.now()
                    isFault = True

                    measuring_started = False
                    standby_measuring_started = True

                elif power_on == True and standby == True and laser == True and standby_measuring_started == True and machine_state != MACHINE_STATE_STANDBY_MEASURE:
                    
                    machine_state = MACHINE_STATE_STANDBY_MEASURE
                    print("\nMachine standby duration:")
                    end_time = datetime.now()
                    duration = end_time - start_time
                    print("\nStandby time :",duration)

                    data = {
                        "Machine ID":machine_id,
                        "Start":str(start_time) ,
                        "End": str(end_time),
                        "Duration": str(duration),
                        "isFault" : str(isFault)
                        }

                    production_times.append(data)

                    print("\nMachine data:")
                    for datakey, datavalue in data.items():
                        print(datakey,":",datavalue)

                    self.dataSendDb(machine_id, start_time, end_time, duration, isFault)
                    
                    standby_measuring_started = False
                    
                # machine state laser on, production running
                elif power_on == True and standby == True and laser == True and measuring_started == False and machine_state != MACHINE_STATE_RUNNING:
                    print("\nLaser ON")
                    print("Machine state: Running\n")
                    
                    start_time = datetime.now()

                    machine_state = MACHINE_STATE_RUNNING
                    measuring_started = True
                    
                    time.sleep(0.1)

                # machine state production end
                elif power_on == True and standby == True and laser == False and measuring_started == True and machine_state !=MACHINE_STATE_PART_READY:
                    print("\nLaser OFF")
                    print("Machine state: Part ready\n")
                    measuring_started = False
                    machine_state = MACHINE_STATE_PART_READY
                    end_time = datetime.now()
                    duration = end_time- start_time
                    
                    #print("start time: ", start_time)
                    #print("duration: ", duration)

                    isFault = False
                    data = {
                        "Machine ID":machine_id,
                        "Start":str(start_time) ,
                        "End": str(end_time),
                        "Duration": str(duration),
                        "isFault" : str(isFault)
                        }

                    production_times.append(data)
                    self.dataSendDb(machine_id, start_time, end_time, duration, isFault)

                    #standby_measuring_started = False
                    print("\nMachine data:")
                    for datakey, datavalue in data.items():
                        print(datakey,":",datavalue)
                    start_time = datetime.now()
                    print("Datan keruu aika: ",start_time)
                    time.sleep(0.1)
                    

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
        self.tryConnection()

if __name__ == '__main__':
    paa = mainClass()
    paa.main()
