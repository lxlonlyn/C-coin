# -*- coding:utf-8 -*-

from sha256 import my_sha256

class In(object):
    def __init__(self, preOut, index, sender):
        # preOut 为引用的上一个交易哈希， preUTXO是维护余额

        # 该输入的原输出的地址
        self.sender = sender
        self.preOut = preOut
        self.index = index
        # 解锁脚本
        private_key = sender.menu.get_private_key_from_wif(sender.wif)
        public_key = sender.menu.get_public_key_from_private_key(private_key)
        self.script = [sender.menu.gen_signature(preOut.outList[index].script, int(private_key, 16)), public_key]
        # 维护的UTXO数据
        self.utxo = preOut.outList[index].value

    def toString(self):
        string = self.preOut.hash
        string += str(self.script[0][0]) + str(self.script[0][1]) + str(self.script[1][0]) + str(self.script[1][1])
        return string

    def verify(self):
        public_key = self.sender.menu.get_public_key_from_private_key(self.sender.wif, True)
        return self.sender.menu.verify_signature(self.preOut.outList[self.index].script, public_key, self.script[0])

class Out(object):
    def __init__(self, value, addr):
        # 交易数额
        self.value = value
        # 所在交易集合的索引
        self.index = None
        # 锁定脚本
        self.script = addr
        # 是否已经被使用
        self.isUsed = False

    def toString(self):
        return str(self.value) + self.script    

class Transaction(object):
    def __init__(self):
        self.inList = []
        self.outList = []
        self.hash = None

    def computeHash(self):
        string = ''
        for each in self.inList:
            string += each.toString()
        for each in self.outList:
            string += each.toString()
        self.hash = my_sha256(string)

    def addIn(self, new):
        self.inList.append(new)

    def addOut(self, new):
        self.outList.append(new)
        self.outList[-1].index = len(self.outList) - 1

    def seal(self):
        self.computeHash()

if __name__ == '__main__':
    input = In(50, None)
    output = Out(10)
    t = Transaction()
    t.addIn(input)
    t.addOut(output)
    t.seal()
    print('hello')