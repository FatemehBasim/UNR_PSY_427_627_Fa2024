"""
Experiment 2

"""

from psychopy import visual, core, event
import os
import random


# %% Function to set up the screen
def setup_screen(screen_size=(1920, 1080), fullscreen=True, screen_color=(0.5, 0.5, 0.5)):
    """
    Sets up the screen window for the experiment.
    """
    if fullscreen:
        win = visual.Window(
            fullscr=True,
            color=screen_color,
            units='pix',
            allowGUI=False
        )
    else:
        win = visual.Window(
            size=screen_size,
            color=screen_color,
            fullscr=False,
            units='pix',
            allowGUI=False
        )
    return win


# %% Function to get all images matching a pattern
def get_images_matching_pattern(directory, pattern):
    """
    Get all image file paths from a directory that match a given substring pattern.
    """
    matched_files = []
    for file in os.listdir(directory):
        if pattern in file.lower():
            matched_files.append(os.path.join(directory, file))
    return matched_files


# %% Function to generate a trial plan
def generate_trial_plan(categories, images, n_trials):
    """
    Generate a trial plan with exactly half identical and half different image pairs.
    """
    n_same = n_trials // 2
    n_different = n_trials - n_same
    trial_pairs = []

    # Generate "same" trials
    for _ in range(n_same):
        while True:
            category = random.choice(list(categories.keys()))
            sub_class = random.choice(list(images[category].keys()))
            if len(images[category][sub_class]) >= 2:
                img1, img2 = random.sample(images[category][sub_class], 2)
                trial_pairs.append((img1, img1, "same"))
                break

    # Generate "different" trials
    for _ in range(n_different):
        while True:
            category1, category2 = random.sample(list(categories.keys()), 2)
            sub_class1 = random.choice(list(images[category1].keys()))
            sub_class2 = random.choice(list(images[category2].keys()))
            if images[category1][sub_class1] and images[category2][sub_class2]:
                img1 = random.choice(images[category1][sub_class1])
                img2 = random.choice(images[category2][sub_class2])
                trial_pairs.append((img1, img2, "different"))
                break

    random.shuffle(trial_pairs)
    return trial_pairs


# %% Function to collect response
def collect_response(same_key, different_key, timeout, correct_response):
    """
    Collect participant response during a trial.
    """
    response = None
    reaction_time = None
    correctness = "incorrect"

    trial_clock = core.Clock()
    while trial_clock.getTime() < timeout:
        keys = event.getKeys(keyList=[same_key, different_key, 'escape'], timeStamped=trial_clock)
        if keys:
            response, response_time = keys[0]
            reaction_time = response_time
            if response == 'escape':
                return {"response": "quit", "reaction_time": reaction_time, "correctness": "quit"}
            break

    if response is not None:
        if correct_response == "same" and response == same_key:
            correctness = "correct"
        elif correct_response == "different" and response == different_key:
            correctness = "correct"

    return {
        "response": "same" if response == same_key else "different" if response == different_key else "no_response",
        "reaction_time": reaction_time if reaction_time is not None else timeout,
        "correctness": correctness
    }


# %% Main Script
win = setup_screen(screen_size=(1920, 1080), fullscreen=True, screen_color=(0.5, 0.5, 0.5))

fixation = visual.ShapeStim(
    win=win,
    vertices='cross',
    size=(30, 30),
    lineWidth=2,
    lineColor='black',
    fillColor='black',
    units='pix'
)

fdir = 'D:/UNR/Semester_4/ComputerApp/fLoc_stimuli/fLoc_stimuli'

categories = {
    'Faces': ['adult', 'child'],
    'Places': ['corridor', 'house'],
    'Bodies': ['body', 'limb'],
    'Text': ['word', 'number'],
    'Objects': ['instrument', 'car'],
    'Scrambled': ['scrambled']
}

images = {cat: {sub: get_images_matching_pattern(fdir, sub) for sub in subcats}
          for cat, subcats in categories.items()}

for cat, subcats in images.items():
    for sub in subcats:
        random.shuffle(images[cat][sub])

instruction_text = visual.TextStim(win, height=25, wrapWidth=800, color=[-1, -1, -1])
instruction_text.text = "Press a key for 'SAME':"
instruction_text.draw()
win.flip()
same_key = event.waitKeys()[0]

instruction_text.text = f"You chose '{same_key}' for 'SAME'. Now press a key for 'DIFFERENT':"
instruction_text.draw()
win.flip()
different_key = event.waitKeys()[0]

confirmation_text = f"Press '{same_key}' for 'SAME' and '{different_key}' for 'DIFFERENT'. Press any key to start."
instruction_text.text = confirmation_text
instruction_text.draw()
win.flip()
event.waitKeys()

num_trials = 30
trial_pairs = generate_trial_plan(categories, images, num_trials)

instructions = f"""You will see pairs of images.
Press '{same_key}' if they are the SAME and '{different_key}' if they are DIFFERENT.
Press 'Esc' to quit the experiment.
Press any key to start."""
instruction_text.text = instructions
instruction_text.draw()
win.flip()
event.waitKeys()

# Get monitor refresh rate
frame_dur = 1 / win.getActualFrameRate()  
frames_for_100ms = round(0.1 / frame_dur)  

output_file = 'experiment_results.csv'
with open(output_file, 'w') as datafile:
    datafile.write('trial,image1,image2,response,reaction_time,correctness,correct_answer\n')

for trial_num, (img1, img2, correct_response) in enumerate(trial_pairs, start=1):
    # Draw fixation cross 
    fixation.draw()
    win.flip()
    core.wait(0.5)

    # Prepare image stimuli
    img1_stim = visual.ImageStim(win, image=img1, size=(500, 500), pos=(-300, 0))
    img2_stim = visual.ImageStim(win, image=img2, size=(500, 500), pos=(300, 0))

    # Log timing information
    start_time = core.getTime()

    # Display stimuli for calculated number of frames
    for frame in range(frames_for_100ms):
        img1_stim.draw()
        img2_stim.draw()
        fixation.draw()
        win.flip()

    # Clear the screen 
    fixation.draw()
    win.flip()

    end_time = core.getTime()

    # Log timing 
    actual_duration = end_time - start_time
    print(f"Trial {trial_num}: Start time = {start_time:.4f}, End time = {end_time:.4f}, Duration = {actual_duration:.5f} seconds.")

    # Collect response
    response_data = collect_response(same_key, different_key, 15, correct_response)

    if response_data["correctness"] == "quit":
        break

    # Write trial results
    with open(output_file, 'a') as datafile:
        datafile.write(
            f"{trial_num},{img1},{img2},{response_data['response']},{response_data['reaction_time']:.4f},{response_data['correctness']},{correct_response}\n"
        )

    # Provide feedback
    fixation.fillColor = 'green' if response_data["correctness"] == "correct" else 'red'
    fixation.draw()
    win.flip()
    core.wait(1)

    # Show "continue" message
    cont_text = visual.TextStim(win, text="Press any key to continue.", height=25, pos=(0, 100), color=[-1, -1, -1])
    cont_text.draw()
    fixation.fillColor = 'black'
    fixation.draw()
    win.flip()
    event.waitKeys()

end_text = visual.TextStim(win, text="Experiment complete. Thank you!", height=30, pos=(0, 200), color=[-1, -1, -1])
end_text.draw()
fixation.draw()
win.flip()
event.waitKeys()

win.close()
core.quit()
