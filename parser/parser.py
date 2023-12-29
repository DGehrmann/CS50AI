import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
import sys
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP
NP -> N | Det N | Det AdjP | AdvP Det | AdjP NP | N PP | Det N AdvP
PP -> P NP 
VP -> V | V NP | AdvP NP | VP NP PP | VP PP | V Adv
AdjP -> Adj | AdjP NP | Adj AdjP
AdvP -> Adv | Adv VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    lst_words = word_tokenize(sentence)

    lst_words_lower = []
    for word in lst_words:
        word = word.lower()
        lst_words_lower.append(word)
    
    for word in lst_words_lower:
        regex = re.search(r"^.*[a-z]+.*", word)
        if regex == None:
            lst_words_lower.remove(word)
    
    return lst_words_lower

    # raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    """ The height of a tree
    containing no children is 1; the height of a tree
    containing only leaves is 2; and the height of any other
    tree is one plus the maximum of its children's
    heights. """
    """
    lst_NP = []
    height = tree.height() 

    if height == 1:
        if tree.label() == "NP":
            lst_NP.append(tree)
    elif height == 2:
        for leaf in tree:
            if leaf.label() == "NP":
                lst_NP.append(leaf)
    else:
        subtree = tree
        for i in range(height):
            subtree = subtree[i]
    """
    
    #print(tree.height())
    #print(len(tree))
    #print(tree[0].label())
    #print(tree[0])
    #print(len(tree[0]))
    
    lst_chunks = find_NP(tree)
    # print(lst_chunks)
    lst_chunks_copy = lst_chunks.copy()
    for subtree in lst_chunks:
        # print(f"subtree: {subtree}")
        found_NP = False
        for s in subtree.subtrees():
            # print(s)
            if s != subtree:
                if s.label() == "NP":
                    found_NP = True
        if found_NP:
            lst_chunks_copy.remove(subtree)    

    return lst_chunks_copy

    # raise NotImplementedError

def find_NP(tree):
    lst_NP = []
    for i in range(len(tree)):
        # print(i)
        # print(len(tree))
        if len(tree) != 1:
            lst_next = find_NP(tree[i])
            lst_NP += lst_next

        # print(tree[i])
        try:
            if tree[i].label() == "NP":
                lst_NP.append(tree[i])
        except AttributeError:
            continue
    return lst_NP


if __name__ == "__main__":
    main()
