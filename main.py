import pygame, sys
import settings

from board import Board

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("UNO!")
        self.clock = pygame.time.Clock()

        self.board = Board()
    
    def run(self):
        while True:
            exit = self.update()
            self.clock.tick(settings.FPS)
            if exit: break
    
    def update(self) -> None:
        """called once per frame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        self.screen.fill('black')

        finished = self.board.update()

        pygame.display.update()

        return finished

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()