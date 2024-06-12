# from physic import *
from timer import *
from datetime import datetime
from physic import *

PHYSIC = True

class FarmScheduler():
    
    def __init__(self, physicController, debug=False):
        self.sched = []
        self.currSched = {}
        self.currState = "IDLE"
        self.physicController = physicController
        self.debug = debug
        self.stop = False
        
    def run(self):        
        if (not self.currSched):
            result = self.checkSched()
            if (result != -1):
                self.currSched = self.sched[result].copy()
            else: 
                return
        
        if (self.debug):
            print(str(timer_counter[0]) + " second left")
        
        match self.currState:
            case "IDLE":
                if (int(self.currSched['cycle']) > 0):
                    self.stop = False
                    if (self.debug):
                        print("NEW CYLCLE!")
                    setTimer(0, int(self.currSched['mixer1']))
                    self.currState = "MIXER1"
                    self.currSched['cycle'] -= 1
                    #TURN ON MIXER1
                    if PHYSIC:
                        self.physicController.setActuators(MIXER1, True)
                else:
                    if (not self.stop):
                        print("CYCLE IS FINISHED !!!")
                        self.stop = True
                    now = datetime.now()
                    current_time = now.strftime("%H:%M")
                    if (self.currSched['startTime'] != current_time):
                        self.currSched = {}
                
            case "MIXER1":
                if (timer_flag[0]):
                    if (self.debug):
                        print("MIXER1 HAS FINISHED!")
                    self.currState = "MIXER2"
                    setTimer(0, int(self.currSched['mixer2']))
                    #TURN OFF MIXER1 AND TURN ON MIXER2
                    if PHYSIC:
                        self.physicController.setActuators(MIXER1, False)
                        self.physicController.setActuators(MIXER2, True)
                 
            case "MIXER2":
                if (timer_flag[0]):
                    if (self.debug):
                        print("MIXER2 HAS FINISHED!")
                    self.currState = "MIXER3"
                    setTimer(0, int(self.currSched['mixer3']))
                    #TURN OFF MIXER2 AND TURN ON MIXER3
                    if PHYSIC:
                        self.physicController.setActuators(MIXER2, False)
                        self.physicController.setActuators(MIXER3, True)
        
            case "MIXER3":
                if (timer_flag[0]):
                    if (self.debug):
                        print("MIXER3 HAS FINISHED!")
                    self.currState = "PUMPIN"
                    setTimer(0, int(self.currSched['pump_in']))
                    #TURN OFF MIXER3 AND TURN ON PUMPIN
                    if PHYSIC:
                        self.physicController.setActuators(MIXER3, False)
                        self.physicController.setActuators(PUMPIN, True)    

            case "PUMPIN":
                if (timer_flag[0]):
                    if (self.debug):
                        print("PUMPIN HAS FINISHED!")
                    self.currState = "PUMPOUT"
                    setTimer(0, int(self.currSched['pump_out']))
                    #TURN OFF PUMPIN AND TURN ON PUMPOUT
                    if PHYSIC:
                        self.physicController.setActuators(PUMPIN, False)
                        self.physicController.setActuators(PUMPOUT, True)  

            case "PUMPOUT":
                if (timer_flag[0]):
                    if (self.debug):
                        print("PUMPOUT HAS FINISHED!")
                    self.currState = "IDLE"
                    setTimer(0, 0)
                    #TURN OFF PUMPOUT
                    if PHYSIC:
                        self.physicController.setActuators(PUMPOUT, False)
            case _:
                print("THERE IS A UNDETERMINED STATE")
    
    
    def appendSched(self, data):
        self.sched.append(data)
        if (self.debug):
            print(self.sched)
            
    def checkSched(self):
        if (len(self.sched) == 0):
            return -1
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        for i in range(len(self.sched)):
            if (current_time == self.sched[i]['startTime']):
                return i
        return -1