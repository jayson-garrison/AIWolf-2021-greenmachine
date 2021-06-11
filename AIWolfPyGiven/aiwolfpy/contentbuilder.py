# cb is constructed according to regulations on http://aiwolf.org/control-panel/wp-content/uploads/2019/05/protocol_3_6.pdf

# 2.1 should be good
def estimate(subject, target, role):
    return 'Agent[' + "{0:02d}".format(subject) + '] ESTIMATE Agent[' + "{0:02d}".format(target) + '] ' + role

def comingout(subject, target, role):
    return 'Agent[' + "{0:02d}".format(subject) + '] COMINGOUT Agent[' + "{0:02d}".format(target) + '] ' + role

# 2.2
def divinization(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] DIVINIZATION Agent[' + "{0:02d}".format(target) + ']'
    
def guard(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] GUARD Agent[' + "{0:02d}".format(target) + ']'
    
def vote(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] VOTE Agent[' + "{0:02d}".format(target) + ']'

def attack(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] ATTACK Agent[' + "{0:02d}".format(target) + ']'

# 2.3 needs work
def divined(subject, target, species):
    return 'Agent[' + "{0:02d}".format(subject) + '] DIVINED Agent[' + "{0:02d}".format(target) + '] ' + species

def identified(subject, target, species):
    return 'Agent[' + "{0:02d}".format(subject) + '] IDENTIFIED Agent[' + "{0:02d}".format(target) + '] ' + species

def guarded(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] GUARDED Agent[' + "{0:02d}".format(target) + ']'

# 2.4 Needs work
def agree(subject, talknumber):
    return 'Agent[' + "{0:02d}".format(subject) + '] AGREE '+ talktype + ' day' + str(day) + ' ID:' + str(id)

def disagree(subject, talknumber):
    return 'Agent[' + "{0:02d}".format(subject) + '] DISAGREE '+ talktype + ' day' + str(day) + ' ID:' + str(id)

# 2.5 fine
def skip():
    return 'SKIP'

def over():
    return 'OVER'

# 3 needs work
def request(subject, target, sentence):
    return 'Agent[' + "{0:02d}".format(subject) + '] REQUEST(' + text + ''


# \/ NEW PROTOCOLS CODE BELOW \/

def voted(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] '

def attacked(subject, target):
    return 'Agent[' + "{0:02d}".format(subject) + '] '

def inquire(subject, target, sentence):
    return 'Agent[' + "{0:02d}".format(subject) + '] '

def because(subject, sentence1, sentence2):
    return 'Agent[' + "{0:02d}".format(subject) + '] '

def logicaland(subject, sentences):
    # where sentences is a list of sentences such that:
    # X states A and B and C and... where A, B, C,... are sentences
    # and X is the agent
    return 'Agent[' + "{0:02d}".format(subject) + '] '
def logicalor(subject, sentences):
    # same property as logicaland
    return 'Agent[' + "{0:02d}".format(subject) + '] '
def logicalxor(subject, sentence1, sentence2):
    return 'Agent[' + "{0:02d}".format(subject) + '] '

def logicalnot(subject, sentence):
    return 'Agent[' + "{0:02d}".format(subject) + '] '

def day(subject, daynumber, sentence):
    return 'Agent[' + "{0:02d}".format(subject) + '] '




