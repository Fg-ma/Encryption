# save path, folders, editable browsers

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from encryption import *
from vars import *

# Program mainwindow
class MainWindowUI(QMainWindow): 
    def __init__(self):
        super(MainWindowUI, self).__init__()

        loadUi("Encryption-Decryption.ui", self)

        self.errorLabel.hide()


    # Handles opening the directory for file selection
    def browseFiles(self):
        dialog = QtWidgets.QFileDialog.getOpenFileNames(self)
        if len(dialog[0]) > 1:
            files.clear()

            for i in dialog[0]:
                files.append(i)

            ui.selectedFileBox.clear()
            for i in files:
                ui.selectedFileBox.insertPlainText(i + "\n")
        else:
            try:
                files.clear()
                files.append(dialog[0][0])
                ui.selectedFileBox.clear()
                self.selectedFileBox.insertPlainText(dialog[0][0])
            except:
                pass

    
    # Handles opening the directory for savepath
    def savePath(self):
        savePath.clear()
        savePath.append(QFileDialog.getExistingDirectory(self, "Select Directory", "C:\\"))
        self.savePathBox.clear()
        self.savePathBox.insertPlainText(savePath[0])


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
    reconnectReset(ui.filesPathBox.textChanged, pathBoxUpdate)
    reconnectReset(ui.unmaskPasswordButton.clicked, unmaskPassword)
    reconnectReset(ui.unmaskConfirmPasswordButton.clicked, unmaskConfirmPassword)


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


# Handles updates to the paths list box
def pathBoxUpdate():
    if addingFiles[0] == "False":
        txt = ui.filesPathBox.toPlainText()
        lines = txt.split("\n")
        filesList.clear()
        for i in lines:
            if i != "":
                filesList.append(i)


# Adds the selected file to the files list
def addToFilesFunction():
    if files != []:
        addingFiles[0] = "True"
        for i in files:
            filesList.append(i)
        ui.filesPathBox.clear()
        for path in filesList:
            ui.filesPathBox.insertPlainText(path + "\n")
    addingFiles[0] = "False"


# Clears the file lists
def clearFilesListFunction():
    if filesList != []:
        addingFiles[0] == "True"
        filesList.clear()
        ui.filesPathBox.clear()
    addingFiles[0] == "False"


# Updates password when user types in box
def updatePassword():
    password[0] = ui.passwordBox.text()
    raiseError()


# Updates comfirm password when user types in box
def verifyPassword():
    confirmPassword[0] = ui.confirmPasswordBox.text()
    raiseError()


# unmasks and remask password on button click for privacy
def unmaskPassword():
    if passwordMode[0] == "Password":
        passwordMode[0] = "Normal"
        ui.passwordBox.setEchoMode(QLineEdit.EchoMode.Normal)
        ui.unmaskPasswordButton.setIcon(QIcon("resources\\hidden.png"))
    elif passwordMode[0] == "Normal":
        passwordMode[0] = "Password"
        ui.passwordBox.setEchoMode(QLineEdit.EchoMode.Password)
        ui.unmaskPasswordButton.setIcon(QIcon("resources\\unhidden.png"))


# unmasks and remask confirm password on button click for privacy
def unmaskConfirmPassword():
    if confirmPasswordMode[0] == "Password":
        confirmPasswordMode[0] = "Normal"
        ui.confirmPasswordBox.setEchoMode(QLineEdit.EchoMode.Normal)
        ui.unmaskConfirmPasswordButton.setIcon(QIcon("resources\\hidden.png"))
    elif confirmPasswordMode[0] == "Normal":
        confirmPasswordMode[0] = "Password"
        ui.confirmPasswordBox.setEchoMode(QLineEdit.EchoMode.Password)
        ui.unmaskConfirmPasswordButton.setIcon(QIcon("resources\\unhidden.png"))


# Handles raising all errors
def raiseError():
    if passwordMatchError[0] != "":
        ui.errorLabel.setText("Mismatched passwords!")
        ui.errorLabel.adjustSize()
        ui.errorLabel.show()
        ui.resize(ui.width(), ui.height() - errorShift[0])
    elif failedPaths != []:
        error = "Did not encrypt the following broken pathways:"
        ui.resize(ui.width(), ui.height() - errorShift[0])
        errorShift[0] = 20
        for path in failedPaths:
            error += "\n" + ">>>" + path
            errorShift[0] = errorShift[0] + 20
        ui.resize(ui.width(), ui.height() + errorShift[0])
        ui.errorLabel.setText(error)
        ui.errorLabel.adjustSize()
        ui.errorLabel.show()
    else:
        ui.resize(ui.width(), ui.height() - errorShift[0])
        passwordMatchError[0] = ""
        ui.errorLabel.hide()


# Gets file name and sends it to the proper encryption place
def encryptFile():
    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if a file has actually been selected
        if files != []:
            addingFiles[0] = "True"

            enc = encryptor(generate_key(password[0]))

            fileCount = 0
            failedPaths.clear()
            # Iterates over all of the selected files
            for file in files:
                # Differentiates between files and folders inputted and handles them differently
                if file[-1] == "\\":
                    folder = os.scandir(file)

                    for f in folder:
                        try:
                            enc.encrypt_file(f)
                        except:
                            failedPaths.append(f)
                else:
                    try:
                        enc.encrypt_file(file)
                        files[fileCount] += ".enc"
                    except:
                        failedPaths.append(file)
                fileCount += 1

            ui.selectedFileBox.clear()
            for i in files:
                ui.selectedFileBox.insertPlainText(i + "\n")

            # Updates fileslist incase the encrypted files were in it
            if filesList != []:
                for i in files:
                    fcount = 0
                    for j in filesList:
                        if j == i[:-4]:
                            filesList[fcount] = i
                        fcount += 1
                ui.filesPathBox.clear()
                for path in filesList:
                    ui.filesPathBox.insertPlainText(path + "\n")
            addingFiles[0] = "False"
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
            addingFiles[0] = "True"

            enc = encryptor(generate_key(password[0]))

            fileCount = 0
            failedPaths.clear()
            # Iterates over all of the selected files
            for file in files:
                # Differentiates between files and folders inputted and handles them differently
                if file[-1] == "\\":
                    folder = os.scandir(file)

                    for f in folder:
                        try:
                            enc.decrypt_file(f)
                        except:
                            failedPaths.append(f)
                else:
                    try:
                        enc.decrypt_file(file)
                        files[fileCount] = file[:-4]
                    except:
                        failedPaths.append(file)
                fileCount += 1

            ui.selectedFileBox.clear()
            for i in files:
                ui.selectedFileBox.insertPlainText(i + "\n")

            # Updates fileslist incase the encrypted files were in it
            if filesList != []:
                for i in files:
                    fcount = 0
                    for j in filesList:
                        if j == i + ".enc":
                            filesList[fcount] = i
                        fcount += 1
                ui.filesPathBox.clear()
                for path in filesList:
                    ui.filesPathBox.insertPlainText(path + "\n")
            addingFiles[0] = "False"
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
            addingFiles[0] = "True"

            enc = encryptor(generate_key(password[0]))

            fileCount = 0
            failedPaths.clear()
            # Iterates over all of the selected files
            for file in filesList:
                # Differentiates between files and folders inputted and handles them differently
                if file[-1] == "\\":
                    folder = os.scandir(file)

                    for f in folder:
                        try:
                            enc.encrypt_file(f)
                        except:
                            failedPaths.append(f)
                else:
                    try:
                        enc.encrypt_file(file)
                        filesList[fileCount] += ".enc"
                    except:
                        failedPaths.append(file)
                fileCount += 1

            # Updating values of displayed paths
            ui.filesPathBox.clear()
            for path in filesList:
                ui.filesPathBox.insertPlainText(path + "\n")

            # Updates files in case any of the changed files were in the files list
            if files != []:
                for j in filesList:
                    fcount = 0
                    for i in files:
                        if j == i + ".enc":
                            files[fcount] = j
                        fcount += 1

                ui.selectedFileBox.clear()
                for i in files:
                    ui.selectedFileBox.insertPlainText(i + "\n")

            addingFiles[0] = "False"
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
            addingFiles[0] = "True"

            enc = encryptor(generate_key(password[0]))

            fileCount = 0
            failedPaths.clear()
            # Iterates over all of the selected files
            for file in filesList:
                # Differentiates between files and folders inputted and handles them differently
                if file[-1] == "\\":
                    folder = os.scandir(file)

                    for f in folder:
                        try:
                            enc.decrypt_file(f)
                        except:
                            failedPaths.append(f)
                else:
                    try:
                        enc.decrypt_file(file)
                        filesList[fileCount] = file[:-4]
                    except:
                        failedPaths.append(file)
                fileCount += 1

            # Updating values of displayed paths
            ui.filesPathBox.clear()
            for path in filesList:
                ui.filesPathBox.insertPlainText(path + "\n")

            # Updates files in case any of the changed files were in the files list
            if files != []:
                for j in filesList:
                    fcount = 0
                    for i in files:
                        if j == i[:-4]:
                            files[fcount] = j
                        fcount += 1
                
                ui.selectedFileBox.clear()
                for i in files:
                    ui.selectedFileBox.insertPlainText(i + "\n")

            addingFiles[0] = "False"
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