import math
import random

AGENT_PHY_HP = 10
AGENT_PSY_HP = 10

class Agent:
    def __init__(self, x, y, place, active, creator):
        self.psi_hp = AGENT_PSY_HP
        self.phy_hp = AGENT_PHY_HP
        self.ix = x
        self.iy = y
        self.place = place             #площадь
        self.active = active           #живая клетка
        self.creator = creator         #родитель

        self.purpose = 0               #цель
        self.shift = 0                 #сдвиг
        self.course = [0, 0]           #направление движения
        self.coord_purpose = [x, y]    #координаты цели


    def sum_neighbours(self, matrix):
        x_min, x_max, y_min, y_max = self.place.point_matrix_scanning(self.ix, self.iy)
        sum = 0
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                if i == self.ix and j == self.iy:
                    continue
                if matrix[i][j] == 1:
                    for k in self.place.agent_list:
                        if k.ix == i and k.iy == j and k.active == 1:
                            sum += 1
        return sum

    def movement(self):
        agents = self.place.agent_list
        distance= []
        self.psi_hp -= 1
        for a in agents:
            distance.append(math.sqrt(math.pow(a.ix, 2) + math.pow(a.iy, 2)))
        step = distance.index(min(distance))
        return agents[step].ix, agents[step].iy

    def agent_motion(self):
        axis_x = self.coord_purpose[0] - self.ix
        axis_y = self.coord_purpose[1] - self.iy
        direction = 0
        if axis_x != 0 and axis_y != 0:
            direction = random.randint(0, 2)
        elif axis_x != 0 and axis_y == 0:
            direction = 1
        elif axis_x == 0 and axis_y != 0:
            direction = 0
        if direction == 1:
            self.course[1] = 0
            if axis_x > 0:
                self.course[0] = 1
            else:
                self.course[0] = -1
        else:
            self.course[0] = 0
            if axis_y > 0:
                self.course[1] = 1
            else:
                self.course[1] = -1

    ##########################################################
    def agent_food_motion(self):
        x_min, x_max, y_min, y_max = self.place.point_matrix_scanning(self.ix, self.iy)
        for i in range(x_min, x_max + 1):
            for j in range(y_min, y_max + 1):
                if self.place.map_food[i][j] != 0 and self.place.map_ag[i][j] != 1:
                    self.coord_purpose[0] = i
                    self.coord_purpose[1] = j
                    self.agent_motion()
                    self.shift = 1

    def logic(self, matrix):
        cnt_agents = self.sum_neighbours(matrix)
        if self.phy_hp < 5:
            val = self.place.get_food(self.ix, self.iy)
            self.phy_hp += val
            if self.phy_hp > AGENT_PHY_HP:
                self.phy_hp = AGENT_PHY_HP
        if cnt_agents == 0 and self.purpose == 0:
            self.coord_purpose[0], self.coord_purpose[1] = self.movement()
            self.purpose = 1
        if cnt_agents == 0 and self.purpose == 1:
            self.agent_motion()
            self.shift = 1
        if cnt_agents > 0:
            self.shift = 0
            self.purpose = 0
            if self.phy_hp < 9:
                val = self.place.get_food(self.ix, self.iy)
                if val == 0:
                    self.agent_food_motion()
        return cnt_agents