# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class VoteWidget(QWidget):
    def __init__(self) -> None:
        super(VoteWidget, self).__init__()
        
        self.VBL = QVBoxLayout()
        
        # majority type btn
        self.majorityGroup = QButtonGroup()
        self.SimpleMajorityBTN = QRadioButton("Simple Majority")
        self.QualifiedMajorityBTN = QRadioButton("Qualified Majority")
        self.majorityGroup.addButton(self.SimpleMajorityBTN)
        self.majorityGroup.addButton(self.QualifiedMajorityBTN)
        
        # for, against, abstain btns
        self.ForBTN = QPushButton()
        
        # voting results label
        self.ResultLabel = QLabel()
        
        # put everything into layout
        self.VBL.addWidget(self.SimpleMajorityBTN)
        self.VBL.addWidget(self.QualifiedMajorityBTN)