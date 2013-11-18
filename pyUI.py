#!/usr/bin/env python

import os
import sys
import json

from pygments import highlight
from pygments.lexers import CLexer
from pygments.formatters import HtmlFormatter

from PySide import QtCore, QtGui, QtXml
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QFileDialog
 
from ui_test1 import Ui_MainWindow

def json2xml(json_obj, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("<%s>" % (tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("</%s>" % (tag_name))

        return "\n".join(result_list)

    return "%s" % (json_obj)

class DomItem(object):
    def __init__(self, node, row, parent=None):
        self.domNode = node
        # Record the item's location within its parent.
        self.rowNumber = row
        self.parentItem = parent
        self.childItems = {}
 
    def node(self):
        return self.domNode
 
    def parent(self):
        return self.parentItem
 
    def child(self, i):
        if i in self.childItems:
            return self.childItems[i]
 
        if i >= 0 and i < self.domNode.childNodes().count():
            childNode = self.domNode.childNodes().item(i)
            childItem = DomItem(childNode, i, self)
            self.childItems[i] = childItem
            return childItem
 
        return None
 
    def row(self):
        return self.rowNumber
 
 
class DomModel(QtCore.QAbstractItemModel):
    def __init__(self, document, parent=None):
        super(DomModel, self).__init__(parent)
 
        self.domDocument = document
 
        self.rootItem = DomItem(self.domDocument, 0)
 
    def columnCount(self, parent):
        return 3
 
    def data(self, index, role):
        if not index.isValid():
            return None
 
        if role != QtCore.Qt.DisplayRole:
            return None
 
        item = index.internalPointer()
 
        node = item.node()
        attributes = []
        attributeMap = node.attributes()
 
        if index.column() == 0:
            return node.nodeName()
 
        elif index.column() == 1:
            for i in range(0, attributeMap.count()):
                attribute = attributeMap.item(i)
                attributes.append(attribute.nodeName() + '="' +
                                  attribute.nodeValue() + '"')
 
            return " ".join(attributes)
 
        if index.column() == 2:
            value = node.nodeValue()
            if value is None:
                return ''
 
            return ' '.join(node.nodeValue().split('\n'))
 
        return None
 
    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
 
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
 
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Name"
 
            if section == 1:
                return "Attributes"
 
            if section == 2:
                return "Value"
 
        return None
 
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
 
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
 
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()
 
    def parent(self, child):
        if not child.isValid():
            return QtCore.QModelIndex()
 
        childItem = child.internalPointer()
        parentItem = childItem.parent()
 
        if not parentItem or parentItem == self.rootItem:
            return QtCore.QModelIndex()
 
        return self.createIndex(parentItem.row(), 0, parentItem)
 
    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
 
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
 
        return parentItem.node().childNodes().count()

 
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.fileName = ""
    def useConsole(self):
        self.consoleField.setVisible(True)
        self.treeView.setVisible(False)
    def useTree(self):
        self.treeView.setVisible(True)
        self.consoleField.setVisible(False)
    def openFile(self):
        self.useConsole()
        fileName = QFileDialog.getOpenFileName(self, self.tr("Open Image"), "~/", self.tr("Source Files (*.dl)"))
        self.fileName = fileName[0]
        print fileName
        #os.system("highlight --syntax=c --inline-css " + fileName[0] + " > tmp.highlight")
        #with open("tmp.highlight", 'r') as f:
        with open(self.fileName, 'r') as f:
			html=highlight( f.read() , CLexer() , HtmlFormatter() )
        with open("./misc/github.css", 'r') as f:
			html = "<html><head><style>"+f.read()+"</style></head><body>"+html+"</body></html>"
        #os.system("rm tmp.highlight")
        print html
        self.consoleField.setHtml( html )
    def lexCheck(self):
        self.useConsole()
        with os.popen("python dllex.py < " + self.fileName) as f:
            self.consoleField.setPlainText(f.read())
    def grammarAnalysis(self):
        self.useTree()
        os.system("python dlcheck.py < "+ self.fileName + "| tail -n +4 > tmp.json")
        with open("tmp.json", 'r') as f:
            j = json.loads(f.read())
            text_file = open("tmp.xml", "w")
            text_file.write("<body>\n")
            text_file.write(json2xml(j))
            text_file.write("</body>\n")
            text_file.close()
        os.system("rm tmp.json")
        fileName = "tmp.xml"
        if True:
            f = QtCore.QFile(fileName)
            if f.open(QtCore.QIODevice.ReadOnly):
                document = QtXml.QDomDocument()
                if document.setContent(f):
                    newModel = DomModel(document, self)
                    self.treeView.setModel(newModel)
                    self.model = newModel
                    self.xmlPath = fileName
                f.close()
        os.system("rm tmp.xml")
    def semanticCheck(self):
        pass
    def codeGen(self):
        pass
    def close(self):
        super(MainWindow, self).close()
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()    
    app.exec_()
