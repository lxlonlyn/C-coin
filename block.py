# -*- coding:utf-8 -*-

# 文件介绍：
# 区块链的区块结构结构
# 该区块链并不是符合比特币规范版本的区块链，原因是我俩只开发了一周
# 只保留可以进行交易的必要区块头信息

import time
import Transaction
from sha256 import my_sha256

# 一个新区快的构建

class Block (object):

    # 创建一个新区快， 传入交易记录
    def __init__(self, minerAddr):
        self.timeStamp = self.setTimeStamp()
        # data为交易的list
        self.data = self.digSource(minerAddr)
        self.preHash = '0' * 64
        self.merkleHash = None
        self.setMerkleHash()
        self.blockHash = None
        self.setBlockHash()

    # 创建时间戳
    def setTimeStamp(self):
        # 通过当前时间得到一个时间戳的规范形式
        return time.time()

    # 每个新区快的交易信息生成
    def digSource(self, minerAddr):
        # 创建一个初始的交易：只包含挖矿所得
        coinbase = Transaction.Transaction()
        new = Transaction.Out(50, minerAddr)
        coinbase.addOut(new)
        coinbase.seal()
        return [coinbase]

    # 在该区块中增加交易
    def addTransaction(self, new):
        self.data.append(new)
        self.setMerkleHash()
        self.setBlockHash()
    

    def setMerkleHash(self):
        # 通过传入的deals来计算当前的merkleHash
        cur = []
        for each in self.data:
            cur.append(each.hash)
        nxt = []
        while len(cur) != 1:
            last = None
            for i, each in enumerate(cur):
                if(i % 2 == 0):
                    if(i == len(cur) - 1):
                        nxt.append(my_sha256(my_sha256(each + each)))
                    else:
                        last = each
                else:
                    nxt.append((my_sha256(last + each)))
            cur = nxt
            nxt = []
        self.merkleHash = cur[0]



    def setBlockHash(self):
        # 通过传入的区块来计算当前区块的blockHash
        string = str(self.timeStamp)
        for each in self.data:
            string += each.hash
        string += self.preHash + self.merkleHash
        self.blockHash = my_sha256(string)

    def link(self, pre):
        self.preHash = pre
        self.setBlockHash()

if __name__ == '__main__':
    block = Block()
    print('hello')
