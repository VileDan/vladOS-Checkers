import os
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication
import json
import re
import main
from cipherClass import ADFGVX
from main import GameCicle
from main import running

LoginForm, LoginWindow = uic.loadUiType("loginWindow.ui")

app = QApplication([])
loginWindow = LoginWindow()
loginForm = LoginForm()
loginForm.setupUi(loginWindow)
loginWindow.show()

MainForm, MainWindow = uic.loadUiType("mainWindow.ui")

mainWindow = MainWindow()
mainForm = MainForm()
mainForm.setupUi(mainWindow)

logo = QPixmap("sprites/logo.png")
loginForm.logoLabel.setPixmap(logo)

# Загрузка списка пользователей В пароль только маленькие латинские буквы и цифры !
PCHARS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
POLYBIUS = ''.join(PCHARS)
cipher = ADFGVX(POLYBIUS, "vlados")
usersList = {}
userIndex = 0
try:
    with open('users/userList.json') as json_file:
        usersList = json.load(json_file)
except FileNotFoundError:
    with open('users/userList.json', 'w') as outfile:
        usersList = {"users": []}
        json.dump(usersList, outfile)

def difficultyMenuAdd():
    mainForm.difChoice.addItem("Легкая")
def signUp():
    if len(loginForm.loginEdit.text()) > 0 and len(loginForm.passwordEdit.text()) > 0:
        inputLogin = loginForm.loginEdit.text()
        inputPassword = loginForm.passwordEdit.text()
        userCreate(inputLogin, inputPassword)


def mainMenuFormOpen(user, index, uL):
    loginWindow.close()
    mainWindow.show()
    mainForm.helloLabel.setText(f"Добро пожаловать в vladOS Checkers, {user}")
    global isLogIn
    isLogIn = isLogIn
    isLogIn = True
    global userIndex
    userIndex = userIndex
    userIndex = index
    mainForm.winCounter.setText("Количество побед: " + str(uL["users"][userIndex]["wins"]))

def passwordValidate(password):
    return re.match("^[A-Za-z0-9_-]*$", password)
def signIn():
    global tempIndex
    tempIndex = 0
    if len(loginForm.loginEdit.text()) > 0 and len(loginForm.passwordEdit.text()) > 0:
        inputLogin = loginForm.loginEdit.text()
        inputPassword = loginForm.passwordEdit.text()
        inputPassword = inputPassword.upper()
        isUserExist = False
        neededPassword = ""
        for x in range(len(usersList["users"])):
            if usersList["users"][x]["login"] == inputLogin:
                isUserExist = True
                neededPassword = cipher.decrypt(usersList["users"][x]["password"])
                tempIndex = x
                break
        if not isUserExist or inputPassword != neededPassword:
            loginForm.statusText.setText("Неправильный пользователь или пароль")
        elif isUserExist and inputPassword == neededPassword:
            loginForm.statusText.setText("Успешный вход")
            mainMenuFormOpen(inputLogin, tempIndex, usersList)
    else:
        loginForm.statusText.setText("Пустые поля")


def userCreate(iL, iP):
    global tempIndex
    tempIndex = 0
    isUserExist = False
    # Проверка, есть ли пользователь
    if len(usersList["users"]) > 0:
        for x in range(len(usersList["users"])):
            if usersList["users"][x]["login"] == iL:
                loginForm.statusText.setText("Такой пользователь уже существует! Пароль восстановить невозможно(")
                print("Такой пользователь уже существует! Пароль восстановить невозможно(")
                isUserExist = True
                break
    else:
        loginForm.statusText.setText("Пустые поля")
    if not passwordValidate(iP):
        loginForm.statusText.setText("Пароль может содержать только маленькие латинские буквы и цифры")
        return
    if not isUserExist:
        cipherPassword = cipher.encrypt(iP)
        usersList["users"].append({"login": iL, "password": cipherPassword, "wins": 0})
        tempIndex = len(usersList["users"]) - 1
        with open('users/userList.json', 'w') as outfile:
            json.dump(usersList, outfile)
            loginForm.statusText.setText("Регистрация успешна")
            print("Регистрация успешна!")
            mainMenuFormOpen(iL, tempIndex, usersList)
def playTheFCNGame():
    #mainWindow.close()
    main.newGame()
    main.userIndex = userIndex

isLogIn = False
loginForm.loginButton.clicked.connect(signIn)
loginForm.registerButton.clicked.connect(signUp)
mainForm.playButton.clicked.connect(playTheFCNGame)
difficultyMenuAdd()

def checkersResult(loseOrWin):
    if loseOrWin:
        usersList["users"][userIndex]["wins"] += 1
    mainForm.winCounter.setText("Количество побед: " + str(usersList["users"][userIndex]["wins"]))

app.exec()




