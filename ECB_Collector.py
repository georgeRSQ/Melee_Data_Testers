#ECB DATA DOCUMENTER


import csv
import melee #you will need to install libmelee fuckin obviously
from pathlib import Path
import re

mlog = melee.logger.Logger()
#change the writer to have the categories you will use in the testMove function
mlog.writer = csv.DictWriter(mlog.csvfile, fieldnames=["Character","Move","Action_State","Frame","ECB_Bottom_Offset","ECB_Top","ECB_Bottom","ECB_Left","ECB_Right","Is_IASA"], extrasaction='ignore')
#presumably this will NOT be the path to YOUR slippi dolphin folder
console = melee.Console(path="C:/Users/George/AppData/Roaming/Slippi Launcher/netplay/",slippi_address = "127.0.0.1",logger=mlog)

controller = melee.Controller(console=console, port=1)
controller_human = melee.Controller(console=console, port=2)

#ditto as above
console.run(iso_path = "C:/Users/George/Downloads/$$BM/SSBMv102.iso")
console.connect()

controller.connect()
controller_human.connect()

framesInfo = melee.framedata.FrameData()

'''ecbCsv = open('ecbList.csv', newline='')
ecbWriter = csv.writer(ecbCsv, delimiter=",")'''
def initGame():
    conFrame = 0
    while True:
        conFrame+=1
        gamestate = console.step()
        if gamestate is None and console is not None:
            continue
        if gamestate.menu_state in [melee.enums.Menu.IN_GAME]:
            '''ecbFrame = gamestate.PlayerState.ecb
            ecbCSV.writerow(ecbFrame);'''
            break
        elif conFrame < 60:
            melee.menuhelper.MenuHelper.choose_versus_mode(gamestate,controller_human);
        else:
            break

def seqCSS(charOI):
    conFrame = 0
    gamestate = console.step()
    while gamestate.menu_state not in [melee.enums.Menu.IN_GAME]:
            gamestate = console.step()
            conFrame += 1
            if conFrame < 70:
                melee.menuhelper.MenuHelper.choose_character(charOI,
                                                     gamestate,
                                                     controller,
                                                     0,
                                                     0,
                                                     swag = False,
                                                     start = False);
            elif 110 >= conFrame >= 70:
                melee.menuhelper.MenuHelper.choose_character(melee.enums.Character.FALCO,
                                                     gamestate,
                                                     controller_human,
                                                     0,
                                                     0,
                                                     swag = False,
                                                     start = False);
            elif conFrame > 110  and gamestate.menu_state in [melee.enums.Menu.CHARACTER_SELECT]:
                controller.press_button(melee.enums.Button.BUTTON_START)
            else:
                melee.menuhelper.MenuHelper.choose_stage(melee.enums.Stage.BATTLEFIELD, gamestate, controller)



def inputMove(movetype,movedir):
    stickOIX = 0
    stickOIY = 0
    match movedir:
        case "UP":
            stickOIY = 1
            stickOIX = 0
        case "DOWN":
            stickOIY = -1
            stickOIX = 0
        case "LEFT":
            stickOIX = -1
            stickOIY = 0
        case "RIGHT":
            stickOIX = 1
            stickOIY = 0
        case "UALEFT":
            stickOIX = -1
            stickOIY = 0.4
        case "DALEFT":
            stickOIX = -1
            stickOIY = -0.4
        case "UARIGHT":
            stickOIX = 1
            stickOIY = 0.4
        case "DARIGHT":
            stickOIX = 1
            stickOIY = -0.4
        case "NEUTRAL":
            stickOIX = 0
            stickOIY = 0
    match movetype:
        case "AIR":
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN, stickOIX, stickOIY)
            controller.press_button(melee.enums.Button.BUTTON_A)
        case "TILT":
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN,0,-1)
            controller.press_button(melee.enums.Button.BUTTON_R)
            console.step()
            controller.release_all()
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN, stickOIX/2, stickOIY/2)
            for i in range(1,30):
                console.step() 
            controller.press_button(melee.enums.Button.BUTTON_A)
        case "SPECIAL":
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN, stickOIX, stickOIY)
            controller.press_button(melee.enums.Button.BUTTON_B)
        case "AIRDODGE":
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN, stickOIX, stickOIY)
            controller.press_button(melee.enums.Button.BUTTON_R)
        case "GROUND_JUMP":
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN,0,-1)
            controller.press_button(melee.enums.Button.BUTTON_R)
            console.step()
            controller.release_all()
            for i in range(1,30):
                console.step() 
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN, stickOIX, 0)
            controller.press_button(melee.enums.Button.BUTTON_Y)
        case "SMASH":
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_MAIN,0,-1)
            controller.press_button(melee.enums.Button.BUTTON_R)
            console.step()
            controller.release_all()
            for i in range(1,30):
                console.step() 
            controller.tilt_analog_unit(melee.enums.Button.BUTTON_C, stickOIX, stickOIY)

def LRA_START():
    controller_human.release_all()
    controller_human.press_button(melee.enums.Button.BUTTON_L)
    controller_human.press_button(melee.enums.Button.BUTTON_R)
    controller_human.press_button(melee.enums.Button.BUTTON_A)
    controller_human.press_button(melee.enums.Button.BUTTON_START)
    console.step()
    console.step()
    console.step()
    console.step()
    console.step()
    console.step()
    controller_human.release_all()
    console.step()
    console.step()
    console.step()
    '''controller_human.press_button(melee.enums.Button.BUTTON_START)
    console.step()
    console.step()
    console.step()
    controller_human.release_all();'''
    



def testMove(moveToTest):
    cframe = 0
    gamestate = console.step()
    play1 = gamestate.players[1]
    while not ((cframe > 105) and (play1.action in [melee.enums.Action.STANDING,melee.enums.Action.FALLING,melee.enums.Action.FALLING_FORWARD,melee.enums.Action.FALLING_BACKWARD,melee.enums.Action.FALLING_AERIAL,melee.enums.Action.FALLING_AERIAL_FORWARD,melee.enums.Action.FALLING_AERIAL_BACKWARD,melee.enums.Action.DEAD_FALL,melee.enums.Action.LANDING,melee.enums.Action.LANDING_SPECIAL])):
        gamestate = console.step();
        controller.release_all();
        if cframe == 100:
            inputMove(moveToTest["type"], moveToTest["dir"])
        play1 = gamestate.players[1]
        x = play1.action
        xFrame = play1.action_frame
        if cframe >= 101:
            mlog.log("Character", characterOI, concat = False)
            mlog.log("Move", moveToTest["dir"]+moveToTest["type"], concat = False)
            mlog.log("Action_State", str(x), concat = False)
            mlog.log("Frame", str(xFrame),concat = False)
            mlog.log("ECB_Bottom_Offset", str(play1.ecb.bottom.y), concat = True)
            mlog.log("ECB_Top", str(play1.ecb.top),concat=True)
            mlog.log("ECB_Right", str(play1.ecb.right), concat=True)
            mlog.log("ECB_Bottom", str(play1.ecb.bottom), concat = True)
            mlog.log("ECB_Left", str(play1.ecb.left), concat = True)
            try:
                mlog.log("Is_IASA", str(xFrame >= framesInfo.iasa(play1.character,x)), concat = False)
            except:
                mlog.log("Is_IASA", "NA", concat = False)
            mlog.writeframe()
        cframe+=1




moveOI = {"type": "AIR", "dir": "DOWN"}
characterOI = melee.enums.Character.FOX


initGame()

for k in melee.enums.Character:
    characterOI = k
    if characterOI in [melee.enums.Character.SHEIK]:
        continue #There's like 90% for sure an easy way to get Sheik with LibMelee's menuhelper function but what the fuck am i, a CS major?
    if characterOI in [melee.enums.Character.WIREFRAME_MALE]:
        mlog.writelog()
        console.stop()
    for i in ["UP","DOWN","LEFT","RIGHT","NEUTRAL"]:
        for j in ["AIR","SPECIAL"]:
            if characterOI in [melee.enums.Character.MEWTWO] and i == "NEUTRAL" and j == "SPECIAL":
                continue; #Mewtwo will charge neutral-b forever and break the program without a change to testMove/inputMove, and I was not going to do that just for gd Tora's sake
            moveOI = {"type": j, "dir":i}
            #mlog.csvfile = open("Logs" / Path(re.sub("Character.","",str(characterOI)) + "_" + str(moveOI["dir"]+ "_" + moveOI["type"]) + ".csv"), 'w') #hope to modify this program to separate info soon
            seqCSS(characterOI)
            testMove(moveOI)
            LRA_START()







