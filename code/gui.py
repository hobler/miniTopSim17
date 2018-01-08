"""
Shows a GUI to create a Config File
"""
import os
import sys

from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import *
import configparser as cp


# noinspection PyPep8Naming
class ConfigGUI(QWidget):
    """
    The Master Class for the GUI
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("miniTopSim Config GUI")
        # self.setMinimumWidth(450)

        buttonPanel = QHBoxLayout()
        btnOK = QPushButton("OK", self)
        # noinspection PyUnresolvedReferences
        btnOK.clicked.connect(self.on_ok_click)
        btnCancel = QPushButton("Cancel", self)
        # noinspection PyUnresolvedReferences
        btnCancel.clicked.connect(self.close)
        buttonPanel.addWidget(btnOK)
        buttonPanel.addWidget(btnCancel)
        self.sections = list()

        layout = QVBoxLayout()
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        layout.addLayout(buttonPanel)
        self.setLayout(layout)

    def addSection(self, section):
        """
        Sets a Section and returns it
        :param section: Section
        """
        self.sections.append(section)
        self.tabs.addTab(section, section.name)

    def checkParameters(self):
        """
        Checks whether all parameters are valid
        :return: bool
        """
        for section in self.sections:
            for param in section.parameters:
                if not param.isValid():
                    QMessageBox.critical(self, "Validation Error",
                                         "{0}/{1} is not valid\nViolates: \"{2}\"".format(param.section, param.name,
                                                                                          param.query),
                                         QMessageBox.Ok, QMessageBox.Ok)
                    return False
        return True

    def saveConfiguration(self, fileName=os.path.join(os.getcwd(), 'beispiel.cfg')):
        """
        Saves the current configuration (independent of correctness)
        :param fileName: String
        """
        if os.path.exists(fileName):
            os.remove(fileName)
        db_write = cp.ConfigParser()
        # db_write.read(fileName)
        for section in self.sections:
            db_write.add_section(section.name)
            for param in section.parameters:
                value = globals()[param.name]
                if type(value) == str:
                    value = "\'{}\'".format(value)
                else:
                    value = str(value)
                db_write.set(section.name, param.name, value)
        file = open(fileName, 'w')
        db_write.write(file)
        file.close()

    def on_ok_click(self):
        """
        Event for OK button click
        """
        if self.checkParameters():
            self.saveConfiguration()
            self.close()


class Section(QWidget):
    """
    Class Holding the Parameters for a Section
    """

    def __init__(self, name):
        super(Section, self).__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.parameters = list()
        self.name = name

    def addParameter(self, param):
        """
        Adds a Parameter to the Grid
        :type param: Parameter
        """
        next_row = self.grid.rowCount()
        self.grid.addWidget(param.gui_label, next_row, 0 )
        self.grid.addWidget(param.gui_element, next_row, 1)
        self.parameters.append(param)


class Parameter:
    """
    Holds One Parameter of a Section
    """

    def __init__(self, section, name, default, query, comment):
        self.name = name.upper()
        self.section = section
        self.query = query
        self.comment = comment.strip('\'').strip()
        self.gui_element = None
        if type(default) == type:
            self.type = default
            self.default = default()
        else:
            self.default = default
            if query is not None and ' in ' in query:
                self.type = list
                self.items = eval(query.split(" in ")[1].strip())
            else:
                self.type = type(default)
        globals()[self.name] = self.default

        # Create GUI Element
        self.gui_label = QLabel(self.name)
        if self.type == bool:
            gui_element = QCheckBox()
            gui_element.setChecked(self.default)
            # noinspection PyUnresolvedReferences
            gui_element.stateChanged.connect(lambda: self.isValid())
        elif self.type == float:
            gui_element = QLineEdit(str(self.default))
            gui_element.setValidator(QDoubleValidator())
            # noinspection PyUnresolvedReferences
            gui_element.textChanged.connect(lambda: self.isValid())
        elif self.type == str:
            gui_element = QLineEdit(str(self.default))
            # noinspection PyUnresolvedReferences
            gui_element.textChanged.connect(lambda: self.isValid())
        elif self.type == list:
            gui_element = QComboBox()
            gui_element.addItems(self.items)
            # noinspection PyUnresolvedReferences
            gui_element.currentIndexChanged.connect(lambda: self.isValid())
        else:
            gui_element = None
            print("UNKNOWN PARAMETER TYPE!!!")

        if self.comment is not None:
            gui_element.setToolTip(self.comment)
        gui_element.setMinimumWidth(100)
        self.gui_element = gui_element
        self.isValid()

    def isValid(self):
        """
        Checks if entered Value is valid
        :rtype: bool
        """
        gui_element = self.gui_element
        if self.type == str:
            globals()[self.name] = gui_element.text()
        elif self.type is float:
            globals()[self.name] = float(gui_element.text())
        elif self.type is bool:
            globals()[self.name] = gui_element.isChecked()
        elif self.type is list:
            globals()[self.name] = gui_element.currentText()
        if self.query is None:
            return True
        else:
            if not (eval(self.query)):
                print("Invalid Value in " + self.name)
                gui_element.setStyleSheet('border: 2px solid red;')
                violation = "\nViolates: \"{}\"".format(self.query)
                gui_element.setToolTip(self.comment + "\n" + violation)
                return False
            else:
                gui_element.setStyleSheet('')
                gui_element.setToolTip(self.comment)
                return True


def loadSectionGui(section=None):
    """
    Executes Gui for a DB-Section
    :rtype: ConfigGUI
    :param section: String
    """
    db_file = os.path.join(os.path.dirname(__file__), 'parameters.db')
    db = cp.ConfigParser()
    db.read(db_file)
    sections = list()
    if section is None:
        sections = db.sections()
    else:
        if section not in db.sections():
            print("Unknown Section\nAvailable are:\n\t", end='')
            print(db.sections())
            exit(-1)
        else:
            sections.append(section)

    config_gui = ConfigGUI()

    for section in sections:
        gui_section = Section(section)
        for option in db.options(section):
            gui_section.addParameter(Parameter(section, option.upper(), *eval(db.get(section, option))))
        config_gui.addSection(gui_section)
    config_gui.show()
    return config_gui


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_section = sys.argv[1]
        print("Using Section: " + arg_section)
        app = QApplication(sys.argv)
        if arg_section == "all":
            gui = loadSectionGui()
        else:
            gui = loadSectionGui(arg_section)
        sys.exit(app.exec_())
    else:
        print("No Section Provided\nUsage:\n\tpython3 <path-to-code>gui.py <all / section- name>")
        exit(-1)
