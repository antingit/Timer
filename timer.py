import datetime
import time
import os
import sys
import serial
from ConfigParser import SafeConfigParser

starttime = ""
stoptime = ""

def start(daynow):
  if daynow == 0:
    starttime = config.get("Monday", "start")
  elif daynow == 1:
    starttime = config.get("Tuesday", "start")
  elif daynow == 2:
    starttime = config.get("Wednesday", "start")
  elif daynow == 3:
    starttime = config.get("Thursday", "start")
  elif daynow == 4:
    starttime = config.get("Friday", "start")
  elif daynow == 5:
    starttime = config.get("Saturday", "start")
  elif daynow == 6:
    starttime = config.get("Sunday", "start")
  else:
    starttime = "off"
  return starttime

def stop(daynow):
  if daynow == 0:
    stoptime = config.get("Monday", "stop")
  elif daynow == 1:
    stoptime = config.get("Tuesday", "stop")
  elif daynow == 2:
    stoptime = config.get("Wednesday", "stop")
  elif daynow == 3:
    stoptime = config.get("Thursday", "stop")
  elif daynow == 4:
    stoptime = config.get("Friday", "stop")
  elif daynow == 5:
    stoptime = config.get("Saturday", "stop")
  elif daynow == 6:
    stoptime = config.get("Sunday", "stop")
  else:
    stoptime = "off"
  return stoptime

def cmdsend(data):
  ser = serial.Serial(
    port = prt,
    baudrate = brate,
    parity = par,
    stopbits = stpb,
    bytesize = bs
  )
  ser.write(data)
  ser.close()

try:
  file = open("timer.cfg" , "r")
  file.close()

except:
  print "timer.cfg not found program will exit"
  sys.exit(1)

while True:

  timenow = datetime.datetime.now().strftime('%H:%M')
  daynow = datetime.datetime.today().weekday()
  weekday = " Day of week " + str(daynow)
  ymd = datetime.datetime.now().strftime("%Y-%m-%d")

  config = SafeConfigParser()
  config.read("timer.cfg")

  holyday = config.get("HOLYDAY", "holydays")
  prt = config.get("PORT_CONFIG", "port")
  brate = config.get("PORT_CONFIG" , "baudrate")
  par = config.get("PORT_CONFIG" , "parity")
  stpb = config.get("PORT_CONFIG" , "stopbits")
  bs = config.get("PORT_CONFIG" , "bytesize")
  command_on = config.get("DATA_COMMAND" , "command_on")
  command_off = config.get("DATA_COMMAND" , "command_off")
  command_holyday = config.get("DATA_COMMAND" , "command_holyday")
  p_time = config.get("DATA_COMMAND", "p_time")
  brate = int(brate)
  stpb = int(stpb)
  bs = int(bs)
  p_time = int(p_time)
  command_on = command_on.decode("hex")
  command_off = command_off.decode("hex")
  command_holyday = command_holyday.decode("hex") 

  starttime = start(daynow)
  stoptime = stop(daynow)

  print timenow + weekday + " " + ymd
  print ""
  print "starttime: " + starttime
  print "stoptime : " + stoptime
  print "p_time: " + str(p_time)
  print "holydays: " + holyday
  if ymd in holyday :

    print "command send <holyday>"
    cmdsend(command_holyday)

    starttime = "off"
    stoptime = "off"

  else: 
    print "not found holyday record for this day"
  
  if starttime == "off" or stoptime == "off" :
    print "Timer is off"

  elif timenow >= stoptime :
    print "command send <off>"
    cmdsend(command_off)

  elif timenow >= starttime :
    print "command send <on>"
    cmdsend(command_on)

  else :
    print "command send <off>"
    cmdsend(command_off)

  time.sleep(p_time)
  os.system("clear")

#END

