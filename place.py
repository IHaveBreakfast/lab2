import numpy as np
import random
from agent import Agent

PSY_COST_OF_POPULATION = 1
PSY_COST_OF_BIRTH = 2
PHY_COST_OF_MOVED = 1
PHY_COST_OF_BIRTH = 4
PHY_COST_OF_TICK = 1
AMOUNT_OF_FOOD = 1
AMOUNT_GET_FOOD = 0
UPDATE_FOOD = 1
MINIMAL_NEIGHBOUR = 0
MAXIMAL_NEIGHBOUR = 5
NEIGHBOUR_BIRTH = 3


class Place:
    def __init__(self, x, y, agents, seed):
        self.ix = x
        self.iy = y
        self.agents = agents
        self.seed = seed
        self.map_ag = np.zeros((self.iy, self.ix), dtype= np.bool)
        self.map_food = np.random.randint(0, AMOUNT_OF_FOOD, (self.iy, self.ix), dtype= np.int)
        self.agent_list = []
        random.seed(self.seed)
        for a in range(0, agents):
            agent = Agent(random.randint(0, self.ix - 1), random.randint(0, self.iy - 1), self, 1, 0)
            self.agent_list.append(agent)
            self.map_ag[agent.iy, agent.ix] = 1

    def rule(self):
        for item in self.agent_list:
            count = item.logic(self.map_ag)
            item.phy_hp -= PHY_COST_OF_TICK
            if count > MAXIMAL_NEIGHBOUR or count < MINIMAL_NEIGHBOUR:
                item.psi_hp -= PSY_COST_OF_POPULATION
            elif count == NEIGHBOUR_BIRTH:
                item.creator = 1
            if item.psi_hp <= 0 or item.phy_hp <= 0:
                item.active = 0
            if item.shift != 0:
                item.phy_hp -= PHY_COST_OF_MOVED

    def point_matrix_scanning(self, x, y):
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

    def get_food(self, x, y):
        value = self.map_food[y, x]
        if value != 0 and value != 1:
            self.map_food[y, x] -= AMOUNT_GET_FOOD
            hand_over = 2
        elif value == 1:
            self.map_food[y, x] -= 1
            hand_over = 1
        else:
            hand_over = 0
        return hand_over

    def update_food(self):
        for i in range(0, self.iy):
            for j in range(0, self.ix):
                if self.map_food[i][j] == 0:
                    self.map_food[i][j] = random.randint(0, AMOUNT_OF_FOOD)

    def update(self):
        for item in self.agent_list:
            if item.creator == 1:
                min_x, max_x, min_y, max_y = self.point_matrix_scanning(item.ix, item.iy)
                free_cell = False
                for i in range(0, 9):
                    rand_x = random.randint(min_x, max_x)
                    rand_y = random.randint(min_y, max_y)
                    if self.map_ag[rand_y][rand_x] == 0:
                        free_cell = True
                        break
                if free_cell:
                    item.creator = 0
                    item.phy_hp -= PHY_COST_OF_BIRTH
                    item.psi_hp -= PSY_COST_OF_BIRTH
                    agent = Agent(rand_x, rand_y, self, 1, 0)
                    self.map_ag[rand_y, rand_x] = 1
                    self.agent_list.append(agent)
            if item.shift:
                if item.course[0] != 0:
                    self.map_ag[item.iy, item.ix] = 0
                    item.ix += item.course[0]
                elif item.course[1] != 0:
                    self.map_ag[item.iy, item.ix] = 0
                    item.iy += item.course[1]
                self.map_ag[item.iy, item.ix] = 1
            if item.active:
                continue
            else:
                self.map_ag[item.iy, item.ix] = 0
                self.agent_list.remove(item)
        if UPDATE_FOOD == 1:
            self.update_food()

    def get_agents_matrix(self):
        return self.map_ag

    def get_food_matrix(self):
        return self.map_food