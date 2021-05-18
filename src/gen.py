from collections import Counter
from datetime import datetime
import networkx as nx
import os
import pathlib
import pickle
import re
import time

import arguments
import common
import constants

TIME = datetime.now().strftime('%Y%m%d_%H%M')


def normalize_input_line(line):
    line = re.sub(' +', ' ', line).strip(' \t\n')
    return line


def load_data(data_path, chunk_freq_threshold=1):
    dic = Counter()
    sents = []
    with open(data_path) as f:
        for line in f:
            line = normalize_input_line(line)
            if len(line) == 0:
                continue

            chunks = line.split(constants.SL_TOKEN_DELIM)
            dic.update(chunks)

            raw_sen = ''
            for chunk in chunks:
                raw_sen += chunk
            sents.append(raw_sen)

    # filter vocab
    dic = filter_dic_by_freq(dic, chunk_freq_threshold)

    return sents, dic


def load_external_dictionary(data_path, chunk_freq_threshold=1, dic=None):
    vocabs = []
    if not dict:
        dic = Counter()

    with open(data_path) as f:
        for vocab in f:
            vocab = normalize_input_line(vocab)
            vocabs.append(vocab)

    dic.update(vocabs)
    dic = filter_dic_by_freq(dic, chunk_freq_threshold)
    return dic


def filter_dic_by_freq(dic, freq_threshold):
    dic = Counter(
        {chunk: freq
         for chunk, freq in dic.items() if freq >= freq_threshold})
    return dic


def gen_trie(dic, case_insensitive=True):
    trie = common.init_trie_automaton(dic, case_insensitive=case_insensitive)
    return trie


def gen_lattices(trie,
                 sents,
                 unuse_single_token=False,
                 init_token=constants.INIT_TOKEN,
                 eos_token=constants.EOS_TOKEN):

    graphs = []
    for sent in sents:
        G = nx.DiGraph()

        # add start node
        G.add_node((init_token, (0, 0)))

        # add nodes (single token)
        if not unuse_single_token:
            tokens = list(sent)
            offset = 0
            for token in tokens:
                span = (offset, offset + 1)
                G.add_node((token, span))
                offset += 1

        # add nodes (chunk)
        chunks = trie.search_all(sent)
        for chunk, offset in chunks:
            if not unuse_single_token and len(chunk) < 2:
                continue
            span = (offset, offset + len(chunk))
            G.add_node((chunk, span))

        # add ending node
        G.add_node((eos_token, (len(sent), len(sent))))

        # add edges
        nodes = list(G.nodes())
        for i in range(len(nodes)):
            node_i = nodes[i]
            chunk_i, span_i = node_i
            for j in range(i + 1, len(nodes)):
                node_j = nodes[j]
                chunk_j, span_j = node_j
                if span_i[1] == span_j[0]:
                    G.add_edge(node_i, node_j)

        graphs.append(G)

    return graphs


def save_data(trie,
              dic,
              lattices=None,
              path_prefix='/outputs',
              prefix_filename=None,
              save_dic=False):
    if not prefix_filename:
        prefix_filename = pathlib.Path(TIME)
    output_prefix_path = path_prefix / prefix_filename
    output_trie_path = output_prefix_path.parent / (output_prefix_path.name +
                                                    constants.TRIE_FORMAT)

    if not os.path.exists(path_prefix):
        os.makedirs(path_prefix)

    with open(output_trie_path, 'wb') as f:
        pickle.dump(trie, f)
        print('### Save trie automaton to {}'.format(output_trie_path))

    if lattices:
        output_lattice_path = output_prefix_path.parent / (
            output_prefix_path.name + constants.LATTICE_FORMAT)
        with open(output_lattice_path, 'wb') as f:
            pickle.dump(lattices, f)
            print('### Save lattices to {}'.format(output_lattice_path))

    if save_dic:
        output_dic_path = output_prefix_path.parent / (
            output_prefix_path.name + constants.DIC_FORMAT)
        with open(output_dic_path, 'w') as f:
            for k, v in dic.most_common():
                f.write('{}\t{}\n'.format(k, v))
            print('### Save dictionary to {}'.format(output_dic_path))


if __name__ == '__main__':
    started_time = time.time()

    # get arguments
    parser = arguments.ArgumentLoader()
    args = parser.parse_args()

    # load data and generate dictionary
    input_data_path = args.input_data
    sents, dic = load_data(input_data_path,
                           chunk_freq_threshold=args.chunk_freq_threshold)

    # load external dictionary if any
    if args.external_dic_path:
        dic = load_external_dictionary(
            args.external_dic_path,
            chunk_freq_threshold=args.chunk_freq_threshold,
            dic=dic)

    # get trie created by dict
    trie = gen_trie(dic, case_insensitive=not args.case_sensitive)

    # get lattice sentences by utilzing trie
    lattices = gen_lattices(
        trie, sents, args.unuse_single_token) if args.gen_lattice else None

    # write data
    save_data(trie,
              dic,
              lattices,
              path_prefix=args.output_data_path_prefix,
              prefix_filename=args.output_data_filename_prefix,
              save_dic=args.save_dic)

    elapsed_time = time.time() - started_time
    print('\nElapsed time: {} second(s)'.format(elapsed_time))
