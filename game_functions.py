from settings import *
import time,pygame,json

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

gridSquareList = []

def create_grid():
    for x in range(0, WINDOW_WIDTH - 80, GRIDSQUARESIZE):
        for y in range(0, WINDOW_HEIGHT, GRIDSQUARESIZE):
            global gridSquare
            gridSquare = pygame.Rect(x, y, GRIDSQUARESIZE, GRIDSQUARESIZE)
            gridSquareList.append(gridSquare)
            pygame.draw.rect(SCREEN, GRASS, gridSquare)

def mouse_square():
    KEYS = pygame.key.get_pressed()
    global MOUSESQUAREVAR

    if KEYS[pygame.K_d] and MOUSESQUAREVAR.right < 720:
        time.sleep(0.25)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(40, 0)

    elif KEYS[pygame.K_s] and MOUSESQUAREVAR.bottom < 800:
        time.sleep(0.25)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(0, 40)
    elif KEYS[pygame.K_a] and MOUSESQUAREVAR.left > 0:
        time.sleep(0.25)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(-40, 0)

    elif KEYS[pygame.K_w] and MOUSESQUAREVAR.top > 40:
        time.sleep(0.25)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(0, -40)
    pygame.draw.rect(SCREEN, RED, MOUSESQUAREVAR)

buildingOptions = ["Road", "House"]
selectedBuilding = buildingOptions[0]
cycleCounter = 0

def cycle_buildings():
    global selectedBuilding, cycleCounter, buildingOptions, moneyNeeded, incomeGenerated
    KEYS = pygame.key.get_pressed()
    if KEYS[pygame.K_RIGHT]:
        time.sleep(0.25)
        try:
            selectedBuilding = buildingOptions[cycleCounter + 1]
            cycleCounter += 1
        except IndexError:
            selectedBuilding = buildingOptions[0]
            cycleCounter = 0
    if KEYS[pygame.K_LEFT]:
        time.sleep(0.25)
        try:
            selectedBuilding = buildingOptions[cycleCounter - 1]
            cycleCounter -= 1
        except IndexError:
            selectedBuilding = buildingOptions[-1]
            cycleCounter = buildingOptions.index(buildingOptions[-1])
    if selectedBuilding == "House":
        moneyNeeded = 30
        incomeGenerated = 10
    elif selectedBuilding == "Road":
        moneyNeeded = 10
        incomeGenerated = 0
    else:
        moneyNeeded = 0
        incomeGenerated = 0

houseCoords = []
roadCoords = []

constructTextRect = CONSTRUCTTEXT.get_rect()

backspaceTextRect = BACKSPACETEXT.get_rect()

instructionTextRect = INSTRUCTIONTEXT.get_rect()

def check_double_build():
    global houseCoords,roadCoords,MOUSESQUAREVAR,doubleBuildAttempt
    doubleBuildAttempt = False
    for i in houseCoords:
        if MOUSESQUAREVAR.topleft == i:
            print("You cant build here!")
            doubleBuildAttempt = True
    for i in roadCoords:
        if MOUSESQUAREVAR.topleft == i:
            print("You cant build there!")
            doubleBuildAttempt = True

def construction_func():
    global CONSTRUCTBUTTONSELECTED, houseCoords, CONSTRUCTBUTTON, TREASURY, doubleBuildAttempt, roadCoords, INCOME
    #print(houseCoords)
    KEYS = pygame.key.get_pressed()
    pygame.draw.rect(SCREEN, BLUE, CONSTRUCTBUTTONSELECTED)
    backspaceTextRect.center = CONSTRUCTBUTTONSELECTED.center
    instructionTextRect.center = (400, 600)
    SCREEN.blit(BACKSPACETEXT, backspaceTextRect), SCREEN.blit(INSTRUCTIONTEXT, instructionTextRect)

    if KEYS[pygame.K_SPACE]:
        time.sleep(0.25)
        
        check_double_build()

        if TREASURY < moneyNeeded:
            print("Not enough money!")

        elif TREASURY >= moneyNeeded and doubleBuildAttempt == False:
            if selectedBuilding == "House":
                houseCoords.append(MOUSESQUAREVAR.topleft)
                TREASURY -= moneyNeeded
                INCOME += incomeGenerated
            elif selectedBuilding == "Road":
                roadCoords.append(MOUSESQUAREVAR.topleft)
                TREASURY -= moneyNeeded
        else:
            print("skill issue")

    buildingInfoText = FONTTYPE.render(f"Selected building: {selectedBuilding}, cost: ${moneyNeeded}, generates: ${incomeGenerated}",True,BLACK)
    buildingInfoTextRect = buildingInfoText.get_rect()
    buildingInfoTextRect.center = (400, 620)
    SCREEN.blit(buildingInfoText, buildingInfoTextRect)

    [SCREEN.blit(HOUSEMODELONE, i) for i in houseCoords]
    [SCREEN.blit(ROADMODELONE, i) for i in roadCoords]


timer = 0
def count_sec():
    global timer, INCOME, TREASURY, incomeTextRect, treasuryTextRect, incomeText, treasuryText
    incomeText = FONTTYPE.render(f"INCOME: ${INCOME} every 3 seconds", True, BLACK)
    incomeTextRect = incomeText.get_rect()
    treasuryText = FONTTYPE.render(f"TREASURY: ${TREASURY}", True, BLACK)
    treasuryTextRect = treasuryText.get_rect()
    incomeTextRect.topleft = (120, 20)
    treasuryTextRect.topleft = (20, 20)
    SCREEN.blit(treasuryText, treasuryTextRect), SCREEN.blit(incomeText, incomeTextRect)
    if timer < 1000:
        timer += 1

    else:
        timer = 0
        TREASURY += INCOME

numHouses = 0
def tax_the_poor():
    global numHouses, INCOME, houseCoords

    for buildings in houseCoords:
        if numHouses <= houseCoords.index(houseCoords[-1]):
            time.sleep(0.1)
            numHouses += 1
            INCOME += 10

def check_save():
    global TREASURY
    while True:
        user_input = input("Do you want to open a saved game? Y/N ")
        if user_input.upper() == "Y":
            try:
                user_input = input("Enter name of save game: ")
                with open(f"{user_input}.json", "r") as file:
                    save_game = json.load(file)
                    TREASURY = save_game["savedTreasury"]
                    for coords in save_game["savedHouses"]:
                        houseCoords.append(tuple(coords))
                    for coords in save_game["savedRoads"]:
                        roadCoords.append(tuple(coords))
                    break
            except FileNotFoundError:
                print(
                    "Sorry, this file could not be found. Make sure you spelled it correctly!"
                )
                continue
            except json.decoder.JSONDecodeError:
                print("Corrupted file. You probably did something stupid.")
                continue

        elif user_input.upper() == "N":
            break
        else:
            print("Invalid")
            continue
        time.sleep(0.25)
        try:
            selectedBuilding = BUILDINGOPTIONS[cycleCounter + 1]
            cycleCounter += 1
        except IndexError:
            selectedBuilding = BUILDINGOPTIONS[0]
            cycleCounter = 0
    if KEYS[pygame.K_LEFT]:
        time.sleep(0.25)
        try:
            selectedBuilding = BUILDINGOPTIONS[cycleCounter - 1]
            cycleCounter -= 1
        except IndexError:
            selectedBuilding = BUILDINGOPTIONS[-1]
            cycleCounter = BUILDINGOPTIONS.index(BUILDINGOPTIONS[-1])

HOUSECOORDS = []
ROADCOORDS = []
def construction_func(given_list=None, moneyNeeded=0, incomeGenerated=0):
    global CONSTRUCTBUTTONSELECTED, HOUSECOORDS, CONSTRUCTBUTTON, TREASURY, doubleBuildAttempt, ROADCOORDS

    if given_list != None:
        doubleBuildAttempt = False

        for i, j in list(zip(HOUSECOORDS, ROADCOORDS)):
            if MOUSESQUAREVAR.topleft == i or MOUSESQUAREVAR.topleft == j:
                time.sleep(0.25)
                print("You cant build here!")
                doubleBuildAttempt = True
        if TREASURY < moneyNeeded:
            time.sleep(0.25)
            print("Not enough money!")

        elif TREASURY >= moneyNeeded and doubleBuildAttempt == False:
            time.sleep(0.25)
            given_list.append(MOUSESQUAREVAR.topleft)
            TREASURY -= moneyNeeded
        else:
            print("skill issue")

    buildingInfoText = FONTTYPE.render(f"Selected building: {selectedBuilding}, cost: ${moneyNeeded}, generates: ${incomeGenerated}",True,BLACK)
    buildingInfoTextRect = buildingInfoText.get_rect()
    buildingInfoTextRect.center = (400, 620)
    SCREEN.blit(buildingInfoText, buildingInfoTextRect)

    HOUSECOORDS = list(dict.fromkeys(HOUSECOORDS))
    for x, y in HOUSECOORDS:
        SCREEN.blit(HOUSEMODELONE, (x, y))
    ROADCOORDS = list(dict.fromkeys(ROADCOORDS))
    for x, y in ROADCOORDS:
        SCREEN.blit(ROADMODELONE, (x, y))

timer = 0
def count_sec():
    global timer, INCOME, TREASURY, incomeTextRect, treasuryTextRect, incomeText, treasuryText
    incomeText = FONTTYPE.render(f"INCOME: ${INCOME} every 10 seconds", True, BLACK)
    incomeTextRect = incomeText.get_rect()
    treasuryText = FONTTYPE.render(f"TREASURY: ${TREASURY}", True, BLACK)
    treasuryTextRect = treasuryText.get_rect()
    incomeTextRect.topleft = (120, 20)
    treasuryTextRect.topleft = (20, 20)
    SCREEN.blit(treasuryText, treasuryTextRect), SCREEN.blit(incomeText, incomeTextRect)
    if timer < 1000:
        timer += 1

    else:
        timer = 0
        TREASURY += INCOME

numHouses = 0
def tax_the_poor():
    global numHouses, INCOME, HOUSECOORDS

    for buildings in HOUSECOORDS:
        if numHouses <= HOUSECOORDS.index(HOUSECOORDS[-1]):
            time.sleep(0.1)
            numHouses += 1
            INCOME += 10

def check_save():
    global TREASURY
    while True:
        user_input = input("Do you want to open a saved game? Y/N ")
        if user_input.upper() == "Y":
            try:
                user_input = input("Enter name of save game: ")
                with open(f"{user_input}.json", "r") as file:
                    save_game = json.load(file)
                    TREASURY = save_game["savedTreasury"]
                    for coords in save_game["savedHouses"]:
                        HOUSECOORDS.append(tuple(coords))
                    for coords in save_game["savedRoads"]:
                        ROADCOORDS.append(tuple(coords))
                    break
            except FileNotFoundError:
                print(
                    "Sorry, this file could not be found. Make sure you spelled it correctly!"
                )
                continue
            except json.decoder.JSONDecodeError:
                print("Corrupted file. You probably did something stupid.")
                continue

        elif user_input.upper() == "N":
            break
        else:
            print("Invalid")
            continue
