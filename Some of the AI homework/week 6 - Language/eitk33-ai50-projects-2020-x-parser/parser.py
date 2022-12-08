import nltk
import sys

#EK
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
#EK
NONTERMINALS = """
S -> NP VP | NP
AdvP -> Adv | Adv VP | Adv NP 
PP -> P | P NP | P VP | NP PP
ConjP -> Conj | Conj NP | Conj VP 
AdjP -> Adj | Adj AdjP
NP -> Nom | Det Nom | PP NP | Nom NP | AdjP NP | NP ConjP | NP AdvP 
Nom -> AdjP N | N
VP -> V | V NP | V PP NP | VP AdvP | VP ConjP | VP NP VP | VP AdjP
"""
#EK
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
    # EK
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tor = [word.lower()
           for word in
           nltk.word_tokenize(sentence)
           if word.isalpha()]
    return tor


def np_chunk(tree):
    # EK
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    tor = []
    for item in tree:
        if type(item) != str:
            a = [ite for ite in item.subtrees(filter=lambda t: t.label() == "NP")]
            if len(a) > 1:
                tor.extend(np_chunk(item))
            elif len(a) == 1:
                tor.append(*a)
    return tor


if __name__ == "__main__":
    main()
