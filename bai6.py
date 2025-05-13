input_str = input("Nhap X,Y: ")
dimen = [int(x) for x in input_str.split(',')]
rowNum = dimen[0]
colNum =dimen[1]
multilist = [[0 for col in range(colNum)] for row in range(rowNum)]
for row in range(rowNum):
    for col in range(colNum):
        multilist[row][col]= row*col
print(multilist)