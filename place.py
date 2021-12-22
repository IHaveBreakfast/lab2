import numpy as np
import random
from agent import Agent

LOST_HP_IN_TICK = 1
LOST_BIRTH_HP = 1
LOST_ENERGY_POPULATION = 0
LOST_ENERGY_BIRTH = 2
LOST_HP_OF_MOVEMENT = 2
AMOUNT_ENERGY = 1
AMOUNT_GET_HP = 2
UPDATE_ADD_HP = 1

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
        self.amount_energy = np.random.randint(0, AMOUNT_ENERGY, (self.iy, self.ix), dtype= np.int)
        random.seed(self.seed)
        for a in range(0, agents):
            agent = Agent(random.randint(0, self.ix - 1), random.randint(0, self.iy - 1), self, 1, 0)
            self.agent_list.append(agent)
            self.map[agent.iy, agent.ix] = 1

    def rule(self):
        for item in self.agent_list:
            count = item.logic(self.map)
            item.hp -= LOST_HP_IN_TICK
            if count > NEIGHBOUR_MAX or count < NEIGHBOURS_MIN:
                item.energy -= LOST_ENERGY_POPULATION
            elif count == NEIGHBOUR_FOR_NEXTGEN:
                item.creator = 1
            if item.energy <= 0 or item.hp <= 0:
                item.active = 0
            if item.shift != 0:
                item.hp -= LOST_HP_OF_MOVEMENT

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

    def amount_get_hp(self, x, y):
        value = self.amount_energy[y, x]
        if value != 0 and value != 1:
            self.amount_energy[y, x] -= AMOUNT_GET_HP
            hand_over = 2
        elif value == 1:
            self.amount_energy[y, x] -= 1
            hand_over = 1
        else:
            hand_over = 0
        return hand_over

    def update_add_hp(self):
       for i in range(0, self.iy):
            for j in range(0, self.ix):
              if self.amount_energy[i][j] == 0:
                    self.amount_energy[i][j] = random.randint(0, AMOUNT_ENERGY)

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
                    item.hp -= LOST_BIRTH_HP
                    item.energy -= LOST_ENERGY_BIRTH
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
        if UPDATE_ADD_HP == 1:
            self.update_add_hp()

    def get_agents_matrix(self):
        return self.map

    def get_coeficient_3_matrix(self):
        return self.amount_energy