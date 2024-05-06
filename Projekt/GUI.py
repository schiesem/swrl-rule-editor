from PyQt5.QtWidgets import * 
from PyQt5 import uic
import os
from owlready2 import *
import owlready2
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidgetItem, QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel
from PyQt5.QtCore import Qt


#Main Window
class SWRLRuleEditor(QMainWindow):

    def __init__(self):
        super(SWRLRuleEditor, self).__init__()
        uic.loadUi("Projekt\MainWindow.ui", self)
        self.show()
        ontology_names = list_files_in_folder("Ontologien")
        self.comboBoxOntologies.addItems(ontology_names)
        self.comboBoxOntologies.setCurrentIndex(-1)
        self.comboBoxOntologies.currentIndexChanged.connect(self.ontologySelected)
        self.onto = get_ontology("file://" + "Ontologien\ghibli.rdf").load()                    #ontologie vor laden, wird dann später überschrieben, wenn eine ausgewählt wird. hier leere ontologie einfügen.
        self.pushButton.clicked.connect(self.open_second_window)
        self.rule_listWidget.itemClicked.connect(self.open_second_window)

        # Suchfeld für Regeln
        self.rule_lineEdit.textChanged.connect(self.search_rules)
        self.rule_lineEdit.installEventFilter(self)

        #listwidget
        self.rule_listWidget.installEventFilter(self)

        # Liste für die gefundenen Regeln
        self.rule_list = []

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
        
        # Regeln des ListWidgets löschen und Liste leeren
        self.rule_listWidget.clear()
        self.rule_list = []

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
        

            # Regeln hinzufügen
        for rule in self.onto.rules():
            is_enabled = rule.isRuleEnabled.first() if rule.isRuleEnabled else False
            rule_label = rule.label.first() if rule.label else "Unnamed Rule"
            self.rule_list.append(rule)  # Speichere das Regelobjekt selbst
    
        # Regeln nach Namen sortieren, um die Suchergebnisse hervorzuheben
        self.rule_list.sort(key=lambda x: x.label.first().lower())
    
        # Liste aktualisieren
        self.updateRuleListWidget()
    
    
        self.test = "Test neu!"
        self.onto = onto


    def search_rules(self, text):
        # Regeln nach Namen sortieren und Liste aktualisieren
        self.rule_list.sort(key=lambda x: -x[0].lower().find(text.lower()))
        self.updateRuleListWidget()

    def updateRuleListWidget(self):
        self.rule_listWidget.clear()
        for rule in self.rule_list:
            is_enabled = rule.isRuleEnabled.first() if rule.isRuleEnabled else False
            widget_item = QtWidgets.QListWidgetItem(self.rule_listWidget)
            item_widget = RuleWidgetItem(rule, is_enabled)

            if self.rule_lineEdit.text().lower() in rule.label.first().lower():
                item_widget.setStyleSheet("background-color: lightblue;")

            self.rule_listWidget.addItem(widget_item)
            self.rule_listWidget.setItemWidget(widget_item, item_widget)
            widget_item.setSizeHint(item_widget.sizeHint())
        
   
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
        listOfClasses = return_elements(self.onto.classes())
        listOfProperties = return_elements(self.onto.properties())
        OntologyName = self.comboBoxOntologies.currentText()
        self.second_window = SecondWindow(OntologyName, self.onto, listOfClasses, listOfProperties)
        self.second_window.show()

#Rule Editor Window
class SecondWindow(QMainWindow):
    def __init__(self, OntologyName, onto, listOfClasses, listOfProperties ):
        super(SecondWindow, self).__init__()
        uic.loadUi("Projekt\SecondWindow.ui", self)
        self.show()
    
        self.lines = []  # Liste zum Speichern der Linienlayouts
        self.lines_2 = []  # Falls Sie zwei verschiedene Layouts haben
 
        self.Label_selectedOntology.setText(OntologyName)

        self.add_line(listOfClasses, listOfProperties)
        self.add_line_2(listOfClasses, listOfProperties)
        self.AddLine.clicked.connect(lambda: self.add_line(listOfClasses, listOfProperties))
        self.AddLine_2.clicked.connect(lambda: self.add_line_2(listOfClasses, listOfProperties))
        self.RemoveLine.clicked.connect(self.remove_line)
        self.RemoveLine_2.clicked.connect(self.remove_line_2)
        self.pushButtonAddToOnto.clicked.connect(lambda: self.add_to_onto_and_return(onto))
 
 
 
    def add_line(self, listOfClasses, listOfProperties):        #add lines on premise side
        line_layout = QHBoxLayout()        #create line

        comboboxClass1 = QComboBox()        #create combobox for class1
        comboboxClass1.addItems(listOfClasses)
        comboboxClass1.setCurrentIndex(-1)
        line_layout.addWidget(comboboxClass1)

        qlineeditVar1 = QLineEdit()         #create lineEdit for Var1 of Class1
        line_layout.addWidget(qlineeditVar1)

        comboboxProperty = QComboBox()      #create combobox for property to connect the variables with
        comboboxProperty.addItems(listOfProperties)
        comboboxProperty.setCurrentIndex(-1)
        line_layout.addWidget(comboboxProperty)

        comboboxClass2 = QComboBox()        #create combobox for class2
        comboboxClass2.addItems(listOfClasses)
        comboboxClass2.setCurrentIndex(-1)
        line_layout.addWidget(comboboxClass2)

        qlineeditVar2 = QLineEdit()         #create lineEdit for Var2 of Class2
        line_layout.addWidget(qlineeditVar2)
 
        self.verticalLayout.addLayout(line_layout)
        self.verticalLayout.setAlignment(Qt.AlignTop)
        self.lines.append(line_layout)      #add line to vertical layout
 
    def add_line_2(self, listOfClasses, listOfProperties):      #add lines on conclusion side
        line_layout = QHBoxLayout()        #create line

        comboboxClass1 = QComboBox()        #create combobox for class1
        comboboxClass1.addItems(listOfClasses)
        comboboxClass1.setCurrentIndex(-1)
        line_layout.addWidget(comboboxClass1)

        qlineeditVar1 = QLineEdit()         #create lineEdit for Var1 of Class1
        line_layout.addWidget(qlineeditVar1)

        comboboxProperty = QComboBox()      #create combobox for property to connect the variables with
        comboboxProperty.addItems(listOfProperties)
        comboboxProperty.setCurrentIndex(-1)
        line_layout.addWidget(comboboxProperty)

        comboboxClass2 = QComboBox()        #create combobox for class2
        comboboxClass2.addItems(listOfClasses)
        comboboxClass2.setCurrentIndex(-1)
        line_layout.addWidget(comboboxClass2)

        qlineeditVar2 = QLineEdit()         #create lineEdit for Var2 of Class2
        line_layout.addWidget(qlineeditVar2)
 
        self.verticalLayout_2.addLayout(line_layout)
        self.verticalLayout_2.setAlignment(Qt.AlignTop)
        self.lines_2.append(line_layout)      #add line to vertical layout
 
    def remove_line(self):
        if len(self.lines) > 1:
            line_layout = self.lines.pop()  # Letztes Layout aus der Liste entfernen
            for i in reversed(range(line_layout.count())):
                widget = line_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()  # Löscht das Widget korrekt
                line_layout.removeWidget(widget)
            self.verticalLayout.removeItem(line_layout)

    def remove_line_2(self):
        if len(self.lines_2) > 1:
            line_layout = self.lines_2.pop()  # Letztes Layout aus der Liste entfernen
            for i in reversed(range(line_layout.count())):
                widget = line_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()  # Löscht das Widget korrekt
                line_layout.removeWidget(widget)
            self.verticalLayout.removeItem(line_layout)

    def add_to_onto_and_return(self, onto):
        #add rule to Ontologie logic missing
        rule_str = "cloudsystem(?p) ^ hasAssignment(?p, ?T) ^ Train(?T) ^ AiSystem(?a) -> hasAssignment(?a, ?T)  " #test
        #rule_str = "Person(?p) ^ hasAge(?p, ?age) ^ swrlb:greaterThan(?age, 18) -> Adult(?p)"
        def parse_swr_rule(rule_str):
            return onto.world.swr_parse(rule_str)
    
        # SWRL-Regel zu Ontologie hinzufügen
        try:
            rule = parse_swr_rule(rule_str)
            onto.rules.append(rule)
            print(f"SWRL-Regel hinzugefügt: {rule_str}")
        except Exception as e:
            print(f"Fehler beim Hinzufügen der SWRL-Regel: {e}")

        # Ontologie speichern
        onto.save()



        self.close()


class RuleWidgetItem(QtWidgets.QWidget):
    def __init__(self, rule, is_enabled):
        super().__init__()
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.rule = rule
        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.setChecked(is_enabled)
        self.checkbox.stateChanged.connect(self.toggle_rule)
        label = QtWidgets.QLabel(f"Regel: {rule.label.first()}")
        layout.addWidget(label)
        layout.addWidget(self.checkbox)

    def toggle_rule(self, state):
        new_state = state == QtCore.Qt.Checked
        self.rule.isRuleEnabled = [new_state]
        # Speichere die Ontologie in einer lokalen Datei, statt URL verwenden
        self.save_ontology(self.rule.namespace.ontology)

    def save_ontology(self, ontology):
        # Stellen Sie sicher, dass der Pfad existiert und gültig ist
        save_path = "Ontologien\ghibli.rdf"  # Ersetzen Sie dies durch den tatsächlichen Pfad zu Ihrer Ontologie-Datei
        ontology.save(file=save_path)


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