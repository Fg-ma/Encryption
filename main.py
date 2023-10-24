# save path, errors, editable browser

import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QFileDialog, QPlainTextEdit, QLabel
from PyQt5.uic import loadUi

from encryption import *
from vars import *

# Program mainwindow
class MainWindowUI(QMainWindow): 
    def __init__(self):
        super(MainWindowUI, self).__init__()

        loadUi("Encryption-Decryption.ui", self)


    # Handles opening the directory for file selection
    def browseFiles(self):
        dialog = QtWidgets.QFileDialog.getOpenFileNames(self)
        if len(dialog[0]) > 1:
            for i in dialog[0]:
                filesList.append(i)
            self.filesPathBox.clear()
            for path in filesList:
                self.filesPathBox.insertPlainText(path + "\n")
            files.clear()
            files.append(dialog[0][-1])
            self.selectedFileLabel.setText(dialog[0][-1])
        else:
            files.clear()
            files.append(dialog[0][0])
            self.selectedFileLabel.setText(dialog[0][0])

    
    # Handles opening the directory for savepath
    def savePath(self):
        savePath = QFileDialog.getExistingDirectory(self, "Select Directory", "C:\\")
        self.savePathLabel.setText(savePath)


# Connects the buttons to the appropriate functions given the under the present condition
def functions():
    reconnectReset(ui.browseButton.clicked, ui.browseFiles)
    reconnectReset(ui.savePathButton.clicked, ui.savePath)
    reconnectReset(ui.encryptButton.clicked, encryptFile)
    reconnectReset(ui.decryptButton.clicked, decryptFile)
    reconnectReset(ui.encryptAllButton.clicked, encryptAllFile)
    reconnectReset(ui.decryptAllButton.clicked, decryptAllFile)
    reconnectReset(ui.addToFilesButton.clicked, addToFilesFunction)
    reconnectReset(ui.clearFilesListButton.clicked, clearFilesListFunction)
    reconnectReset(ui.passwordBox.textChanged, updatePassword)
    reconnectReset(ui.confirmPasswordBox.textChanged, verifyPassword)


# Swaps function reference for buttons and connects a reference to resetFunction
def reconnectReset(signal, newhandler=None, oldhandler=None):        
    try:
        if oldhandler is not None:
            while True:
                signal.disconnect(oldhandler)
        else:
            signal.disconnect()
    except TypeError:
        pass
    if newhandler is not None:
        signal.connect(newhandler)
        signal.connect(restFunction)


# Swaps function reference for buttons
def reconnect(signal, newhandler=None, oldhandler=None):        
    try:
        if oldhandler is not None:
            while True:
                signal.disconnect(oldhandler)
        else:
            signal.disconnect()
    except TypeError:
        pass
    if newhandler is not None:
        signal.connect(newhandler)


# Updates what functions are called when swapping from base functions to alpha to 2nd
def restFunction():
    functions()    


# Adds the selected file to the files list
def addToFilesFunction():
    if files[0] != "":
        filesList.append(files[0])
        ui.filesPathBox.clear()
        for path in filesList:
            ui.filesPathBox.insertPlainText(path + "\n")


# Clears the file lists
def clearFilesListFunction():
    filesList.clear()
    ui.filesPathBox.clear()


# Updates password when user types in box
def updatePassword():
    password[0] = ui.passwordBox.text()
    raiseError()


# Updates comfirm password when user types in box
def verifyPassword():
    confirmPassword[0] = ui.confirmPasswordBox.text()
    raiseError()


# Handles raising all errors
def raiseError():
    try:
        ui.errorLayout.removeWidget(ui.errorLabel)
    except:
        pass
    if passwordMatchError[0] != "":
        ui.errorLabel = QLabel('Passwords do not match!')
        ui.errorLayout.addWidget(ui.errorLabel)
    else:
        passwordMatchError[0] = ""
        try:
            ui.errorLayout.removeWidget(ui.errorLabel)
        except:
            pass


# Gets file name and sends it to the proper encryption place
def encryptFile():
    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if a file has actually been selected
        if files != []:

            enc = encryptor(generate_key(password[0]))

            # Differentiates between files and folders inputted and handles them differently
            if files[0][-1] == "\\":
                folder = os.scandir(files[0])
                for file in folder:
                    enc.encrypt_file(file)
            else:
                enc.encrypt_file(files[0])
                files[0] += ".enc"
                ui.selectedFileLabel.setText(files[0])
    else:
        passwordMatchError[0] = "Error"
        raiseError()
        return
    raiseError()


# Gets file name and sends it to the proper decryption place
def decryptFile():
    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if a file has actually been selected
        if files != []:

            enc = encryptor(generate_key(password[0]))

            # Differentiates between files and folders inputted and handles them differently
            if files[0][-1] == "\\":
                folder = os.scandir(files[0])
                for file in folder:
                    enc.decrypt_file(file)
            else:
                enc.decrypt_file(files[0])
                files[0] = files[0][:-4]
                ui.selectedFileLabel.setText(files[0])
    else:
        passwordMatchError[0] = "Error"
        raiseError()
        return
    raiseError()


# Gets all file names and sends them to the proper encryption place
def encryptAllFile():
    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if any file have actually been selected
        if filesList != []:

            enc = encryptor(generate_key(password[0]))

            # Iterates over all of the selected files
            fileCount = 0
            for file in filesList:
                # Differentiates between files and folders inputted and handles them differently
                if file[-1] == "\\":
                    folder = os.scandir(file)
                    for f in folder:
                        enc.encrypt_file(f)
                else:
                    enc.encrypt_file(file)
                    filesList[fileCount] += ".enc"
                fileCount += 1
            ui.filesPathBox.clear()
            for path in filesList:
                ui.filesPathBox.insertPlainText(path + "\n")
    else:
        passwordMatchError[0] = "Error"
        raiseError()
        return
    raiseError()


# Gets all file names and sends them to the proper decryption place
def decryptAllFile():
    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if any file have actually been selected
        if filesList != []:

            enc = encryptor(generate_key(password[0]))

            # Iterates over all of the selected files
            fileCount = 0
            for file in filesList:
                # Differentiates between files and folders inputted and handles them differently
                if file[-1] == "\\":
                    folder = os.scandir(file)
                    for f in folder:
                        enc.decrypt_file(f)
                else:
                    enc.decrypt_file(file)
                    filesList[fileCount] = file[:-4]
                fileCount += 1
            ui.filesPathBox.clear()
            for path in filesList:
                ui.filesPathBox.insertPlainText(path + "\n")
    else:
        passwordMatchError[0] = "Error"
        raiseError()
        return
    raiseError()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindowUI()
    functions()
    ui.show()
    app.exec_()