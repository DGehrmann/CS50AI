set2 = {(1,2)}
set1 = {(1,2),(2,3)}
set3 = set()

if set3.issubset(set2):
    print("Is subset")
else:
    print("Is not subset")

"""
if sentence2.issubset(sentence):
    print(True)
    print(sentence-sentence2)
else:
    print(False)

cell = (1,2)

sentence2.remove(cell)
print(sentence2)
"""

"""
knowledge = [set1, set2]
knowledge_copy = knowledge.copy()
for sentence in knowledge_copy:
    print(sentence)
    for sentence2 in knowledge_copy:
        print(sentence2)
        if sentence != sentence2:
            if sentence2.issubset(sentence):
                new_set = sentence - sentence2
                #new_count = sentence.count - sentence2.count
                knowledge.append(new_set)
            else:
                continue
        else:
            continue

print(knowledge)
"""