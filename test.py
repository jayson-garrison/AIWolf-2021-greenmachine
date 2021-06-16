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
