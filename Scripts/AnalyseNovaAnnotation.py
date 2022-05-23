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

# if the folder doesn't exist then create it
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
    
    # creating a datframe which has count of each category
    # will be used to insert missing categories
    df = data.groupby('ekman_annotation')['ekman_annotation'].count()
    dfd = df.to_dict()
    
    comp_annotation_list = list(range(8)) # complete list of annotations used (0-7)
    # adding missing annotations
    for i in comp_annotation_list:
        if comp_annotation_list[i] in dfd:
            continue
        else:
            dfd[comp_annotation_list[i]] = 0
        
    # creating the dataframe to use for plotting
    dfd_items = dfd.items()
    data_list = list(dfd_items)
    df = pd.DataFrame(data_list)
    df.set_index(0, inplace= True, drop=True)
    df.sort_index(inplace = True)
    df = df.rename(columns={1: 'Count'})
    
    #plot
    ax.bar(ekman_annotations,df['Count'], color= 'steelblue')
    ax.set_title(plot_title, fontweight='bold', pad=10)

    # modifing x and y tick_params
    ax.tick_params(axis='x', which='major', pad = 15, labelrotation= 45.0)
    ax.tick_params(axis='y', which='major', pad = 15)

    return ax.get_figure()

# function to draw boxplot
def draw_boxplot(data, plot_title, ekman_annotations):
    fig, ax2 = plt.subplots()

    # all annotations present in file
    available_annotations = data['ekman_annotation'].unique().tolist()

    # complete list of annotations used (0-7) 
    comp_annotation_list = list(range(8))
    # adding missing annotations
    for i in comp_annotation_list:
        if comp_annotation_list[i] in available_annotations:
            continue
        else:
            data.loc[data.shape[0]] = [0.0, 0.0, comp_annotation_list[i], 1, 0 ]

    # showfliers = false to remove outliers
    box = sns.boxplot(x = 'ekman_annotation', y = 'frame_duration', data=data, ax=ax2, color='steelblue', showfliers=False,)
    box.set_title(plot_title, fontweight='bold', pad=10)
    plt.xlabel('') #x labels seems to be redundant
    plt.ylabel('Frame duration')
    ax2.set_xticklabels(ekman_annotations)

    ax2.tick_params(axis='x', which='major', pad = 15, labelrotation= 45.0)
    ax2.tick_params(axis='y', which='major', pad = 15)
    
    return box.get_figure()

countplot_fig = draw_countplot(df,
                               'Label annotation count (0-7)',
                                ['Happyness', 'Sadness', 'Surprise', 'Fear', 'Anger', 'Disgust', 'Contempt', 'Other'],
                               )
# saving bar plot
save_countplot_path = os.path.join(dest_dir, 'countplot_ekman_annotations.png')
print("Saving countplot {}... ".format(save_countplot_path))
countplot_fig.savefig(save_countplot_path)

boxplot_fig = draw_boxplot(df, 
                    'Frame duration (secs)',
                    ['Happyness', 'Sadness', 'Surprise', 'Fear', 'Anger', 'Disgust', 'Contempt', 'Other'],
                )
# saving boxplot 
save_boxplot_path = os.path.join(dest_dir, 'boxplot_ekman_annotations.png')
print("Saving boxplot {}... ".format(save_boxplot_path))
boxplot_fig.savefig(save_boxplot_path)

print("All done.")