# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:14:29 2024

@author: fchba
"""

#%% Imports
from psychopy import visual, core
import numpy as np
import colorsys  

#%%
win = visual.Window(size=[400, 400], color=(0.5, 0.5, 0.5), units='pix')

#%% random color pair
def generate_color_pair(hue_diff_range):
    hue_base = np.random.rand()
    hue_1 = hue_base
    hue_2 = (hue_base + np.random.uniform(*hue_diff_range)) % 1.0 

    # Convert HSV to RGB
    color_1 = colorsys.hsv_to_rgb(hue_1, 1.0, 1.0)
    color_2 = colorsys.hsv_to_rgb(hue_2, 1.0, 1.0)

    return color_1, color_2

#%% Draw color patches
def draw_color_pair(hue_diff_range):
    color_1, color_2 = generate_color_pair(hue_diff_range)
    patch1 = visual.Rect(win, width=100, height=100, fillColor=color_1, pos=[-60, 0])
    patch2 = visual.Rect(win, width=100, height=100, fillColor=color_2, pos=[60, 0])
    patch1.draw()
    patch2.draw()

#%% Block
def run_block(hue_diff_range):
    for repeat in range(16):  #the whole block supposed to take 20s, so it would be 16 pair I guess ?!
        draw_color_pair(hue_diff_range)
        win.flip()
        core.wait(1)  # each pair 1 second
        win.flip()
        core.wait(0.25)  # Gap between pairs

#%% 
def run_experiment():
    hue_ranges = [(0.0, 0.1), (0.1, 0.2), (0.4, 0.5)]  
    for hue_range in hue_ranges:
        run_block(hue_range)
        core.wait(3)  

#%% Run the experiment
run_experiment()

#%% Close the window when finished
win.close()
