import matplotlib.pyplot as plt
from conf.configuration import *
import matplotlib

import numpy as np
import pandas as pd

def load_topic_ontology_map(ontology):
    path_ontology_topics=get_path_topics('ontology-'+ontology)
    df_ontology_topics=pd.read_csv(path_ontology_topics,sep=",",encoding="utf-8",dtype={'id':str})
    topic_map={}
    for i,ontology_topic_record in df_ontology_topics.iterrows():
        topic_map[ontology_topic_record['id']]=ontology_topic_record['name']
    return topic_map

def produce_corpora_count_over_topic(ontology):
    topic_map=load_topic_ontology_map(ontology)
    path_corpora_over_topic_count_ontology=get_path_histogram_two_parameters('ontology-'+ontology,'corpora-count','ontology-topic')
    path_figure_corpora_over_topic_ontology_count=get_path_figure_histogram_two_parameters('ontology-'+ontology,'corpora-count','ontology-topic')
    path_ground_truth_corpora=get_path_ground_truth_corpora('topic-inventory',ontology)
    df_ground_truth_corpora=pd.read_csv(path_ground_truth_corpora,sep=",",encoding="utf-8",dtype={'ontology-topic-id':str})
    df_ground_truth_corpora=df_ground_truth_corpora[~df_ground_truth_corpora['ontology-topic-id'].isin(['-1','-2'])]
    df_ground_truth_corpora['ontology-topic']=df_ground_truth_corpora['ontology-topic-id'].apply(lambda topic_id:topic_map[topic_id] )
    corpora_count_over_topic=df_ground_truth_corpora.groupby('ontology-topic').agg({'corpus':'count','ontology-topic-id':'unique'
                                                                                    }).sort_values('corpus')
    corpora_count_over_topic.to_csv(path_corpora_over_topic_count_ontology,sep=",",encoding="utf-8")


def shorten_labels(top_k_ontology_topics,max_label_size):
    ticklabels=[]
    for i,ticklabel in enumerate(top_k_ontology_topics):
        if len(ticklabel) > max_label_size:
            ticklabels.append(ticklabel[:max_label_size])
        else:
            to_add=max_label_size-len(ticklabel)
            ticklabel=ticklabel+to_add*" "

            ticklabels.append(ticklabel)
    return ticklabels



def prdoce_corpora_count_over_topic_figure(ontology, k, radial_step,max_label_size,size,offset):
    print(ontology)
    matplotlib.rcParams['pdf.fonttype']='truetype'
    path_corpora_over_topic_count_ontology=get_path_histogram_two_parameters('ontology-'+ontology,'corpora-count','ontology-topic')
    path_figure_corpora_over_topic_ontology_count=get_path_figure_histogram_two_parameters('ontology-'+ontology,'corpora-count','ontology-topic')

    df=pd.read_csv(path_corpora_over_topic_count_ontology,sep=",",encoding="utf-8")
    df.sort_values('corpus',inplace=True,ascending=False)
    ontology_topics=df['ontology-topic'].values
    corpora_count=df['corpus'].values
    if len(corpora_count)>k:
        top_k_corpora_count=corpora_count[:k-1]
        tail_corproa_count= sum(corpora_count[:k-1])
        if tail_corproa_count > corpora_count[0]:
            tail_corproa_count=corpora_count[0]
        top_k_corpora_count=np.append(top_k_corpora_count,[tail_corproa_count])
        top_k_ontology_topics=ontology_topics[:k-1]
        top_k_ontology_topics=np.append(top_k_ontology_topics,['Misc.'])
    else:
        top_k_corpora_count=corpora_count
        top_k_ontology_topics=ontology_topics
        k=len(ontology_topics)

    fig,ax = plt.subplots(figsize=size, subplot_kw=dict(polar=True))
    rlabels=list(range(0,top_k_corpora_count[0],radial_step))
    width = 2*np.pi / k
    theta = np.linspace(0.0, 2 * np.pi, k, endpoint=False)
    colors = plt.cm.viridis(np.linspace(0, 1, k))

    ax.set_rticks(list(rlabels))
    ticks= np.linspace(0,360,k+1)
    ax.set_xticks(np.deg2rad(ticks[:-1]))

    ticklabels =shorten_labels(top_k_ontology_topics,max_label_size)
    ax.set_xticklabels(ticklabels, fontsize=10)


    plt.gcf().canvas.draw()
    angles = np.linspace(0,2*np.pi,len(ax.get_xticklabels())+1)
    angles[np.cos(angles) < 0] = angles[np.cos(angles) < 0] + np.pi
    angles = np.rad2deg(angles)
    labels = []
    for label, angle in zip(ax.get_xticklabels(), angles):
        x,y = label.get_position()
        lab = ax.text(x,y+0.5-offset, label.get_text(), transform=label.get_transform(),
                      ha=label.get_ha(), va=label.get_va())
        lab.set_rotation(angle)
        labels.append(lab)
    ax.set_xticklabels([])

    ax.bar(theta, top_k_corpora_count, width=width, bottom=0.0, color=colors, alpha=0.5)



    fig.savefig(path_figure_corpora_over_topic_ontology_count)