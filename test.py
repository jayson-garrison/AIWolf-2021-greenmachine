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

g = [
[1,2,3,4],
[7,3,2]
]

if [7,3,2] in g:
    print('passed')

#print(g)


COs = {
    "1":[5,6,7,8] ,
    "2":[7,8,3,5,2] ,
    "3": [4,0,4,7,3]
}


'''
str = 'bruh'

if 'uh' in str:
    print('g')

l = "{0:02d}".format(9)

print(l)


s = 'hello'
print(s[0:2])
'''