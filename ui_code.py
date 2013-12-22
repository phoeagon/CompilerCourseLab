# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compilerUI.ui'
#
# Created: Sun Nov 17 22:06:16 2013
#	  by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_CodeWindow(object):
	def setContent( self , html ) :
		self.consoleField.setHtml(html)
		
	def setupUi(self, MainWindow, title="Code"):
		MainWindow.setObjectName("CodeWindow")
		MainWindow.resize(687, 638)
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.consoleField = QtGui.QTextEdit(self.centralwidget)
		self.consoleField.setEnabled(True)
		self.consoleField.setGeometry(QtCore.QRect(40, 150, 601, 431))
		self.consoleField.setReadOnly(True)
		self.consoleField.setObjectName("consoleField")
		MainWindow.setCentralWidget(self.consoleField)
		self.retranslateUi(MainWindow, title)

	def retranslateUi(self, MainWindow, title):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("Code", title, None, QtGui.QApplication.UnicodeUTF8))
		self.consoleField.setHtml(QtGui.QApplication.translate("Code", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


