###                               TO DO                         ###
### Iteration not behaving properly, values dont sum up to one. ###

import os
import random
import re
import sys

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
    list_pages = []
    for key in corpus:
        list_pages.append(key)

    number_pages = len(list_pages)

    dict_transition = {}
    for key in corpus:
        if key == page:
            number_links = len(corpus[key])
            if number_links == 0:
                for p in list_pages:
                    dict_transition[p] = 1 / number_pages
                
                return dict_transition
            
            else:
                for linked_page in corpus[key]:
                    dict_transition[linked_page] = damping_factor / number_links + (1 - damping_factor) / number_pages

                for p in list_pages:
                    if not p in dict_transition:
                        dict_transition[p] = round((1 - damping_factor) / number_pages, 4) # evtl. round wieder entfernen...

                return dict_transition

    # raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # list with all pages in the corpus
    list_pages = []
    for key in corpus:
        list_pages.append(key)

    dict_count_pages = {}
    
    for page in list_pages:
        dict_count_pages[page] = 0

    current_page = random.choice(list_pages)
    current_n = 0

    while current_n < n:

        dict_count_pages[current_page] += 1
        prob_distribution = transition_model(corpus, current_page, damping_factor)
        
        pages = []
        probs = []
        for key in prob_distribution:
            pages.append(key)
            probs.append(prob_distribution[key])

        new_page = random.choices(pages, probs) #random choice from pages with weighting probs
        
        current_page = new_page[0]
        current_n += 1
    
    dict_pagerank = {}

    for key in dict_count_pages:
        dict_pagerank[key] = dict_count_pages[key] / n

    return dict_pagerank

    # raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    print(f"Corpus: {corpus}")

    list_pages = []
    for key in corpus:
        list_pages.append(key)
    print(f"pages in corpus = {list_pages}")
    
    N = len(list_pages)
    print(f"N (total number of pages in corpus) = {N}")

    dict_pagerank = {} # PR(p)
    for page in list_pages:
        dict_pagerank[page] = 1 / N # start values

    # check for pages with no links to other pages
    for key in corpus:
        if len(corpus[key]) == 0:
            for page in list_pages:
                corpus[key].add(page)
    print(f"new corpus: {corpus}")

    # dictionary with pages i (values) linking to page p (key)
    dict_links = {}
    for page in list_pages:
        dict_links[page] = []

    for page in list_pages:
        for key in corpus:
            if page in corpus[key]: # and not page == key:
                dict_links[page].append(key)
    print(f"dictionary with pages i (values) linking to page p (key): {dict_links}")

    dict_residual = {} # dict mapping the change of pr_p with each iteration
    dict_pagerank_new = {} # dict mapping the updated/new pagerank after iteration
    condition = False
    counter = 0
    while condition == False:
        for page_p in list_pages:
            s = 0 # sum of pr_i/num_links_i

            # if no page links to page_p, treat it as if every page links to it!?!
            if len(dict_links[page_p]) == 0:
                pr_page = 1/ N
            else:
                for page_i in dict_links[page_p]:
                    pr_i = dict_pagerank[page_i]
                    num_links_i = len(corpus[page_i])
                    s += (pr_i / num_links_i)

                pr_page = (1 - damping_factor) / N + damping_factor * s
            
            current_pr = dict_pagerank[page_p]
            delta = abs(current_pr - pr_page)
            dict_residual[page_p] = delta

            dict_pagerank_new[page_p] = pr_page # store new pagerank for page p
            print(f"count: {counter} - new page ranks: {dict_pagerank_new}")
        
        counter += 1
        print(f"Counter: {counter} - residuals: {dict_residual}")
        # check if converged
        for key in dict_residual:
            if dict_residual[key] <= 0.001:
                condition = True
            else: 
                condition = False
                break
        
        # update dict_pagerank for next iteration
        for page in list_pages:
            dict_pagerank[page] = dict_pagerank_new[page]
    
    return dict_pagerank

    # raise NotImplementedError


if __name__ == "__main__":
    main()
