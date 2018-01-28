# -*- coding: utf-8 -*-
#DFA
# 没有*边
# 一个符号，只能转移到一个状态
class stateMachine:
    length = 0
    def __init__(self):
        self.allState = [] #所有状态
        self.handlers = {}  # 状态转移函数字典
        self.endFrom = []  # 是否是接受状态
        self.nfaState = {}  #NFA集合
        self.nfaHanders = {}
        self.side = []
        self.endState = []
        self.miniArr = {}
        self.nfaState = {}
        self.dfaHanders = {}
     #添加状态
    def add_state(self,state):
       self.allState.append(state)
    #添加终结状态
    def add_end(self,end):
       self.endFrom.append(end)
    #添加转移函数
    def add_hander(self,start,key,end):
        if self.handlers.has_key(start) == False:
            self.handlers[start] = {}
            self.handlers[start][key] = []

        self.handlers[start][key].append(end)

    def add_side(self,word):
        self.side.append(word)




    #判断nfa这个状态是否已存在
    def is_same(self,num):
        flag = len(self.nfaState[num])
        for i in self.nfaState:
            temp = len(self.nfaState[i])
            if i != num:
                n = 0
                for j in self.nfaState[i]:
                    for t in self.nfaState[num]:
                        if t == j:
                            n = n + 1
                if temp == n and flag == n:
                    return i
        return -1

    #看是nfa里否已存在状态
    def is_exit(self,start,index):
        for i in self.nfaState[str(start)]:
            if i == index:
                return True
        return False

    # 求所有等价状态
    def e_close(self,start,index):
        for i in self.endFrom:
            if i == index:
                return
        if self.handlers[index].has_key('*') == True:
            for i in self.handlers[index]['*']:
                if self.is_exit(start,i) == False:
                    self.nfaState[start].append(i)
                self.e_close(start,i)

     #根据输入值，化为NFA
    def to_NFA(self,start,index,word):
        self.nfaState[index] = []
        # 根据状态集里的每个状态，看输入一个word会转移到哪里
        for i in self.nfaState[start]:
            self.scanner_word(index,i,word)
        temp = self.is_same(index)  #是否已经存在了这个状态
        if self.nfaHanders.has_key(start) == False:
            self.nfaHanders[start] = {} #创建新的状态
        if temp != -1:   # 存在的话
            del self.nfaState[index]  #删除当前索引
            self.nfaHanders[start][word] = temp  # 将状态转移边移到原有状态集合里的状态
            self.length = self.length -1  # 循环的状态数减少
        else:   # 不存在的话
            self.nfaHanders[start][word] = index  # 设置状态转移边
            for i in self.nfaState[index]:
                for j in self.endFrom:
                    if i == j: # 如果存在终结符号
                        self.endState.append(index) # 加入至终结状态



     #一个字符扫描判断
    def scanner_word(self,start,index,word):
        st = str(index)
        for i in self.endFrom:
            if i == index:
                return
        for i in self.handlers[st]:
            for j in self.handlers[st][i]:
                if i == word:
                    if self.is_exit(start,j) == False:
                        self.nfaState[start].append(j)
                        self.e_close(start,j)

    def NFA(self):
        L = str(self.length)
        self.nfaState[L] = []
        self.nfaState[L].append(L)
        #求每个状态的所有等价状态，化为一个nfa状态
        self.e_close(L,L)
        t = 0
        # 直到不再出现新的状态集合
        while t <= self.length:
            for i in self.side:
                # 求每条边包含的状态，看是否是新的状态集
                if i != '*':
                    self.length = self.length + 1
                    L1 = str(self.length)  # 状态集合加一个
                    self.to_NFA(str(t),L1,i)
            t = t +1

    def judge_two(self,start,index):
        tmp1 = 0
        tmp2 = 0
        for i in self.endState:
            if i == start:
                tmp1 = 1
            if i == index:
                tmp2 = 1
        if tmp1 != tmp2:
            self.miniArr[str(start)][str(index)] = False
            return
        flag = {}
        for i in self.side:
            if i != '*':
                temp1 = self.nfaHanders[start][i]
                temp2 = self.nfaHanders[index][i]
                if temp1 != temp2:
                    flag[i] = []
                    flag[i].append(temp1)
                    flag[i].append(temp2)
        if flag == {}:
            self.miniArr[start][index] = True
        else:
            self.miniArr[start][index] = flag

    def judge(self,x,y,start,index):
        tmp1 = 0
        tmp2 = 0
        for i in self.endState:
            if i == start:
                tmp1 = 1
            if i == index:
                tmp2 =1
        if tmp1 != tmp2:
            self.miniArr[x][y] = False
            return
        flag = {}
        for i in self.side:
            if i != '*':
                temp1 = self.nfaHanders[start][i]
                temp2 = self.nfaHanders[index][i]
                if temp1 != temp2:
                    flag[i] = []
                    flag[i].append(temp1)
                    flag[i].append(temp2)
        if flag == {}:
            self.miniArr[x][y] = True
        else:
            self.miniArr[x][y] = flag

    def is_stop(self):  # 不再有除了勾和叉以外的状态
        for i in self.miniArr:
            for j in self.miniArr[i]:
                if self.miniArr[i][j] != True and self.miniArr[i][j] != False:
                    return True
        return False
    # 求同法
    def miniDFA(self):
        for i in self.nfaState:
            self.miniArr[i] = {}
            # 构造三角矩阵
            for t in self.nfaState:
                if t > i:
                    self.miniArr[i][t] = {}
        for i in self.nfaState:
            for j in self.nfaState:
                if j > i:
                    self.judge_two(i,j)  # 判断两个状态是否等价
        stop = self.is_stop()  # 是否可以停止
        while(stop):
            for i in self.miniArr:
                for j in self.miniArr[i]:
                    if self.miniArr[i][j] != True and self.miniArr[i][j] != False:
                        for t in self.miniArr[i][j]:
                            self.judge(i,j,self.miniArr[i][j][t][0],self.miniArr[i][j][t][1])  # 判断两个有可转移边的是否相等
            stop = self.is_stop()
        self.merge()

    def merge(self):
        for i in self.miniArr:
            for j in self.miniArr[i]:
                if self.miniArr[i][j] == True :
                    del self.nfaState[j]
                    del self.nfaHanders[j]

    def show_hander(self):
        for j in self.nfaHanders:
            print "state:"+j
            for t in self.nfaHanders[j]:
                print "add:"+t +"  to:"+self.nfaHanders[j][t]

    def judge_word(self,init,item):
        initS = str(init)
        if self.nfaHanders[initS].has_key(item) == False:
            return -1
        res = self.nfaHanders[initS][item]
        return res

    def is_dfa(self):
        a = 'aaaaaabbb'
        print '判断字符串：'+a
        res = 0
        for item in a:
            if res == -1:
                return res
            res = self.judge_word(res,item)
        if res == True:
            return True
        if res == -1:
            return -1
        if res != True or res != -1:
            for i in self.endState:
                if i == res:
                    return True
            return -1


