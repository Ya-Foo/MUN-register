# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class VoteWidget(QWidget):
    def __init__(self) -> None:
        super(VoteWidget, self).__init__()
        
        self.VBL = QVBoxLayout()
        
        # vote type frame
        self.majorityFrame = QFrame()
        self.majorityFrameLayout = QHBoxLayout()
        
        # majority type btn
        self.majorityGroup = QButtonGroup()
        self.SimpleMajorityBTN = QRadioButton("Simple Majority")
        self.SimpleMajorityBTN.clicked.connect(self.calculate)
        self.QualifiedMajorityBTN = QRadioButton("Qualified Majority")
        self.QualifiedMajorityBTN.clicked.connect(self.calculate)
        self.majorityGroup.addButton(self.SimpleMajorityBTN)
        self.majorityGroup.addButton(self.QualifiedMajorityBTN)
        self.SimpleMajorityBTN.setChecked(True)
        
        # add vote type into frame
        self.majorityFrameLayout.addWidget(self.SimpleMajorityBTN)
        self.majorityFrameLayout.addWidget(self.QualifiedMajorityBTN)
        self.majorityFrame.setLayout(self.majorityFrameLayout)
        
        # frame for counting votes
        self.votecountFrame = QFrame()
        self.votecountFrameLayout = QGridLayout()
        
        # for, against, abstain btns
        self.ForBTNPlus = QPushButton("+")
        self.ForBTNPlus.clicked.connect(self.incrementVoteFor)
        self.ForBTNMinus = QPushButton("−")
        self.ForBTNMinus.clicked.connect(self.decrementVoteFor)
        
        self.AbstainBTNPlus = QPushButton("+")
        self.AbstainBTNPlus.clicked.connect(self.incrementVoteAbstain)
        self.AbstainBTNMinus = QPushButton("−")
        self.AbstainBTNMinus.clicked.connect(self.decrementVoteAbstain)
        
        self.AgainstBTNPlus = QPushButton("+")
        self.AgainstBTNPlus.clicked.connect(self.incrementVoteAgainst)
        self.AgainstBTNMinus = QPushButton("−")
        self.AgainstBTNMinus.clicked.connect(self.decrementVoteAgainst)
        
        # vote count labels
        self.ForCount = QLabel("0")
        self.AbstainCount = QLabel("0")
        self.AgainstCount = QLabel("0")
        
        # add stuff to vote count frame
        self.votecountFrameLayout.addWidget(self.ForBTNPlus, 0, 0)
        self.votecountFrameLayout.addWidget(self.ForCount, 1, 0)
        self.votecountFrameLayout.addWidget(self.ForBTNMinus, 2, 0)
        self.votecountFrameLayout.addWidget(self.AbstainBTNPlus, 0, 1)
        self.votecountFrameLayout.addWidget(self.AbstainCount, 1, 1)
        self.votecountFrameLayout.addWidget(self.AbstainBTNMinus, 2, 1)
        self.votecountFrameLayout.addWidget(self.AgainstBTNPlus, 0, 2)
        self.votecountFrameLayout.addWidget(self.AgainstCount, 1, 2)
        self.votecountFrameLayout.addWidget(self.AgainstBTNMinus, 2, 2)
        self.votecountFrame.setLayout(self.votecountFrameLayout)
        
        # voting results label
        self.ResultLabel = QLabel("Awaiting votes...")
        
        # put everything into layout
        self.VBL.addWidget(self.majorityFrame)
        self.VBL.addWidget(self.votecountFrame)
        self.VBL.addWidget(self.ResultLabel)
        self.setLayout(self.VBL)
        
    def incrementVoteFor(self):
        value = int(self.ForCount.text())
        self.ForCount.setText(f"{value+1}")
        self.calculate()
        
    def incrementVoteAbstain(self):
        value = int(self.AbstainCount.text())
        self.AbstainCount.setText(f"{value+1}")
        self.calculate()
        
    def incrementVoteAgainst(self):
        value = int(self.AgainstCount.text())
        self.AgainstCount.setText(f"{value+1}")
        self.calculate()
        
    def decrementVoteFor(self):
        value = int(self.ForCount.text())
        if not value: return
        self.ForCount.setText(f"{value-1}")
        self.calculate()
        
    def decrementVoteAbstain(self):
        value = int(self.AbstainCount.text())
        if not value: return
        self.AbstainCount.setText(f"{value-1}")
        self.calculate()
        
    def decrementVoteAgainst(self):
        value = int(self.AgainstCount.text())
        if not value: return
        self.AgainstCount.setText(f"{value-1}")
        self.calculate()
    
    def calculate(self):
        for_c, against_c = int(self.ForCount.text()), int(self.AgainstCount.text())
        total = for_c + against_c
        majority = self.majorityGroup.checkedButton().text()
        if majority == "Simple Majority":
            if for_c >= total // 2 + 1:
                self.ResultLabel.setText("PASSED")
            else:
                self.ResultLabel.setText("NOT PASSED")
        else:
            if for_c >= total // 3 * 2:
                self.ResultLabel.setText("PASSED")
            else:
                self.ResultLabel.setText("NOT PASSED")