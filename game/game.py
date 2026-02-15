from get_taas import get_tas

dast=0

for taas in get_tas():
    print(taas)
    if dast >5 :
        break
    else:
        dast+=1