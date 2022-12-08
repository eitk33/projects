import os
import random
import re
import sys
import copy
import math

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # EK
    dict_to_return = {}
    page_links = corpus[page[0]]
    oa_links = []
    for item in [x for x in corpus.values() if x]:
        for ite in item:
            oa_links.append(ite)
    oa_links = set(oa_links)

    for k in corpus:
        dict_to_return[k] = 1 / len(corpus.keys()) * 0.15
    if page_links:
        for v in page_links:
            dict_to_return[v] += 1/(len(page_links)) * 0.85
    else:
        for k in corpus.keys():
            dict_to_return[k] += 1 / len(corpus.keys())

    return dict_to_return



def sample_pagerank(corpus, damping_factor, n):
    # EK
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict_to_up = dict.fromkeys(corpus.keys(), 0)

    page = random.choices([x for x in corpus.keys()], k=1)
    tm = transition_model(corpus, page, damping_factor)

    for item in tm:
        dict_to_up[item] += tm[item]

    for i in range(n - 1):
        page = random.choices([x for x in tm.keys()], weights=[x for x in tm.values()], k=1)
        tm = transition_model(corpus, page, damping_factor)
        for item in tm:
            dict_to_up[item] += tm[item]

    dict_to_return = dict.fromkeys(corpus.keys(), 0)
    for item in dict_to_up:
        dict_to_return[item] = dict_to_up[item]/sum(dict_to_up.values())

    return dict_to_return



def iterate_pagerank(corpus, damping_factor):
    # EK
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dict_to_return = {}
    n = len(corpus.keys())
    for item in corpus.keys():
        if not corpus[item]:
            corpus[item] = corpus.keys()
        dict_to_return[item] = 1 / n

    count = 0
    sum = 1
    while True:
        dict_to_up = copy.deepcopy(dict_to_return)

        count += 1
        check = 0
        for item in dict_to_return:

            iter = 0
            for ite in corpus:
                if item in corpus[ite]:
                    iter += dict_to_return[ite] / len(corpus[ite])
            res = (1 - damping_factor)/n + iter * damping_factor

            oa_detla = abs(res - dict_to_up[item])


            if oa_detla > 0.001:
                check = 1
            dict_to_return[item] = res

        sum = math.fsum(dict_to_return.values())

        dict_to_return = {item: value / sum for (item, value) in dict_to_return.items()}

        if check == 0:
            break
    return dict_to_return


if __name__ == "__main__":
    main()
