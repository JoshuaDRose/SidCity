import pygame, time, os, json
from settings import *
import game_functions
from game_functions import houseCoords, numHouses, roadCoords # edit: added spacing

# TODO
# fix construction feature

# check that the save feature works - save feature works
# construction feature is not working, can double build and income variable doesnt work
# can double build
# cant seem to build a house

if not pygame.get_init():
    pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

pygame.display.set_caption("City Builder")

constructTextRect = CONSTRUCTTEXT.get_rect()

backspaceTextRect = BACKSPACETEXT.get_rect()

instructionTextRect = INSTRUCTIONTEXT.get_rect()

pygame.draw.rect(SCREEN, RED, CONSTRUCTBUTTON)

mousePos = pygame.mouse.get_pos()

checkConstructButton = [None]

game_functions.check_save()

menuButtonSelected = [None]

pause = [None]

running = True

def main_menu():
    while pause == True:
        SCREEN.fill(GREY)
        saveAndQuitButton = pygame.Rect(200, 600, 400, 50)
        text = pygame.font.Font("freesansbold.ttf", 18)
        SQText = text.render("Save and quit", True, BLACK)
        SQTextRect = SQText.get_rect()
        pygame.draw.rect(SCREEN, WHITE, saveAndQuitButton)
        """
        if mouse[0] >= 200 and mouse[0] <= 600:
            if mouse[1] >= 600 and mouse[1] <= 650:
                pygame.draw.rect(SCREEN, DARKWHITE, saveAndQuitButton)
        """ 
        # can be shortened to:
        if mouse[0] in range(200, 600) and mouse[1] in range(600, 650):
            pygame.draw.rect(SCREEN, DARKWHITE, saveAndQuitButton)
        SQTextRect.center = saveAndQuitButton.center


while running:

    KEYS = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    if KEYS[pygame.K_q]:
        running = False

    game_functions.create_grid()

    if CONSTRUCTBUTTON.collidepoint(
        pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and \
                pygame.mouse.get_pressed() == (1, 0, 0):
        checkConstructButton[0] = True
        time.sleep(0.25)

    if checkConstructButton[0] == True:

        game_functions.cycle_buildings()

        game_functions.mouse_square()

        game_functions.construction_func()

    [SCREEN.blit(HOUSEMODELONE, i) for i in houseCoords]
    [SCREEN.blit(ROADMODELONE,  i) for i in roadCoords]

    if KEYS[pygame.K_BACKSPACE]:
        checkConstructButton[0] = None

    if checkConstructButton[0] != True:
        pygame.draw.rect(SCREEN, RED, CONSTRUCTBUTTON)
        constructTextRect.center = CONSTRUCTBUTTON.center
        SCREEN.blit(CONSTRUCTTEXT, constructTextRect)

    menuButton = pygame.image.load("pause_button.png")
    menuButtonRect = menuButton.get_rect()
    mouse = pygame.mouse.get_pos()
    SCREEN.blit(menuButton, (720, 0))
    menuButtonRect.topleft = (720, 0)
    if menuButtonRect.collidepoint(
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and \
            pygame.mouse.get_pressed() == (1, 0, 0):
        time.sleep(0.25)
        pause[0] = True

    # SKILL ISSUE WITH THIS PART
    if pause[0]:
        while pause:
            SCREEN.fill(GREY)
            saveAndQuitButton = pygame.Rect(200, 600, 400, 50)
            text = pygame.font.Font("freesansbold.ttf", 18)
            SQText = text.render("Save and quit", True, BLACK)
            SQTextRect = SQText.get_rect()
            pygame.draw.rect(SCREEN, WHITE, saveAndQuitButton)
            if mouse[0] >= 200 and mouse[0] <= 600:
                if mouse[1] >= 600 and mouse[1] <= 650:
                    pygame.draw.rect(SCREEN, DARKWHITE, saveAndQuitButton)
            SQTextRect.center = saveAndQuitButton.center
            pygame.display.flip()

    game_functions.tax_the_poor()
    game_functions.count_sec()

    pygame.display.update()

print("Number of houses:", numHouses)
print("INCOME:", INCOME)
print("Bank:", TREASURY)

SAVEVARIABLES = {
    savedIncome: INCOME,
    savedTreasure: TREASURY,
    savedHouses: houseCoords,
    savedRoads: roadCoords
}

while True:
    save_input = input("Do you want to save? Y/N ")
    if save_input.upper() == "Y":
        try:
            filename = input("Enter save name: ")
            file = open(f"{filename}.json", "x")
        except FileExistsError:
            raw_input = input(
                "This file already exists! Are you sure you want to overwrite it? Y/N "
            )
            if raw_input.upper() == "Y":
                if os.path.exists(f"{filename}.json"):
                    os.remove(f"{filename}.json")
                    with open(f"{filename}.json", "w") as save:
                        json.dump(SAVEVARIABLES, save)
                break
            elif raw_input.upper() == "N":
                continue
            else:
                print("Invalid")
                continue
        else:
            json.dump(SAVEVARIABLES, file)
            file.close()
            break
    elif save_input.upper() == "N":
        break
    else:
        print("Invalid")
        continue

pygame.quit()
