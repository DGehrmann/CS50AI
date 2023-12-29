import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    zero_gene = set()
    for person in people:
        if not person in one_gene and not person in two_genes:
            zero_gene.add(person)

    # persons with no known parents
    no_parents = []
    # persons with knwon parents
    has_parents = []
    for person in people:
        if people[person]["mother"] == None and people[person]["father"] == None:
            no_parents.append(person)
        else:
            has_parents.append(person)
    
    probs_zero_genes = []
    probs_one_gene = []
    probs_two_genes = []
    # calculate probs for persons without known parents
    for person in no_parents:
        # calculate probs for persons with zero genes
        if person in zero_gene:
            # persons with zero genes and no trait
            if not person in have_trait:
                prob = PROBS["gene"][0] * PROBS["trait"][0][False]
            # person with zero genes and has trait
            else:
                prob = PROBS["gene"][0] * PROBS["trait"][0][True]
            
            probs_zero_genes.append(prob)

        # calculate probs for persons with one gene:
        elif person in one_gene:
            # person with one gene and no trait
            if not person in have_trait:
                prob = PROBS["gene"][1] * PROBS["trait"][1][False]
            # person with one gene and has trait
            else:
                prob = PROBS["gene"][1] * PROBS["trait"][1][True]
        
            probs_one_gene.append(prob)
        
        # calculate probs for persons with two genes
        else:
            # person with two genes and no trait
            if not person in have_trait:
                prob = PROBS["gene"][2] * PROBS["trait"][2][False]
            # person with two genes and has trait
            else:
                prob = PROBS["gene"][2] * PROBS["trait"][2][True]

            probs_two_genes.append(prob)

    #probs_genes_noParents = sum(probs_zero_genes) + sum(probs_one_gene) + sum(probs_two_genes)
    probs_genes_noParents = probs_zero_genes + probs_one_gene + probs_two_genes
    # print(probs_genes_noParents)

    # calculate probs for persons with parents
    probs_parents = [1-PROBS["mutation"], 0.5, PROBS["mutation"]] # 0.99, 0.5, 0.01

    probs_genes_hasParents = []

    for person in has_parents:

        if people[person]["mother"] in zero_gene:
            mother = 0
        elif people[person]["mother"] in one_gene:
            mother = 1
        else:
            mother = 2
        
        if people[person]["father"] in zero_gene:
            father = 0
        elif people[person]["father"] in one_gene:
            father = 1
        else:
            father = 2
        
        # person with no gene
        if person in zero_gene:

            child = 0

            prob_gene = probs_parents[mother] * probs_parents[father]

            """
            ### both parents do not have the gene
            if people[person]["mother"] in zero_gene and people[person]["father"] in zero_gene:
                prob_gene = (probs_parents[0])**2
            # father has one gene, mother none OR mother has one gene, father none
            elif people[person]["mother"] in zero_gene and people[person]["father"] in one_gene:
                prob_gene = (1 - PROBS["mutation"]) * 0.5
            # father has two genes, mother none
            elif people[person]["mother"] in zero_gene and people[person]["father"] in two_genes:
                prob_gene = (1 - PROBS["mutation"]) * PROBS["mutation"]
            ### father has one gene, mother one
            elif people[person]["mother"] in one_gene and people[person]["father"] in one_gene:
                prob_gene = 0.5 * 0.5
            # father has two genes, mother one
            elif people[person]["mother"] in one_gene and people[person]["father"] in two_genes:
                prob_gene = 0.5 * PROBS["mutation"]
            ### both have two genes
            else:
                prob_gene = (PROBS["mutation"])**2
            """
        
        # person with one gene
        elif person in one_gene:    # 0: 0.99; 1: 0.5; 2: 0.01
            child = 1
            
            if mother == 0 and father == 0:
                prob_gene = probs_parents[2] * probs_parents[0] + probs_parents[0] * probs_parents[2]
            elif (mother == 0 and father == 1) or (father == 0 and mother == 1):
                prob_gene = probs_parents[2] * probs_parents[1] + probs_parents[1] * probs_parents[0]
            elif mother == 0 and father == 2 or (father == 0 and mother == 2):
                prob_gene = probs_parents[2] * probs_parents[2] + probs_parents[0] * probs_parents[0]
            elif mother == 1 and father == 1:
                prob_gene = probs_parents[1] * probs_parents[1] + probs_parents[1] * probs_parents[1]
            elif (mother == 1 and father == 2) or (mother == 2 and father == 1):
                prob_gene = probs_parents[1] * probs_parents[2] + probs_parents[1] * probs_parents[0]
            else: # if mother == 2 and father == 2:
                prob_gene = probs_parents[0] * probs_parents[2] + probs_parents[2] * probs_parents[0]
        
        # person with two genes
        else:
            child = 2
            
            prob_gene = probs_parents[-(1+mother)] * probs_parents[-(1+father)]

        
        # person with no trait
        if not person in have_trait:
            prob = prob_gene * PROBS["trait"][child][False]
        else:
            prob = prob_gene * PROBS["trait"][child][True]
            
        probs_genes_hasParents.append(prob)

    # print(f"probs_genes_hasParents: {probs_genes_hasParents}")
    probs_genes_all = probs_genes_noParents + probs_genes_hasParents
    # print(probs_genes_all)

    #joint_probs = probs_genes_noParents + sum(probs_genes_hasParents)
    # print(joint_probs)

    joint_probs = 1
    for prob in probs_genes_all:
        joint_probs *= prob
    
    return joint_probs


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        sum_genes = 0
        for i in range(3):
            sum_genes += probabilities[person]["gene"][i]

        for j in range(3):
            probabilities[person]["gene"][j] = probabilities[person]["gene"][j] / sum_genes

        sum_trait = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        probabilities[person]["trait"][True] = probabilities[person]["trait"][True] / sum_trait
        probabilities[person]["trait"][False] = probabilities[person]["trait"][False] / sum_trait


if __name__ == "__main__":
    main()
