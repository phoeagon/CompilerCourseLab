# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'compilerUI.ui'
#
# Created: Sun Nov 17 22:06:16 2013
#      by: pyside-uic 0.2.13 running on PySide 1.1.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(687, 638)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.openButt = QtGui.QPushButton(self.centralwidget)
        self.openButt.setGeometry(QtCore.QRect(30, 20, 114, 32))
        self.openButt.setObjectName("openButt")
        self.lexButt = QtGui.QPushButton(self.centralwidget)
        self.lexButt.setGeometry(QtCore.QRect(30, 70, 141, 71))
        self.lexButt.setObjectName("lexButt")
        self.grammarButt = QtGui.QPushButton(self.centralwidget)
        self.grammarButt.setGeometry(QtCore.QRect(190, 70, 141, 71))
        self.grammarButt.setObjectName("grammarButt")
        self.semanticButt = QtGui.QPushButton(self.centralwidget)
        self.semanticButt.setGeometry(QtCore.QRect(350, 70, 141, 71))
        self.semanticButt.setObjectName("semanticButt")
        self.codeGenButt = QtGui.QPushButton(self.centralwidget)
        self.codeGenButt.setGeometry(QtCore.QRect(510, 70, 141, 71))
        self.codeGenButt.setObjectName("codeGenButt")
        self.consoleField = QtGui.QTextEdit(self.centralwidget)
        self.consoleField.setEnabled(True)
        self.consoleField.setGeometry(QtCore.QRect(40, 150, 601, 431))
        self.consoleField.setReadOnly(True)
        self.consoleField.setObjectName("consoleField")
        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(40, 150, 601, 431))
        self.treeView.setObjectName("treeView")
        self.treeView.header().setVisible(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 687, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.lexButt, QtCore.SIGNAL("clicked()"), MainWindow.lexCheck)
        QtCore.QObject.connect(self.openButt, QtCore.SIGNAL("clicked()"), MainWindow.openFile)
        QtCore.QObject.connect(self.grammarButt, QtCore.SIGNAL("clicked()"), MainWindow.grammarAnalysis)
        QtCore.QObject.connect(self.semanticButt, QtCore.SIGNAL("clicked()"), MainWindow.semanticCheck)
        QtCore.QObject.connect(self.codeGenButt, QtCore.SIGNAL("clicked()"), MainWindow.codeGen)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Dlang", None, QtGui.QApplication.UnicodeUTF8))
        self.openButt.setText(QtGui.QApplication.translate("MainWindow", "Open..", None, QtGui.QApplication.UnicodeUTF8))
        self.lexButt.setText(QtGui.QApplication.translate("MainWindow", "Lexial Check", None, QtGui.QApplication.UnicodeUTF8))
        self.grammarButt.setText(QtGui.QApplication.translate("MainWindow", "Grammar Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.semanticButt.setText(QtGui.QApplication.translate("MainWindow", "Semantic Check", None, QtGui.QApplication.UnicodeUTF8))
        self.codeGenButt.setText(QtGui.QApplication.translate("MainWindow", "Code Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.consoleField.setHtml(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open..", None, QtGui.QApplication.UnicodeUTF8))

