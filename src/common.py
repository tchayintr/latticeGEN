from ahocorapy.keywordtree import KeywordTree


def init_trie_automaton(dic, case_insensitive=True):
    trie = KeywordTree(case_insensitive=case_insensitive)
    vocabs = dic.keys()
    for vocab in vocabs:
        trie.add(vocab)
    trie.finalize()
    return trie
