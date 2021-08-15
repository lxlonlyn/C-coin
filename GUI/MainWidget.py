# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, \
    QVBoxLayout, QTabWidget, QMessageBox, QLabel, QFrame, QScrollArea, QInputDialog
from GUI import BlockWidget
from blockchain.block import Block, Blockchain
from blockchain.main import createUser, User, getUTXO, makeDeal


class MainWindow(QTabWidget):
    def __init__(self):
        super().__init__()
        self.tab4_layout = QFormLayout()
        self.tab3_layout = QHBoxLayout()
        self.user_scroll = QScrollArea()
        self.tab2_layout = QHBoxLayout()
        self.blocksBox = QWidget()
        self.blockchain = Blockchain()
        self.scroll = QScrollArea()
        self.setWindowTitle("C coin——全新的数字货币")
        self.resize(1200, 800)
        self.func()
        self.new_usersBox = QWidget()

    def func(self):
        self.welcome_widget = QWidget()
        self.block_widget = QWidget()
        self.account_widget = QWidget()
        self.deal_widget = QWidget()

        self.addTab(self.welcome_widget, "欢迎页面")
        self.addTab(self.block_widget, "区块信息")
        self.addTab(self.account_widget, "账户信息")
        self.addTab(self.deal_widget, "交易页面")

        # 增加点击切换界面
        self.currentChanged.connect(self.display)

        # 初始化
        # 创建用户
        self.all_user = []
        for i in range(10):
            self.all_user.append(User(createUser()))

        print("The message below helps you to try generating a new block and transaction.")
        print("An example address (User 2): " + self.all_user[2].address)
        print("An example wif (User 1): " + self.all_user[1].wif)

        # 创建区块链
        # 首先创建创世区块，矿工为 bright
        foundation = Block(self.all_user[0].address)
        second_block = Block(self.all_user[1].address)
        # 创建区块链
        blockchain = Blockchain()
        blockchain.add_block(foundation)
        blockchain.add_block(second_block)
        self.set_blockchain(blockchain)

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()

    def display(self, index):
        pass
        # self.setCurrentIndex(index)

    def tab1UI(self):
        layout = QVBoxLayout()
        wel = QLabel()
        wel.setText("欢迎使用 C-coin 系统")
        wel.setFont(QFont("Microsoft YaHei", 20, 60))
        wel.setAlignment(Qt.AlignCenter)
        self.time = QLabel()
        self.time.setText(QTime.currentTime().toString())
        self.time.setFont(QFont("Microsoft YaHei", 15, 60))
        self.time.setAlignment(Qt.AlignCenter)
        layout.addStretch(10)
        layout.addWidget(wel, 0, Qt.AlignHCenter)
        layout.addStretch(1)
        layout.addWidget(self.time, 0, Qt.AlignHCenter)
        layout.addStretch(10)
        self.welcome_widget.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.clock_update)
        self.timer.start(1000)

    def clock_update(self):
        self.time.setText(QTime.currentTime().toString())

    def tab2UI(self):

        # 左侧：区块链显示
        self.blocksBox.setMinimumSize(750, max(800, 20 + len(self.blockchain.blockList) * 215))
        self.scroll.setAlignment(Qt.AlignCenter)
        self.scroll.setWidget(self.blocksBox)
        self.scroll.setFrameShape(QFrame.Box)
        self.scroll.setMinimumWidth(750)
        self.tab2_layout.addWidget(self.scroll, 3)

        # 右侧：空间按钮

        buttonBox = QFrame()
        buttonBox.setFrameShape(QFrame.Box)
        btn_createBlock = QPushButton()
        btn_createBlock.setParent(buttonBox)
        btn_createBlock.setText("创建新区块")
        btn_createBlock.setFixedSize(200, 80)
        btn_createBlock.move(45, 50)
        self.tab2_layout.addWidget(buttonBox, 1)

        btn_createBlock.clicked.connect(self.create_block_clicked)

        self.block_widget.setLayout(self.tab2_layout)

    def blocksbox_update(self):
        self.new_blocksBox = QWidget()
        self.new_blocksBox.setMinimumSize(750, max(800, 20 + len(self.blockchain.blockList) * 215))

        for i in range(len(self.blockchain.blockList)):
            block = self.blockchain.blockList[i]
            a = BlockWidget.QBlockWidget()
            a.setParent(self.new_blocksBox)
            a.move(0, 10 + i * 215)
            a.set_hash(block.blockHash)
            a.set_time(str(block.timeStamp))
            a.set_prehash(block.preHash)
            a.set_merkle(block.merkleHash)

        self.blocksBox = self.new_blocksBox
        self.scroll.setMinimumWidth(750)
        self.scroll.setWidget(self.blocksBox)

    def set_blockchain(self, new_blockchain):
        self.blockchain = new_blockchain
        self.blocksbox_update()

    def add_block(self, new_block):
        self.blockchain.add_block(new_block)
        self.blocksbox_update()

    def create_block_clicked(self):
        input_addr, okPressed = QInputDialog.getText(self, "确认打工人", "请输入打工人的地址", QLineEdit.Normal, "")
        found = -1
        for i in range(len(self.all_user)):
            if self.all_user[i].address == input_addr:
                found = i
                break
        if found == -1:
            print("Error: No user address '" + input_addr + "' found.")
        else:
            print("Successfully found user: " + str(found))
        if okPressed:
            if found != -1:
                msg = QMessageBox.information(self, "新区块已创立", "好耶，是新区块！", QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.Yes)
                self.add_block(Block(input_addr))
                self.usersbox_update()
            else:
                msg = QMessageBox.information(self, "新区块创立失败", "随便输一个可是过不了的 ╮(╯▽╰)╭ ", QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.Yes)

    def tab3UI(self):
        # 左侧：User 显示
        self.usersBox = QWidget()
        self.usersBox.setMinimumSize(750, max(800, 20 + len(self.all_user) * 215))

        for i in range(len(self.all_user)):
            a = QFrame()
            a.setParent(self.usersBox)
            a.setFixedSize(740, 220)
            a.setFrameShape(QFrame.Box)
            a.setContentsMargins(10, 10, 10, 10)
            a.move(0, 10 + i * 215)

            addr = self.all_user[i].address
            money = getUTXO(addr, self.blockchain)

            lb_addr = QLabel()
            lb_addr.setText("地址：" + addr)
            lb_addr.setParent(a)
            lb_money = QLabel()
            lb_money.setText("持有金额：" + str(money))
            lb_money.setParent(a)
            font = QFont("Microsoft YaHei", 10, 60)
            lb_addr.setFont(font)
            lb_money.setFont(font)

            lb_addr.move(20, 80)
            lb_money.move(20, 120)

        self.user_scroll.setMinimumWidth(750)
        self.user_scroll.setWidget(self.usersBox)

        self.user_scroll.setAlignment(Qt.AlignCenter)
        self.user_scroll.setWidget(self.usersBox)
        self.user_scroll.setFrameShape(QFrame.Box)
        self.user_scroll.setMinimumWidth(750)
        self.tab3_layout.addWidget(self.user_scroll, 3)

        # 右侧：空间按钮

        buttonBox = QFrame()
        buttonBox.setFrameShape(QFrame.Box)
        btn_createUser = QPushButton()
        btn_createUser.setParent(buttonBox)
        btn_createUser.setText("创建新账户")
        btn_createUser.setFixedSize(200, 80)
        btn_createUser.move(45, 50)
        self.tab3_layout.addWidget(buttonBox, 1)

        btn_createUser.clicked.connect(self.create_user_clicked)

        self.account_widget.setLayout(self.tab3_layout)

    def create_user_clicked(self):
        new_user = User(createUser())
        msg = QMessageBox.information(self, "新用户已创立", "好耶，是新用户！记住你的信息：\n" + "地址：" + new_user.address + "\n" + \
                                      "压缩私匙 wif：" + new_user.wif, QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.Yes)
        self.all_user.append(new_user)
        self.usersbox_update()

    def usersbox_update(self):
        self.new_usersBox = QWidget()
        self.new_usersBox.setMinimumSize(750, max(800, 20 + len(self.all_user) * 215))

        for i in range(len(self.all_user)):
            a = QFrame()
            a.setParent(self.new_usersBox)
            a.setFixedSize(740, 220)
            a.setFrameShape(QFrame.Box)
            a.setContentsMargins(10, 10, 10, 10)
            a.move(0, 10 + i * 215)

            addr = self.all_user[i].address
            money = getUTXO(addr, self.blockchain)

            lb_addr = QLabel()
            lb_addr.setText("地址：" + addr)
            lb_addr.setParent(a)
            lb_money = QLabel()
            lb_money.setText("持有金额：" + str(money))
            lb_money.setParent(a)
            font = QFont("Microsoft YaHei", 10, 60)
            lb_addr.setFont(font)
            lb_money.setFont(font)

            lb_addr.move(20, 80)
            lb_money.move(20, 120)

        self.usersBox = self.new_usersBox
        self.user_scroll.setMinimumWidth(750)
        self.user_scroll.setWidget(self.usersBox)

    def tab4UI(self):
        self.le_wif = QLineEdit()
        self.le_addr = QLineEdit()
        self.le_number = QLineEdit()
        btn_deal = QPushButton()
        btn_deal.setText("点我进行交易")
        btn_deal.clicked.connect(self.deal_clicked)
        self.tab4_layout.addRow("你的压缩私匙 wif：", self.le_wif)
        self.tab4_layout.addRow("转账对象的地址：", self.le_addr)
        self.tab4_layout.addRow("转账金额：", self.le_number)
        self.tab4_layout.addRow(btn_deal)

        self.deal_widget.setLayout(self.tab4_layout)

    def deal_clicked(self):
        occurred = False
        for u in self.all_user:
            if u.wif == self.le_wif.text():
                occurred = True
                break
        to_pos = -1
        for i in range(len(self.all_user)):
            if self.all_user[i].address == self.le_addr.text():
                to_pos = i
                break
        if to_pos == -1 or occurred == False:
            if not occurred:
                msg = QMessageBox.information(self, "无法交易", "冒充别人充钱是不好的(￢_￢)。", QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.Yes)
            elif to_pos == -1:
                msg = QMessageBox.information(self, "无法交易", "请确定你的地址输入正确(￢_￢)。", QMessageBox.Yes | QMessageBox.No,
                                              QMessageBox.Yes)
        else:
            msg = QMessageBox.information(self, "交易成功", "请查看账户来确认完成交易。", QMessageBox.Yes | QMessageBox.No,
                                          QMessageBox.Yes)
            makeDeal(User(self.le_wif.text()), self.le_addr.text(), int(self.le_number.text(), 10), self.blockchain)
            self.blocksbox_update()
            self.usersbox_update()
