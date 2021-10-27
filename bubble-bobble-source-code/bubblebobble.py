# Bubble Bobble
import pgzrun
import random
bub = Actor('bubr0',(400,300))
bub.direction = "r"
count = bub.jump = 0
bub.onground = False
platformActors = []
bubbles = []
for r in range(40):
    for c in range(20):
        if c == 0 or c == 19 or r == 0 or r== 39 or ((r == 10 or r == 20 or r == 30) and c != 3  and c != 4 and c != 15  and c != 16):
            platformActors.append(Actor('platform11',(50+(c*37),80+(r*12))))

def draw():
    screen.blit("background", (0, 0))
    drawPlatforms()
    drawBubbles()
    bub.draw()

def update():
    global count
    if count%20 == 0: bub.image = "bub"+ bub.direction + "0"
    if keyboard.left:
        moveBub(-1,0)
        bub.direction = "l"
        bub.image = "bubl"+ str(int(count/8)%3)
    if keyboard.right:
        moveBub(1,0)
        bub.direction = "r"
        bub.image = "bubr"+ str(int(count/8)%3) 
    checkGravity()
    updateBubbles()
    count += 1
    
def on_key_down(key):
    if key.name == "UP":
        if bub.onground == True: bub.jump = 60
    if key.name == "SPACE": fireBubble()

def drawPlatforms():
    for p in range(len(platformActors)): platformActors[p].draw()
    
def moveBub(x,y):
    if bub.x+x < 720 and bub.x+x > 80:
        bub.x += x*2
        for b in range(len(bubbles)):
            if bubbles[b].collidepoint((bub.x,bub.y)): bubbles[b].x += x*2

def checkGravity():
    if bub.jump > 0:
        if bub.y > 85: bub.y -= 3 + (bub.jump/30)
        bub.jump -=1
        if bub.jump <= 0: bub.y = (bub.y // 2) *2
        for b in range(len(bubbles)):
            if bubbles[b].collidepoint((bub.x,bub.y)) and bubbles[b].status == 0:
                bubbles[b].countdown = 10
                bub.jump = 0
                bub.y = (bub.y // 2) *2
    bub.onground = False
    for p in range(len(platformActors)):
        if((bub.x > platformActors[p].x-20 and bub.x < platformActors[p].x+20) and bub.y+18 == platformActors[p].y-14): bub.onground = True
    if bub.onground == False: bub.y += 2

def fireBubble():
    bub.image = "bub"+ bub.direction+ "3"
    bubbles.append(Actor('bubble4',(bub.x,bub.y)))
    bubbles[len(bubbles)-1].status = 20
    bubbles[len(bubbles)-1].direction = bub.direction
    bubbles[len(bubbles)-1].driftx = 0
    bubbles[len(bubbles)-1].drifty = -0.5
    bubbles[len(bubbles)-1].countdown = 1000
    
def drawBubbles():
    for b in range(len(bubbles)): bubbles[b].draw()
    
def updateBubbles():
    for b in range(len(bubbles)):
        if bubbles[b].status > 0:
            if bubbles[b].direction == "l":
                bubbles[b].pos = checkCollision(bubbles[b],-bubbles[b].status,0)
            else:
                bubbles[b].pos = checkCollision(bubbles[b],bubbles[b].status,0)
            bubbles[b].status -= 1
        else:
            bubbles[b].pos = checkCollision(bubbles[b],bubbles[b].driftx,bubbles[b].drifty)
            if random.randint(0, 500) == 1: bubbles[b].driftx = (random.randint(0, 4)-2)/10
        if bubbles[b].countdown > 10: bubbles[b].image = "bubble"+str(int(bubbles[b].status/5))
        else: bubbles[b].image = "bubble-1"
        bubbles[b].countdown -= 1
    for b in range(len(bubbles)):
        if bubbles[b].countdown < 0:
            bubbles.remove(bubbles[b])
            break;
                
def checkCollision(o,xinc,yinc):
    if o.x+xinc > 720 or o.x +xinc < 80 or o.y+yinc < 90 or o.y+yinc > 550:
        o.drifty = o.drifty *-1
        o.driftx = o.driftx *-1
        return o.pos
    for b in range(len(bubbles)):
        if bubbles[b].collidepoint((o.x+xinc,o.y+yinc)) and o != bubbles[b]:
            bubbles[b].x += xinc
            bubbles[b].driftx = (random.randint(0, 4)-2)/10
    return o.x+xinc,o.y+yinc
        
pgzrun.go()
