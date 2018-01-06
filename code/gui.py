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

        buttonPanel = QHBoxLayout()
        btnOK = QPushButton("OK", self)
        # noinspection PyUnresolvedReferences
        btnOK.clicked.connect(self.on_ok_click)
        btnCancel = QPushButton("Cancel", self)
        # noinspection PyUnresolvedReferences
        btnCancel.clicked.connect(self.close)
        buttonPanel.addWidget(btnOK)
        buttonPanel.addWidget(btnCancel)

        layout = QVBoxLayout()
        self.section = SectionGrid()
        layout.addLayout(self.section)
        layout.addLayout(buttonPanel)
        self.setLayout(layout)

    def setSection(self, name):
        """
        Sets a Section and returns it
        :rtype: SectionGrid
        :param name: String
        """
        self.section.name = name
        return self.section

    def checkParamters(self):
        """
        Checks whether all parameters are valid
        :return: bool
        """
        for param in self.section.parameters:
            if not param.isValid():
                QMessageBox.critical(self, "Validation Error", "{0}/{1} is not valid\nViolates: \"{2}\"".format(param.section,param.name,param.query), QMessageBox.Ok,
                                     QMessageBox.Ok)
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
        db_write.add_section(self.section.name)
        for param in self.section.parameters:
            value = globals()[param.name]
            if type(value) == str:
                value = "\'{}\'".format(value)
            else:
                value = str(value)
            db_write.set(self.section.name, param.name, value)
        file = open(fileName, 'w')
        db_write.write(file)
        file.close()

    def on_ok_click(self):
        """
        Event for OK button click
        """
        if self.checkParamters():
            self.saveConfiguration()
            self.close()


class SectionGrid(QVBoxLayout):
    """
    Class Holding the Parameters for a Section
    """

    def __init__(self, name=""):
        super(SectionGrid, self).__init__()
        self.grid = QGridLayout()
        self.addLayout(self.grid)
        self.parameters = list()
        self.name = name

    def addParameter(self, param):
        """
        Adds a Parameter to the Grid
        :type param: Parameter
        """
        label = QLabel(param.name)
        if param.type == bool:
            inp = QCheckBox()
            inp.setChecked(param.default)
            # noinspection PyUnresolvedReferences
            inp.stateChanged.connect(lambda: param.isValid(inp))
        elif param.type == float:
            inp = QLineEdit(str(param.default))
            inp.setValidator(QDoubleValidator())
            # noinspection PyUnresolvedReferences
            inp.textChanged.connect(lambda: param.isValid(inp))
        elif param.type == str:
            inp = QLineEdit(str(param.default))
            # noinspection PyUnresolvedReferences
            inp.textChanged.connect(lambda: param.isValid(inp))
        else:
            inp = None
            print("UNKNOWN PARAMETER TYPE!!!")

        if param.comment is not None:
            inp.setToolTip(param.comment)
        inp.setMinimumWidth(100)
        param.gui_element = inp
        param.isValid(inp)
        nextrow = self.grid.rowCount()
        self.grid.addWidget(label, nextrow, 0, )
        self.grid.addWidget(inp, nextrow, 1)
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
            self.type = type(default)
            self.default = default
        globals()[self.name] = self.default

    def isValid(self, gui_element=None):
        """
        Checks if entered Value is valid
        :type gui_element: QWidget
        """
        if gui_element is None:
            if self.gui_element is not None:
                gui_element = self.gui_element
            else:
                return False

        if self.type == str:
            globals()[self.name] = gui_element.text()
        elif self.type is float:
            globals()[self.name] = float(gui_element.text())
        elif self.type is bool:
            globals()[self.name] = gui_element.isChecked()

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
                gui_element.toolTip()
                gui_element.setToolTip(self.comment)
                return True


def loadSectionGui(section):
    """
    Executes Gui for a DB-Section
    :rtype: ConfigGUI
    :param section: String
    """
    db_file = os.path.join(os.path.dirname(__file__), 'parameters.db')
    db = cp.ConfigParser()
    db.read(db_file)
    if section not in db.sections():
        print("Unknown Section\nAvailable are:\n\t", end='')
        print(db.sections())
        exit(-1)

    configgui = ConfigGUI()

    gs = configgui.setSection(section)
    for option in db.options(section):
        gs.addParameter(Parameter(section, option.upper(), *eval(db.get(section, option))))
        configgui.show()
    return configgui


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_section = sys.argv[1]
        print("Using Section: " + arg_section)
        app = QApplication(sys.argv)
        gui = loadSectionGui(arg_section)
        sys.exit(app.exec_())
    else:
        print("No Section Provided\nUsage:\n\tpython3 <path-to-code>gui.py <section- name>")
        exit(-1)
