import random 

def get_best(best_count,best_person,count,name):
    if count<=best_count:
        best_person=name
        best_count=count
    return best_person,best_count

print("welcome to the game!")
again=1
best_count=99999999999999999
gamers={}
best_person="no one"
while(again==1):
    name=input("enter your name : ")
    gamers[name]=0
    ans=random.randint(1,10)
    win = False
    count=0
    while (not win):
        guess=int(input("your num :"))
        count+=1
        if(ans==guess):
            win=True
        elif(guess< ans):
            print("no greater")
        else :
            print("no smaller")
    gamers[name]=count
    print("you won !!!!!")
    best_person,best_count=get_best(best_count,best_person,count,name)
    print(f"until now winer is {best_person} with guess num = {best_count}")
    again=int(input("wanna play again (1/0) :"))
print("game ended.")
    
    