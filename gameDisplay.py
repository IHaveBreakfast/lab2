import pygame

EDGE_WIDTH = 0
X_POSITION = 0
Y_POSITION = 0
LINE_WIDTH = 1
AGENT_WIDTH = 1

class GameDisplay:
    def __init__(self, width = 800, height = 800, cell_size = 50):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("lab2")
        self.screen.fill(pygame.Color('white'))

        self.cell_width = (self.width - 2 * EDGE_WIDTH) // self.cell_size
        self.cell_height = (self.height - 2 * EDGE_WIDTH) // self.cell_size

    def draw_cell(self, a_matrix, f_matrix):
        self.screen.fill(pygame.Color('white'))
        for i in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), [X_POSITION, Y_POSITION + i],
                             [self.width - X_POSITION, Y_POSITION + i], LINE_WIDTH)
        for i in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), [X_POSITION + i, Y_POSITION],
                             [X_POSITION + i, self.height - Y_POSITION], LINE_WIDTH)
        for i in range(0, self.cell_height):
            for j in range(0, self.cell_width):
                if f_matrix[i][j] > 10:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     [X_POSITION + self.cell_size * j + LINE_WIDTH,
                                      Y_POSITION + self.cell_size * i + LINE_WIDTH,
                                      self.cell_size - LINE_WIDTH, self.cell_size - LINE_WIDTH])
                elif 0 < f_matrix[i][j] <= 10:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     [X_POSITION + self.cell_size * j + LINE_WIDTH,
                                      Y_POSITION + self.cell_size * i + LINE_WIDTH,
                                      self.cell_size - LINE_WIDTH, self.cell_size - LINE_WIDTH])
                else:
                    pygame.draw.rect(self.screen, pygame.Color('black'),
                                     [X_POSITION + self.cell_size * j + LINE_WIDTH,
                                      Y_POSITION + self.cell_size * i + LINE_WIDTH,
                                      self.cell_size - LINE_WIDTH, self.cell_size - LINE_WIDTH])
                if a_matrix[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('red'),
                                     [X_POSITION + self.cell_size * j + LINE_WIDTH + AGENT_WIDTH,
                                      Y_POSITION + self.cell_size * i + LINE_WIDTH + AGENT_WIDTH,
                                      self.cell_size - LINE_WIDTH - AGENT_WIDTH * 2, self.cell_size - LINE_WIDTH - AGENT_WIDTH * 2])
