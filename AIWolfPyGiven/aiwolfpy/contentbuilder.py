# cb is constructed according to regulations on http://aiwolf.org/control-panel/wp-content/uploads/2019/05/protocol_3_6.pdf
# edited by Jayson C. Garrison

# 2.1 should be good
def estimate(subject, target, role):
    return 'Agent[' + "{0:02d}".format(subject) + '] ESTIMATE Agent[' + "{0:02d}".format(target) + '] ' + role

def comingout(subject, target, role):
    return 'Agent[' + "{0:02d}".format(subject) + '] COMINGOUT Agent[' + "{0:02d}".format(target) + '] ' + role

# 2.2 should be good, the "I will do [action]"
def divinization(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] DIVINIZATION Agent[' + "{0:02d}".format(target) + ']'
    
def guard(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] GUARD Agent[' + "{0:02d}".format(target) + ']'
    
def vote(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] VOTE Agent[' + "{0:02d}".format(target) + ']'

def attack(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] ATTACK Agent[' + "{0:02d}".format(target) + ']'

# 2.3 should be good
def divined(subject, target, species):
    return 'Agent[' + "{0:02d}".format(subject) + '] DIVINED Agent[' + "{0:02d}".format(target) + '] ' + species

def identified(subject, target, species):
    return 'Agent[' + "{0:02d}".format(subject) + '] IDENTIFIED Agent[' + "{0:02d}".format(target) + '] ' + species

def guarded(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] GUARDED Agent[' + "{0:02d}".format(target) + ']'

# 2.4 Needs work ,  talktype + ' day' + str(day) + ' ID:' + str(id)
def agree(subject, talknumber):
    return 'Agent[' + "{0:02d}".format(subject) + '] AGREE ' + str(talknumber)

def disagree(subject, talknumber):
    return 'Agent[' + "{0:02d}".format(subject) + '] DISAGREE ' + str(talknumber)

# 2.5 fine
def skip():
    return 'SKIP'

def over():
    return 'OVER'

# 3 should be good
def request(subject, target, sentence):
    return 'Agent[' + "{0:02d}".format(subject) + '] REQUEST Agent[' + "{0:02d}".format(target) + '] ' + sentence


# \/ NEW PROTOCOLS CODE BELOW \/ # All should be ok

def voted(subject, target): # should be good
    return 'Agent[' + "{0:02d}".format(subject) + '] VOTED Agent[' + "{0:02d}".format(target) + ']'

def attacked(subject, target): # should be good
    return 'Agent[' + "{0:02d}".format(subject) + '] ATTACKED Agent[' + "{0:02d}".format(target) + ']'

def inquire(subject, target, sentence): # should be good
    return 'Agent[' + "{0:02d}".format(subject) + '] INQUIRE Agent[' + "{0:02d}".format(target) + ']' + '(' + sentence + ') '

def because(subject, sentence1, sentence2): # should be good
    return 'Agent[' + "{0:02d}".format(subject) + '] BECAUSE ' + '(' + sentence1 + ') ' '(' + sentence2 + ') '

def logicaland(subject, sentences):
    # where sentences is a list of sentences such that:
    # X states A and B and C and... where A, B, C,... are sentences
    # and X is the agent
    andStr = 'Agent[' + "{0:02d}".format(subject) + '] AND '
    for element in sentences:
        andStr = andStr + '(' + element + ') '
    return andStr
def logicalor(subject, sentences):
    # same property as logicaland
    orStr = 'Agent[' + "{0:02d}".format(subject) + '] OR '
    for element in sentences:
        andStr = andStr + '(' + element + ') '
    return orStr
def logicalxor(subject, sentence1, sentence2):
    return 'Agent[' + "{0:02d}".format(subject) + '] XOR ' + '(' + sentence1 + ') ' '(' + sentence2 + ') '

def logicalnot(subject, sentence):
    return 'Agent[' + "{0:02d}".format(subject) + '] NOT ' + '(' + sentence + ') '

def day(subject, daynumber, sentence):
    return 'Agent[' + "{0:02d}".format(subject) + '] DAY ' + str(daynumber) + '(' + sentence + ') '

def test():
    print("HIIIII")




