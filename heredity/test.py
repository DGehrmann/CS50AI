from heredity import joint_probability

people = {
  'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
  'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
  'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
}

"""
one_gene = {"Harry"}
print(one_gene)
two_genes = {"James"}
print(two_genes)
zero_gene = set()
for person in people:
    print(person)
    if not person in one_gene and not person in two_genes:
        zero_gene.add(person)

print(zero_gene)

no_parents = []
for person in people:
    if people[person]["mother"] == None and people[person]["father"] == None:
        no_parents.append(person)

print(no_parents)

liste = [1,2,3]
print(liste[-(1+2)])
"""

print(joint_probability(people, {"Harry"}, {"James"}, {"James"}))