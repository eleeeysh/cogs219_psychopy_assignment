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

max_rt = 2

# task 7: create incongruent
def make_incongruent(stim):
    sampled = random.choice([c for c in stimuli if c != stim])
    return sampled

# task 9
def generate_trials(subj_code, prop_incongruent, num_trials=100):
    '''
    Writes a file named {subj_code_}trials.csv, one line per trial. Creates a trials subdirectory if one does not exist
    subj_code: a string corresponding to a participant's unique subject code
    prop_incongruent: float [0-1] corresponding to the proportion of trials that are incongruent
    num_trials: integer specifying total number of trials (default 100)
    '''
    import os
    import random
    
    try:
        os.mkdir('trials')
    except FileExistsError:
        print('Trials directory exists; proceeding to open file')

    n_congruent = int(num_trials * (1 - prop_incongruent/100))
    n_incongruent = num_trials - n_congruent

    configs = [subj_code, prop_incongruent]
    congruency = ['congruent',] * n_congruent + ['incongruent'] * n_incongruent
    orientations = ['upright',] * (n_congruent // 2) +\
        ['upside_down',] * (n_congruent - n_congruent // 2) +\
        ['upright',] * (n_incongruent // 2) +\
        ['upside_down',] * (n_incongruent - n_incongruent // 2)
    all_stimuli = random.sample(stimuli, num_trials)

    # generate color
    all_colors = all_stimuli[:n_congruent]
    for s in all_stimuli[n_congruent:]:
        all_colors.append(make_incongruent(s))

    # generate congruent trials
    separator = ","
    des_name = f"trials/{subj_code}_trials.csv"
    with open(des_name, "w") as f:
        # write header
        header = separator.join(["subj_code","prop_incongruent", 'word','color','congruency','orientation'])
        f.write(header + '\n')

        trials = []
        for i in range(n_congruent):
            new_trial = configs[:] + [
                all_stimuli[i],
                all_colors[i],
                congruency[i],
                orientations[i]]
            new_trial_str = separator.join(map(str, new_trial))
            trials.append(new_trial_str)

        random.shuffle(trials)
        for trial_str in trials:
            f.write(trial_str + '\n')

    return des_name

def read_trials(trial_file):
    separator = ","
    # read header
    with open(trial_file, 'r') as f:
        col_names = f.readline().rstrip().split(separator)
    # read trials
    trials_list = []
    with open(trial_file, 'r') as f:
        for line in f:
            cur_trial = line.rstrip().split(separator)
            trial_dict = dict(zip(col_names, cur_trial))
            trials_list.append(trial_dict)
    return trials_list

# task 10
def get_runtime_vars():
    #Get run time variables, see http://www.psychopy.org/api/gui.html for explanation
    vars_to_get = {
        'subj_code': 'stroop_101', 
        'prop_incongruent': ['Choose', '25', '50', '75'],
    }
    vars_order = ['subj_code', 'prop_incongruent']
    infoDlg = gui.DlgFromDict(
        dictionary=vars_to_get, title='stroop', order=vars_order)
    return infoDlg.ok, vars_to_get


# task 10: get config input
_, runtime_vars= get_runtime_vars()

# tasl 11: loop through trials
trial_file = generate_trials(runtime_vars['subj_code'], int(runtime_vars['prop_incongruent']))
trials_generated = read_trials(trial_file)
for trial in trials_generated:
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
    word_stim.setText(trial['word'])
    # task 7: set incongruent color
    word_stim.setColor(trial['color'])
    word_stim.setOri(0 if trial['orientation'] == 'upright' else 180)
    
    placeholder.draw()
    word_stim.draw()
    win.flip()

    # task 3: wait for response
    # task 4: record RT
    response_start_time = timer.getTime()
    response_keys = event.waitKeys(maxWait=max_rt, keyList=['r','o','y','g','b', 'q'])
    response_end_time = timer.getTime()
    response_rt = response_end_time - response_start_time
    RTs.append(response_rt)

    if not response_keys:
        # task 6: cutoff too long RT
        placeholder.draw()
        word_stim.setText("Too slow")
        word_stim.setColor("black")
        word_stim.draw()
        win.flip()
        core.wait(1)
    
    elif 'q' in response_keys:
        win.close()
        core.quit()

    # task 5: feedback
    elif response_keys[0] != cur_stim[0]:
        placeholder.draw()
        word_stim.setText("incorrect")
        word_stim.setColor("black")
        word_stim.draw()
        win.flip()
        core.wait(1)


    placeholder.draw()
    instruction.draw()    
    win.flip()
    core.wait(.15)
