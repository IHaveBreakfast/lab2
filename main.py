import pygame
from gameDisplay import GameDisplay
from place import Place

WIDTH = 800
HEIGHT = 800
FPS = 15

def main(display):
    running = True
    start_game = Place(display.cell_width, display.cell_height, 80, 213313)
    print(start_game.get_agents_matrix())
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display.draw_cell(start_game.get_agents_matrix(), start_game.get_coeficient_3_matrix())
        pygame.display.flip()
        start_game.rule()
        start_game.update()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    main(GameDisplay())