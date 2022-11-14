import nltk
import sys
import os
import string
import math
from collections import Counter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    mil = []
    tor = dict()
    for root, dirs, files in os.walk(directory):
        if dirs:
            continue
        a, b = os.path.split(root)
        files_of_sub_dir = [os.path.join(root, name) for name in files]
    for item in files_of_sub_dir:
        with open(item, 'r', encoding='utf-8') as f:
            a, b = os.path.split(item)
            tor[b] = f.read()
    return tor


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """

    tor = [word.lower()
           for word in
           nltk.word_tokenize(document)
           if word.isalpha() and word.lower() not in nltk.corpus.stopwords.words("english")
           and word not in string.punctuation]

    return tor


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    tor = dict()
    words = ()
    for page in documents:
        word = documents[page]
        words += tuple(word)
    words = set(words)

    for word in words:
        counter = 0
        for page in documents:
            if word in documents[page]:
                counter += 1
        tor[word] = math.log(len(documents.keys())/counter)
    return tor


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tor = []
    score = {}
    for word in query:
        for file in files:
            if word in files[file]:
                res = idfs[word] * files[file].count(word)
                if file in score.keys():
                    score[file] += res
                else:
                    score[file] = res
    for item in score:
        tor.append((item, score[item]))

    tor.sort(key=lambda counts: counts[1], reverse=True)
    tor = tor[:n]
    tor = [x[0] for x in tor]
    return tor


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    tor = []
    score = {}
    ties = []
    to_fix = []

    for sentence in sentences:
        for word in query:
            if word in set(tuple(sentences[sentence])):
                res = idfs[word]
                if sentence in score.keys():
                    score[sentence] += res
                else:
                    score[sentence] = res

    for item in score:
        tor.append((item, score[item], 0))

    tor.sort(key=lambda counts: counts[1], reverse=True)

    count = Counter([x[1] for x in tor])
    for item in count.items():
        if item[1] > 1:
            ties.append(item[0])
    if ties:
        for tie in ties:
            to_fix = [x for x in tor if x[1] == tie]
            tor = list(set(tor) - set(to_fix))
            for item in to_fix:
                sec_score = 0
                for word in query:
                    if word in item[0]:
                        sec_score += 1
                tor.append((item[0], item[1], sec_score/len(item[0])))
        tor.sort(key=lambda counts: (counts[1], counts[2]), reverse=True)
    tor = [x[0] for x in tor]
    tor = tor[:n]
    return tor


if __name__ == "__main__":
    main()
