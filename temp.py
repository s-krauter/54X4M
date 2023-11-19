import pickle

#todoDatas = {}

with open("todoDatas.pkl", 'rb') as fp:
    todoDatas = pickle.load(fp)
    
print(todoDatas)