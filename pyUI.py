#!/usr/bin/env python

import os
import sys
import json
import re

from pygments import highlight
from pygments.lexers import CLexer
from pygments.formatters import HtmlFormatter

from PySide import QtCore, QtGui, QtXml
from PySide.QtGui import QMainWindow, QPushButton, QApplication, QFileDialog, QMessageBox
 
from ui_test1 import Ui_MainWindow
from ui_code  import Ui_CodeWindow

import pickle

def json2xml(json_obj, mytag="Node", line_padding=""):
	result_list = list()

	json_obj_type = type(json_obj)

	cnt = 0 ;
	if json_obj_type is list:
		if len(json_obj)==1:
			return json2xml(json_obj[0], mytag , line_padding)
		for sub_elem in json_obj:
			#print len(json_obj)
			result_list.append(json2xml(sub_elem, "Node" , line_padding))
			cnt += 1
		
		inner = "\n".join(result_list)
		return inner ;
		#print inner
		#return "<"+mytag+">"+ inner +"</"+mytag+">";

	myparams = {}
	if json_obj_type is dict:
		for tag_name in json_obj:
			sub_obj = json_obj[tag_name]
			#result_list.append("<%s>" % (tag_name))
			#print type(sub_obj)
			if ( type(sub_obj) is unicode ) or ( type(sub_obj) is str ) :
				myparams[ tag_name ] = sub_obj 
			else:
				result_list.append(json2xml(sub_obj, tag_name , "\t" + line_padding))
		
		tmp_tag = "<" + mytag ;
		#print myparams
		for attr in myparams:
			tmp_tag = tmp_tag + " " + attr +"='" + myparams[attr] + "'";
		tmp_tag = tmp_tag + ">"
		result_list.insert( 0 , tmp_tag );
		result_list.append("</%s>" % (mytag))

		return "\n".join(result_list)
	
	#if ( json_obj == u"<-" ) or ( json_obj ==u"->" ):
	return "<![CDATA["+json_obj+"]]>"
	#return "%s" % (json_obj)

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
				if ( attribute.nodeName()=="type" ):
					return attribute.nodeValue()
				#attributes.append(attribute.nodeName() + '="' +
				#				  attribute.nodeValue() + '"')
 
			return " ".join(attributes)
 
		if index.column() == 2:
			for i in range(0, attributeMap.count()):
				attribute = attributeMap.item(i)
				if ( attribute.nodeName()=="value" ):
					return attribute.nodeValue()
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

ignoreList = ['int', 'float', 'char', '@params-cnt']

class SymItem(object):
	def __init__(self, node, row, parent=None):
		self.domNode = node
		# Record the item's location within its parent.
		self.rowNumber = row
		self.parentItem = parent
		self.itemList = None
		if type(node[1]) == type({}):
			self.itemList = []
			for tup in node[1].items():
				if tup[0] in ignoreList:
					pass
				elif tup[0][0:7]!='@fields' and node[0][0:7]=='@struct':
					pass
				else:
					self.itemList.append(tup)
				
			self.childItems = {}
		else:
			self.childItems = None
 
	def node(self):
		return self.domNode

	def parent(self):
		return self.parentItem
 
	def child(self, i):
		if i in self.childItems:
			return self.childItems[i]
 
		if i >= 0 and i < len(self.itemList):
			childNode = self.itemList[i]
			if childNode[0][0:7] != "@_func_" or self.domNode[0][0:7] != "@_func_":
				childItem = SymItem(childNode, i, self)
			else:
				childItem = SymItem((childNode[0], childNode[0]), i, self)
			self.childItems[i] = childItem
			return childItem
 
		return None
 
	def row(self):
		return self.rowNumber

	def childCount(self):
		if type(self.domNode[1]) == type({}):
			return len(self.domNode[1].items())
		else:
			return 0
 
 
class SymModel(QtCore.QAbstractItemModel):
	def __init__(self, document, parent=None):
		super(SymModel, self).__init__(parent)
 
		self.domDocument = document
 
		self.rootItem = SymItem(self.domDocument, 0)
 
	def columnCount(self, parent):
		return 2
 
	def data(self, index, role):
		if not index.isValid():
			return None
 
		if role != QtCore.Qt.DisplayRole:
			return None
 
		item = index.internalPointer()
 
		node = item.node()
 
		if index.column() == 0:
			return node[0]
 
		elif index.column() == 1:
			if type(node[1]) != type({}):
				return node[1]
			else:
				return ""
 
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
 
		return parentItem.childCount()

class CodeWindow(QMainWindow, Ui_CodeWindow):
	def __init__( self , html , parent=None):
		super( CodeWindow , self).__init__(parent)
		self.setupUi(self)
		self.setContent( html )
	def close( self ):
		super( CodeWindow , self ).close()
	
	
class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.fileName = ""
		self.codeFrame = None
		self.grammarButt.setEnabled(False)
		self.semanticButt.setEnabled(False)
		self.symbolTable.setEnabled(False)
		self.codeGenButt.setEnabled(False)
		self.lexButt.setEnabled(False)
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
		#print fileName
		if self.fileName == u'':
			return
		#os.system("highlight --syntax=c --inline-css " + fileName[0] + " > tmp.highlight")
		#with open("tmp.highlight", 'r') as f:
		with open(self.fileName, 'r') as f:
			html=highlight( f.read() , CLexer() , HtmlFormatter() )
		with open("./misc/github.css", 'r') as f:
			html = "<html><head><style>"+f.read()+"</style></head><body>"+html+"</body></html>"
		#os.system("rm tmp.highlight")
		#print html
		#self.consoleField.setHtml( html )
		self.consoleField.setHtml("")
		if self.codeFrame is None:
			self.codeFrame = CodeWindow("", self)
		self.codeFrame.setContent( html )
		self.codeFrame.show()
		self.lexButt.setEnabled(True)
		self.semanticButt.setEnabled(False)
		self.codeGenButt.setEnabled(False)
		self.grammarButt.setEnabled(False)
	def lexCheck(self):
		self.useConsole()
		okay = True
		with os.popen("python dllex.py < " + self.fileName) as f:
			content=""
			for line in f.readlines():
				if  line[0:7]=='Illegal' :
					okay = False
					line = '<font style="color:red;">' + line + '</font>';
				content = content + line + "<br/>" ;
			self.consoleField.setHtml( content )
		self.grammarButt.setEnabled(True)
		if not okay:
			msgBox = QMessageBox()
			msgBox.setText("Lexer Error Occurred!")
			msgBox.exec_()
		
		
	def grammarAnalysis(self):
		self.useTree()
		os.system("python dlcheck.py < "+ self.fileName + "| tail -n +3 > tmp.json")
		try:
			with open("tmp.json", 'r') as f:
				j = json.loads(f.read())
				text_file = open("tmp.xml", "w")
				#text_file.write("<body>\n")
				text_file.write(json2xml(j))
				#text_file.write("</body>\n")
				text_file.close()
		except:
			msgBox = QMessageBox()
			msgBox.setText("Syntax Error.")
			msgBox.exec_()
			self.useConsole()
			with open("tmp.json", 'r') as f:
				self.consoleField.setPlainText( f.read() )
			return
			
		#os.system("rm tmp.json")
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
		#os.system("rm tmp.xml")
		self.semanticButt.setEnabled(True)
		self.symbolTable.setEnabled(True)
	def semanticCheck(self):
		self.codeGenButt.setEnabled(True)
		pass
	def showSymbolTable(self):
		self.useTree()
		os.system("python dlcheck.py --serializeTheOBJ < "+ self.fileName + " | grep -n -P '(Syntax error)|(Fatal)' > symTab")
		with open("symTab", 'r') as f:
			tmp = f.read()
			if len(tmp) != 0:
				msgBox = QMessageBox()
				msgBox.setText("Panic!\n"+tmp)
				msgBox.exec_()
				return
		inputFile = open("symTab.dump", 'rb')
		context = pickle.load(inputFile)
		inputFile.close()
		print context
		
		if True:
			newModel = SymModel(("root", context), self)
			self.treeView.setModel(newModel)
			self.model = newModel
			self.xmlPath = fileName
		#self.useConsole()
		#self.consoleField.setPlainText(str)
		pass
	def codeGen(self):
		print "hello world"
		pass
	def close(self):
		if self.codeFrame is not None:
			self.codeFrame.close();
		super(MainWindow, self).close()
	   
if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()	
	app.exec_()
