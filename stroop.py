import time
import sys
import random
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200])

# task 1: create fixation
fixation = visual.TextStim(win, text="+", height=15, color="black")

# task 2: set auto-draw
instruction.setAutoDraw(True)

# task 4: record RT
timer = core.Clock()
RTs = []

while True:
    # task 1: show fixation
    placeholder.draw()
    fixation.draw()
    win.flip()
    core.wait(0.5)

    # task 1: remove fixation stimuli
    placeholder.draw()
    win.flip()
    core.wait(0.5)

    cur_stim = random.choice(stimuli)
    word_stim.setText(cur_stim)
    word_stim.setColor(cur_stim)
    placeholder.draw()
    instruction.draw()
    word_stim.draw()
    win.flip()

    # task 3: wait for response
    # task 4: record RT
    response_start_time = timer.getTime()
    response_keys = event.waitKeys(keyList=['r','o','y','g','b', 'q'])
    response_end_time = timer.getTime()
    response_rt = response_end_time - response_start_time
    RTs.append(response_rt)


    placeholder.draw()
    instruction.draw()    
    win.flip()
    core.wait(.15)

    if 'q' in response_keys:
        win.close()
        core.quit()