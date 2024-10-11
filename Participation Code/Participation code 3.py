# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 13:44:11 2024

@author: fchba
"""

import psychopy
from psychopy import visual, core, event

#%% Open window

try:
    fullscr = False
    screen_size = [800, 600]
    win = visual.Window(size=screen_size, 
                        color=(0.5, 0.5, 0.5),
                        fullscr=fullscr, 
                        units='pix')
    
    # Display message:
    my_str = 'Press left or right arrow to respond, or "q" to quit!'
    txt_stim = visual.TextStim(win, text=my_str)
    txt_stim.draw()
    win.flip()
    t0 = core.getTime()

    # Create a patch 
    patch = visual.Rect(win, width=100, height=100, fillColor='blue')
    
    # Display blue patch
    patch.draw()
    win.flip()

    core.wait(2)  

    # Change the color
    patch.fillColor = 'red'
    patch.draw()
    win.flip()
    change_time = core.getTime()

    # Choose a key for responses
    chosen_key = event.waitKeys(keyList=['left', 'right', 'q'], timeStamped=True)
    if chosen_key:
        key, key_time = chosen_key[0]
        if key == 'q':
            print('Experiment ended by the participant.')
        else:
            reaction_time = key_time - change_time
            print(f'Response: {key}, Reaction Time: {reaction_time:.5f} seconds')
    else:
        print('Response timed out!')

except Exception as e:
    win.close()
    print(f'Error: {e}')
    raise
finally:
    win.close()
    core.quit()
