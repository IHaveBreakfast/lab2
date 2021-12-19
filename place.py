import numpy as np
import random
from agent import Agent

COEF_1_TICK = 1
COEF_1_CREATE = 1
COEF_2_POPULATION = 0
COEF_2_CREATE = 2
COEF_2_SHIFT = 2
COEF_3 = 1
COEF_4 = 2
UPDATE_COEF_3 = 1

NEIGHBOURS_MIN = 2
NEIGHBOUR_MAX = 3
NEIGHBOUR_FOR_NEXTGEN = 3


class Place:
    def __init__(self, x, y, agents, seed):
        self.ix = x
        self.iy = y
        self.agents = agents
        self.seed = seed
        self.agent_list = []
        self.map = np.zeros((self.iy, self.ix), dtype= np.bool)
        self.coeficient_3 = np.random.randint(0, COEF_3, (self.iy, self.ix), dtype= np.int)
        random.seed(self.seed)
        for a in range(0, agents):
            agent = Agent(random.randint(0, self.ix - 1), random.randint(0, self.iy - 1), self, 1, 0)
            self.agent_list.append(agent)
            self.map[agent.iy, agent.ix] = 1

    def rule(self):
        for item in self.agent_list:
            count = item.logic(self.map)
            item.coef_1 -= COEF_1_TICK
            if count > NEIGHBOUR_MAX or count < NEIGHBOURS_MIN:
                item.coef_2 -= COEF_2_POPULATION
            elif count == NEIGHBOUR_FOR_NEXTGEN:
                item.creator = 1
            if item.coef_2 <= 0 or item.coef_1 <= 0:
                item.active = 0
            if item.shift != 0:
                item.coef_1 -= COEF_2_SHIFT

    def scan(self, x, y):
        if x == 0:
            max_x = x + 2
            min_x = x
        elif x == (self.ix - 1):
            max_x = x
            min_x = x - 2
        else:
            max_x = x + 1
            min_x = x - 1
        if y == 0:
            max_y = y + 2
            min_y = y
        elif y == (self.iy - 1):
            max_y = y
            min_y = y - 2
        else:
            max_y = y + 1
            min_y = y - 1
        return min_x, max_x, min_y, max_y

    def coeficient_4(self, x, y):
        value = self.coeficient_3[y, x]
        if value != 0 and value != 1:
            self.coeficient_3[y, x] -= COEF_4
            hand_over = 2
        elif value == 1:
            self.coeficient_3[y, x] -= 1
            hand_over = 1
        else:
            hand_over = 0
        return hand_over

    def update_coeficient_3(self):
       for i in range(0, self.iy):
            for j in range(0, self.ix):
              if self.coeficient_3[i][j] == 0:
                    self.coeficient_3[i][j] = random.randint(0, COEF_3)

    def update(self):
        for item in self.agent_list:
            if item.creator == 1:
                min_x, max_x, min_y, max_y = self.scan(item.ix, item.iy)
                free_cell = False
                for i in range(0, 9):
                    rand_x = random.randint(min_x, max_x)
                    rand_y = random.randint(min_y, max_y)
                    if self.map[rand_y][rand_x] == 0:
                        free_cell = True
                        break
                if free_cell:
                    item.creator = 0
                    item.coef_1 -= COEF_1_CREATE
                    item.coef_2 -= COEF_2_CREATE
                    agent = Agent(rand_x, rand_y, self, 1, 0)
                    self.map[rand_y, rand_x] = 1
                    self.agent_list.append(agent)
            if item.shift:
                if item.course[0] != 0:
                    self.map[item.iy, item.ix] = 0
                    item.ix += item.course[0]
                elif item.course[1] != 0:
                    self.map[item.iy, item.ix] = 0
                    item.iy += item.course[1]
                self.map[item.iy, item.ix] = 1
            if item.active:
                continue
            else:
                self.map[item.iy, item.ix] = 0
                self.agent_list.remove(item)
        if UPDATE_COEF_3 == 1:
            self.update_coeficient_3()

    def get_agents_matrix(self):
        return self.map

    def get_coeficient_3_matrix(self):
        return self.coeficient_3