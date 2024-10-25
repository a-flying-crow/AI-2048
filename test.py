from flask import Flask, request, jsonify

app = Flask(__name__)
from Grid_3       import Grid
from ComputerAI_3 import ComputerAI
from PlayerAI_3   import PlayerAI
from Displayer_3  import Displayer
from random       import randint
import time
from flask import Flask, request, jsonify

import json
from flask_cors import CORS  # 导入CORS

app = Flask(__name__)
CORS(app)  # 启用CORS，允许所有来源访问
defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.05
grid = Grid(4)
possibleNewTiles = [2, 4]
probability = defaultProbability##0.9
initTiles  = defaultInitialTiles#2
computerAI = None
playerAI   = None
displayer  = None
over       = False
print('-------------------------------!')
playerAI  	= PlayerAI()
computerAI  = ComputerAI()
displayer 	= Displayer()

def setComputerAI(computerAI):
    computerAI = computerAI

def setPlayerAI(playerAI):
    playerAI = playerAI

def setDisplayer(displayer):
    displayer = displayer

def updateAlarm(currTime):
    ## print(currTime-prevTime)
    if currTime - prevTime > timeLimit + allowance:
        ## print(currTime-prevTime)##0.2+0.05
        over = False
    else:
        while time.perf_counter() - prevTime < timeLimit + allowance:
            pass

        prevTime = time.perf_counter()

    # 初始化游戏接口
@app.route('/initialize', methods=['POST'])
def initialize():
    print('12324123213123213123213')
    data = request.json

    setDisplayer(displayer)
    setPlayerAI(playerAI)
    setComputerAI(computerAI)

    print(data)
    board = data['board']           # 初始棋盘状态
    for i in range(len(board)):
        for j in range(len(board[0])):
            grid.setCellValue([i,j],int(board[i][j]))
    
    gridCopy = grid.clone()
    move = playerAI.getMove(gridCopy)##查询AI要走那个方向
    print(actionDic[move])

    # Validate Move
    if move != None and move >= 0 and move < 4:
        if grid.canMove([move]):##看在这个方向上能不能移动
            grid.move(move)

            # Update maxTile
            maxTile = grid.getMaxTile()
        else:
            print("Invalid PlayerAI Move")
            over = True
    displayer.display(grid)
            

    # 初始化后的第一步推荐和更新棋盘状态
    updated_board = grid  # 根据算法更新后的棋盘状态
    '''
    a=[]
    for i in range(len(grid)):
        b=[]
        for j in range(len(grid[0])):
            b.append(grid[i][j])
        a.append(b)
            
    a=json.dumps(a)
    '''

    return jsonify({
        'boardState': updated_board.map,
        'nextMove': ""+actionDic[move]
    })

# 常规移动接口
@app.route('/move', methods=['POST'])
def move():
    data = request.json

    # Player AI Goes First
    turn = PLAYER_TURN
    maxTile = 0

    prevTime = time.perf_counter()

    # Copy to Ensure AI Cannot Change the Real Grid to Cheat
    gridCopy = grid.clone()
           
            

    move = None

    print("Computer's turn:")
    y=int(data["newTile"]["col"])
    x=int(data["newTile"]["row"])
    move=[x,y]

    # Validate Move
    if move and grid.canInsert(move):
        #grid.setCellValue(move, pow(2,int(input())))
        grid.setCellValue(move, int(data["newTile"]["value"]))
    else:
        print("Invalid Computer AI Move")
        over = True

    print("Player's Turn:", end="")
               
    move = playerAI.getMove(gridCopy)##查询AI要走那个方向
    print(actionDic[move])

    # Validate Move
    if move != None and move >= 0 and move < 4:
        if grid.canMove([move]):##看在这个方向上能不能移动
            grid.move(move)

            # Update maxTile
            maxTile = grid.getMaxTile()
        else:
            print("Invalid PlayerAI Move")
            over = True
    else:
        print("Invalid PlayerAI Move - 1")
        over = True

    displayer.display(grid)

    # Exceeding the Time Allotted for Any Turn Terminates the Game
    #updateAlarm(time.perf_counter())
    #print(over)

    turn = 1 - turn
    print(maxTile)
    return jsonify({
    'boardState': grid.map,
    'nextMove': actionDic[move]
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000,debug=True)
