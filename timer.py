'''
    Software timer
'''
import numpy as np

NUM_TIMERS = 4

timer_counter = np.zeros(NUM_TIMERS, dtype = int)
timer_flag = np.zeros(NUM_TIMERS, dtype = int)
    
def setTimer(ID, duration):
    timer_counter[ID] = duration
    timer_flag[ID] = 0

def timerRun():
    for i in range (len(timer_counter)):
        if (timer_counter[i] > 0):
            timer_counter[i] -= 1
            if (timer_counter[i] <= 0):
                timer_flag[i] = 1
