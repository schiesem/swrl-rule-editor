from PyQt5.QtWidgets import * 
from PyQt5 import uic



class SWRLRuleEditor(QMainWindow):

    def __init__(self):
        super(SWRLRuleEditor, self).__init__()
        uic.loadUi("Projekt\MainWindow.ui", self)
        self.show()

def main():
    project = QApplication([])
    window = SWRLRuleEditor()
    project.exec_()


if __name__== "__main__":
    main()