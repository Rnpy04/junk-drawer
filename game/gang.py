import random

marhale = 7
di=dict()

print("_______________O-O__________________")
try:
    play=int(input("play(0/1) :"))  
except:
    print("000000 ya 11111")
    play=int(input("play(0/1) :"))  

while(play):
    name=input("\n name :")
    if name not in di:
        di[name] = {"win": 0, "kelid": 0}
    joon = 3
    kelid = 0
    for i in range(1, marhale + 1):
        print(f"\nMarhale {i} | Joon: {joon} | Kelid: {kelid}")
        doors =["daam", "khaali", "kelid", "majoon","jayze"]
        random.shuffle(doors)

        
        entekhab = input("Dar 1, 2 , 3 ,4 ,5: ")
        if entekhab not in ["1","2","3","4","5"]:
            print("naaaa 1 , 2 , 3 ,4 ,5 !")
            entekhab = input("Dar 1, 2 , 3 ,4 ,5: ")

        natije = doors[int(entekhab) - 1]

        if natije == "daam":
            joon -= 1
            print("Daam! :(")
        elif natije == "kelid":
            kelid += 1
            print("Kelid gerefti :)")
        elif natije == "jayze":
            kelid += 2
            joon+=1
            print("jayzeeee :}")
        elif natije == "majoon":
            joon += 1
            print("Majoon! :]")
        else:
            print("Khaali :|")

        if joon == 0:
            print("Joonat tamoom shod:((((((((((((")
            break
        if kelid == 3:
            print("kelid ha peyda shod :))))))))))!")
            di[name]["win"] += 1
            break

    if joon > 0 and kelid < 3:
        print(f"payan .Kelid: {kelid} :|||||||||||")
        di[name]["kelid"] += kelid
    print(f"\n{name}:\n  Bord: {di[name]['win']}, Kelid ha: {di[name]['kelid']}\n")
    try:
        play=int(input("play(0/1) :"))  
    except:
        print("000000 ya 11111")
        play=int(input("play(0/1) :"))  


print("\n________________________+_+______________________________")
for n, stats in di.items():
    print(f"{n} -> Bord: {stats['win']} | Kelid: {stats['kelid']}")