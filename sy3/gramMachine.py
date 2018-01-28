# -*- coding: utf-8 -*-
class gram:
    def __init__(self):
        self.terminator = []
        self.non = []
        self.rule = {}
        self.t = 0
        self.str = ['Q','W','E','R','T','Y','U']
        self.I = ''
        self.start = ''
        self.added = {}

    # 加非终结符号
    def add_terinator(self,word):
        self.non.append(word)
   # 加终结符号
    def add_non(self,word):
        self.terminator.append(word)
    # 加推导规则
    def add_rule(self,key,point):
        if self.rule.has_key(key)==False:
            self.rule[key] = []

        self.rule[key].append(point)

    # 判断是否是非终结符号
    def in_non_terinaor(self,word):
        for i in self.non:
            if i == word:
                return True
        return False
    # 消除左递归时需要改变数据结构
    def add_new_non(self,key,index,new):
        temp = ''
        tmp = []
        # 处理提取了左递归后的字符串
        for i in index:
            if i != key:
                temp= temp+i
        temp=temp +new
        if len(self.rule[str(key)]) == 1:
            tmp.append(new)
        elif len(self.rule[str(key)]) > 1:
            # 判断是否可以为空
            if '&' in self.rule[new]:
                self.rule[key].remove(index+new)
                tmp = self.rule[key]
            else:
                self.rule[new].append('&')
                #更换成新的带自创的推导式子
                for j in self.rule[str(key)]:
                    if j != index:
                        tmp.append(j+new)
        self.rule[key] = tmp
        self.rule[new].append(temp)

    # 代入流程
    def substitution(self,start,target,index):
        temp = ''
        tmp = []
        # 处理提取了左递归后的字符串
        for i in index:
            if i != target:
                temp = temp +i
        for i in self.rule[target]:
            self.rule[start].append(i+temp)
        self.rule[start].remove(index)

    # 消除直接左递归
    def non_recursion(self,start):
        for i  in self.rule[str(start)]:
            # 直接左递归
            if i[0] == start:
                if self.added.has_key(i[0]) == False:
                    # 是否要创新的
                    new = self.str[self.t]
                    self.t = self.t + 1
                    self.added[i[0]]=new
                else:
                    new = self.added[i[0]]
                if self.rule.has_key(new) == False:
                    self.add_terinator(new)
                    self.rule[new] = []
                self.add_new_non(start,i,new)
            else:
                print i
   #判断是否要先递归
    def is_judge(self,key,bei):
        if self.non.index(str(key)) > self.non.index(str(bei)):
            return True
        else:
            return False
    # 是否可以进行代入
    def is_subsititution(self,key,bei,flag):
        if self.non.index(str(key)) > self.non.index(str(bei)):
            return True
        elif self.non.index(str(key)) == self.non.index(str(bei)) and flag == 0:
            self.non_recursion(bei)
        else:
            return False
    # 代入法
    def all_sub(self,start):
        Flag = 0
        #判断是否需要先递归
        for i in self.rule[str(start)]:
            if self.in_non_terinaor(i[0]) == True and self.is_judge(start,i[0]) == True:
                Flag = 1
        #根据上文判断，可进行先递归，不需要则执行代入流程
        for i in self.rule[str(start)]:
            if self.in_non_terinaor(i[0]) == True and self.is_subsititution(start,i[0],Flag) == True:
                self.substitution(start,i[0],i)
        return
    #消除直接和间接的递归
    def eliminate(self):
        for i in self.non:
            self.all_sub(i)
        for i in self.non:
            self.non_recursion(i)
        for i in self.non:
            self.draw_common(i)

    def sub_str(self,a,b):
        str = ''
        if len(a) > len(b):
            lens = len(b)
        else:
            lens =len(a)
        i = 0
        while i < lens:
            if a[i] == b[i]:
                str = str + a[i]
            else:
                return str
            i = i +1
        return str
    def add_center(self,new,start,index,num):
        str = ''
        i = num
        while i < len(self.rule[start][index]):
            str = str + self.rule[start][index][i]
            i = i+1
        self.rule[new].append(str)
    #提取左公因子
    def draw_common(self,start):
        lens = len(self.rule[start])
        i = 0
        j = 1
        while i < lens:
            while j < lens:
                index = self.sub_str(self.rule[start][i],self.rule[start][j])
                if index != '':
                    new = self.str[self.t]
                    self.t = self.t +1
                    self.add_terinator(new)
                    self.rule[new] = []
                    lens = len(index)
                    self.add_center(new,start,i,lens)
                    self.add_center(new,start,j,lens)
                    del self.rule[start][j]
                    del self.rule[start][i]
                    self.rule[start].append(index+new)
                j = j+1
            i = i +1

    def is_first(self,start,word):
        for i in self.rule[start]:
            if i[0] == word:
                return 1
        return 0

    def scanner_word(self,start,word):
        if start == word:
            return True
        for i in self.rule[start]:
            # 找到了匹配的式子，替换原有表达式
            if i[0] == word:
                self.I=self.I.replace(start,i,1)
                return True
            #没有的直接匹配的情况下，有非终结符号存在，则递归非终结符号
            elif self.is_first(start,word) == 0 and self.in_non_terinaor(i[0]):
                self.I=self.I.replace(start,i,1)
                res = self.scanner_word(i[0],word)
                if res == True:
                    return True
                elif res == False:
                    return  False
        for i in self.rule[start]:
            if i == '&':
                self.I=self.I.replace(start,'',1)
                return
        return False

    def is_e(self,start):
        for i in self.rule[start]:
            if i == '&':
                return True
        return False
    def digui(self,start,str):
        print '判断语句：'+str
        lens = len(str)
        i=0
        while i<lens:
            res = self.scanner_word(self.I[0],str[i])
            if res == True:
                self.I = self.I[1:]
                i = i + 1
            elif res == False:
                print '不合法'
                break
        if i == lens:
            if self.I == 0:
                print '合法'
            else:
                flag = 0
                for j in self.I:
                    if self.in_non_terinaor(j) == True:
                        if self.is_e(j) == False:
                            flag = 1
                            break
                    else:
                        flag = 1
                        break
                if flag == 0:
                    print '合法'
                elif flag == 1:
                    print '不合法'


    def main(self):
       # for i in self.non:
          #  self.is_null(i)
        str = ['i+i','i+i*i+(i+i)','i+*','+((i)*(i))+(i+i*i)','i*i*i*i']
        #str = ['i+i','i+i*i+(i+i)','i+*','+((i)*(i))+(i+i*i)','i*i*i*i','(i/i)']
        #str = ['b','cd','bdad','bdcccca','bdc','bdca']
        for i in str:
            self.I = self.start
            self.digui(self.I[0],i)









