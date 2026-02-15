import random
import time
import os

players = {}

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def math_question(level):
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


def pattern_question():
    pattern_type = random.choice(["add", "mul", "mix"])

    if pattern_type == "add":
        start = random.randint(1, 20)
        step = random.randint(2, 10)
        seq = [start + i * step for i in range(5)]
        ans = seq[-1] + step

    elif pattern_type == "mul":
        start = random.randint(1, 10)
        step = random.randint(2, 5)
        seq = [start * (step ** i) for i in range(5)]
        ans = seq[-1] * step

    else:
        start = random.randint(2, 10)
        m = random.randint(2, 4)
        a = random.randint(1, 5)
        seq = [start]
        for i in range(4):
            if i % 2 == 0:
                seq.append(seq[-1] * m)
            else:
                seq.append(seq[-1] + a)

        if 4 % 2 == 0:
            ans = seq[-1] * m
        else:
            ans = seq[-1] + a

    return seq, ans


def missing_equation():
    a = random.randint(2, 20)
    b = random.randint(2, 20)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        result = a + b
    elif op == "-":
        result = a - b
    else:
        result = a * b

    position = random.choice(["a", "b"])

    if position == "a":
        q = f"? {op} {b} = {result}"
        ans = a
    else:
        q = f"{a} {op} ? = {result}"
        ans = b

    return q, ans


def compare_question():
    a1 = random.randint(10, 100)
    b1 = random.randint(2, 20)
    a2 = random.randint(10, 100)
    b2 = random.randint(2, 20)

    expr1 = a1 * b1
    expr2 = a2 + b2

    q = f"1) {a1} * {b1}\n2) {a2} + {b2}\nWhich is bigger? (1/2/equal): "

    if expr1 > expr2:
        ans = "1"
    elif expr2 > expr1:
        ans = "2"
    else:
        ans = "equal"

    return q, ans


def memory_question():
    numbers = [random.randint(10, 99) for _ in range(5)]
    print("Memorize:", numbers)
    time.sleep(20)
    clear()
    user = input("Enter numbers separated by space: ")
    user_list = user.split()
    return numbers, user_list


def iq_round(name, level):
    score = 0
    time_limit = max(3, 38 - level)

    for i in range(15):
        game_type = random.choice(
            ["math", "pattern", "missing", "compare", "memory"]
        )

        start = time.time()

        if game_type == "math":
            q, ans = math_question(level)
            user = input(q)

        elif game_type == "pattern":
            seq, ans = pattern_question()
            print("Pattern:", seq, "?")
            user = input("Next: ")

        elif game_type == "missing":
            q, ans = missing_equation()
            user = input(q + " ")

        elif game_type == "compare":
            q, ans = compare_question()
            user = input(q)

        else:
            correct, user = memory_question()
            if user == list(map(str, correct)):
                print("Correct!")
                score += 3
            else:
                print("Wrong!", correct)
            continue

        end = time.time()

        if end - start > time_limit:
            print("Too slow!")
            print("Answer:", ans)
            continue

        try:
            if str(user) == str(ans):
                print("Correct!")
                score += 2 * level
            else:
                print("Wrong!")
                print("Answer:", ans)
        except:
            print("Invalid")
            print("Answer:", ans)

    players[name]["score"] += score
    return score


print("==== ULTIMATE IQ TRAINER ====")
play = int(input("play(0/1): "))

while play:
    name = input("Name: ")

    if name not in players:
        players[name] = {"score": 0}

    level = int(input("Level (1-3): "))
    clear()
    round_score = iq_round(name, level)

    print("\nRound Score:", round_score)
    print("Total Score:", players[name]["score"])

    play = int(input("play(0/1): "))

print("\n=== FINAL RANKING ===")
for n, d in players.items():
    print(n, "=>", d["score"])
