#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mypy: ignore-errors


# import needed libraries
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
from tqdm import tqdm


# set environment arguments
plt.style.use('ggplot')


def processes_integer_labeled_embeddings(embedding, node_list):
    """Iterates over a list of embeddings and derives a dictionary where the keys are node types and the values are
    embeddings.

    Args:
        embedding (list): A nested list where each inner list is a vector of embeddings.
        node_list (list): A list of node types.

    Returns:
        A nested list where each inner list contains the node type, node label, and embedding list..
    """

    print('\n' + '=' * 100)
    print('Mapping Embeddings to Node Types')
    print('=' * 100 + '\n')

    embedding_info = []

    for row in tqdm(embedding):
        for node_label in node_list:
            if row.split('\t')[1].startswith(node_label) or node_label in row:
                embedding_info.append([node_label,
                                       row.split('\t')[0],
                                       list(map(float, row.split('\t')[-1].strip('\n').split(', ')))])

    return embedding_info


def plots_embeddings(colors, names, groups, legend_arg, label_size, tsne_size, title, title_size):

    # set up plot
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.margins(0.05)

    # iterate through groups to layer the plot
    for name, group in groups:

        if name == 'Chemicals':
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=names[name],
                    color=colors[name], mec='none', alpha=0.8)

        if name == 'Gene Ontology':
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=names[name],
                    color=colors[name], mec='none', alpha=0.7)

        if name == 'Genes':
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=names[name],
                    color=colors[name], mec='none', alpha=0.6)

        if name == 'Phenotypes':
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=names[name],
                    color=colors[name], mec='none', alpha=0.6)

        if name == 'Pathways':
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=names[name],
                    color=colors[name], mec='none', alpha=0.6)

        if name == 'Vaccines':
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=names[name],
                    color=colors[name], mec='none', alpha=0.3)

        if name == 'Diseases':
            ax.plot(group.x, group.y, marker='o', linestyle='', ms=3, label=names[name],
                    color=colors[name], mec='none', alpha=0.3)

    plt.legend(handles=legend_arg[0], fontsize=legend_arg[1], frameon=False, loc=legend_arg[2], ncol=legend_arg[3])

    ax.tick_params(labelsize=label_size)
    plt.ylim(-(tsne_size + 5), tsne_size)
    plt.xlim(-tsne_size, tsne_size)
    plt.title(title, fontsize=title_size)
    plt.show()
    plt.close()


def main():

    # CONVERT EMBEDDINGS INTO PANDAS DATAFRAME
    # read in embedding file and re-generate node labels
    input_embedding = './resources/embeddings/PheKnowLator_v2_Full_BioKG_Closed_512_100_20_10_100_003_formatted.txt'
    embed_df_out = './resources/embeddings/PheKnowLator_v2_Full_BioKG_Closed_512_100_20_10_100_003_dataframe.csv'

    embedding_file = open(input_embedding).readlines()[1:]
    node_list = ['HP', 'CHEBI', 'VO', 'DOID', 'reactome', 'GO', 'geneid']

    # convert embeddings to df
    embeddings = processes_integer_labeled_embeddings(embedding_file, node_list)
    embedding_data = pd.DataFrame(embeddings, columns=['node_type', 'node', 'embedding'])
    # embedding_data.to_pickle('./resources/embeddings/PheKnowLator_embedding_dataframe')
    embedding_data.to_csv(embed_df_out, index=None, header=True)

    # update column names (NotClosed: (sigma 0.164356; KL@250 iterations 91.896)
    # update column names (Closed: (sigma 0.177756; KL@250 iterations 89.458)
    embedding_data['node_category'] = embedding_data['node_type'].map({'HP': 'Phenotypes',
                                                                       'DOID': 'Diseases',
                                                                       'VO': 'Vaccines',
                                                                       'CHEBI': 'Chemicals',
                                                                       'GO': 'Gene Ontology',
                                                                       'geneid': 'Genes',
                                                                       'reactome': 'Pathways'})

    embedding_data.groupby(['node_type']).size()

    # DIMENSIONALITY REDUCTION
    x_reduced = TruncatedSVD(n_components=50, random_state=1).fit_transform(list(embedding_data['embedding']))
    x_embedded = TSNE(n_components=2, random_state=1, verbose=True, perplexity=50.0).fit_transform(x_reduced)
    np.save('./resources/embeddings/tsne/' + input_embedding.split('/')[-1].strip('.txt'), x_embedded)
    # x_embedded = np.load('./resources/embeddings/tSNE/PheKnowLator_v2_Full_BioKG_Embeddings_128_10_50_20_tsne.npy')

    # PLOT T-SNE
    # set up colors and legend labels
    colors = {'Diseases': '#009EFA',
              'Chemicals': 'mediumpurple',
              'Vaccines': 'firebrick',
              'Gene Ontology': '#F79862',
              'Genes': '#4fb783',
              'Pathways': 'orchid',
              'Phenotypes': '#A3B14B'}

    names = {key: key for key in colors.keys()}

    # create data frame to use for plotting data by node type
    df = pd.DataFrame(dict(x=x_embedded[:, 0], y=x_embedded[:, 1], group=list(embedding_data['node_category'])))
    groups = df.groupby('group')
    groups.size()


    # create legend arguments
    dis = mpatches.Patch(color='#009EFA', label='Diseases')
    vo = mpatches.Patch(color='firebrick', label='Vaccines')
    drg = mpatches.Patch(color='mediumpurple', label='Chemicals')
    go = mpatches.Patch(color='#F79862', label='GO Concepts')
    ge = mpatches.Patch(color='#4fb783', label='Genes')
    pat = mpatches.Patch(color='orchid', label='Pathways')
    phe = mpatches.Patch(color='#A3B14B', label='Phenotypes')

    legend_args = [[dis, vo, drg, go, ge, pat, phe], 14, 'lower center', 7]
    title = 't-SNE: Biological Knowledge Graph Without Deductive Closure (512 dimensions)'

    plots_embeddings(colors, names, groups, legend_args, 16, 40, title, 20)
