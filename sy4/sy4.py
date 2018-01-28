# -*- coding: utf-8 -*-
# 先写出每个推导的FIRST和FOLLOW集
#根据是否有#推导结构，构建每个推导的SELECT集
# 根据select集的交集关系判断是否符合LL1文法
# 用栈记录输入的字符串进行匹配
from LL1Machine import gram
import re
f = open("E:/study/byyl/youxian/sy4/gram.txt","r")

lines = f.readlines()#读取全部内容
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
    word = re.split('-|\n' , lines[i])
    start.append(word[0])
    is_different(fei,word[0])
    end.append(word[1])
    i = i + 1

if __name__ == "__main__":
    new = gram()
    j=0
    while j<len(fei):
        new.add_non(fei[j])
        j = j+1
    j=0
    while j<len(start):
        new.add_rule(start[j],end[j])
        j = j+1
    new.start = lines[len(lines)-1]
    new.main()
