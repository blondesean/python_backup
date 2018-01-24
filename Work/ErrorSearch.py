#All states and the number of policies that were rescored

search = 'ERROR: File WORK'
with open('C:\\Users\\u57p23\\Desktop\\brokenstates.txt') as f1:
    lines = f1.readlines()
    print("START")
    for i, line in enumerate(lines):
        if line.startswith(search):
          print(line) #also change 14 to 7

    print("END")
f1.close()

#for word in line.split():
#if word.endswith('could'):
# print(line[15:])
#print(lines[i+2])