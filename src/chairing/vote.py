# Import PyQT
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pyautogui
import math

# Constants
width, height = pyautogui.size()

class VoteWidget(QWidget):
    def __init__(self) -> None:
        super(VoteWidget, self).__init__()
        
        self.VBL = QVBoxLayout()
        self.setStyleSheet("""
            .QPushButton{
                background: transparent; 
                color: white; 
                font: 14pt
            }
            .QLineEdit {
                background: transparent;
                color: white;
                border: none;
                padding: 10px;
            }
            .QRadioButton {
                font: 12pt;
                margin-bottom: 20px;
            }
        """)
        self.setFixedSize(int(width*0.4), height//2)
        self.VBL.setAlignment(Qt.AlignTop)
        self.setContentsMargins(25, 10, 10, 10)
        
        # vote type frame
        self.majorityFrame = QFrame()
        self.majorityFrameLayout = QHBoxLayout()
        self.majorityFrameLayout.setSpacing(0)
        
        # majority type btn
        self.majorityGroup = QButtonGroup()
        self.SimpleMajorityBTN = QRadioButton("Simple Majority")
        self.SimpleMajorityBTN.clicked.connect(self.calculate)
        self.QualifiedMajorityBTN = QRadioButton("Super Majority")
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
        self.votecountFrameLayout = QHBoxLayout()
        
        # vote type frame
        self.ForFrame = QFrame()
        self.ForFrame.setStyleSheet(".QFrame{border: 2px solid green; border-radius: 30px;}")
        self.ForFrameLayout = QVBoxLayout()
        self.ForFrameLayout.setSpacing(0)
        self.ForFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.AbstainFrame = QFrame()
        self.AbstainFrame.setStyleSheet(".QFrame{border: 2px solid yellow; border-radius: 30px;}")
        self.AbstainFrameLayout = QVBoxLayout()
        self.AbstainFrameLayout.setSpacing(0)
        self.AbstainFrameLayout.setContentsMargins(0, 0, 0, 0)
        self.AgainstFrame = QFrame()
        self.AgainstFrame.setStyleSheet(".QFrame{border: 2px solid red; border-radius: 30px;}")
        self.AgainstFrameLayout = QVBoxLayout()
        self.AgainstFrameLayout.setSpacing(0)
        self.AgainstFrameLayout.setContentsMargins(0, 0, 0, 0)
        
        # for, abstain, against btn
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
        self.ForCount = QLineEdit("0")
        self.ForCount.setAlignment(Qt.AlignCenter)
        self.ForCount.editingFinished.connect(self.calculate)
        self.AbstainCount = QLineEdit("0")
        self.AbstainCount.setAlignment(Qt.AlignCenter)
        self.AbstainCount.editingFinished.connect(self.calculate)
        self.AgainstCount = QLineEdit("0")
        self.AgainstCount.setAlignment(Qt.AlignCenter)
        self.AgainstCount.editingFinished.connect(self.calculate)
        
        # add stuff to for frame
        self.ForFrameLayout.addWidget(self.ForBTNPlus)
        self.ForFrameLayout.addWidget(self.ForCount)
        self.ForFrameLayout.addWidget(self.ForBTNMinus)
        self.ForFrame.setLayout(self.ForFrameLayout)
        
        # add stuff to for frame
        self.AbstainFrameLayout.addWidget(self.AbstainBTNPlus)
        self.AbstainFrameLayout.addWidget(self.AbstainCount)
        self.AbstainFrameLayout.addWidget(self.AbstainBTNMinus)
        self.AbstainFrame.setLayout(self.AbstainFrameLayout)
        
        # add stuff to for frame
        self.AgainstFrameLayout.addWidget(self.AgainstBTNPlus)
        self.AgainstFrameLayout.addWidget(self.AgainstCount)
        self.AgainstFrameLayout.addWidget(self.AgainstBTNMinus)
        self.AgainstFrame.setLayout(self.AgainstFrameLayout)
        
        # add stuff to vote count frame
        self.votecountFrameLayout.addWidget(self.ForFrame)
        self.votecountFrameLayout.addWidget(self.AbstainFrame)
        self.votecountFrameLayout.addWidget(self.AgainstFrame)
        self.votecountFrame.setLayout(self.votecountFrameLayout)
        
        # voting results label
        self.ResultLabel = QLabel("Awaiting votes...")
        self.ResultLabel.setStyleSheet("""
            background: rgba(255, 255, 255, 0.4);
            border: 1px solid transparent;
            border-radius: 15px;
            margin: 0px 20px;
            padding: 120px 0px;
            font: 14pt;
        """)
        self.ResultLabel.setAlignment(Qt.AlignCenter)
        
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
        try:
            for_c, against_c = int(self.ForCount.text()), int(self.AgainstCount.text())
            total = for_c + against_c
            majority = self.majorityGroup.checkedButton().text()
            
            # calculate results
            if majority == "Simple Majority":
                if for_c >= math.floor(total / 2 + 1):
                    self.ResultLabel.setText("PASSED")
                else:
                    self.ResultLabel.setText("NOT PASSED")
            else:
                if for_c >= math.floor(total / 3 * 2):
                    self.ResultLabel.setText("PASSED")
                else:
                    self.ResultLabel.setText("NOT PASSED")
                    
            # change GUI based on results
            if self.ResultLabel.text() == "PASSED":
                self.ResultLabel.setStyleSheet("""
                    background: rgba(0, 255, 0, 0.1);
                    border: 1px solid transparent;
                    border-radius: 15px;
                    margin: 0px 20px;
                    padding: 120px 0px;
                    font: 14pt;
                    color: green;
                """)
            else:
                self.ResultLabel.setStyleSheet("""
                    background: rgba(255, 0, 0, 0.1);
                    border: 1px solid transparent;
                    border-radius: 15px;
                    margin: 0px 20px;
                    padding: 120px 0px;
                    font: 14pt;
                    color: red;
                """)
        except:
            self.ResultLabel.setText("ERROR: Invalid input")