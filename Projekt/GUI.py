import sys
from PyQt5.QtWidgets import * 
from PyQt5 import uic
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from random import randint


class SWRLRuleEditor(QMainWindow):

    def __init__(self):
        super(SWRLRuleEditor, self).__init__()
        self.w = None
        uic.loadUi("Projekt\MainWindow.ui", self)
        self.show()
        #self.form_widget = AppDemo(self)
        self.button = QPushButton("Push for Window")
        self.button.clicked.connect(self.show_new_window)
        self.setCentralWidget(self.button)

        #self.setCentralWidget(self.Button1)

        #self.setCentralWidget(self.form_widget) 

    def show_new_window(self,checked):
         if self.w is None:
              self.w= AppDemo()
          
         self.w.show()
        
        
class AppDemo (QWidget):
        def __init__(self):
            super().__init__()
            #self.resize(160,100)
            wlayout = QVBoxLayout()
            self.label = QLabel("AppDemo % d" % randint(0,100))
            
            

            rules = ('Rule1', 'Rule2', 'Rule3', 'Rule4', 'Rule5', 'Rule5')
            model = QStandardItemModel(len(rules), 1)
            model.setHorizontalHeaderLabels(['Rules'])
    
            for row, rules in enumerate(rules):
                item = QStandardItem(rules)
                model.setItem(row, 0, item)

            search_field = QLineEdit()
            search_field.setStyleSheet('font-size: 35px; height: 60px')  
            wlayout.addWidget(search_field)

            table= QTableView()
            table.setStyleSheet('font-size: 35px;')
            wlayout.addWidget(table)


            self.setLayout(wlayout)


#def main():
#    project = QApplication([])
#    window = SWRLRuleEditor()
#    project.exec_()


#if __name__== "__main__":
#    main()

app = QApplication(sys.argv)
w = SWRLRuleEditor()
w.show()
app.exec()