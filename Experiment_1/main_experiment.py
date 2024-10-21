import psychopy
from psychopy import visual, core, event
import csv


# %% Open window
fullscr = True
win = visual.Window(size=[1920, 1080],
                    color=(0.5, 0.5, 0.5),
                    fullscr=fullscr,
                    units='pix')

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

# %% Load the trial sequence 
trial_file = 'trial_sequence.csv'
trials = []

with open(trial_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        trials.append(row)

# %% Output files
output_file = 'experiment_results.csv'
datafile = open(output_file, 'w')
datafile.write('image,condition,response_key,reaction_time,time_since_last_repeat,response_type\n')

display_log_file = 'image_display_log.csv'
display_log = open(display_log_file, 'w')
display_log.write('image,condition,onset_time,total_display_time\n')

global_clock = core.Clock()

# %% Experiment

fixation_dot.draw()
win.flip()

feedback_timer = None
shown_images = {}

current_block = None
for trial in trials:
    img_path = trial['image']
    block = trial['condition']
   
    if block != current_block:
        if current_block is not None:
            core.wait(1)
        current_block = block  

    img_onset_time = global_clock.getTime()
    timing = core.StaticPeriod(screenHz=60)

    image_stim = visual.ImageStim(win, image=img_path, size=(500, 500))
    image_stim.draw()
    fixation_dot.draw()

    timing.start(0.5)
    win.flip()
    onset_time = core.getTime()
    timing.complete()


    offset_time = core.getTime()
    total_display_time = offset_time - onset_time


    display_log.write(f'{img_path},{block},{img_onset_time:.4f},{total_display_time:.4f}\n')

    is_repeat = img_path in shown_images
    time_since_last_repeat = img_onset_time - shown_images.get(img_path, img_onset_time) if is_repeat else 'N/A'
    shown_images[img_path] = img_onset_time

    keys = event.getKeys(keyList=[response_key, 'escape'], timeStamped=global_clock)
    reaction_time = None
    response_type = 'N/A'

    if keys:
        for key, press_time in keys:
            if key == 'escape':
                datafile.close()
                display_log.close()
                win.close()
                core.quit()

            if key == response_key:
                reaction_time = press_time - img_onset_time
                

                if is_repeat and reaction_time <= 1.0:
                    response_type = 'True Positive'
                    fixation_dot.fillColor = 'green'
                else:
                    response_type = 'False Alarm'
                    fixation_dot.fillColor = 'red'

                feedback_timer = core.Clock()

    if is_repeat and reaction_time is None:
        response_type = 'Miss'

    datafile.write(f'{img_path},{block},{response_key},{reaction_time},{time_since_last_repeat},{response_type}\n')

    if feedback_timer is not None and feedback_timer.getTime() >= 2.0:
        fixation_dot.fillColor = 'yellow'
        feedback_timer = None

    fixation_dot.draw()
    win.flip()
    core.wait(0.1)


# %% End of experiment

end_text = visual.TextStim(
    win, text="The experiment is now over. Thank you!", height=30, color=[-1, -1, -1])
end_text.draw()
win.flip()
event.waitKeys()

datafile.close()
display_log.close()

win.close()
core.quit()
