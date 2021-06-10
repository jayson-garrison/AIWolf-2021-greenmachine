# cb is constructed according to regulations on http://aiwolf.org/control-panel/wp-content/uploads/2019/05/protocol_3_6.pdf

# 2.1
def estimate(subject, target, role):
    return 'ESTIMATE Agent[' + "{0:02d}".format(target) + '] ' + role

def comingout(subject, target, role):
    return 'COMINGOUT Agent[' + "{0:02d}".format(target) + '] ' + role

# 2.2
def divine(target):
    return 'DIVINE Agent[' + "{0:02d}".format(target) + ']'
    
def guard(subject, target):
    return 'GUARD Agent[' + "{0:02d}".format(target) + ']'
    
def vote(subject, target):
    return 'VOTE Agent[' + "{0:02d}".format(target) + ']'

def attack(subject, target):
    return 'ATTACK Agent[' + "{0:02d}".format(target) + ']'

# 2.3
def divined(subject, target, species):
    return 'DIVINED Agent[' + "{0:02d}".format(target) + '] ' + species

def identified(subject, target, species):
    return 'IDENTIFIED Agent[' + "{0:02d}".format(target) + '] ' + species

def guarded(subject, target):
    return 'GUARDED Agent[' + "{0:02d}".format(target) + ']'

# 2.4
def agree(subject, talknumber):
    return 'AGREE '+ talktype + ' day' + str(day) + ' ID:' + str(id)

def disagree(subject, talknumber):
    return 'DISAGREE '+ talktype + ' day' + str(day) + ' ID:' + str(id)

# 2.5
def skip():
    return 'SKIP'

def over():
    return 'OVER'

# 3
def request(subject, target, sentence):
    return 'REQUEST(' + text + ''


# \/ NEW PROTOCOLS CODE BELOW \/

def voted(subject, target):

def attacked(subject, target):

def inquire(subject, target, sentence):

def because(subject, sentence1, sentence2):

def logicaland(subject, sentences):
    # where sentences is a list of sentences such that:
    # X states A and B and C and... where A, B, C,... are sentences
    # and X is the agent
def logicalor(subject, sentences):
    # same property as logicaland
def logicalxor(subject, sentence1, sentence2):

def logicalnot(subject, sentence):

def day(subject, daynumber, sentence):




