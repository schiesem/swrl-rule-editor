from PyQt5.QtWidgets import * 
from PyQt5 import uic
import os
from owlready2 import *
import owlready2
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton
from PyQt5.QtCore import Qt


#Main Window
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
        self.pushButton.clicked.connect(self.open_second_window)

        # Suchfeld für Regeln
        self.rule_lineEdit.textChanged.connect(self.search_rules)
        self.rule_lineEdit.installEventFilter(self)

        #listwidget
        self.rule_listWidget.installEventFilter(self)

        # Liste für die gefundenen Regeln
        self.rule_list = []

    #def eventFilter(self, obj, event):
    #    if obj == self.searchLineEdit:
    #       
    #       if event.type() == QtCore.QEvent.MouseButtonPress:
    #        # Bei Klick auf die Suchleiste die Liste ausblenden
    #        self.ruleListWidget.hide()
    #        return False
    #       
    #    elif obj == self.ruleListWidget:
    #        if event.type() == QtCore.QEvent.MouseButtonPress:
    #        # Bei Klick auf die Liste die Liste anzeigen
    #        self.ruleListWidget.show()
    #        return False
    #    
    #    return super().eventFilter(obj, event)    
        
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
  
        #selection of ontology
        file_name = f"{selected_text}"
        folder_path = r"Ontologien"
        file_path_save = os.path.join(folder_path, file_name)
        onto = get_ontology("file://" + file_path_save).load()
        print("The ontology has been loaded")                                       #testing
        
        
        #Creates class-hierarchy
        self.treeOfClasses.clear()
        hierarchy_classes_data = create_hierarchy(Thing)
        self.printClassTree(hierarchy_classes_data)

        self.treeOfObjectProperties.clear()
        hierarchy_ObjectProperties_data = create_hierarchy(ObjectProperty)
        self.printObjectTree(hierarchy_ObjectProperties_data)

        self.treeOfDataProperties.clear()
        hierarchy_DataProperties_data = create_hierarchy(DataProperty)
        self.printDataTree(hierarchy_DataProperties_data)



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
        self.rule_listWidget.clear()

        # Durchsuche die sortierte Regel-Liste nach dem eingegebenen Text
        for rule_label, is_enabled in self.rule_list:
            item_text = f"Regel: {rule_label}\nAktiviert: {is_enabled}"
            item = QtWidgets.QListWidgetItem(item_text)
            # Hervorhebung der Übereinstimmungen in hellblau
            if self.rule_lineEdit.text().lower() in rule_label.lower():
                item.setBackground(QtGui.QColor("lightblue"))
            self.rule_listWidget.addItem(item)

        
   
    def printClassTree(self, hierarchy_data):
        visited = []

        # Function to recursively traverse and add items to the tree
        def add_items(parent_item, items):
            for item in items:
                if item not in visited:
                    child_item = QTreeWidgetItem(parent_item)
                    child_item.setText(0, item)
                    child_item.setExpanded(True)
                    visited.append(item)
                    if item in hierarchy_data:
                        add_items(child_item, hierarchy_data[item])

        for name in hierarchy_data:
            if name not in visited:
                # Create parent item
                parent_item = QTreeWidgetItem(self.treeOfClasses)
                parent_item.setText(0, name)
                parent_item.setExpanded(True)
                visited.append(name)
                if name in hierarchy_data:
                    add_items(parent_item, hierarchy_data[name])
        self.treeOfClasses.header().setStretchLastSection(False)
        self.treeOfClasses.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def printObjectTree(self, hierarchy_data):
        visited = []

        # Function to recursively traverse and add items to the tree
        def add_items(parent_item, items):
            for item in items:
                if item not in visited:
                    child_item = QTreeWidgetItem(parent_item)
                    child_item.setText(0, item)
                    child_item.setExpanded(True)
                    visited.append(item)
                    if item in hierarchy_data:
                        add_items(child_item, hierarchy_data[item])

        for name in hierarchy_data:
            if name not in visited:
                # Create parent item
                parent_item = QTreeWidgetItem(self.treeOfObjectProperties)
                parent_item.setText(0, name)
                parent_item.setExpanded(True)
                visited.append(name)
                if name in hierarchy_data:
                    add_items(parent_item, hierarchy_data[name]) 
        self.treeOfObjectProperties.header().setStretchLastSection(False)
        self.treeOfObjectProperties.header().setSectionResizeMode(QHeaderView.ResizeToContents)               

    def printDataTree(self, hierarchy_data):
        visited = []

        # Function to recursively traverse and add items to the tree
        def add_items(parent_item, items):
            for item in items:
                if item not in visited:
                    child_item = QTreeWidgetItem(parent_item)
                    child_item.setText(0, item)
                    child_item.setExpanded(True)
                    visited.append(item)
                    if item in hierarchy_data:
                        add_items(child_item, hierarchy_data[item])

        for name in hierarchy_data:
            if name not in visited:
                # Create parent item
                parent_item = QTreeWidgetItem(self.treeOfDataProperties)
                parent_item.setText(0, name)
                parent_item.setExpanded(True)
                visited.append(name)
                if name in hierarchy_data:
                    add_items(parent_item, hierarchy_data[name])
        self.treeOfDataProperties.header().setStretchLastSection(False)
        self.treeOfDataProperties.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def open_second_window(self):
        self.second_window = SecondWindow()
        self.second_window.show()

#Rule Editor Window
class SecondWindow(QMainWindow):
    def __init__(self):
        super(SecondWindow, self).__init__()
        uic.loadUi("Projekt\SecondWindow.ui", self)
        self.show()

        self.add_line()
        self.add_line_2()
        self.AddLine.clicked.connect(self.add_line)
        self.AddLine_2.clicked.connect(self.add_line_2)
        self.RemoveLine.clicked.connect(self.remove_line)

    def add_line(self):
        # Create horizontal layout for line
        line_layout = QHBoxLayout()

        # Add Line Edits and Combo Boxes
        line_layout.addWidget(QComboBox())
        line_layout.addWidget(QLineEdit())
        line_layout.addWidget(QComboBox())
        line_layout.addWidget(QComboBox())
        line_layout.addWidget(QLineEdit())
        print(line_layout)

        # Add the horizontal layout to the vertical layout
        self.verticalLayout.addLayout(line_layout)
        self.verticalLayout.setAlignment(Qt.AlignTop)

    def add_line_2(self):
        # Create horizontal layout for line
        line_layout = QHBoxLayout()

        # Add Line Edits and Combo Boxes
        line_layout.addWidget(QComboBox())
        line_layout.addWidget(QLineEdit())
        line_layout.addWidget(QComboBox())
        line_layout.addWidget(QComboBox())
        line_layout.addWidget(QLineEdit())


        # Add the horizontal layout to the vertical layout
        self.verticalLayout_2.addLayout(line_layout)
        self.verticalLayout_2.setAlignment(Qt.AlignTop)
        

    def remove_line(self):                                      #not working properly.....................................................................................
        count = self.verticalLayout.count()
        if count == 1:
            return
        item = self.verticalLayout.itemAt(count - 2)
        self.verticalLayout.removeItem(item)



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
            
def create_hierarchy(selected_class):       #recursive function to create hierarchy from ontology. Should be called with root-element as input for selected_class
    hierarchy = {selected_class.__name__: []}
    subclasses = list(selected_class.subclasses())
    for subclass in subclasses:
        hierarchy[selected_class.__name__].append(subclass.__name__)
        hierarchy.update(create_hierarchy(subclass))
    return hierarchy


def main():

    project = QApplication([])
    window = SWRLRuleEditor()
    project.exec_()
    print("!")


if __name__== "__main__":
    main()