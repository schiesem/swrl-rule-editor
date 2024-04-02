from PyQt5.QtWidgets import * 
from PyQt5 import uic
import os
#import owlready2
from os import path


class SWRLRuleEditor(QMainWindow):

    def __init__(self):
        super(SWRLRuleEditor, self).__init__()
        uic.loadUi("Projekt\MainWindow.ui", self)
        self.show()
        ontology_names = list_files_in_folder("Ontologien")
        self.comboBoxOntologies.addItems(ontology_names)
        self.comboBoxOntologies.currentIndexChanged.connect(self.ontologySelected)
        

    def ontologySelected(self):    
        selected_text = self.comboBoxOntologies.currentText()
        print(selected_text)

        
        """file_name = f"{selected_text}"
        folder_path = r"Ontologien"
        file_path_save = os.path.join(folder_path, file_name)
        onto = get_ontology("file://" + file_path_save).load()
        print("The ontology has been loaded")"""




def list_files_in_folder(folder_path):

    if not os.path.exists(folder_path):
        print("folder not found")
        return []

    files = os.listdir(folder_path)

    files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
    
    return files

def main():

    project = QApplication([])
    window = SWRLRuleEditor()
    project.exec_()


if __name__== "__main__":
    main()