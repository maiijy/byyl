# -*- coding: utf-8 -*-
from stateMachine  import stateMachine
import re
f = open("test.txt","r")
lines = f.readlines()#读取全部内容
n = lines[0]  #状态值
statement = lines[1] #赋值语句长度
length = int(statement)
i=0
lens =0
len1 = 0
state = []
start = []
end = []

side = []
hand = []
terminal = []
def is_different(word):
    j = 0
    while j < lens:
        if state[j] == word:
            return 0
        j = j +1
    return 1

def is_di_side(word):
    j = 0
    while j < len1:
        if hand[j] == word:
            return 0
        j = j + 1
    return 1

while i<length:
    word = re.split('-|-|\n',lines[i+2])
    start.append(word[0])
    end.append(word[1])
    side.append(word[2])
    if is_different(word[0]) == 1:
        state.append(word[0])
        lens = lens + 1
    if is_different(word[1]) == 1:
        state.append(word[1])
        lens = lens + 1
    if is_di_side(word[2]) == 1:
        hand.append(word[2])
        len1 = len1 + 1
    i=i+1

terminal.append(lines[2+length])
if __name__ == "__main__":
    new = stateMachine()
    j=0
    while j<lens:
        new.add_state(state[j])
        j = j +1

    new.add_end(terminal[0])
    j=0
    while j<i:
        new.add_hander(start[j],side[j],end[j])
        j = j+1

    j=0
    while j<len1:
        new.add_side(hand[j])
        j = j + 1

    new.NFA()
    new.miniDFA()
    new.show_hander()
    res = new.is_dfa()
    if(res == -1):
        print "不符合dfa"
    elif(res == True):
        print  "符合dfa"

