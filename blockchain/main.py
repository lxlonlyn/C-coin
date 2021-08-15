# -*- coding:utf-8 -*-

from utils.sha256 import my_sha256
import transaction
from utils.ecdsa import ECDSA
from blockchain.block import Block, Blockchain
import error


class User(object):
    """
    用户类。
    """
    def __init__(self, input_wif: str) -> None:
        """
        生成新用户，获取用户的私匙、公匙、wif、address 等信息。

        :param input_wif: 压缩私匙 wif
        """
        self.menu = ECDSA()
        self.wif = input_wif
        self.private_key = ECDSA.get_private_key_from_wif(self.wif)
        self.public_key = ECDSA.get_public_key_from_private_key(self.private_key)
        compressed_public_key = ECDSA.get_compressed_public_key_from_public_key(self.public_key)
        self.address = self.menu.get_address_from_compressed_public_key(compressed_public_key)


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
        raise error.BlockIsOverFlow()

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
                if eachOut.script == sender.address and eachOut.isUsed == False:
                    curTot += eachOut.value
                    curTranscation.append([blockIndex, transcationIndex, outIndex])
                    if curTot >= value:
                        flag = True
    # 根据UXTO生成交易输入
    t = transaction.Transaction()
    if flag == False:
        raise error.CoinNotEnough()
    for each in curTranscation:
        new = transaction.In(blockchain.blockList[each[0]].data[each[1]], each[2], sender)
        if new.verify():
            t.addIn(new)
            blockchain.blockList[each[0]].data[each[1]].outList[each[2]].isUsed = True
        else:
            raise error.AccessDenied()
    # 构建输出
    aim = transaction.Out(value, receiverAddr)
    # receiver.UTXO += value
    # 开始找零
    returnCoin = transaction.Out(curTot - value, sender.address)
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
    blockchain.blockList[-1].add_transaction(t)


if __name__ == '__main__':
    # 创建用户
    lonlynwif = createUser()
    brightwif = createUser()
    # 用户登录
    lonlyn = User(lonlynwif)
    bright = User(brightwif)

    # 创建区块链
    # 首先创建创世区块，矿工为 bright
    foundation = Block(bright.address)
    print("foundation is created.")
    # 创建区块链
    global blockchain
    blockchain = Blockchain()

    # bright - 40 -> lonlyn
    # input = Transaction.In(foundation.data.)
    # 问题：如何为新建的输入寻找合适的上一个输出？

    blockchain.add_block(foundation)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(bright, lonlyn.address, 2, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(lonlyn, bright.address, 1, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(bright, lonlyn.address, 2, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(bright, lonlyn.address, 2, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(lonlyn, bright.address, 1, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(bright, lonlyn.address, 2, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(bright, lonlyn.address, 2, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(lonlyn, bright.address, 1, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(bright, lonlyn.address, 2, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(bright, lonlyn.address, 2, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(lonlyn, bright.address, 1, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    makeDeal(bright, lonlyn.address, 2, blockchain)
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
    print(getUTXO(bright.address, blockchain), getUTXO(lonlyn.address, blockchain))
