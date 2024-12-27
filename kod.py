import numpy as np
import random
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

os.system('cls')

class Entity:
    def __init__(self, pos, velocity, dir, state, age, resistance, board) -> None:
        self.pos = pos
        self.velocity = velocity
        self.dir = dir
        self.state = state
        self.age = age
        self.resistance = resistance
        self.board = board
        self.progress = 0
        self.progress_level = 0
        self.counter = 0
        self.pos['x2'] = self.pos['x']
        self.pos['y2'] = self.pos['y']
        self.meetings = set()
        self.day = 0
        
    def meet(self) -> bool:
        x = self.pos['x2']
        y = self.pos['y2']
        _choices = dirs.copy()
        to_remove = []

        # krawędzie 
        # lewa 
        if x - 1 == 0:
            to_remove.append('left')
            to_remove.append('top-left')
            to_remove.append('bottom-left')
            to_remove.append('bottom')
            to_remove.append('top')

        # górna
        if y - 1 == 0:
            to_remove.append('left')
            to_remove.append('right')
            to_remove.append('top')
            to_remove.append('top-left')
            to_remove.append('top-right')

        # dolna
        if y == self.board.shape[0]:
            to_remove.append('bottom')
            to_remove.append('left')
            to_remove.append('right')
            to_remove.append('bottom-left')
            to_remove.append('bottom-right')

        # prawa
        if x == self.board.shape[1]:
            to_remove.append('right')
            to_remove.append('top')
            to_remove.append('bottom')
            to_remove.append('top-right')
            to_remove.append('bottom-right')


        # przypadek spotkania        
        if y - 2 >= 0 and y - 2 < self.board.shape[1] and x - 2 < self.board.shape[0] and x - 2 >= 0:
            if self.board[y - 2][x - 2] != None:
                to_remove.append('top-left')
                to_remove.append('left')
                to_remove.append('top')
                self.meetings.add(self.board[y - 2][x - 2])
        
        if y - 1 >= 0 and y - 1 < self.board.shape[1] and x - 2 < self.board.shape[0] and x - 2 >= 0:
            if self.board[y - 1][x - 2] != None:
                to_remove.append('top-left')
                to_remove.append('left')
                to_remove.append('bottom-left')
                self.meetings.add(self.board[y - 1][x - 2])

        if y >= 0 and y < self.board.shape[1] and x - 2 < self.board.shape[0] and x - 2 >= 0:
            if self.board[y][x - 2] != None:
                to_remove.append('left')
                to_remove.append('bottom-left')
                to_remove.append('bottom')
                self.meetings.add(self.board[y][x - 2])

        if y - 2 >= 0 and y - 2 < self.board.shape[1] and x - 1 < self.board.shape[1] and x - 1 >= 0:
            if self.board[y - 2][x - 1] != None:
                to_remove.append('top')
                to_remove.append('top-right')
                to_remove.append('top-left')
                self.meetings.add(self.board[y - 2][x - 1])

        if y >= 0 and y < self.board.shape[1] and x - 1 < self.board.shape[1] and x - 1 >= 0:
            if self.board[y][x - 1] != None:
                to_remove.append('bottom')
                to_remove.append('bottom-right')
                to_remove.append('bottom-left')
                self.meetings.add(self.board[y][x - 1])

        if y - 2 >= 0 and y - 2 < self.board.shape[1] and x < self.board.shape[1] and x >= 0:
            if self.board[y - 2][x] != None:
                to_remove.append('top')
                to_remove.append('top-right')
                to_remove.append('right')
                self.meetings.add(self.board[y - 2][x])

        if y - 1 >= 0 and y - 1 < self.board.shape[1] and x < self.board.shape[1] and x >= 0:
            if self.board[y - 1][x] != None:
                to_remove.append('right')
                to_remove.append('top-right')
                to_remove.append('bottom-right')
                self.meetings.add(self.board[y - 1][x])

        if y >= 0 and y < self.board.shape[1] and x < self.board.shape[1] and x >= 0:
            if self.board[y][x] != None:
                to_remove.append('bottom')
                to_remove.append('bottom-right')
                to_remove.append('right')
                self.meetings.add(self.board[y][x])

        for t in to_remove:
            try:
                _choices.remove(t)
            except: pass

        if len(_choices) == 0:
            self.dir = None
            return

        if self.dir not in _choices:
            self.dir = random.choice(_choices)

    def update(self) -> None:
        self.counter += 1
        self.progress += self.velocity / round_steps
        self.progress_level += 1
        x = self.pos['x']
        y = self.pos['y']
        self.meet() 
        self.move(self.velocity / round_steps)
        x = self.pos['x']
        y = self.pos['y']

        # poprawanie jeśli wyszło poza zakres
        rest = 0
        if x > self.board.shape[0]:
            rest = x - self.board.shape[0]
            self.pos['x'] = self.board.shape[0]
        if x < 1:
            rest = np.abs(x)
            self.pos['x'] = 1
        if y > self.board.shape[1]:
            rest = y - self.board.shape[1]
            self.pos['y'] = self.board.shape[1]
        if y < 1:
            rest = np.abs(y)
            self.pos['y'] = 1

        if rest > 0:
            self.meet()
            x, y, x2, y2 = self.move(rest)
    
    def move(self, distance):
        x = self.pos['x']
        y = self.pos['y']
        x2 = self.pos['x2']
        y2 = self.pos['y2']
        self.board[y2 - 1][x2 - 1] = None
        
        if self.dir == 'bottom-right':
            x = self.pos['x'] + distance
            y = self.pos['y'] + distance
            x2 = np.floor(x)
            y2 = np.floor(y)

        elif self.dir == 'bottom-left':
            x = self.pos['x'] - distance
            y = self.pos['y'] + distance
            x2 = np.ceil(x)
            y2 = np.floor(y)

        elif self.dir == 'top-right':
            x = self.pos['x'] + distance
            y = self.pos['y'] - distance
            x2 = np.floor(x)
            y2 = np.ceil(y)

        elif self.dir == 'top-left':
            x = self.pos['x'] - distance
            y = self.pos['y'] - distance
            x2 = np.ceil(x)
            y2 = np.ceil(y)

        elif self.dir == 'top':
            y = self.pos['y'] - distance
            y2 = np.ceil(y)

        elif self.dir == 'bottom':
            y = self.pos['y'] + distance
            y2 = np.floor(y)

        elif self.dir == 'right':
            x = self.pos['x'] + distance
            x2 = np.floor(x)

        elif self.dir == 'left':
            x = self.pos['x'] - distance
            x2 = np.ceil(x)
        else:
            return x, y, x2, y2

        if self.progress_level == round_steps:
            self.pos['x'] = np.round(x)
            self.pos['y'] = np.round(y)
            self.pos['x2'] = int(np.round(x))
            self.pos['y2'] = int(np.round(y))
        else:
            self.pos['x'] = x
            self.pos['y'] = y
            self.pos['x2'] = int(x2)
            self.pos['y2'] = int(y2)

        if self.pos['x2'] > self.board.shape[0]:
            self.pos['x2'] = self.board.shape[0]
        if self.pos['x2'] < 1:
            self.pos['x2'] = 1
        if self.pos['y2'] > self.board.shape[1]:
            self.pos['y2'] = self.board.shape[1]
        if self.pos['y2'] < 1:
            self.pos['y2'] = 1

        self.board[self.pos['y2'] - 1][self.pos['x2'] - 1] = self
        
        return x, y, x2, y2
        

    def __str__(self) -> str:
        return str({
            'pos': self.pos,
            'velocity': self.velocity,
            'dir': self.dir,
            'state': self.state,
            'age': self.age,
            'resistance': self.resistance
        })
    
    __repr__ = __str__

n = 100

size = 100

dirs = ['left', 'right', 'top', 'bottom', 'top-left', 'top-right', 'bottom-left', 'bottom-right']

states = ['Z', 'C', 'ZD', 'ZZ']

# inicjalizacja 

entities = []

board = np.full((size, size), None, dtype=Entity)

# nadawanie początkowych wartości
for i in range(n):
    age = random.randint(0, 60)
    dir = dirs[random.randint(0, len(dirs) - 1)]
    state = states[random.randint(0, len(states) - 1)]
    x = random.randint(1, size)
    y = random.randint(1, size)
    while board[x - 1][y - 1] != None:
       x = random.randint(1, size)
       y = random.randint(1, size) 
    pos = {'x': x, 'y': y}
    velocity = random.randint(1, 3)
    if age < 15 or age >= 70:
        resistence = 3
    elif age >= 40 and age < 70:
        resistence =  6
    elif age >= 15 and age < 40:
        resistence = 10
    entity = Entity(pos, velocity, dir, state, age, resistence, board)
    board[y - 1][x - 1] = entity
    entities.append(entity)

rounds = 50

round_steps = 3

def replace(board):
    new_board = np.zeros([i for i in board.shape] + [3]).astype(int)
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if isinstance(col, Entity):
                if board[y][x].state == 'C':
                    new_board[y][x] = (255, 0, 0)
                elif board[y][x].state == 'Z':
                    new_board[y][x] = (255, 255, 0)
                elif board[y][x].state == 'ZD':
                    new_board[y][x] = (255, 127, 80)
                elif board[y][x].state == 'ZZ':
                    new_board[y][x] = (0, 255, 0)
                else: raise Exception('No state for entity')
            else:
                new_board[y][x] = (0, 0, 0)
    return new_board

fig, ax = plt.subplots()
cax = ax.imshow(replace(board), cmap='viridis', vmin=0, vmax=8)

def init():
    cax.set_data(replace(board))
    return cax,

def update(frame):
    if frame % round_steps == 0:
        print(f'runda: {int(frame / round_steps + 1)}')
        to_remove = []
        for entity in entities:
            entity.progress = 0
            entity.progress_level = 0
            entity.age += 1
            if entity.age == 100 or entity.resistance == 0:
                board[entity.pos['y2'] - 1][entity.pos['x2'] - 1] = None
                to_remove.append(entity)
                continue
            if entity.age < 15 or entity.age >= 70 and entity.resistance > 3:
                entity.resistance = 3
            elif entity.age >= 40 and entity.age < 70 and entity.resistance <= 3:
                entity.resistance =  3.1
            elif entity.age >= 40 and entity.age < 70 and entity.resistance > 6:
                entity.resistance = 6
            elif entity.age >= 15 and entity.age < 40 and entity.resistance <= 6:
                entity.resistance = 10
            if entity.day == 2 and entity.state == 'Z':
                entity.state = 'C'
                entity.day = 0
            if entity.day == 7 and entity.state == 'C':
                entity.state = 'ZD'
                entity.day = 0
            if entity.day == 5 and entity.state == 'ZD':
                entity.state = 'ZZ'
                entity.day = 0

            if entity.state == 'Z':
                entity.resistance -= 0.1
            if entity.state == 'C':
                entity.resistance -= 0.5
            if entity.state == 'ZD':
                entity.resistance += 0.1
            if entity.state == 'ZZ':
                entity.resistance += 0.05

            if entity.age >= 20 and entity.age <= 40:
                for meeting in entity.meetings:
                    # relacje 
                    if entity.state == 'ZZ' and meeting.state == 'Z':
                        if entity.resistance <= 3:
                            entity.state = 'Z'
                    if entity.state == 'ZZ' and meeting.state == 'Z':
                        if meeting.resistance <= 3:
                            meeting.state = 'Z'
                    if entity.state == 'ZZ' and meeting.state == 'C':
                        if entity.resistance <= 6:
                            entity.state = 'Z'
                        elif entity.resistance > 6:
                            entity.resistance -= 3
                    if entity.state == 'ZZ' and meeting.state == 'Z':
                        if meeting.resistance <= 6:
                            meeting.state = 'Z'
                        elif meeting.resistance > 6:
                            meeting.resistance -= 3
                    if entity.state == 'ZZ' and meeting.state == 'ZD':
                        meeting.resistance += 1
                    if entity.state == 'ZZ' and meeting.state == 'ZD':
                        entity.resistance += 1
                    if entity.state == 'ZZ' and meeting.state == 'ZZ':
                        if entity.age < 15 or entity.age >= 70:
                            entity.resistance = 3
                        elif entity.age >= 40 and entity.age < 70:
                            entity.resistance = 6
                        elif entity.age >= 15 and entity.age < 40:
                            entity.resistance = 10
                        if meeting.age < 15 or meeting.age >= 70:
                            meeting.resistance = 3
                        elif meeting.age >= 40 and meeting.age < 70:
                            meeting.resistance = 6
                        elif meeting.age >= 15 and meeting.age < 40:
                            meeting.resistance = 10
                    if entity.state == 'C' and meeting.state == 'Z':
                        if meeting.resistance <= 6:
                            meeting.state = 'C'
                        entity.day = 0
                    if entity.state == 'Z' and meeting.state == 'C':
                        if entity.resistance <= 6:
                            entity.state = 'C'
                        meeting.day = 0
                    if entity.state == 'C' and meeting.state == 'ZD':
                        if meeting.resistance <= 6:
                            meeting.state = 'Z'
                    if entity.state == 'ZD' and meeting.state == 'C':
                        if entity.resistance <= 6:
                            entity.state = 'Z'
                    if entity.state == 'C' and meeting.state == 'C':
                        if entity.age < 15 or entity.age >= 70:
                            entity.resistance = 0.1
                        elif entity.age >= 40 and entity.age < 70:
                            entity.resistance = 3.1
                        elif entity.age >= 15 and entity.age < 40:
                            entity.resistance = 6.1
                        if meeting.age < 15 or meeting.age >= 70:
                            meeting.resistance = 0.1
                        elif meeting.age >= 40 and meeting.age < 70:
                            meeting.resistance = 3.1
                        elif meeting.age >= 15 and meeting.age < 40:
                            meeting.resistance = 6.1
                    if entity.state == 'Z' and meeting.state == 'ZD':
                        meeting.resistance -= 1
                    if entity.state == 'ZD' and meeting.state == 'Z':
                        entity.resistance -= 1 
                    if entity.state == 'Z' and meeting.state == 'Z':
                        entity.resistance -= 1
                        meeting.resistance -= 1
                    if entity.state == 'ZD' and meeting.state == 'ZD':
                        pass
                    for i in range(random.randint(1, 2)):
                        if meeting.age >= 20 and meeting.age <= 40:
                            age = 0
                            dir = dirs[random.randint(0, len(dirs) - 1)]
                            state = 'ZZ'
                            x = random.randint(1, size)
                            y = random.randint(1, size)
                            while board[x - 1][y - 1] != None:
                                x = random.randint(1, size)
                                y = random.randint(1, size) 
                            pos = {'x': x, 'y': y}
                            velocity = random.randint(1, 3)
                            resistence = 10
                            entity_ = Entity(pos, velocity, dir, state, age, resistence, board)
                            board[y - 1][x - 1] = entity_
                            entities.append(entity_)
                        try:
                            meeting.meetings.remove(entity)
                        except: 
                            pass

            entity.meetings = set()
            entity.day += 1
        for tr in to_remove:
            entities.remove(tr)
    for entity in entities:
        entity.update()
    new_board = board.copy()
    cax.set_data(replace(new_board))
    return cax,


ani = animation.FuncAnimation(
    fig, update, frames=np.arange(0, round_steps * rounds), init_func=init, blit=True, repeat=False
)

plt.show()
