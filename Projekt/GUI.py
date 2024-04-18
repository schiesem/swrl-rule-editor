from PyQt5.QtWidgets import * 
from PyQt5 import uic
import os
from owlready2 import *
import owlready2
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets


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

        # Suchfeld für Regeln
        self.rule_lineEdit.textChanged.connect(self.search_rules)
        self.searchLineEdit.installEventFilter(self)

        #listwidget
        self.ruleListWidget.installEventFilter(self)

        # Liste für die gefundenen Regeln
        self.rule_list = []

    def eventFilter(self, obj, event):
        if obj == self.searchLineEdit:
           
           if event.type() == QtCore.QEvent.MouseButtonPress:
            # Bei Klick auf die Suchleiste die Liste ausblenden
            self.ruleListWidget.hide()
            return False
           
        elif obj == self.ruleListWidget:
            if event.type() == QtCore.QEvent.MouseButtonPress:
            # Bei Klick auf die Liste die Liste anzeigen
            self.ruleListWidget.show()
            return False
        
        return super().eventFilter(obj, event)    
        
        #ontoVorlage = get_ontology("file://" + "Ontologien\ghibli.rdf").load()
        #print("...")
        #print(return_elements(ontoVorlage.classes()))

    def addRuleToListWidget(self, rule_label, is_enabled):
        item_text = f"Regel: {rule_label}\nAktiviert: {is_enabled}"
        item = QtWidgets.QListWidgetItem(item_text)
        self.ruleListWidget.addItem(item)    

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

        # Layout für die Anzeige der Regeln
        y = 120  # Anfangsposition für y-Koordinate

        for rule in onto.rules():

            # Zugriff auf das swrl2:isRuleEnabled-Attribut
            is_enabled = rule.isRuleEnabled.first()
            # Zugriff auf das Label der Regel
            rule_label = rule.label.first()
            # Ausgabe des Labels und des Status der Regel
            print("Regel:", rule_label)
            print("Aktiviert:", is_enabled)
            
            self.rule_list.append((rule_label, is_enabled))

        # Regeln nach Namen sortieren, um die Suchergebnisse hervorzuheben
        self.rule_list.sort(key=lambda x: -x[0].lower().find(self.rule_lineEdit.text().lower()))

        # Liste aktualisieren
        self.updateRuleListWidget()
            

        self.test = "Test neu!"
        self.onto = onto
        
    def search_rules(self, text):
        # Regeln nach Namen sortieren und Liste aktualisieren
        self.rule_list.sort(key=lambda x: -x[0].lower().find(text.lower()))
        self.updateRuleListWidget()

    def updateRuleListWidget(self):
        # Liste leeren
        self.ruleListWidget.clear()

        # Durchsuche die sortierte Regel-Liste nach dem eingegebenen Text
        for rule_label, is_enabled in self.rule_list:
            item_text = f"Regel: {rule_label}\nAktiviert: {is_enabled}"
            item = QtWidgets.QListWidgetItem(item_text)
            # Hervorhebung der Übereinstimmungen in hellblau
            if self.rule_lineEdit.text().lower() in rule_label.lower():
                item.setBackground(QtGui.QColor("lightblue"))
            self.ruleListWidget.addItem(item)


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