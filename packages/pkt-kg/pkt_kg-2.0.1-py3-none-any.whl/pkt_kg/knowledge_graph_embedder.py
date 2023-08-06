#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mypy: ignore-errors

# import needed libraries
import glob
import json
import numpy as np
import re
import subprocess

from tqdm import tqdm


def runs_deepwalk(input_file, output_file, threads, dim, nwalks, walklen, window, nprwalks, lr):
    """Performs path embedding of a knowledge graph edge list using the DeepWalk algorithm.
    https://github.com/xgfs/deepwalk-c

    Args:
        input_file (str): A file path/file storing an RDF graph.
        output_file (str): A string containing the name and file path to write out results.
        threads (int): An integer specifying the number of workers to dedicate to running the process.
        dim (int): An integer specifying the number of dimensions for the resulting embeddings.
        nwalks (int): An integer specifying the number of walks to perform.
        walklen (int): An integer specifying the length of walks.
        window (int): An integer specifying the number of dimensions for the window.
        nprwalks (nt): Number of random walks for HSM tree (default 100)
        lr (float): Initial learning rate

    Returns:
        None.
    """

    print('\n\n' + '=' * len('Running DeepWalk Algorithm'))
    print('Running DeepWalk-C Algorithm')
    print('=' * len('Running DeepWalk Algorithm'))

    outputargs = '_{dim}_{nwalks}_{walklen}_{window}_{nprwalks}_{lr}.txt'.format(dim=dim, nwalks=nwalks,
                                                                                 walklen=walklen,
                                                                                 window=10,
                                                                                 nprwalks=nprwalks,
                                                                                 lr=lr)

    # set command line argument
    try:
        subprocess.check_call(['./deepwalk-c/src/deepwalk',
                               '-input' + str(input_file),
                               '-output' + output_file + outputargs,
                               '-threads' + str(threads),
                               '-dim' + str(dim),
                               '-nwalks' + str(nwalks),
                               '-walklen' + str(walklen),
                               '-window' + str(window),
                               '-nprwalks' + str(nprwalks),
                               '-lr' + str(lr),
                               '-verbose 2'])

    except subprocess.CalledProcessError as error:
        print(error.output)

    return None


def processes_embedded_nodes(file_list, original_edges, kg_node_int_label_map):
    """Takes a list of file paths that map to embedding files saved in binary compressed sparse row graph format
    converts them into numpy arrays and then writes them to the same directory as text files.

    ASSUMPTION: A filename must have the following ordering:
        file_name_128_100_20_10_100_001.out, where:
            any combination of strings can be used before the first '_#'
            128 - dimensions (assumes dimensions are 2-3 digits long)
            100 - # walks
            20 - walk length
            10 - window
            100 - # random walks for HSM tree
            001 - learning rate (with '.' removed)
    Args:
        file_list (lst): A list of file paths.
        original_edges (str): A string naming the filepath to the original edge list.
        kg_node_int_label_map (str): A string naming the name and file path to write out results.

    Returns:
        None.
    """

    print('\n' + '=' * 75)

    # iterate over the embedding files and convert the data to numpy array
    for file in tqdm(file_list):
        print(file)

        print('\nProcessing Embedding File: {0}'.format(file.split('/')[-1]))

        # read map to convert node integers back to labels
        node_labeler = dict(map(reversed, json.loads(open(kg_node_int_label_map).read()).items()))

        # read in data and reverse mapping created by deepwalk-c
        original_nodes = set(x for y in [line.strip('\n').split('\t') for line in open(original_edges, 'r')] for x in y)

        # read in embedding data
        dim = int(re.search(r'\d{2,3}_', file).group(0).strip('_'))
        original_embeddings = np.fromfile(file, np.float32).reshape(len(original_nodes), dim)

        # re-order embeddings and write to drive
        out_loc = open('./' + file.split('.')[1] + '_formatted.txt', 'w')

        for nodes in sorted(list(dict(zip(sorted(map(int, original_nodes)), range(len(original_nodes)))).items())):
            out_loc.write(node_labeler[nodes[0]] + '\t' + str(list(original_embeddings[nodes[1]])).strip('[|]') + '\n')

        out_loc.close()

    print('=' * 75 + '\n')

    return None


    #### ADD TO NOTEBOOK
    ##############################
    # KNOWLEDGE GRAPH EMBEDDINGS #
    ##############################

    print('\n' + '=' * 33 + '\nCREATE KNOWLEDGE GRAPH EMBEDDINGS\n' + '=' * 33 + '\n')

    # set file path
    embed_path = './resources/embeddings/'

    # runs_deepwalk(input_file=ont_kg + 'PheKnowLator_v2_Full_BioKG_NoDisjointness_Closed_ELK_Triples_Integers.txt',
    #               output_file=embed_path + 'PheKnowLator_v2_Full_BioKG_DeepWalk_Embeddings_128_10_50_20.txt',
    #               threads=100,
    #               dim=128,
    #               nwalks=100,
    #               walklen=20,
    #               window=10,
    #               nprwalks=100,
    #               lr=0.01)

    # read in embeddings to convert from binary compressed sparse row (BCSR) into numpy array
    # not closed graphs
    processes_embedded_nodes(out,
                             glob.glob(
                                 'releases/v1.0.0/graphs/not_closed/PheKnowLator_v1_Full_BioKG_NoDisjointness_NotClosed_Triples_Integers.txt')[0],
                             glob.glob('releases/v1.0.0/graphs/not_closed/PheKnowLator_v1_Full_BioKG_NotClosed_Triples_Integer_Labels_Map.json')[0])

    # closed graphs
    processes_embedded_nodes(glob.glob('./resources/embeddings/*_Closed_*.out'),
                             glob.glob('./resources/knowledge_graphs/kg_closed/*Triples_Integers.txt')[0],
                             glob.glob('./resources/knowledge_graphs/kg_closed/*.json')[0])


    ############################################
    ### ADD TO EMBEDDING NOTEBOOK

    # CELL 1 - MARKDOWN
    # ** *
    # ** *
    #
    # ## Generate Mechanism Embeddings <a class="anchor" id="generate-embeddings"></a>
    #
    # To
    # create
    # estimates
    # of
    # modlecular
    # mechanisms, we
    # embed
    # knowledge
    # graph
    # information
    # extracted
    # by[DeepWalk](https: // github.com / phanein / deepwalk).This
    # repository
    # contains
    # code
    # to
    # run
    # two
    # different
    # versions
    # of
    # the[original
    # method](http: // www.perozzi.net / publications / 14_kdd_deepwalk.pdf)
    # developed
    # by[Bryan
    # Perozzi](https: // github.com / phanein):
    #
    # ** *
    #
    # -  [`DeepWalk algorithm - C`](https: // github.com / xgfs / deepwalk - c): an
    # implementation
    # of
    # the
    # original
    # algorithm in C + + (
    #     with some improvements to speed up initialize the hierarchical softmax tree that was developed by[Anton
    #     Tsitsulin](https: // github.com / xgfs).
    #
    #     To
    # run
    # this
    # from the command
    # line and not through
    # this
    # program, enter
    # the
    # following
    # from
    # `. / deepwalk - c - master / src
    # `:
    #
    # ```bash
    #        . / deepwalk - input.. / PheKnowLator_v2_Full_BioKG_NoDisjointness_Full_Triples_Integers_.bcsr - output..
    #    / PheKnowLator_v2_Full_BioKG_NotClosed_128_100_20_10_100_003.out - threads
    # 32 - dim
    # 128 - nwalks
    # 100 - walklen
    # 20 - window
    # 10 - nprwalks
    # 100 - lr
    # 0.03 - verbose
    # 2
    # ```
    #
    #   ** *
    #
    #   - [`DeepWalk - RDF`](https: // github.com / bio - ontology - research - group / walking - rdf - and -owl): an
    # extension
    # of
    # the
    # original
    # algorithm
    # that
    # also
    # embeds
    # graph
    # edges;
    # developed
    # by[the
    # Bio - Ontology
    # Research
    # Group](https: // github.com / bio-ontology-research-group / walking-rdf- and -owl).
    #       - ‼ ** Note: ** This
    # library
    # depends
    # on
    # the[C + + Boost
    # library](https: // www.pyimagesearch.com / 2015 / 04 / 27 / installing
    # -boost- and -boost-python-on-osx-with-homebrew /) and [Boost Threadpool Header Files](
    #     http: // threadpool.sourceforge
    #                  .net /).For
    # the
    # Headers, the
    # sub - directory
    # called
    # `Boost`
    # at
    # the
    # top - level
    # of
    # the
    # `walking - rdf - and -owl - master
    # `
    # directory.In
    # order
    # to
    # compile and run
    # `Deepwalk - RDF`
    # on
    # OSX, there
    # are
    # a
    # few
    # important
    # changes
    # that
    # will
    # need
    # to
    # be
    # made:
    # - Change
    # `TIME_UTC`
    # to
    # `TIME_UTC_` in the
    # `boost / threadpool / task_adaptors.hpp`.
    # - Change
    # the
    # `-lboost_thread`
    # argument
    # to
    # `-lboost_thread - mt` in the
    # `walking - rdf - and -owl - master / Makefile`
    # - To
    # troubleshoot
    # incompatability
    # issues
    # between
    # Deepwalk and Gensim, run
    # the
    # following in this
    # order:
    # - `pip
    # uninstall
    # gensim
    # `
    # - `pip
    # uninstall
    # deepwalk
    # `
    # - `pip
    # install
    # gensim == 0.10
    # .2
    # `
    # - `pip
    # install
    # deepwalk
    # `
    #
    # To
    # run
    # this
    # from the command
    # line and not through
    # this
    # program, enter
    # the
    # following
    # from
    # `. / walking - rdf - and -owl - master / `:
    #
    # ```bash
    # deepwalk - -workers
    # 64 - -representation - size
    # 256 - -format
    # edgelist - -input
    # applications / inputs / PheKnowLator_v2_Full_BioKG_NoDisjointness_Closed_ELK_Triples_Integers.txt - -output
    # applications / outputs / PheKnowLator_v2_Full_BioKG_NoDisjointness_Closed_ELK_Embedddings_256_10_50_40.txt - -window - size
    # 10 - -number - walks
    # 50 - -walk - length
    # 40
    # ```
    #
    #   ** *
    #
    #  ** NOTE. ** It
    # 's both faster and less taxing on your computer to run this code from the command line rather than from here.
    #
    # _The
    # current
    # analysis
    # implemented
    # DeepWalk - C as its
    # runtime
    # was
    # nearly
    # 10
    # times
    # faster
    # than
    # DeepWalk - RDF_


# CELL 2 - CODE
# set file path
# embed_path = './resources/embeddings/'
#
# runs_deepwalk(input_file=ont_kg + 'PheKnowLator_v2_Full_BioKG_NoDisjointness_Closed_ELK_Triples_Integers.txt',
#               output_file=embed_path + 'PheKnowLator_v2_Full_BioKG_DeepWalk_Embeddings_128_10_50_20.txt',
#               threads=100,
#               dim=128,
#               nwalks=100,
#               walklen=20,
#               window=10,
#               nprwalks=100,
#               lr=0.01)

# CELL 3 - MARKDOWN
# **Process and Format Embeddings for Analysis**
# Read in embeddings and replace integer node labels with their more meaningful biological knowledge graph identifiers.

# _Not Deductively Closed Knowledge Graph_
# not closed graphs
# processes_embedded_nodes(glob.glob('./resources/embeddings/*_NotClosed_*.out'),
#                          glob.glob('./resources/knowledge_graphs/kg_not_closed/*Triples_Integers.txt')[0],
#                          glob.glob('./resources/knowledge_graphs/kg_not_closed/*.json')[0])


# _Deductively Closed Knowledge Graph_

# # closed graphs
# processes_embedded_nodes(glob.glob('./resources/embeddings/*_Closed_*.out'),
#                          glob.glob('./resources/knowledge_graphs/kg_closed/*Triples_Integers.txt')[0],
#                          glob.glob('./resources/knowledge_graphs/kg_closed/*.json')[0])


# **Preproess Embedding Data to Prepare for Analysis**
# read in embedding file and re-generate node labels
# input_embedding = './resources/embeddings/PheKnowLator_v2_Full_BioKG_Closed_128_100_20_10_100_003_formatted.txt'
# embed_df_out = './resources/embeddings/PheKnowLator_v2_Full_BioKG2_Embedding_128_100_20_10_100_003_dataframe.csv'
#
# input_embeddings = glob.glob('./resources/embeddings/*_formatted.txt')
#
# for file in glob.glob('./resources/embeddings/*_formatted.txt'):
#
#     embedding_file = open(file).readlines()[1:]
#     node_list = ['HP', 'CHEBI', 'VO', 'DOID', 'R-HSA', 'GO', 'geneid']
#
#     # convert embeddings to df
#     embeddings = processes_integer_labeled_embeddings(embedding_file, node_list)
#     embedding_data = pd.DataFrame(embeddings, columns=['node_type', 'node_id', 'embedding'])
#
#     # update column names (128: (sigma 0.196289; KL@50 iterations 103.057411)
#     embedding_data['node_category'] = embedding_data['node_type'].map({'HP': 'Phenotypes',
#                                                                        'DOID': 'Diseases',
#                                                                        'VO': 'Vaccines',
#                                                                        'CHEBI': 'Chemicals',
#                                                                        'GO': 'Gene Ontology',
#                                                                        'geneid': 'Genes',
#                                                                        'R-HSA': 'Pathways'})
#
#     # save locally
#     embedding_data[['node_type', 'node_type', 'node_id', 'embedding']].to_csv(embed_df_out, index=None, header=True)
#
# # preview data
# embedding_data.head(n=10)


## MARKDOWN

#
# ***
# ***
#
# ## t-SNE Plot <a class="anchor" id="tsne-plot"></a>
# To visualize the relationships between the embedded nodes, we first need to redduce the dimensions of the molecular mechanism embeddings. To this we use [t-SNE](). Once reduce, we can visualize the results in a scatter plot.

# **Biological Knowledge Graph**
# _Process Embeddings_
# _Dimensionality Reduction with t-SNE_

# x_reduced = TruncatedSVD(n_components=50, random_state=1).fit_transform(list(embedding_data['embeddings']))
# x_embedded = TSNE(n_components=2, random_state=1, verbose=True, n_iter=1000, learning_rate=20, perplexity=50.0)\
#     .fit_transform(x_reduced)
# np.save('./resources/embeddings/PheKnowLator_v2_Full_BioKG_NoDisjointness_Closed_ELK_Embeddings_128_10_50_40_tsne', x_embedded)

# # set-up plot arguments
# # set up colors and legend labels
# colors = {'Diseases': '#009EFA',
#           'Chemicals': 'indigo',
#           'GO Concepts': '#F79862',
#           'Genes': '#4fb783',
#           'Pathways': 'orchid',
#           'Phenotypes': '#A3B14B'}
#
# names = {key: key for key in colors.keys()}
#
# # create data frame to use for plotting data by node type
# df = pd.DataFrame(dict(x=x_embedded[:, 0], y=x_embedded[:, 1], group=list(embedding_data['node_type'])))
# groups = df.groupby('group')
#
# # create legend arguments
# dis = mpatches.Patch(color='#009EFA', label='Diseases')
# drg = mpatches.Patch(color='indigo', label='Drugs')
# go = mpatches.Patch(color='#F79862', label='GO Concepts')
# ge = mpatches.Patch(color='#4fb783', label='Genes')
# pat = mpatches.Patch(color='orchid', label='Pathways')
# phe = mpatches.Patch(color='#A3B14B', label='Phenotypes')
#
# legend_args = [[dis, drg, go, ge, pat, phe], 14, 'lower center', 3]
# title = 't-SNE: Biological Knowledge Graph'
#
# plots_embeddings(colors, names, groups, legend_args, 16, 100, title, 20)
