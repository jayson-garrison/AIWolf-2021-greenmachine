# cb is constructed according to regulations on http://aiwolf.org/control-panel/wp-content/uploads/2019/05/protocol_3_6.pdf
# edited by Jayson C. Garrison

# 2.1 should be good
def estimate(subject, target, role):
    return 'Agent' + str(subject) + ' ESTIMATE Agent' + str(target) + ' ' + role


def comingout(subject, target, role):
    if subject == '':
        return 'COMINGOUT Agent' + str(target) + ' ' + role
    else:
        return 'Agent' + str(subject) + ' COMINGOUT Agent' + str(target) + ' ' + role

# 2.2 should be good, the "I will do action"
def divinization(subject, target):
    return 'Agent' + str(subject) + ' DIVINIZATION Agent' + str(target) + ''
    
def guard(subject, target):
    if subject == '':
        return 'GUARD Agent' + str(target) + ''
    else:
        return 'Agent' + str(subject) + ' GUARD Agent' + str(target) + ''
    
def vote(subject, target):
    if subject == '':
        return 'VOTE Agent' + str(target) + ''
    else: 
        return 'Agent' + str(subject) + ' VOTE Agent' + str(target) + ''

def attack(subject, target):
    if subject == '':
        return 'ATTACK Agent' + str(target) + ''
    else:
        return 'Agent' + str(subject) + ' ATTACK Agent' + str(target) + ''

# 2.3 should be good
def divined(subject, target, species):
    if subject == '':
        return 'DIVINED Agent' + str(target) + ' ' + species
    else:
        return 'Agent' + str(subject) + ' DIVINED Agent' + str(target) + ' ' + species

def identified(subject, target, species):
    if subject == '':
        return 'IDENTIFIED Agent' + str(target) + ' ' + species
    else:
        return 'Agent' + str(subject) + ' IDENTIFIED Agent' + str(target) + ' ' + species

def guarded(subject, target):
    return 'Agent' + str(subject) + ' GUARDED Agent' + str(target) + ''

# 2.4 Needs work ,  talktype + ' day' + str(day) + ' ID:' + str(id)
def agree(subject, talknumber):
    return 'Agent' + str(subject) + ' AGREE ' + str(talknumber)

def disagree(subject, talknumber):
    return 'Agent' + str(subject) + ' DISAGREE ' + str(talknumber)

# 2.5 fine
def skip():
    return 'SKIP'

def over():
    return 'OVER'

# 3 should be good
def request(subject, target, sentence):
    return 'Agent' + str(subject) + ' REQUEST Agent' + str(target) + ' ' + sentence


# \/ NEW PROTOCOLS CODE BELOW \/ # All should be ok

def voted(subject, target): # should be good
    return 'Agent' + str(subject) + ' VOTED Agent' + str(target) + ''

def attacked(subject, target): # should be good
    return 'Agent' + str(subject) + ' ATTACKED Agent' + str(target) + ''

def inquire(subject, target, sentence): # should be good
    return 'Agent' + str(subject) + ' INQUIRE Agent' + str(target) + '' + '(' + sentence + ') '

def because(subject, sentence1, sentence2): # should be good
    return 'Agent' + str(subject) + ' BECAUSE ' + '(' + sentence1 + ') ' '(' + sentence2 + ') '

def logicaland(subject, sentences):
    # where sentences is a list of sentences such that:
    # X states A and B and C and... where A, B, C,... are sentences
    # and X is the agent
    andStr = 'Agent' + str(subject) + ' AND '
    for element in sentences:
        andStr = andStr + '(' + element + ') '
    return andStr
def logicalor(subject, sentences):
    # same property as logicaland
    orStr = 'Agent' + str(subject) + ' OR '
    for element in sentences:
        andStr = andStr + '(' + element + ') '
    return orStr
def logicalxor(subject, sentence1, sentence2):
    return 'Agent' + str(subject) + ' XOR ' + '(' + sentence1 + ') ' '(' + sentence2 + ') '

def logicalnot(subject, sentence):
    return 'Agent' + str(subject) + ' NOT ' + '(' + sentence + ') '

def day(subject, daynumber, sentence):
    return 'Agent' + str(subject) + ' DAY ' + str(daynumber) + '(' + sentence + ') '

def test():
    return "HIIIII"




