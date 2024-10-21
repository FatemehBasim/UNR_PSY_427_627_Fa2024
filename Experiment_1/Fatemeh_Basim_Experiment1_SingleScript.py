# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 12:56:40 2024

@author: fchba
"""

import psychopy
from psychopy import visual, core, event
import os
import random

# %% Open window

fullscr = True
win = visual.Window(size=[1920, 1080],
                    color=(0.5, 0.5, 0.5),
                    fullscr=fullscr,
                    units='pix')

waitBlanking = False

# %% Create fixation dot

fixation_dot = visual.Circle(
    win,
    radius=7.5,  # Because it's 15 pixels wide
    fillColor='yellow',
    lineColor='yellow',
    units='pix'
)

# %% Instructions screen

instructions = """In this experiment, you will see images of faces, places, bodies, objects, and text, along with scrambled images.
As you watch the images go by, please press [a button] as fast as you can if you see a repeated image.
Press any key to continue."""

instruction_text = visual.TextStim(
    win, text=instructions, height=25, wrapWidth=800, color=[-1, -1, -1])

instruction_text.draw()
win.flip()

# Wait for keypress
event.waitKeys()

# %% Choose the response key

response_text = "Which button would you like to use to respond? Press a key now."
response_text_stim = visual.TextStim(
    win, text=response_text, height=25, wrapWidth=800, color=[-1, -1, -1])

response_text_stim.draw()
win.flip()

# Save the response key
response_key = event.waitKeys()[0]

print(f"Participant chose {response_key} as the response key.")

# %% Load fLoc images

fdir = 'D:/UNR/Semester 4/Computer App/fLoc_stimuli/fLoc_stimuli'

categories = {
    'Faces': ['adult', 'child'],
    'Places': ['corridor', 'house'],
    'Bodies': ['body', 'limb'],
    'Text': ['word', 'number'],
    'Objects': ['instrument', 'car'],
    'Scrambled': ['scrambled']
}

images = {cat: [] for cat in categories}
for cat, subcats in categories.items():
    for subcat in subcats:
        for file in os.listdir(fdir):
            if subcat in file:
                images[cat].append(os.path.join(fdir, file))

for cat in images:
    random.shuffle(images[cat])

# %% Set block

image_duration = 0.5
gap_duration = 0.1
block_duration = 12
images_per_block = int(
    block_duration / (image_duration + gap_duration))  # = 20 images in each block


# %% Output files

output_file = 'experiment_results.csv'
datafile = open(output_file, 'w')

datafile.write(
    'image,condition,response_key,reaction_time,time_since_last_repeat,response_type\n')

#datafile.write(
#    'image,condition,response_key,reaction_time,press_time_since_beginning,time_since_last_repeat,response_type\n')

display_log_file = 'image_display_log.csv'
display_log = open(display_log_file, 'w')
display_log.write('image,condition,onset_time,total_display_time\n')

global_clock = core.Clock()

# %% Experiment

block_order = list(categories.keys()) * 2
random.shuffle(block_order)

fixation_dot.draw()
win.flip()

feedback_timer = None

for block in block_order:

    shown_images = {}

    block_images = random.choices(images[block], k=images_per_block)

    for img_path in block_images:
        img_onset_time = global_clock.getTime()

        timing = core.StaticPeriod(screenHz=60)

        image_stim = visual.ImageStim(win, image=img_path, size=(500, 500))
        image_stim.draw()
        fixation_dot.draw()

        timing.start(image_duration)
        win.flip()
        onset_time = core.getTime()
        timing.complete()

        
        offset_time = core.getTime()
        
        total_display_time = offset_time - onset_time

        
        display_log.write(
            f'{img_path},{block},{img_onset_time:.4f},{total_display_time:.4f}\n')

        # Check for a repeated path
        is_repeat = img_path in shown_images

        # Time since last repeat
        time_since_last_repeat = 'N/A'

        if is_repeat:
            time_since_last_repeat = img_onset_time - shown_images[img_path]

        shown_images[img_path] = img_onset_time

        keys = event.getKeys(
            keyList=[response_key, 'escape'], timeStamped=global_clock)

        reaction_time = None
        response_type = 'N/A'

        if len(keys) > 0:
            for key, press_time in keys:
                if key == 'escape':
                    datafile.close()
                    display_log.close()
                    win.close()
                    core.quit()

                if key == response_key:
                    reaction_time = press_time - img_onset_time
                    #if -0.5 < reaction_time < 0:
                    #    reaction_time = 0
                    

                    if is_repeat:
                        if reaction_time <= 1.0:
                            response_type = 'True Positive'
                            fixation_dot.fillColor = 'green'
                        else:
                            response_type = 'False Alarm'
                            fixation_dot.fillColor = 'red'
                    else:
                        response_type = 'False Alarm'
                        fixation_dot.fillColor = 'red'

                    feedback_timer = core.Clock()

        # Missing a repeated image
        if is_repeat and reaction_time is None:
            response_type = 'Miss'

        # Save data
        datafile.write(
            f'{img_path},{block},{response_key},{reaction_time},{time_since_last_repeat},{response_type}\n')
        
        #datafile.write(
        #    f'{img_path},{block},{response_key},{reaction_time},{press_time},{time_since_last_repeat},{response_type}\n')
        #for also saving the key press time since the beginning of the experiment

        if feedback_timer is not None and feedback_timer.getTime() >= 2.0:
            fixation_dot.fillColor = 'yellow'
            feedback_timer = None

        fixation_dot.draw()
        win.flip()

        core.wait(gap_duration)

    fixation_dot.draw()
    win.flip()

    core.wait(1)

# %% End of experiment
end_text = visual.TextStim(
    win, text="The experiment is now over. Thank you!", height=30, color=[-1, -1, -1])
end_text.draw()
win.flip()
event.waitKeys()

# Close the files
datafile.close()
display_log.close()

win.close()
core.quit()
