# -*- coding:utf-8 -*-

from block import Block

class Blockchain(object):
    def __init__(self):
        self.blockList = []

    def addBlock(self, newBlock):
        if len(self.blockList) > 0:
            newBlock.link(self.blockList[-1].blockHash)
        self.blockList.append(newBlock)