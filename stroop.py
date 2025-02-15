import time
import sys
import random
import os
from psychopy import visual,event,core,gui

stimuli = ['red', 'orange', 'yellow', 'green', 'blue']

win = visual.Window([800,600],color="gray", units='pix',checkTiming=False)
placeholder = visual.Rect(win,width=180,height=80, fillColor="lightgray",lineColor="black", lineWidth=6,pos=[0,0])
word_stim = visual.TextStim(win,text="", height=40, color="black",pos=[0,0])
instruction = visual.TextStim(win,text="Press the first letter of the ink color", height=20, color="black",pos=[0,-200])
feedback = visual.TextStim(win,text="Too Slow", height=40, color="black",pos=[0,0])

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
def generate_trials(subj_code, seed, num_repititions=100):
    '''
    Writes a file named {subj_code_}trials.csv, one line per trial. Creates a trials subdirectory if one does not exist
    subj_code: a string corresponding to a participant's unique subject code
    prop_incongruent: float [0-1] corresponding to the proportion of trials that are incongruent
    num_trials: integer specifying total number of trials (default 100)
    '''
    import os
    import random

    random.seed(seed)
    
    try:
        os.mkdir('trials')
    except FileExistsError:
        print('Trials directory exists; proceeding to open file')

    # generate congruency and 
    import itertools
    congruency_conds = ['congruent', 'incongruent']
    orientation_conds = ['upright', 'upside_down']
    print('are we here')
    all_conditions = list(itertools.product(
        congruency_conds, orientation_conds)) * num_repititions
    congruency, orientations = zip(*all_conditions)

    # generate word stimuli
    num_trials = len(congruency_conds) * len(orientation_conds) * num_repititions
    all_stimuli = random.choices(stimuli, k=num_trials)

    # generate color stimuli
    all_colors = []
    for s, c in zip(all_stimuli, congruency):
        if c == 'congruent':
            all_colors.append(s)
        else:
            all_colors.append(make_incongruent(s))


    configs = [subj_code, seed]

    # write trials
    separator = ","
    des_folder = 'trials'
    os.makedirs(des_folder, exist_ok=True)
    des_name = os.path.join(des_folder, f"{subj_code}.csv")
    with open(des_name, "w") as f:
        # write header
        header = separator.join([
            'subj_code', 'seed',
            'word','color','trial_type','orientation'])
        f.write(header + '\n')

        trials = []
        for i in range(num_trials):
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
    trials_list = []
    # read header
    with open(trial_file, 'r') as f:
        col_names = f.readline().rstrip().split(separator)
        for line in f:
            cur_trial = line.rstrip().split(separator)
            trial_dict = dict(zip(col_names, cur_trial))
            trials_list.append(trial_dict)
    print(trials_list[0])
    return trials_list

# task 10
def get_runtime_vars():
    #Get run time variables, see http://www.psychopy.org/api/gui.html for explanation
    vars_to_get = {
        'subj_code':'stroop_101',
        'seed': 101, 
        'num_reps': 25,
    }
    vars_order = ['subj_code', 'seed', 'num_reps']
    infoDlg = gui.DlgFromDict(
        dictionary=vars_to_get, title='stroop', order=vars_order)
    return infoDlg.OK, vars_to_get


# task 10: get config input
_, runtime_vars= get_runtime_vars()
# tasl 11: loop through trials
trial_file = generate_trials(
    runtime_vars['subj_code'], 
    int(runtime_vars['seed']),
    int(runtime_vars['num_reps']))
trials_generated = read_trials(trial_file)

# task 12: prepare output
output_folder = 'data'
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, f"{runtime_vars['subj_code']}_data.csv")
trial_defined_cols = [
    'subj_code', 'seed', 'word', 'color', 'trial_type', 'orientation',] 
trial_response_cols = ['trial_num', 'response', 'is_correct', 'rt']
with open(output_path, "w") as f:
    # write header
    header_str = ','.join(trial_defined_cols + trial_response_cols)
    f.write(header_str + '\n')

for trial_id, trial in enumerate(trials_generated):
    # task 1: show fixation
    placeholder.draw()
    fixation.draw()
    win.flip()
    core.wait(0.5)

    # task 1: remove fixation stimuli
    placeholder.draw()
    win.flip()
    core.wait(0.5)
    # cur_stim = random.choice(stimuli)
    word_stim.setText(trial['word'])
    # task 7: set incongruent color
    word_stim.setColor(trial['color'])
    # task 11: rotate it
    to_rotate = trial['orientation'] == 'upright'
    word_stim.setOri(0 if to_rotate else 180)
    
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

    is_correct = False
    response = None
    if not response_keys:
        # task 6: cutoff too long RT
        placeholder.draw()
        feedback.setText("Too slow")
        feedback.draw()
        win.flip()
        core.wait(1)
    
    elif 'q' in response_keys:
        win.close()
        core.quit()

    # task 5: feedback
    elif response_keys[0] != trial['color'][0]:
        response = response_keys[0]
        placeholder.draw()
        feedback.setText("incorrect")
        feedback.draw()
        win.flip()
        core.wait(1)

    else:
        response = response_keys[0]
        is_correct = True

    # task 12: write output
    response_data_dict = {
       'trial_num': trial_id+1, 
       'response': response, 
       'is_correct': is_correct, 
       'rt': response_rt
    }
    trial_record = []
    for col in trial_defined_cols:
        trial_record.append(str(trial[col]))
    for col in trial_response_cols:
        trial_record.append(str(response_data_dict[col]))
    
    with open(output_path, "a") as f:
        trial_str = ','.join(trial_record)
        f.write(trial_str+'\n')

    placeholder.draw()  
    win.flip()
    core.wait(.15)
