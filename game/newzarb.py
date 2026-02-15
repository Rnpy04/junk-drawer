import random
import time

players = {}

def generate_question(level):
    if level == 1:
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        op = random.choice(["+", "-"])
    elif level == 2:
        a = random.randint(10, 50)
        b = random.randint(1, 20)
        op = random.choice(["+", "-", "*"])
    else:
        a = random.randint(20, 100)
        b = random.randint(2, 20)
        op = random.choice(["+", "-", "*", "/"])

    if op == "/":
        a = a * b
        correct = a // b
        q = f"{a} / {b} = "
    elif op == "*":
        correct = a * b
        q = f"{a} * {b} = "
    elif op == "+":
        correct = a + b
        q = f"{a} + {b} = "
    else:
        correct = a - b
        q = f"{a} - {b} = "

    return q, correct


print("==== Math IQ Game ====")
play = int(input("play(0/1): "))

while play:
    name = input("Name: ")

    if name not in players:
        players[name] = {"score": 0}

    level = int(input("Level (1-Easy, 2-Medium, 3-Hard): "))
    score = 0
    questions = 5
    time_limit = 5

    for i in range(questions):
        q, correct = generate_question(level)

        start = time.time()
        ans = input(q)
        end = time.time()

        if end - start > time_limit:
            print("Too Slow!")
            print("Answer:", correct)
            continue

        try:
            if int(ans) == correct:
                print("Correct!")
                score += 2 * level
            else:
                print("Wrong!")
                print("Answer:", correct)
        except:
            print("Invalid input")
            print("Answer:", correct)

    players[name]["score"] += score

    print("Round Score:", score)
    print("Total Score:", players[name]["score"])

    play = int(input("play(0/1): "))

print("\n=== Final Scores ===")
for n, data in players.items():
    print(n, "=>", data["score"])
