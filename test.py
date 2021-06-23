'''
import AIWolfPyGiven.aiwolfpy
print("Hello")
print("Hello1.5")
print("Hello2")
print("Hello3")
print("Hello4")
print("Hello end")

sent = ['s', '1', 'de']

def nd(target, sentences):
    retS = 'Test ' + target
    for elm in sentences:
        retS = retS + elm + ' '
    return retS

print( nd('Billy ', sent ) )

x = 25
print("testSTR" + str(x) )

list = [0]

print(list)
list.append([5,3])
print(list)
'''
import random

g = [
[1,2,3,4]

]

#print(g)


COs = {
    "1":[5,6,7,8] ,
    "2":[7,8,3,5,2] ,
    "3": [4,0,4,7,3]
}

for x in COs:
    print(COs[x])


if 0 in COs:
    print('hh')

'''
str = 'bruh'

if 'uh' in str:
    print('g')

l = "{0:02d}".format(9)

print(l)


s = 'hello'
print(s[0:2])
'''
print(random.randint(0,1))