# BoulderDash Editor
import pgzrun
import pickle

editorState = True
editorEnabled = True 

if editorState:
    WIDTH = 1000

gameState = count = 0
editItem = "blank"
editorMessage = ""
editorMessageCount = 0

blockTypes = [
    Actor('blank', center=(900, 250)),
    Actor('soil', center=(900, 300)),
    Actor('rock', center=(900, 350)),
    Actor('gem', center=(900, 400)),
    Actor('wall', center=(900, 450))
    ]

loadButton = Actor('load', center=(850, 580))
saveButton = Actor('save', center=(950, 580))
items = [[] for _ in range(14)]
gems = collected = 0
rockford = Actor('rockford-1', center=(60, 100))

def draw():
    screen.fill((0,0,0))
    if gems == 0 and collected > 0: infoText("YOU COLLECTED ALL THE GEMS!")
    else: infoText("GEMS : "+ str(collected))
    for r in range(0, 14):
        for c in range(0, 20):
            if items[r][c] != "" and items[r][c] != "rockford":
                screen.blit(items[r][c], ((c*40), 40+(r*40)))
    if gameState == 0 or (gameState == 1 and count%4 == 0): rockford.draw()
    drawEditor()
    
def update():
    global count,gems
    mx = my = 0
    if count%10 == 0:
        gems = 0
        for r in range(13, -1, -1):
            for c in range(19, -1, -1):
                if items[r][c] == "gem":
                    gems += 1
                if items[r][c] == "rockford":
                    if keyboard.left: mx = -1
                    if keyboard.right: mx = 1
                    if keyboard.up: my = -1
                    if keyboard.down: my = 1
                if items[r][c] == "rock": testRock(r,c)
        rockford.image = "rockford"+str(mx)
        if gameState == 0 and editorState == False: moveRockford(mx,my)
    count += 1

def on_mouse_down(pos):
    global editItem
    if editorState:
        c = int(pos[0]/40)
        r = int((pos[1]-40)/40)
        if loadButton.collidepoint(pos): loadMap()
        if saveButton.collidepoint(pos): saveMap()
        if r > 0 and r < 14 and c > 0 and c < 20:
            if editItem != "blank":
                items[r][c] = editItem
            else : items[r][c] = ""
        else:
            for b in range(0, len(blockTypes)):
                if blockTypes[b].collidepoint(pos):
                    editItem = blockTypes[b].image

def on_key_down(key):
    global editorState, gameState, rockford, collected, gems
    if key == keys.SPACE and editorEnabled:
        editorState = not editorState
    if key == keys.ESCAPE:
        gems = collected = gameState = 0
        rockford = Actor('rockford-1', center=(60, 100))
        loadMap()

def infoText(t):
    screen.draw.text(t, center = (400, 20), owidth=0.5, ocolor=(255,255,255), color=(255,0,255) , fontsize=40)

def moveRockford(x,y):
    global collected
    rx, ry = int((rockford.x-20)/40), int((rockford.y-40)/40)
    if items[ry+y][rx+x] != "rock" and items[ry+y][rx+x] != "wall":
        if items[ry+y][rx+x] == "gem": collected +=1
        items[ry][rx], items[ry+y][rx+x] = "", "rockford"
        rockford.pos = (rockford.x + (x*40), rockford.y + (y*40))
    if items[ry+y][rx+x] == "rock" and y == 0:
        if items[ry][rx+(x*2)] == "":
            items[ry][rx], items[ry][rx+(x*2)], items[ry+y][rx+x] = "", "rock", "rockford"
            rockford.x += x*40

def testRock(r,c):
    if items[r+1][c] == "":
        moveRock(r,c,r+1,c)
    elif items[r+1][c] == "rock" and items[r+1][c-1] == "" and items[r][c-1] == "":
        moveRock(r,c,r+1,c-1)
    elif items[r+1][c] == "rock" and items[r+1][c+1] == "" and items[r][c+1] == "":
        moveRock(r,c,r+1,c+1)

def moveRock(r1,c1,r2,c2):
    global gameState
    items[r1][c1], items[r2][c2] = "", items[r1][c1]
    if items[r2+1][c2] == "rockford": gameState = 1
    
def drawEditor():
    global editorMessageCount
    screen.draw.text("EDITOR", center = (900, 20), owidth=0.5, ocolor=(255,255,255), color=(0,0,255) , fontsize=40)
    if editorState: screen.draw.text("ON", center = (900, 50), owidth=0.5, ocolor=(255,255,255), color=(255,0,0) , fontsize=40)
    for b in range(0, len(blockTypes)):   
        blockTypes[b].draw()
    if editItem != "":
        screen.blit(editItem,(880,100))
    loadButton.draw()
    saveButton.draw()
    if editorMessageCount > 0:
        screen.draw.text(editorMessage, center = (400, 300), owidth=0.5, ocolor=(255,255,255), color=(0,0,255) , fontsize=40)
        editorMessageCount -= 1

def loadMap():
    global items, rockford, editorMessage, editorMessageCount
    try:
        with open ('mymap.map', 'rb') as fp:
            items = pickle.load(fp)
        editorMessage = "MAP LOADED"
        editorMessageCount = 200
    except IOError:
        editorMessage = "DEFAULT MAP LOADED"
        editorMessageCount = 200
        for r in range(0, 14):
            for c in range(0, 20):
                itype = "soil"
                if(r == 0 or r == 13 or c == 0 or c == 19): itype = "wall"
                items[r].append(itype)
        items[1][1] = "rockford"

def saveMap():
    global editorMessage, editorMessageCount
    try:
        with open('mymap.map', 'wb') as fp:
            pickle.dump(items, fp)
        editorMessage = "MAP SAVED"
        editorMessageCount = 200
    except IOError:
        editorMessage = "ERROR SAVING MAP"
        editorMessageCount = 200
        
loadMap()
pgzrun.go()
