# -*- coding: utf-8 -*-
class gram:
    def __init__(self):
        self.terminator = []
        self.non = []
        self.rule = {}
        self.each_side = {}
        self.first = {}
        self.follow = {}
        self.select = []
        self.start = ''
        self.num = 0
        self.stack =''

    # 加非终结符号
    def add_non(self, word):
        self.non.append(word)
        # 加终结符号

    def add_terminator(self, word):
        self.terminator.append(word)

    # 加推导规则
    def add_rule(self, key, point):
        if self.rule.has_key(key) == False:
            self.rule[key] = []
            self.first[key] = []
            self.follow[key] = []
        self.rule[key].append(point)
        str = {}
        str['start'] = key
        str['end'] = point
        self.select.append(str)
        self.num += 1

    # 判断是否是非终结符号
    def in_non_terinaor(self, word):
        for i in self.non:
            if i == word:
                return True
        return False

    # 判断是否有#推导
    def is_e(self, start):
        for i in self.rule[start]:
            if i == '#':
                return True
        return False
    # first集里是否有 # 推导
    def is_e_first(self, start):
        for i in self.first[start]:
            if i == '#':
                return True
        return False

    def is_e_select(self,start):
        i = 0
        while i < self.num:
            if self.select[i]['start'] == start:
                if self.select[i]['end'] == '#':
                    return True
            i += 1
        return False


    def is_exit(self, start, word):
        for i in self.first[start]:
            if i == word:
                return True
        return False

    def include(self, pa, child):
        # flag = 0
        for i in self.first[child]:
            if self.is_exit(pa, i) == False:
                self.first[pa].append(i)
                # flag = 1
                # if flag == 0:
                #     return False
                # elif flag == 1:
                #     return True

    def add_r_first(self, start):
        for i in self.rule[start]:
            if self.in_non_terinaor(i[0]) == False:
                # 非终结符号加入first集
                self.first[start].append(i[0])
            else:
                tmp = 0
                while tmp < len(i):
                    self.include(start, i[tmp])
                    if self.is_e(i[tmp]) == True:
                        tmp = tmp + 1
                    else:
                        tmp = len(i)
                        # tmp = 0
                        # while tmp < len(i):
                        # if tmp != len(i)-1 and self.in_non_terinaor(i[tmp+1]) == False:
                        # self.follow[i[tmp]].append(i[tmp+1])
                        # tmp = tmp + 1
                        # if self.in_non_terinaor(i[0]) == True:

    def is_exit_follw(self, start, word):
        for i in self.follow[start]:
            if i == word:
                return True
        return False

    # 加first集
    def include_follow(self, pa, child):
        for i in child:
            if self.is_exit_follw(pa, i) == False:
                if i != '#':
                    self.follow[pa].append(i)

    # 加follow集
    def include_follow_arr(self, pa, child):
        for i in self.follow[child]:
            if self.is_exit_follw(pa, i) == False:
                self.follow[pa].append(i)

    def add_r_follow(self, start):
        for i in self.rule[start]:
            lens = len(i) - 1
            if self.in_non_terinaor(i[lens]):
                while lens >= 0:
                    self.include_follow_arr(i[lens], start)
                    if self.is_e(i[lens]):
                        lens -= 1
                    else:
                        lens = -1
            tmp = 0
            while tmp < len(i):
                if self.in_non_terinaor(i[tmp]) == True:
                    if tmp != len(i) - 1:
                        if not self.in_non_terinaor(i[tmp + 1]):
                            if not self.is_exit(i[tmp], i[tmp + 1]):
                                self.follow[i[tmp]].append(i[tmp + 1])
                        else:
                            self.include_follow(i[tmp], self.first[i[tmp + 1]])
                tmp += 1

    def is_exit_select(self, obj, word):
        if not self.select[obj].has_key('Inputs'):
            return False
        for i in self.select[obj]['Inputs']:
            if i == word:
                return True
        return False

    def add_select(self):
        obj = 0
        while obj < self.num:
            i = self.select[obj]['end'][0]
            if i == '#':
                tmp = []
                for x in self.follow[self.select[obj]['start']]:
                    if not self.is_exit_select(obj, x):
                        tmp.append(x)
                self.select[obj]['inputs'] = tmp
            elif not self.in_non_terinaor(i):
                self.select[obj]['inputs'] = i
            else:
                if not self.is_e_first(i):
                    self.select[obj]['inputs'] = self.first[i]
                else:
                    tmp = []
                    for x in self.first[i]:
                        if x != '#':
                            tmp.append(x)
                    for x in self.follow[self.select[obj]['start']]:
                        if not self.is_exit_select(obj, x):
                            tmp.append(x)
                    self.select[obj]['inputs'] = tmp
            obj += 1

    def string_reverse1(self, string):
        return string[::-1]

    def scanner_word(self, start, word):
        i = 0
        while i < self.num:
            if self.select[i]['start'] == start:
                for s in self.select[i]['inputs']:
                    if s == word:
                        print self.select[i]['start'] + '->' + self.select[i]['end']
                        txt = self.select[i]['end']
                        self.stack = self.stack.replace(start,txt,1)
                        return True
            i += 1
        return False

    def analysis(self,str):
        i = 0
        while i < len(str):
            res = self.scanner_word(self.stack[0], str[i])
            if not res:
                print 'error'
                return False
            else:
                if self.stack[0] == '#':
                    self.stack = self.stack[1:]  #弹出
                elif self.stack[0] == str[i]:
                    print str[i]
                    self.stack = self.stack[1:]  #弹出
                    i += 1  #指针后移
        if len(self.stack) == 0:
            return True
        else:
            j = 0
            while j < len(self.stack):
                if not self.is_e_select(self.stack[j]):
                    return False
                j += 1
            return True

    def main(self):
        self.follow[self.start].append('$')
        i = 0
        while i < len(self.non):
            self.add_r_first(self.non[i])
            i += 1
        i -= 1
        while i >= 0:
            for j in self.rule[self.non[i]]:
                if self.in_non_terinaor(j[0]):
                    self.include(self.non[i], j[0])
                    # self.include_follow(j[0],self.non[i])
            i -= 1
        i = 0
        while i < len(self.non):
            self.add_r_follow(self.non[i])
            i += 1
        i = 0
        while i < len(self.non):
            for j in self.rule[self.non[i]]:
                l = len(j) - 1
                if self.in_non_terinaor(j[l]):
                    while l >= 0:
                        self.include_follow_arr(j[l], self.non[i])
                        if self.is_e(j[l]):
                            l -= 1
                        else:
                            l = -1
            i += 1
        self.add_select()
        str = '(a,a)'
        self.stack = self.start
        res = self.analysis(str)
        print '判断语句：'+str
        if res:
            print "最终结果：符合文法"
        elif not res:
            print "最终结果：不符合文法"
