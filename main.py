# -*- coding:utf-8 -*-

from sha256 import my_sha256
import Transaction
from ecdsa import ECDSA
from block import Block
from blockchain import Blockchain
import Errors

class User(object):
    # 初始化用户
    def __init__(self, input_wif):
        self.menu = ECDSA()
        self.wif = input_wif
        self.private_key = self.menu.get_private_key_from_wif(self.wif)
        self.public_key = self.menu.get_public_key_from_private_key(self.private_key)
        compressed_public_key = self.menu.get_compressed_public_key_from_public_key(self.public_key)
        self.addr = self.menu.get_addr_from_compressed_public_key(compressed_public_key)
        # 上面的数据域生成后，为了尽量接近实际的比特币交易，我们在交易中不直接使用公钥和私钥，而是使用wif和addr来实现相关功能


# 创建用户
def createUser():
    temp = ECDSA()
    # 首先，由于ECDSA中生成的公钥和私钥为 int 类型，为了wif的成功生成，将私钥变为64位的16进制字符串
    temp.private_key = hex(temp.private_key)[2:]
    temp.private_key = '0' * (64 - len(temp.private_key)) + temp.private_key
    # 下面计算wif和address
    temp.wif = temp.get_wif_from_private_key(temp.private_key)
    return temp.wif

# 用户UTXO获取
def getUTXO(addr, blockchain):
    ans = 0
    for eachBlock in blockchain.blockList:
        for eachTranscation in eachBlock.data:
            for eachOut in eachTranscation.outList:
                if eachOut.script == addr and eachOut.isUsed == False:
                    ans += eachOut.value
    return ans

# 交易构建
# 注意包含找零过程
def makeDeal(sender, receiverAddr, value, blockchain):
    # 首先，如果最后一个区块已满，则要求创建新区块
    # 这里设定区块中可以容纳 10 条交易，若超过
    if len(blockchain.blockList[-1].data) == 10:
        raise Errors.BlockIsOverFlow()

    # 首先，遍历整个区块链，寻找可用的 UTXO
    curTot = 0
    curTranscation = []
    flag = False
    for blockIndex, eachBlock in enumerate(blockchain.blockList):
        if flag:
            break
        for transcationIndex, eachTranscation in enumerate(eachBlock.data):
            if flag:
                break
            for outIndex, eachOut in enumerate(eachTranscation.outList):
                if flag:
                    break
                if eachOut.script == sender.addr and eachOut.isUsed == False:
                    curTot += eachOut.value
                    curTranscation.append([blockIndex, transcationIndex, outIndex])
                    if curTot >= value:
                        flag = True
    # 根据UXTO生成交易输入
    t = Transaction.Transaction()
    if flag == False:
        raise Errors.CoinNotEnough()
    for each in curTranscation:
        new = Transaction.In(blockchain.blockList[each[0]].data[each[1]], each[2], sender)
        if new.verify():
            t.addIn(new)
            blockchain.blockList[each[0]].data[each[1]].outList[each[2]].isUsed = True
        else:
            raise Errors.AccessDenied()
    # 构建输出
    aim = Transaction.Out(value, receiverAddr)
    # receiver.UTXO += value
    # 开始找零
    returnCoin = Transaction.Out(curTot - value, sender.addr)
    t.addOut(aim)
    t.addOut(returnCoin)
    t.seal()
    # 将该交易打包入区块中
    # # 这里设定区块中可以容纳 10 条交易，若超过
    # if len(blockchain.blockList[-1].data) > 9:
    #     newBlock = Block(sender.addr)
    #     newBlock.addTransaction(t)
    #     blockchain.addBlock(newBlock)
    # else:
    blockchain.blockList[-1].addTransaction(t)

if __name__ == '__main__':
    # 创建用户
    lonlynwif = createUser()
    brightwif = createUser()
    # 用户登录
    lonlyn = User(lonlynwif)
    bright = User(brightwif)

    # 创建区块链
    # 首先创建创世区块，矿工为 bright
    foundation = Block(bright.addr)
    print("foundation is created.")
    # 创建区块链
    global blockchain
    blockchain = Blockchain()

    # bright - 40 -> lonlyn
    # input = Transaction.In(foundation.data.)
    # 问题：如何为新建的输入寻找合适的上一个输出？

    blockchain.addBlock(foundation)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(bright, lonlyn.addr, 2, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(lonlyn, bright.addr, 1, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(bright, lonlyn.addr, 2, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(bright, lonlyn.addr, 2, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(lonlyn, bright.addr, 1, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(bright, lonlyn.addr, 2, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(bright, lonlyn.addr, 2, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(lonlyn, bright.addr, 1, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(bright, lonlyn.addr, 2, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(bright, lonlyn.addr, 2, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(lonlyn, bright.addr, 1, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    makeDeal(bright, lonlyn.addr, 2, blockchain)
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))
    print(getUTXO(bright.addr, blockchain), getUTXO(lonlyn.addr, blockchain))