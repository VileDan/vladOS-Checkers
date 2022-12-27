import copy
import json
import time
import pygame
from sprites import Checker
import enum

WIDTH = 1000
HEIGHT = 600
FPS = 60
WHITE = (227, 230, 255)
BACKCOLOR = (18, 32, 32)
BLACK = (74, 84, 98)
SELECT = (89, 193, 53)
cellSize = 68.75
cellsRect = []
# Инициализация
pygame.init()
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BACKCOLOR)
pygame.display.set_caption("vladOS Checkers.")
pygame.display.set_icon(pygame.image.load("sprites/icon.png"))
clock = pygame.time.Clock()
gameField = pygame.Surface((549, 549))
gameField.fill((255, 255, 255))
indexesFont = pygame.font.Font("fonts/Fifaks10Dev1.ttf", 32)
infoFont = pygame.font.Font("fonts/Fifaks10Dev1.ttf", 26)
userIndex = 0 # Запись индекса играющего для записи победы
# Управление правилами (туфтология ахах)
selectedFigure = None
selectedCell = None
playerCheckers = 1, 2
computerCheckers = 3, 4
playersCounter = 0
computerCounter = 0
computerTurnsDeep = 1
field = [[0, 3, 0, 3, 0, 3, 0, 3],
         [3, 0, 3, 0, 3, 0, 3, 0],
         [0, 3, 0, 3, 0, 3, 0, 3],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [1, 0, 1, 0, 1, 0, 1, 0],
         [0, 1, 0, 1, 0, 1, 0, 1],
         [1, 0, 1, 0, 1, 0, 1, 0]]
checkerList = []
checkers = pygame.sprite.Group()
turnOrder = False  # false игрок true комп
running = False
def checkersCounter():
    global playersCounter
    playersCounter = playersCounter
    global computerCounter
    computerCounter = computerCounter
    global running

    playerCheckers = 0
    botCheckers = 0
    for checker in checkerList:
        if field[checker[1]][checker[2]] == 3 or field[checker[1]][checker[2]] == 4:
            botCheckers += 1
        elif field[checker[1]][checker[2]] == 1 or field[checker[1]][checker[2]] == 2:
            playerCheckers += 1
    print(playerCheckers, botCheckers)
    computerCounter = 12 - playerCheckers
    playersCounter = 12 - botCheckers - 1
    if playerCheckers == 0:
        print("Поражение")
        running = False
    elif botCheckers + 1 == 0:
        print("Победа")
        checkersResult(True)
        running = False
# Рисование поля
def indexTextRender():
    letter = ["A", "B", "C", "D", "E", "F", "G", "H"]
    for i in range(8):
        boardIndexAH = indexesFont.render(letter[i], True, WHITE)
        boardIndexAHRect = boardIndexAH.get_rect()
        boardIndexAHRect.center = (165 + i * cellSize, 575)
        boardIndex18 = indexesFont.render(str(8 - i), True, WHITE)
        boardIndex18Rect = boardIndex18.get_rect()
        boardIndex18Rect.center = (110, 45 + i * cellSize)
        screen.blit(boardIndexAH, boardIndexAHRect)
        screen.blit(boardIndex18, boardIndex18Rect)


def infoTextRender():
    if not turnOrder:
        textOrder = indexesFont.render("ХОД БЕЛЫХ", True, WHITE)
    else:
        textOrder = indexesFont.render("ХОД ЧЕРНЫХ", True, WHITE)
    textOrderRect = textOrder.get_rect()
    textOrderRect.center = (780, 40)
    whiteCounterText = infoFont.render("Счет белых: " + str(playersCounter), True, WHITE)
    blackCounterText = infoFont.render("Счет черных: " + str(computerCounter), True, WHITE)
    whiteCounterRect = whiteCounterText.get_rect()
    blackCounterRect = blackCounterText.get_rect()
    whiteCounterRect.midleft = (707, 80)
    blackCounterRect.midleft = (707, 110)
    screen.blit(textOrder, textOrderRect)
    screen.blit(blackCounterText, blackCounterRect)
    screen.blit(whiteCounterText, whiteCounterRect)

def checkersResult(loseOrWin):
    global usersList
    with open('users/userList.json') as json_file:
        usersList = json.load(json_file)
    if loseOrWin:
        usersList["users"][userIndex]["wins"] += 1
    with open('users/userList.json', 'w') as outfile:
        json.dump(usersList, outfile)
def fieldDraw():
    gameField.fill(WHITE)
    cellsRect.clear()
    blackOrWhite = True
    for x in range(8):
        colorStart = WHITE
        if blackOrWhite:
            colorStart = BLACK
        else:
            colorStart = WHITE
        blackOrWhite = not blackOrWhite
        for y in range(8):
            color = WHITE
            if blackOrWhite:
                color = BLACK
            else:
                color = WHITE

            blackOrWhite = not blackOrWhite
            pygame.draw.rect(gameField, color, (x * cellSize, y * cellSize, cellSize, cellSize))
            rect = pygame.Rect((gameField.get_rect(topleft=(cellSize * 2, cellSize * 2)).x + x * cellSize - 5,
                                gameField.get_rect(topleft=(0, 0)).x + y * cellSize + 27,
                                cellSize, cellSize))
            cellsRect.append((rect, (y, x)))
    pygame.draw.rect(gameField, (0, 0, 0, 0), (0, 0, 549, 549), 5)
    pygame.display.update()


def checkersRender():
    checkerList.clear()
    for i in checkers.sprites():
        checkers.remove(i)
    for x in range(8):
        for y in range(8):
            coordWithSpacing = (y * cellSize + 2, x * cellSize + 2)
            if field[x][y] == 1:
                whiteChecker = Checker(coordWithSpacing[0], coordWithSpacing[1], "sprites/white_checker.png")
                whiteChecker.update(coordWithSpacing[0], coordWithSpacing[1])
                checkers.add(whiteChecker)
                checkerList.append((whiteChecker, x, y))
            elif field[x][y] == 3:
                blackChecker = Checker(coordWithSpacing[0], coordWithSpacing[1], "sprites/black_checker.png")
                blackChecker.update(coordWithSpacing[0], coordWithSpacing[1])
                checkers.add(blackChecker)
                checkerList.append((blackChecker, x, y))
            elif field[x][y] == 4:
                blackCheckerQueen = Checker(coordWithSpacing[0], coordWithSpacing[1], "sprites/black_checker_queen.png")
                blackCheckerQueen.update(coordWithSpacing[0], coordWithSpacing[1])
                checkers.add(blackCheckerQueen)
                checkerList.append((blackCheckerQueen, x, y))
            elif field[x][y] == 2:
                whiteCheckerQueen = Checker(coordWithSpacing[0], coordWithSpacing[1], "sprites/white_checker_queen.png")
                whiteCheckerQueen.update(coordWithSpacing[0], coordWithSpacing[1])
                checkers.add(whiteCheckerQueen)
                checkerList.append((whiteCheckerQueen, x, y))

    checkers.update(gameField)
    checkers.draw(gameField)


def makeATurn(fig, cell):
    global turnOrder
    turnOrder = turnOrder
    try:
        eatedFigure = eatTurnIsPossible(fig, cell)
        print(eatedFigure)
        if turnIsPossible(fig, cell):
            if field[fig[2]][fig[1]] == 2 or field[fig[2]][fig[1]] == 4:
                if queenHunt(fig, cell):
                    field[cell[1][0]][cell[1][1]] = field[fig[2]][fig[1]]
                    field[fig[2]][fig[1]] = 0
                    turnOrder = not turnOrder
                    turkishStrikeCoords = turkishStrike((None, cell[1][1], cell[1][0]))
                if turkishStrikeCoords is not None:
                    turnOrder = not turnOrder
            elif not queenCoronation(fig, cell):
                field[cell[1][0]][cell[1][1]] = field[fig[2]][fig[1]]
                field[fig[2]][fig[1]] = 0
                turnOrder = not turnOrder
            else:
                if field[fig[2]][fig[1]] == 1:
                    field[cell[1][0]][cell[1][1]] = 2
                    turnOrder = True
                elif field[fig[2]][fig[1]] == 3:
                    field[cell[1][0]][cell[1][1]] = 4
                    turnOrder = False
                field[fig[2]][fig[1]] = 0

        elif eatedFigure is not None and queenCoronation(fig, cell):
            if field[fig[2]][fig[1]] == 1:
                field[cell[1][0]][cell[1][1]] = 2
                field[eatedFigure[0]][eatedFigure[1]] = 0
                turnOrder = True
            elif field[fig[2]][fig[1]] == 3:
                field[cell[1][0]][cell[1][1]] = 4
                field[eatedFigure[0]][eatedFigure[1]] = 0
                turnOrder = False
            field[fig[2]][fig[1]] = 0
        elif eatedFigure is not None and not queenCoronation(fig, cell):
            if field[fig[2]][fig[1]] == 1:
                field[cell[1][0]][cell[1][1]] = 1
                field[eatedFigure[0]][eatedFigure[1]] = 0
                turnOrder = True
            elif field[fig[2]][fig[1]] == 3:
                field[cell[1][0]][cell[1][1]] = 3
                field[eatedFigure[0]][eatedFigure[1]] = 0
                turnOrder = False
            field[fig[2]][fig[1]] = 0
            turkishStrikeCoords = turkishStrike((None, cell[1][1], cell[1][0]))
            if turkishStrikeCoords is not None:
                turnOrder = not turnOrder
        screen.fill(BACKCOLOR)
        gameField.fill(WHITE)
        checkersCounter()
        infoTextRender()
        indexTextRender()
        fieldDraw()
        checkersRender()
    except TypeError:
        return


def turnIsPossible(fig, cell):  # Возможность хода
    # Сравнивается позиция шашки и позиция выбранной клетки, если координата клетки на углах шашки, то все пучком
    # Для белых (1 аргумент в cell y второй x - особенности матрицы...)
    # print((fig[1], fig[2]) == (cell[1][1] - 1, cell[1][0] + 1))
    if field[cell[1][0]][cell[1][1]] != 0:
        return False
    if field[fig[2]][fig[1]] == 1 and ((fig[1], fig[2]) == (cell[1][1] + 1, cell[1][0] + 1)  # ЛЕВЫЙ ВЕРХ
                                       or (fig[1], fig[2]) == (cell[1][1] - 1, cell[1][0] + 1)):  # ПРАВЫЙ ВЕРХ
        return True
    # Для черных
    elif field[fig[2]][fig[1]] == 3 and ((fig[1], fig[2]) == (cell[1][1] + 1, cell[1][0] - 1)  # ЛЕВЫЙ НИЗ
                                         or (fig[1], fig[2]) == (cell[1][1] - 1, cell[1][0] - 1)):  # ПРАВЫЙ НИЗ
        return True
    # Для дамок
    elif (field[fig[2]][fig[1]] == 2 or field[fig[2]][fig[1]] == 4) \
            and (abs(cell[1][0] - fig[2] + 1) == cell[1][1] - fig[1] - 1  # ПРАВЫЙ ВЕРХ
                 or cell[1][0] - fig[2] + 1 == cell[1][1] - fig[1] + 1  # ЛЕВЫЙ ВЕРХ и ПРАВЫЙ НИЗ??:
                 or cell[1][0] - fig[2] + 1 == abs(cell[1][1] - fig[1] - 1)):  # ЛЕВЫЙ НИЗ
        return True
    else:
        return False


def eatTurnIsPossible(fig, cell):
    # Еда для белых
    if field[fig[2]][fig[1]] == 1:
        if (fig[1], fig[2]) == (cell[1][1] - 2, cell[1][0] + 2) \
                and (field[fig[2] - 1][fig[1] + 1] == 3 or field[fig[2] - 1][fig[1] + 1] == 4):  # Съесть правую верхнюю
            return (fig[2] - 1, fig[1] + 1)  # Первый индекс это у, а второй х
        elif (fig[1], fig[2]) == (cell[1][1] + 2, cell[1][0] + 2) \
                and (
                field[fig[2] - 1][fig[1] - 1] == 3 or field[fig[2] - 1][fig[1] - 1] == 4):  # Съесть левую верхнюю шашку
            return (fig[2] - 1, fig[1] - 1)
        elif (fig[1], fig[2]) == (cell[1][1] + 2, cell[1][0] - 2) \
                and (
                field[fig[2] + 1][fig[1] - 1] == 3 or field[fig[2] + 1][fig[1] - 1] == 4):  # Съесть левую нижнюю шашку
            return (fig[2] + 1, fig[1] - 1)
        elif (fig[1], fig[2]) == (cell[1][1] - 2, cell[1][0] - 2) \
                and (
                field[fig[2] + 1][fig[1] + 1] == 3 or field[fig[2] + 1][fig[1] + 1] == 4):  # Съесть правую нижнюю шашку
            return (fig[2] + 1, fig[1] + 1)
    elif field[fig[2]][fig[1]] == 3:
        if (fig[1], fig[2]) == (cell[1][1] - 2, cell[1][0] + 2) \
                and (field[fig[2] - 1][fig[1] + 1] == 1 or field[fig[2] - 1][fig[1] + 1] == 2):  # Съесть правую верхнюю
            return (fig[2] - 1, fig[1] + 1)  # Первый индекс это у, а второй х
        elif (fig[1], fig[2]) == (cell[1][1] + 2, cell[1][0] + 2) \
                and (
                field[fig[2] - 1][fig[1] - 1] == 1 or field[fig[2] - 1][fig[1] - 1] == 2):  # Съесть левую верхнюю шашку
            return (fig[2] - 1, fig[1] - 1)
        elif (fig[1], fig[2]) == (cell[1][1] + 2, cell[1][0] - 2) \
                and (
                field[fig[2] + 1][fig[1] - 1] == 1 or field[fig[2] + 1][fig[1] - 1] == 2):  # Съесть левую нижнюю шашку
            return (fig[2] + 1, fig[1] - 1)
        elif (fig[1], fig[2]) == (cell[1][1] - 2, cell[1][0] - 2) \
                and (
                field[fig[2] + 1][fig[1] + 1] == 1 or field[fig[2] + 1][fig[1] + 1] == 2):  # Съесть правую нижнюю шашку
            return (fig[2] + 1, fig[1] + 1)
    else:
        return None


def queenCoronation(fig, cell):
    if field[fig[2]][fig[1]] == 1 and cell[1][0] == 0:
        return True
    elif field[fig[2]][fig[1]] == 3 and cell[1][0] == 7:
        return True
    return False


def findFigure(x, y):
    for i in range(len(checkerList)):
        if checkerList[i][1] == x and checkerList[i][2] == y:
            return checkerList[i][0]
    return None


def queenHunt(fig, cell):
    turnOk = True
    try:
        direction = abs((cell[1][0] - fig[2]) / abs(cell[1][0] - fig[2])) / (
                (cell[1][0] - fig[2]) / abs(cell[1][0] - fig[2])) \
            , abs((cell[1][1] - fig[1]) / abs(cell[1][1] - fig[1])) / ((cell[1][1] - fig[1]) / abs(cell[1][1] - fig[1]))
        distance = abs(fig[2] - cell[1][0])
    except ZeroDivisionError:
        turnOk = False
    listOfEat = []
    if turnOk:
        for i in range(distance):
            indexX = int(fig[2] + direction[0] * (i + 1))
            indexY = int(fig[1] + direction[1] * (i + 1))
            indexXNext = int(fig[2] + direction[0] * (i + 2))
            indexYNext = int(fig[1] + direction[1] * (i + 2))
            indexXPrefer = int(fig[2] + direction[0] * i)
            indexYPrefer = int(fig[1] + direction[1] * i)
            checkCell = field[indexX][indexY]

            if field[fig[2]][fig[1]] != 0 and checkCell != 0 and field[indexXNext][indexYNext] != 0:
                turnOk = False
                break
            elif field[fig[2]][fig[1]] == 2 and (checkCell == 1 or checkCell == 2):
                turnOk = False
                break
            elif field[fig[2]][fig[1]] == 4 and (checkCell == 3 or checkCell == 4):
                turnOk = False
                break
            elif field[fig[2]][fig[1]] == 2 and (checkCell == 3 or checkCell == 4):
                listOfEat.append((indexX, indexY))
            elif field[fig[2]][fig[1]] == 4 and (checkCell == 1 or checkCell == 2):
                listOfEat.append((indexX, indexY))
        if len(listOfEat) <= 1 and turnOk:
            for x in listOfEat:
                field[x[0]][x[1]] = 0
        else:
            turnOk = False
    return turnOk


def turkishStrike(fig):
    coords = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # Направления углов
    # Если после жратвы можно съесть еще раз
    for c in coords:
        try:
            if (field[fig[2]][fig[1]] == 1 or field[fig[2]][fig[1]] == 2) \
                and (field[fig[2] + c[0]][fig[1] + c[1]] == 3
                     or field[fig[2] + c[0]][fig[1] + c[1]] == 4) \
                    and field[fig[2] + c[0] * 2][fig[1] + c[1] * 2] == 0:
                return (fig[2], fig[1], fig[2] + c[0] * 2, fig[1] + c[1] * 2)
            elif (field[fig[2]][fig[1]] == 3 or field[fig[2]][fig[1]] == 4) \
                and (field[fig[2] + c[0]][fig[1] + c[1]] == 1
                     or field[fig[2] + c[0] * 2][fig[1] + c[1] * 2] == 2) \
                and field[fig[2] + c[0] * 2][fig[1] + c[1] * 2] == 0:
                return (fig[2], fig[1], fig[2] + c[0] * 2, fig[1] + c[1] * 2)
        except IndexError:
            pass
    return None

# def tipsDraw():
# Игровой бот FOOL
def possibleBotTurns():
    # Цены хода: Оценочная функция
    # Отберем все шашки бота
    global running
    running = running
    botCheckers = []
    playerCheckers = []
    global liderTurn
    liderTurn = (0, 0, 0, 0, 0)  # y шашки x шашки y клетки x клетки
    for checker in checkerList:
        if field[checker[1]][checker[2]] == 3 or field[checker[1]][checker[2]] == 4:
            botCheckers.append((checker[1], checker[2]))
        elif field[checker[1]][checker[2]] == 1 or field[checker[1]][checker[2]] == 2:
            playerCheckers.append((checker[1], checker[2]))
    if len(botCheckers) == 0:
        running = False
    if len(playerCheckers) == 0:
        running = False
    # Посмотрим все возможные ходы для этих шашек
    coords = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    fieldInBotBrain = copy.deepcopy(field)
    possibleBotTurns = []  # y шашки, x шашки, y клетки, x клетки, цена
    for i in range(computerTurnsDeep):
        global maxCostTurn
        maxCostTurn = (0, 0)
        # Предположительный ход бота
        for checker in botCheckers:
            for c in coords:
                try:
                    if 7 >= checker[0] + c[0] >= 0 \
                            and 7 >= checker[1] + c[1] >= 0:
                        # Ход атака
                        if fieldInBotBrain[checker[0] + c[0]][checker[1] + c[1]] == 1 \
                                and fieldInBotBrain[checker[0] + c[0] * 2][checker[1] + c[1] * 2] == 0:
                            possibleBotTurns.append((checker[0], checker[1], checker[0] + c[0] * 2, checker[1] + c[1] * 2, 5))
                        # Атака дамки
                        elif fieldInBotBrain[checker[0] + c[0]][checker[1] + c[1]] == 2 \
                                and fieldInBotBrain[checker[0] + c[0] * 2][checker[1] + c[1] * 2] == 0:
                            possibleBotTurns.append((checker[0], checker[1], checker[0] + c[0] * 2, checker[1] + c[1] * 2, 6))
                        # Если ход приведет к поеданию противником
                        elif fieldInBotBrain[checker[0] + c[0]][checker[1] + c[1]] == 0 \
                                and (fieldInBotBrain[checker[0] + c[0] * 2][checker[1] + c[1] * 2] == 1
                                     or fieldInBotBrain[checker[0] + c[0] * 2][checker[1] + c[1] * 2] == 2) \
                                and c[0] == 1:
                            possibleBotTurns.append((checker[0], checker[1], checker[0] + c[0], checker[1] + c[1], -2))
                        # Ход дамка
                        elif fieldInBotBrain[checker[0] + c[0]][checker[1] + c[1]] == 0 and checker[0] + c[0] == 7:
                            possibleBotTurns.append((checker[0], checker[1], checker[0] + c[0], checker[1] + c[1], 4))
                        # Просто ход
                        elif fieldInBotBrain[checker[0] + c[0]][checker[1] + c[1]] == 0 and c[0] == 1:
                            possibleBotTurns.append((checker[0], checker[1], checker[0] + c[0], checker[1] + c[1], 0))
                except IndexError:
                    pass

        # Теперь моделируем ситуацию для каждого из возможных ходов хода на предположительно лучший ход игрока
        # а также сортировка
        for turn in possibleBotTurns:
            fieldInBotBrainCalculation = copy.deepcopy(fieldInBotBrain)
            # Расчетный ход
            fieldInBotBrainCalculation[turn[0]][turn[1]] = 0
            fieldInBotBrainCalculation[turn[2]][turn[3]] = 3
            # Моделирование ходов игрока
            for checker in playerCheckers:
                for c in coords:
                    try:
                        if 7 >= checker[0] + c[0] >= 0 \
                                and 7 >= checker[1] + c[1] >= 0:
                            # Ход атака
                            if fieldInBotBrainCalculation[checker[0] + c[0]][checker[1] + c[1]] == 3 \
                                    and fieldInBotBrainCalculation[checker[0] + c[0] * 2][checker[1] + c[1] * 2] == 0:
                                turn = (turn[0], turn[1], turn[2], turn[3], turn[4] - 5)
                            # Атака дамки
                            elif fieldInBotBrainCalculation[checker[0] + c[0]][checker[1] + c[1]] == 4 \
                                    and fieldInBotBrainCalculation[checker[0] + c[0] * 2][checker[1] + c[1] * 2] == 0:
                                turn = (turn[0], turn[1], turn[2], turn[3], turn[4] - 6)
                            # Если ход приведет к поеданию противником
                            elif fieldInBotBrainCalculation[checker[0] + c[0]][checker[1] + c[1]] == 0 \
                                    and (fieldInBotBrainCalculation[checker[0] + c[0] * 2][checker[1] + c[1] * 2] == 3
                                         or fieldInBotBrainCalculation[checker[0] + c[0] * 2][checker[1] + c[1] * 2] == 4)\
                                    and c[0] == -1:
                                turn = (turn[0], turn[1], turn[2], turn[3], turn[4] + 1)
                             # Ход дамка
                            elif fieldInBotBrainCalculation[checker[0] + c[0]][checker[1] + c[1]] == 0\
                                    and checker[0] + c[0] == 0:
                                turn = (turn[0], turn[1], turn[2], turn[3], turn[4] - 4)
                            # Просто ход
                            elif fieldInBotBrainCalculation[checker[0] + c[0]][checker[1] + c[1]] == 0 and c[0] == -1:
                                turn = (turn[0], turn[1], turn[2], turn[3], turn[4])
                    except IndexError:
                        pass
        # Удаляем ходы с отрицательным значением bugs
        for i in range(len(possibleBotTurns)):
            if possibleBotTurns[i][2] < 0 or possibleBotTurns[i][3] < 0:
                possibleBotTurns[i] = (0, 0 , 0 , 0, -1000)
        print(len(possibleBotTurns))
        # Сортируем словарь с ценами
        maxCost = -1000
        for i in possibleBotTurns:
            if i[4] > maxCost:
                maxCost = i[4]
                maxCostTurn = (possibleBotTurns.index(i), maxCost)
        # Выбираем лидера
        if len(possibleBotTurns) > 0:
            liderTurn = possibleBotTurns[maxCostTurn[0]]
        else:
            print("Конец игры для бота")
            checkersResult(True)
            running = False
            break
        fieldInBotBrain[liderTurn[0]][liderTurn[1]] = 0
        fieldInBotBrain[liderTurn[2]][liderTurn[3]] = 3
        print(liderTurn)
    if len(possibleBotTurns) > 0:
        makeATurn((None, liderTurn[1], liderTurn[0]), (None, (liderTurn[2], liderTurn[3])))
    else:
        print("Конец игры для бота")
        running = False
    turnOrder = False
# Игровой бот FOOL

def GameCicle():
    global running
    running = running
    while running:
        if not running:
            exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for cellRect in cellsRect:
                    if cellRect[0].collidepoint(pos):
                        figure = findFigure(cellRect[1][0], cellRect[1][1])
                        if figure is not None:
                            selectedFigure = (figure, cellRect[1][1], cellRect[1][0])
                            figureHas = True
                            print("Выбрана фигура", cellRect[1][0], cellRect[1][1])
                        elif figureHas:
                            selectedCell = cellRect
                            figureHas = False
                            makeATurn(selectedFigure, cellRect)
                            print("Выбрана клетка поля", cellRect[1][0], cellRect[1][1])
        if turnOrder:
            possibleBotTurns()

            # if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # if paraHas:
        screen.blit(gameField, (130, 10))
        pygame.display.flip()
        clock.tick(FPS)

def newGame():
    global field
    global running
    field = field
    field = [[0, 3, 0, 3, 0, 3, 0, 3],
             [3, 0, 3, 0, 3, 0, 3, 0],
             [0, 3, 0, 3, 0, 3, 0, 3],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [1, 0, 1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 0]]
    # Игровой цикл
    screen.fill(BACKCOLOR)
    gameField.fill(WHITE)
    checkersCounter()
    indexTextRender()
    infoTextRender()
    fieldDraw()
    checkersRender()
    running = True
    GameCicle()
##running = True
##GameCicle()