import pickle



index = 428
file = open('cuyoo_index.txt','wb')
pickle.dump(index, file)
file.close()

file1 = open(r'cuyoo_index.txt')
print pickle.load(file1)
file1.close()