from PyQt5.QtWidgets import * 
from PyQt5 import uic
import os
from owlready2 import *
import owlready2
from os import path


class SWRLRuleEditor(QMainWindow):

    def __init__(self):
        super(SWRLRuleEditor, self).__init__()
        uic.loadUi("Projekt\MainWindow.ui", self)
        self.show()
        ontology_names = list_files_in_folder("Ontologien")
        self.comboBoxOntologies.addItem("none")
        self.comboBoxOntologies.addItems(ontology_names)
        self.comboBoxOntologies.currentIndexChanged.connect(self.ontologySelected)
        self.onto = get_ontology("file://" + "Ontologien\ghibli.rdf").load()                    #ontologie vor laden, wird dann später überschrieben, wenn eine ausgewählt wird. hier leere ontologie einfügen.

        #ontoVorlage = get_ontology("file://" + "Ontologien\ghibli.rdf").load()
        #print("...")
        #print(return_elements(ontoVorlage.classes()))

    def ontologySelected(self):    
        selected_text = self.comboBoxOntologies.currentText()
        print(selected_text)                                                        #testing
        #print(ontoVorlage)
        
        file_name = f"{selected_text}"
        folder_path = r"Ontologien"
        file_path_save = os.path.join(folder_path, file_name)
        onto = get_ontology("file://" + file_path_save).load()
        print("The ontology has been loaded")                                       #testing
        #print(return_elements(ontoVorlage.classes()))
        #print("break")
        print(return_elements(onto.classes()))
        self.test = "Test neu!"
        self.onto = onto
        

def return_elements(entities):

    try:
        #Ausgabemöglichkeiten return_elements(...):
        #Eine Liste von  Klassen(onto.classes())
        #                Instanzen(onto.individuals())
        #                Properties(onto.properties())
        #                ...

        listeEntities = []
        for entity in entities:
            name = entity.name
            listeEntities.append(name)
        return listeEntities
    except:
        print("Error")


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
    print("!")


if __name__== "__main__":
    main()