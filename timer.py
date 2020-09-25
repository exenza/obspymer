from datetime import datetime, timedelta
import time, sys, os, json, math

#Defining main variables and functions
invoke_time=datetime.now()
timer={}
def setTimer(stopwatch, start, time_start, end_time):
    global timer
    timer = {
        "stopwatch":stopwatch, #Timer is counting up
        "start":start, #Timer is tiking True/False
        "time_start":time_start.strftime('%Y-%m-%dT%H:%M:%SZ'), #Since when we start the countdown
        "end_time":end_time.strftime('%Y-%m-%dT%H:%M:%SZ'), #Till which time we countdown
        "stop_time":invoke_time.strftime('%Y-%m-%dT%H:%M:%SZ') #When the timer has been stopped (paused)
    }
    json.dump(timer, open("timer.json", "w"))
    return timer
        
def timerReset():
    try:
        os.remove("timer.json")
    except (OSError, IOError):
        print("No file to be deleted")
    setTimer(bool(False), bool(False), invoke_time, invoke_time)
    txt("reset")
    print("Timer has been reset")

def getTimer():
    global timer 
    timer=json.load(open("timer.json", "r"))
    timer["time_start"]=datetime.strptime(timer["time_start"], '%Y-%m-%dT%H:%M:%SZ')
    timer["end_time"]=datetime.strptime(timer["end_time"], '%Y-%m-%dT%H:%M:%SZ')
    timer["stop_time"]=datetime.strptime(timer["stop_time"], '%Y-%m-%dT%H:%M:%SZ')

def runTimer():
    getTimer()
    return timer["start"]

def txt(timestring):
    txt=open("timer.txt", "w+")
    if  timestring == "reset":
        timestring=""
    elif timestring > 0:
        seconds=int(timestring)
        hours = seconds // (60*60)
        seconds %= (60*60)
        minutes = seconds // 60
        seconds %= 60
        timestring="%02i:%02i:%02i" % (hours, minutes, seconds)
    else:
        timestring = "00:00:00"
    
    txt.write(timestring)
    txt.flush()
    txt.close()

#Main timer function invoked based on passed parameters, if no parameters are passed, stopwatch will tik.
def obspymer():  
    
    def tik():
        getTimer()
        if timer["start"] == False:
            exit("Timer stopped")
        if timer["stopwatch"]:
            seconds = ((datetime.now()-timer["time_start"]).total_seconds())
        else:
            seconds = ((timer["end_time"]-timer["time_start"]).total_seconds())
        txt(seconds)
        if timer["stopwatch"]:
            setTimer(bool(True), bool(True), timer["time_start"], timer["end_time"])
        else:
            setTimer(bool(False), bool(True), datetime.now(), timer["end_time"])
        if seconds < 0:
            timerReset()
            txt(0)
            exit("Time is up")
    while(runTimer):
        time.sleep(0.4)
        tik()


#Read timer variables from file, if not present or corrupted, timer will be reset
try:
    timer = json.load(open("timer.json", "r"))
    timer["time_start"]=datetime.strptime(timer["time_start"], '%Y-%m-%dT%H:%M:%SZ')
    timer["end_time"]=datetime.strptime(timer["end_time"], '%Y-%m-%dT%H:%M:%SZ')
    timer["stop_time"]=datetime.strptime(timer["stop_time"], '%Y-%m-%dT%H:%M:%SZ')
except:
    timerReset()


#Read argument to set timer
if len(sys.argv) > 1:
    p = sys.argv[1]
    #Check if parameter is integer
    try:
        p = int(p)
        if timer["stopwatch"] and p < 0:
            exit("Timer is in stopwatch mode")
        elif timer["stopwatch"] and p >0:
            timerReset()
            txt(p)
            print("Reset stopwatch before setting timer")
        else:                     
            if timer["start"]:
                end_time=timer["end_time"]+timedelta(0, p)                                
            else:
                end_time=timer["end_time"]+timedelta(0, round((invoke_time-timer["stop_time"]).total_seconds()))+timedelta(0, p)
                print((end_time-timer["time_start"]).total_seconds())
                           
            setTimer(bool(False), timer["start"], timer["time_start"], end_time)
            txtseconds=round((end_time-invoke_time).total_seconds())
            if txtseconds < 0:
                timerReset()
                exit("Bad timing set, resetted.")
            txt(txtseconds)
            exit("Timer amended: "+str(txtseconds))             
        
    except ValueError:
        if p == "reset":
            timerReset()

        else:
            exit("Invalid parameter, use an integer to set a timer in seconds, a positive number will set/increase timer a negative one will be removed from timer. If no parameters are provided a stopwatch will start or existing timer/stopwatch will be toggled on/off")

else:
    #No arguments provided, stop timer/stopwatch if running, if not stopwatch will start/resume or existing time will resume
    if  timer["start"]:
        setTimer(timer["stopwatch"], bool(False), timer["time_start"], timer["end_time"])
        exit("Timer stopped")
    else:
        #Resume stop watch time
        if timer["stopwatch"]:
            seconds=((timer["stop_time"]-timer["time_start"]).total_seconds())
            start_time=invoke_time-timedelta(0, seconds)
            setTimer(bool(True), bool(True), start_time, start_time)
            exit("Resumed stopwatch")
        #Start new stop watch
        elif timer["time_start"] == timer["end_time"]:
            setTimer(bool(True), bool(True), invoke_time, invoke_time)
        #Resume timer time
        else:
            end_time = timer["end_time"]+timedelta(0, ((invoke_time-timer["stop_time"]).total_seconds()))
            setTimer(bool(False), bool(True), timer["time_start"], end_time)

obspymer()
