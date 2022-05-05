import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

# getting the directories
parser = argparse.ArgumentParser(description='data analysis of a ekman annotations file')
parser.add_argument('--annotationsdir', help='annotations directory (likely, .../Corpus/annotations/)', required=True)
parser.add_argument('--destdir', help='directory to save results', required=True)  

args = parser.parse_args()

# converting the directories to string
annotations_dir = str(args.annotationsdir)
dest_dir = str(args.destdir)

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)


######## GETTING & CLEANING THE DATASET ###############
df = pd.read_csv(annotations_dir, sep=';', header = None)
df.columns = ['framestart', 'frameend', 'ekman_annotation', 'ref']
# adding the column for frame duration
df['frame_duration'] = df['frameend'] - df['framestart']

# cleaning dataframe (removing empty and NaN values)
nan_value = float("NaN")
df.replace("", nan_value, inplace=True)
df.dropna(subset=["framestart", "frameend", "ekman_annotation"], inplace=True)
###########################################


# configuring matplotlib styles (attributes will be taken from json file) 
sns.set_theme(style="darkgrid")
plt.rc('font', size=15)          # controls default text sizes
plt.rc('axes', titlesize=20)     # fontsize of the axes title
plt.rc('axes', labelsize=20)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
plt.rc('legend', fontsize=10)    # legend fontsize
plt.rc('figure', titlesize=20, figsize=(18, 12))


# function to draw the countplot 
def draw_countplot(data, plot_title, ekman_annotations):
    fig, ax = plt.subplots()
    countplot = sns.countplot(x="ekman_annotation", data=data, ax=ax, color= 'steelblue')
    countplot.set_title(plot_title, fontweight='bold', pad=10)
    plt.xlabel('') #x labels seems to be redundant

    # plotting annotations
    for c, p in enumerate(countplot.patches):
        #for drawing exact count of each category above the bar
        countplot.annotate('{}'.format(p.get_height()), (p.get_x()+0.25, p.get_height()+2), size= 15, fontweight = 'bold')
        # for drawing the category name at the bottom of each bar
        countplot.annotate('{}'.format(ekman_annotations[c]), (p.get_x()+0.10, 5), size= 15, fontweight = 'bold')

    # returning the plot
    return countplot.get_figure()


# function to draw boxplot
def draw_boxplot(data, plot_title, ekman_annotations):
    # calculating median to show on boxes
    medians = data.groupby('ekman_annotation')['frame_duration'].median()
    fig, ax2 = plt.subplots()

    # showfliers = false to remove outliers
    box = sns.boxplot(x = 'ekman_annotation', y = 'frame_duration', data=data, ax=ax2, color='steelblue', showfliers=False,)
    box.set_title(plot_title, fontweight='bold', pad=10)
    plt.xlabel('') #x labels seems to be redundant
    plt.ylabel('Frame duration')

    for i in range(len(medians)):
        # for drawing median over each box for the respective category
        box.annotate('{:.2f}'.format(medians[i]), (i, medians[i]+0.01), size=15, fontweight='bold')
        # for drawing the category name at the bottom of each box
        box.annotate('{}'.format(ekman_annotations[i]), (i-0.2, -0.1), size=15, fontweight='bold')

    # returning the plot
    return box.get_figure()


countplot_fig = draw_countplot(df,
                               'Label annotation count (0-7)',
                                ['Happyness', 'Sadness', 'Surprise', 'Fear', 'Anger', 'Disgust', 'Contempt', 'Other'],
                               )
save_countplot_path = os.path.join(dest_dir, 'countplot_ekman_annotations.png')
print("Saving countplot {}... ".format(save_countplot_path))
countplot_fig.savefig(save_countplot_path)

boxplot_fig = draw_boxplot(df, 
                    'Frame duration (secs)',
                    ['Happyness', 'Sadness', 'Surprise', 'Fear', 'Anger', 'Disgust', 'Contempt', 'Other'],
                )
save_boxplot_path = os.path.join(dest_dir, 'boxplot_ekman_annotations.png')
print("Saving boxplot {}... ".format(save_boxplot_path))
boxplot_fig.savefig(save_boxplot_path)

print("All done.")
