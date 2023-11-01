"""
Turns non-encrypted files that are inputted into encrypted files using AES standard encryption.
Turns encrypted files taht are inputted into non-encrypted files using AES standard decryption.
Can handle save paths that designate where files are saved after encryption.
Can handle batch encryption via folders or multiple file inputs.
Requires a password(do not forget it, there is no recovery method).
"""

import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from encryption import *
from vars import *

class MainWindowUI(QMainWindow): 

    """
    Sets up the UI by loading it in from the .ui file.
    """

    def __init__(self):
        super(MainWindowUI, self).__init__()

        loadUi("Encryption-Decryption.ui", self)

        self.errorLabel.hide()


def browseFiles():

    """
    Opens a file browser window and stores the selected file path in the file path selection box.
    Can not selected folder, but paths can be later edited in the file selction box to accomdidate folders.
    """

    addingFiles[0] = "True"
    dialog = QtWidgets.QFileDialog.getOpenFileNames(ui)
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
            ui.selectedFileBox.insertPlainText(dialog[0][0])
        except:
            pass
    addingFiles[0] = "False"

    
def browseSavePath():

    """
    Opens a folder browser window and stores the selected folder path in the save path selection box.
    Can only select folders.
    """

    addingFiles[0] = "True"
    savePath.clear()
    savePath.append(QFileDialog.getExistingDirectory(ui, "Select Directory", "C:\\"))
    ui.savePathBox.clear()
    ui.savePathBox.insertPlainText(savePath[0])
    addingFiles[0] = "False"


def functions():

    """
    Used to reconnect the appropriate buttons with the appropriate functions.
    """

    reconnectReset(ui.browseButton.clicked, browseFiles)
    reconnectReset(ui.savePathButton.clicked, browseSavePath)
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
    reconnectReset(ui.selectedFileBox.textChanged, selectedFileBoxUpdate)
    reconnectReset(ui.savePathBox.textChanged, savePathBoxUpdate)


def reconnectReset(signal, newhandler=None, oldhandler=None): 

    """
    Trys to disconnect the inputted signal(button) from any functions that it may be attached to,
    then trys to reconnect the signal to a new function if inputted.
    """     

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


def restFunction():

    """
    Redirects to the functions function in order to re-establish the functions that each button is connected to
    """

    functions()    


def selectedFileBoxUpdate():

    """
    Updates the relevant variables when updates are detected in the selectedFileBox
    """

    if addingFiles[0] == "False":
        txt = ui.selectedFileBox.toPlainText()
        lines = txt.split("\n")
        files.clear()
        for i in lines:
            if i != "":
                files.append(i)


def savePathBoxUpdate():

    """
    Updates the relevant variables when updates are detected in the savePathBox
    """
    if addingFiles[0] == "False":
        txt = ui.savePathBox.toPlainText()
        savePath.clear()
        savePath.append(txt)
        

def pathBoxUpdate():

    """
    Updates the relevant variables when updates are detected in the filesPathBox
    """
    if addingFiles[0] == "False":
        txt = ui.filesPathBox.toPlainText()
        lines = txt.split("\n")
        filesList.clear()
        for i in lines:
            if i != "":
                filesList.append(i)


def addToFilesFunction():

    """
    Taskes the value(s) from the selected file box and adds it to the filesPathBox as an entry(s) to the list of files
    """
    if files != []:
        addingFiles[0] = "True"
        for i in files:
            filesList.append(i)
        ui.filesPathBox.clear()
        for path in filesList:
            ui.filesPathBox.insertPlainText(path + "\n")
    addingFiles[0] = "False"


def clearFilesListFunction():

    """
    Empties the filesPathBox and filesList to clear the list of files
    """

    if filesList != []:
        addingFiles[0] == "True"
        filesList.clear()
        ui.filesPathBox.clear()
    addingFiles[0] == "False"


def updatePassword():

    """
    Updates the relevant variables when updates are detected in the passwordBox
    """

    password[0] = ui.passwordBox.text()
    raiseError()


def verifyPassword():

    """
    Updates the relevant variables when updates are detected in the passwordBox
    """

    confirmPassword[0] = ui.confirmPasswordBox.text()
    raiseError()


def unmaskPassword():

    """
    Handles hiding an unhiding the inputted password in the passwordBox
    """

    if passwordMode[0] == "Password":
        passwordMode[0] = "Normal"
        ui.passwordBox.setEchoMode(QLineEdit.EchoMode.Normal)
        ui.unmaskPasswordButton.setIcon(QIcon("resources\\hidden.png"))
    elif passwordMode[0] == "Normal":
        passwordMode[0] = "Password"
        ui.passwordBox.setEchoMode(QLineEdit.EchoMode.Password)
        ui.unmaskPasswordButton.setIcon(QIcon("resources\\unhidden.png"))


def unmaskConfirmPassword():

    """
    Handles hiding an unhiding the inputted confirmation password in the confirmPasswordBox
    """

    if confirmPasswordMode[0] == "Password":
        confirmPasswordMode[0] = "Normal"
        ui.confirmPasswordBox.setEchoMode(QLineEdit.EchoMode.Normal)
        ui.unmaskConfirmPasswordButton.setIcon(QIcon("resources\\hidden.png"))
    elif confirmPasswordMode[0] == "Normal":
        confirmPasswordMode[0] = "Password"
        ui.confirmPasswordBox.setEchoMode(QLineEdit.EchoMode.Password)
        ui.unmaskConfirmPasswordButton.setIcon(QIcon("resources\\unhidden.png"))


def raiseError():

    """
    Raises and handles such as unfound paths and mismatched passwords,
    Outputs the errors in a label that is added the the bottom of the window.
    """

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


def encryptFile():

    """
    Gets the appropriate files and folders then unpacks folders into files,
    then inputs are sent to be encrypted in encryption.py.
    Finally updates how the files are displayed and stored to match the new files that have been created.
    """

    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if a file has actually been selected
        if files != []:
            # Variable rest
            fileCount = 0
            failedPaths.clear()
            blankFiles.clear()
            for file in files:
                blankFiles.append(file)
            blankFilesList.clear()
            for file in filesList:
                blankFilesList.append(file)

            addingFiles[0] = "True"

            enc = encryptor(generate_key(password[0]))

            # Iterates over all of the selected files
            for file in files:
                # Trys to ecrypt a single file path if that doesn't work it trys to encrypt a folder path
                # if all that doesn't work it throws an error
                try:
                    enc.encrypt_file(file)
                except:
                    try:
                        enclosedFileNames = [entry.path for entry in os.scandir(file) if entry.is_file()]

                        for item in enclosedFileNames:
                            try:
                                enc.encrypt_file(item)
                            except:
                                failedPaths.append(item)
                    except:
                        failedPaths.append(file)
                fileCount += 1

            # Files values rest
            files.clear()
            for file in blankFiles:
                files.append(file)
            filesList.clear()
            for file in blankFilesList:
                filesList.append(file)

            ui.selectedFileBox.clear()
            for i in files:
                ui.selectedFileBox.insertPlainText(i + "\n")

            # Updates fileslist in case the encrypted files were in it
            if filesList != []:
                ui.filesPathBox.clear()
                for path in filesList:
                    ui.filesPathBox.insertPlainText(path + "\n")
            addingFiles[0] = "False"
    else:
        passwordMatchError[0] = "Error"
        raiseError()
        return
    raiseError()


def decryptFile():

    """
    Gets the appropriate files and folders then unpacks folders into files,
    then inputs are sent to be decrypted in encryption.py.
    Finally updates how the files are displayed and stored to match the new files that have been created.
    """

    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if a file has actually been selected
        if files != []:
            # Variable rest
            fileCount = 0
            failedPaths.clear()
            blankFiles.clear()
            for file in files:
                blankFiles.append(file)
            blankFilesList.clear()
            for file in filesList:
                blankFilesList.append(file)

            addingFiles[0] = "True"

            enc = encryptor(generate_key(password[0]))

            # Iterates over all of the selected files
            for file in files:
                # Trys to ecrypt a single file path if that doesn't work it trys to encrypt a folder path
                # if all that doesn't work it throws an error
                try:
                    enc.decrypt_file(file)
                except:
                    try:
                        enclosedFileNames = [entry.path for entry in os.scandir(file) if entry.is_file()]

                        for item in enclosedFileNames:
                            try:
                                enc.decrypt_file(item)
                            except:
                                failedPaths.append(item)
                    except:
                        failedPaths.append(file)
                fileCount += 1

            # Files values rest
            files.clear()
            for file in blankFiles:
                files.append(file)
            filesList.clear()
            for file in blankFilesList:
                filesList.append(file)

            ui.selectedFileBox.clear()
            for i in files:
                ui.selectedFileBox.insertPlainText(i + "\n")

            # Updates fileslist incase the encrypted files were in it
            if filesList != []:
                ui.filesPathBox.clear()
                for path in filesList:
                    ui.filesPathBox.insertPlainText(path + "\n")
            addingFiles[0] = "False"
    else:
        passwordMatchError[0] = "Error"
        raiseError()
        return
    raiseError()


def encryptAllFile():

    """
    Gets the appropriate files and folders store in filesList then unpacks folders into files,
    then inputs are sent to be encrypted in encryption.py.
    Finally updates how the files are displayed and stored to match the new files that have been created.
    """

    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if any file have actually been selected
        if filesList != []:
            # Variable rest
            fileCount = 0
            failedPaths.clear()
            blankFiles.clear()
            for file in files:
                blankFiles.append(file)
            blankFilesList.clear()
            for file in filesList:
                blankFilesList.append(file)

            addingFiles[0] = "True"

            enc = encryptor(generate_key(password[0]))

            fileCount = 0
            failedPaths.clear()
            # Iterates over all of the selected files
            for file in filesList:
                # Trys to ecrypt a single file path if that doesn't work it trys to encrypt a folder path
                # if all that doesn't work it throws an error
                try:
                    enc.encrypt_file(file)
                except:
                    try:
                        enclosedFileNames = [entry.path for entry in os.scandir(file) if entry.is_file()]

                        for item in enclosedFileNames:
                            try:
                                enc.encrypt_file(item)
                            except:
                                failedPaths.append(item)
                    except:
                        failedPaths.append(file)
                fileCount += 1

            # Files values rest
            files.clear()
            for file in blankFiles:
                files.append(file)
            filesList.clear()
            for file in blankFilesList:
                filesList.append(file)

            # Updating values of displayed paths
            ui.filesPathBox.clear()
            for path in filesList:
                ui.filesPathBox.insertPlainText(path + "\n")
            
            if files != []:
                ui.selectedFileBox.clear()
                for i in files:
                    ui.selectedFileBox.insertPlainText(i + "\n")

            addingFiles[0] = "False"
    else:
        passwordMatchError[0] = "Error"
        raiseError()
        return
    raiseError()


def decryptAllFile():

    """
    Gets the appropriate files and folders in filesList then unpacks folders into files,
    then inputs are sent to be encrypted in decryption.py.
    Finally updates how the files are displayed and stored to match the new files that have been created.
    """

    # Password match check
    if password[0] == confirmPassword[0] and password[0] != "":
        passwordMatchError[0] = ""

        # Checks if any file have actually been selected
        if filesList != []:
            # Variable rest
            fileCount = 0
            failedPaths.clear()
            blankFiles.clear()
            for file in files:
                blankFiles.append(file)
            blankFilesList.clear()
            for file in filesList:
                blankFilesList.append(file)

            addingFiles[0] = "True"

            enc = encryptor(generate_key(password[0]))

            fileCount = 0
            failedPaths.clear()
            # Iterates over all of the selected files
            for file in filesList:
                # Trys to ecrypt a single file path if that doesn't work it trys to encrypt a folder path
                # if all that doesn't work it throws an error
                try:
                    enc.decrypt_file(file)
                except:
                    try:
                        enclosedFileNames = [entry.path for entry in os.scandir(file) if entry.is_file()]

                        for item in enclosedFileNames:
                            try:
                                enc.decrypt_file(item)
                            except:
                                failedPaths.append(item)
                    except:
                        failedPaths.append(file)
                fileCount += 1

            # Files values rest
            files.clear()
            for file in blankFiles:
                files.append(file)
            filesList.clear()
            for file in blankFilesList:
                filesList.append(file)

            # Updating values of displayed paths
            ui.filesPathBox.clear()
            for path in filesList:
                ui.filesPathBox.insertPlainText(path + "\n")

            if files != []:   
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