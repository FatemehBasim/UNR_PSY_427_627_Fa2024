# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 17:30:33 2024

@author: fchba
"""

#%% Imports
from psychopy import visual, core, event
import numpy as np

#%% 
win = visual.Window(size=[400, 400], color=(0.5, 0.5, 0.5), units='pix')

#%% Convert HSV to RGB 
#I'm not sure if I understand this conversion correctly. I used ChatGPT for this part, and I'm still a bit confused!
def hsv_to_rgb(h, s, v):

    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    if i == 0: return [v, t, p]
    if i == 1: return [q, v, p]
    if i == 2: return [p, v, t]
    if i == 3: return [p, q, v]
    if i == 4: return [t, p, v]
    if i == 5: return [v, p, q]

#%% random color pair
def generate_color_pair(hue_diff_range):
    hue_base = np.random.rand() 
    hue_1 = hue_base
    hue_2 = (hue_base + np.random.uniform(*hue_diff_range)) % 1.0  
    color_1 = hsv_to_rgb(hue_1, 1.0, 1.0)  
    color_2 = hsv_to_rgb(hue_2, 1.0, 1.0)
    return color_1, color_2

#%% Create color patches
def draw_color_pair(hue_diff_range):
    color_1, color_2 = generate_color_pair(hue_diff_range)
    patch1 = visual.Rect(win, width=100, height=100, fillColor=color_1, pos=[-60, 0])
    patch2 = visual.Rect(win, width=100, height=100, fillColor=color_2, pos=[60, 0])
    patch1.draw()
    patch2.draw()

#%% Blocks
def run_block(hue_diff_range):
    for _ in range(16): 
        draw_color_pair(hue_diff_range)
        win.flip()
        core.wait(1) 
        win.flip()
        core.wait(0.25)  

#%% Main experiment sequence
def run_experiment():

    hue_ranges = [(0.0, 0.1), (0.1, 0.2), (0.4, 0.5)] 
    for hue_range in hue_ranges:
        run_block(hue_range)
        core.wait(3)  

#%% Run the experiment
run_experiment()

#%% Close the window when finished
win.close()
