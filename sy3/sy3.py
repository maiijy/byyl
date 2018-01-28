# -*- coding: utf-8 -*-
# 消除左递归,对潜在和间接使用代入法
# 提取左公因子，消除回溯问题
# 采用穷举法，得出是否符合文法
from gramMachine import gram
import re
f = open("gram.txt","r")
#f = open("gram4.txt","r")
#f = open("gram3.txt","r")
lines = f.readlines()#读取全部内容
print len(lines)
i=0
start = []
end = []
fei=[]
def is_different(arr,word):
    i=0
    while i<len(arr):
        if(arr[i]==word):
            return
        i =i+1
    arr.append(word)

while i < len(lines)-1:
    word = re.split('::|\n' , lines[i])
    start.append(word[0])
    is_different(fei,word[0])
    end.append(word[1])
    print len(word[1])
    i = i + 1

if __name__ == "__main__":
    new = gram()
    j=0
    while j<len(fei):
        new.add_terinator(fei[j])
        j = j+1
    j=0
    while j<len(start):
        new.add_rule(start[j],end[j])
        j = j+1
    new.start = lines[len(lines)-1]
    new.eliminate()
    new.main()