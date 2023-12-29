""" from pagerank import transition_model

corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
page = "1.html"
damping_factor = 0.85

print(transition_model(corpus,page,damping_factor))
"""
empty_Set = set()

if len(empty_Set) == 0:
    print("True")