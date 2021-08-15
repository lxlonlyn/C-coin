# C-coin

数字货币 C-coin，因为是仿照 BTC 做的，且制作人的名字里都有 C 开头的，所以起了这个名。

本意是糊弄密码学大作业，至于为什么要重复造轮子是因为老师不让调包 QAQ。

## 文件结构

- main.py
- utils
  - sha1.py
  - sha256.py
  - ecdsa.py
- blockchain
  - block.py
  - error.py
  - main.py
  - transaction.py
- GUI
  - BlockWidget.py
  - MainWidget.py

## 更新日志

2021.6.5 Update：

将所有的文件发上去了，如果有时间就后面再改改了。。。

目前手动造区块的确很出戏

2021.8.15 Update:

改变了工程结构，分成了三类：界面，区块链，密码学函数。
