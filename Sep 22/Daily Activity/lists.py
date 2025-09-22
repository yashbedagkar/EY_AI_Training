# Lists
list1 = [5,10,15,20,25,30,35,40]
# accessing the lists
print(list1[0])
print(list1[-1])
list2 = []
for i in list1[::-1]:
    list2.append(i)

print(list2)

for i in list1[3::-1]:
    print (i)