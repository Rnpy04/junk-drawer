import random

players = {}

print("\n______________________________+-*/_____________________________")

try:
    play=int(input("play(0/1) :"))  
except:
    print("000000 ya 11111")
    play=int(input("play(0/1) :"))  

while play:
    name = input("\n Name: ")

    if name not in players:
        players[name] = {"score": 0}

    score = 0
    tedad_soal = 5

    for i in range(tedad_soal):
        op = random.choice(["+", "-", "*", "/"])
        a = random.randint(50, 100)
        b = random.randint(50, 100)

        if op == "/":
            a = a * b  
            correct = a // b
            user_input = input(f"{a} ÷ {b} = ")
        elif op == "*":
            correct = a * b
            user_input = input(f"{a} × {b} = ")
        elif op == "+":
            correct = a + b
            user_input = input(f"{a} + {b} = ")
        else:  # "-"
            correct = a - b
            user_input = input(f"{a} - {b} = ")

        # check answer
        try:
            if int(user_input) == correct:
                print(":)))))))))!")
                score += 1
            else:
                print(f":((((((((: {correct}")
        except:
            print(f":((((((((: {correct}")

    players[name]["score"] += score

    print(f"\n🧠Score: {score}")
    print(f"all : {players[name]['score']} ")

    try:
        play=int(input("play(0/1) :"))  
    except:
        print("000000 ya 11111")
        play=int(input("play(0/1) :"))  



print("\n================================================================")
for n, data in players.items():
    print(f"{n} ➤ Score: {data['score']}")
