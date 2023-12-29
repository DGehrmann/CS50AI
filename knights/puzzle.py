from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Implication(AKnight, And(AKnight, AKnave)),     # If AKnight is true, then AKnight ^ AKnave is true because Knight always says truth
    Implication(AKnave, Not(And(AKnight, AKnave))), # If AKnave is true, then AKnight ^ AKnave is not true because Knave always lies
    Or(AKnight, AKnave)                             # Only AKnight or AKnave are true
    )

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
    Or(AKnight, AKnave),
    Or(BKnight, BKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight)))),
    Or(AKnight, AKnave),
    Or(BKnight, BKnave)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    Implication(BKnight, Implication(AKnight, AKnave)), # If B is a Knight, then if A is a Knight, A said that A is a Knave. 
    Implication(BKnight, Implication(AKnave, Not(AKnave))), # If B is a Knight, then if A is a Knave, A said not that A is a Knave.
    Implication(BKnave, Implication(AKnight, Not(AKnave))), # If B is a Knave, then if A is a Knight, A said not that A is a Knave.
    Implication(BKnave, Implication(AKnave, Not(Not(AKnave)))), # If B is a Knave, then if A is a Knave, A said not that A said not that A is a Knave. (?) :D
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
