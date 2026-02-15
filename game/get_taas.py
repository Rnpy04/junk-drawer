import pickle

def get_tas():
    with open("mosabeghe.taas","rb") as data_file:
        data=pickle.load(data_file)
    for taas in data:
        yield taas
#yield yeki yeki mide age hamasho midadi taraf mi toonest kole taas haro bbine 
        
    