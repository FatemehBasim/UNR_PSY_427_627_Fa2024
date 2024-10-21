import os
import random
import csv


# %% Set directory

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
images_per_block = int(block_duration / (image_duration + gap_duration))

block_order = list(categories.keys()) * 2
random.shuffle(block_order)

# %% Generate sequence

trial_sequence = []

for block in block_order:
    block_images = random.choices(images[block], k=images_per_block)
    for img_path in block_images:
        trial_sequence.append({'image': img_path, 'condition': block})

# Save the trial sequence 
output_file = 'trial_sequence.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['image', 'condition'])
    writer.writeheader()
    writer.writerows(trial_sequence)


