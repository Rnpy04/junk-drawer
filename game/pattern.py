import random

players = {}

def generate_pattern():
    pattern_type = random.choice(["add", "mul", "mix"])
    
    if pattern_type == "add":
        start = random.randint(1, 20)
        step = random.randint(2, 10)
        seq = [start + i * step for i in range(5)]
        answer = seq[-1] + step

    elif pattern_type == "mul":
        start = random.randint(1, 10)
        step = random.randint(2, 5)
        seq = [start * (step ** i) for i in range(5)]
        answer = seq[-1] * step

    else:
        start = random.randint(2, 10)
        step1 = random.randint(2, 5)
        step2 = random.randint(1, 5)
        seq = [start]
        for i in range(4):
            if i % 2 == 0:
                seq.append(seq[-1] * step1)
            else:
                seq.append(seq[-1] + step2)
        if 4 % 2 == 0:
            answer = seq[-1] * step1
        else:
            answer = seq[-1] + step2

    return seq, answer


print("=== Number Pattern IQ Game ===")
play = int(input("play(0/1): "))

while play:
    name = input("Name: ")

    if name not in players:
        players[name] = {"score": 0}

    score = 0
    questions = 20

    for i in range(questions):
        seq, correct = generate_pattern()
        print("\nPattern:", seq, "?")
        user = input("Next number: ")

        try:
            if int(user) == correct:
                print("Correct!")
                score += 1
            else:
                print("Wrong!")
                print("Answer:", correct)
        except:
            print("Invalid input")
            print("Answer:", correct)

    players[name]["score"] += score

    print("\nRound Score:", score)
    print("Total Score:", players[name]["score"])

    play = int(input("play(0/1): "))

print("\n=== Final Scores ===")
for n, data in players.items():
    print(n, "=>", data["score"])
