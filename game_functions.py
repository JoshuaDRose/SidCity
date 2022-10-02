import sys
import time
import json
try:
    import pygame
except ImportError:
    raise ImportError
    sys.exit(1)

from settings import *
from pygame.locals import *

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

roadCoords = []
houseCoords = []
gridSquareList = []

buildingOptions = ["Road", "House"]
selectedBuilding = buildingOptions[0]

timer = 0 # relocated timer variable
numHouses = 0
cycleCounter = 0
default_sleep: float = 0.25

constructTextRect = CONSTRUCTTEXT.get_rect()
backspaceTextRect = BACKSPACETEXT.get_rect()
instructionTextRect = INSTRUCTIONTEXT.get_rect()

def create_grid() -> None:
    global gridSquare
    for x in range(0, WINDOW_WIDTH - 80, GRIDSQUARESIZE):
        for y in range(0, WINDOW_HEIGHT, GRIDSQUARESIZE):
            gridSquare = pygame.Rect(x, y, GRIDSQUARESIZE, GRIDSQUARESIZE)
            gridSquareList.append(gridSquare)
            pygame.draw.rect(SCREEN, GRASS, gridSquare)

def mouse_square() -> None:
    KEYS = pygame.key.get_pressed()

    global MOUSESQUAREVAR

    if KEYS[pygame.K_d] and MOUSESQUAREVAR.right < 720:
        time.sleep(default_sleep)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(40, 0)

    elif KEYS[pygame.K_s] and MOUSESQUAREVAR.bottom < 800:
        time.sleep(default_sleep)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(0, 40)

    elif KEYS[pygame.K_a] and MOUSESQUAREVAR.left > 0:
        time.sleep(default_sleep)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(-40, 0)

    elif KEYS[pygame.K_w] and MOUSESQUAREVAR.top > 40:
        time.sleep(default_sleep)
        MOUSESQUAREVAR = MOUSESQUAREVAR.move(0, -40)

    pygame.draw.rect(SCREEN, RED, MOUSESQUAREVAR)

def cycle_buildings() -> None:
    global selectedBuilding, cycleCounter, buildingOptions, moneyNeeded, incomeGenerated

    KEYS = pygame.key.get_pressed()

    if KEYS[pygame.K_RIGHT]:
        time.sleep(default_sleep)
        try:
            selectedBuilding = buildingOptions[cycleCounter + 1]
            cycleCounter += 1
        except IndexError:
            selectedBuilding = buildingOptions[0]
            cycleCounter = 0
    if KEYS[pygame.K_LEFT]:
        time.sleep(default_sleep)
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


def check_double_build() -> None | bool:
    """ Check that building spot is valid and/or player has required funds """
    global houseCoords,roadCoords,MOUSESQUAREVAR,doubleBuildAttempt
    doubleBuildAttempt = False
    for i in houseCoords:
        if MOUSESQUAREVAR.topleft == i:
            print("You cant build here!")
            doubleBuildAttempt = True
            return False
    for i in roadCoords:
        if MOUSESQUAREVAR.topleft == i:
            print("You cant build there!")
            doubleBuildAttempt = True
            return False

def construction_func() -> None:
    """ Manage construction of houses and roads """
    global CONSTRUCTBUTTONSELECTED, houseCoords, CONSTRUCTBUTTON, TREASURY, doubleBuildAttempt, roadCoords, INCOME

    KEYS = pygame.key.get_pressed()
    pygame.draw.rect(SCREEN, BLUE, CONSTRUCTBUTTONSELECTED)
    backspaceTextRect.center = CONSTRUCTBUTTONSELECTED.center
    instructionTextRect.center = (400, 600)
    SCREEN.blit(BACKSPACETEXT, backspaceTextRect), SCREEN.blit(INSTRUCTIONTEXT, instructionTextRect)

    if KEYS[pygame.K_SPACE]:
        time.sleep(default_sleep)
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
            print("skill issue") # lol

    buildingInfoText = FONTTYPE.render(f"Selected building: {selectedBuilding}, cost: ${moneyNeeded}, generates: ${incomeGenerated}", True, BLACK) # added spacing between vars
    buildingInfoTextRect = buildingInfoText.get_rect()
    buildingInfoTextRect.center = (400, 620)
    SCREEN.blit(buildingInfoText, buildingInfoTextRect)

    [SCREEN.blit(HOUSEMODELONE, i) for i in houseCoords]
    [SCREEN.blit(ROADMODELONE, i) for i in roadCoords]


def count_sec() -> None:
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


def tax_the_poor() -> None:
    """ idk what this function is but the name made me laugh """
    global numHouses, INCOME, houseCoords

    for buildings in houseCoords:
        if numHouses <= houseCoords.index(houseCoords[-1]):
            time.sleep(0.1)
            numHouses += 1
            INCOME += 10

def check_save() -> None | bool:
    """ Manage save files """
    global TREASURY
    while 1:
        try:
            user_input: str = input("Do you want to open a saved game? Y/N ").upper()
        except TypeError:
            print("Only \'Y\' or \'N\' is accepted.")
        if user_input == "Y":
            try:
                user_input = input("Enter name of save: ")
                with open(f"{user_input}.json", "r") as file:
                    save_game = json.load(file)
                    TREASURY = save_game["savedTreasury"]
                    for coords in save_game["savedHouses"]:
                        houseCoords.append(tuple(coords))
                    for coords in save_game["savedRoads"]:
                        roadCoords.append(tuple(coords))
                    break
            except FileNotFoundError:
                print("""
Sorry, this file could not be found. Make sure you spelled it correctly!"""
)
                continue
            except json.decoder.JSONDecodeError:
                print("Corrupted file. You probably did something stupid.")
                continue

        elif user_input == "N":
            return False
        else:
            print("Invalid")
            continue
