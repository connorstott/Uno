import pygame
import settings

class Player():
    def __init__(self, start_hand: list, offset: int):
        self.center = pygame.Vector2(settings.WIDTH//2, settings.HEIGHT - offset)

        self.hand = start_hand

        for card in self.hand:
            card.draggable = True
        
        self.display_surface = pygame.display.get_surface()

        self.is_turn = True

        self.prev_pressed = False # mouse was being pressed last frame
    
    def update(self) -> None:
        self.centreCards()

        if not pygame.mouse.get_pressed()[0]: self.prev_pressed = False
        
        for card in sorted(self.hand, key = lambda card: card.z):
            card.drawCard(self.display_surface)
    
    def turn(self) -> tuple:
        if self.prev_pressed: return None, False
        for card in self.hand:
            c, clicked = card.click()
            if clicked: 
                self.prev_pressed = True
                return c, clicked
        
        return None, False
    
    def centreCards(self) -> None:
        spawn_pos_x = self.center.x 
        half_gap = 10

        for i, card in enumerate(self.hand):
            if i > 0:
                spawn_pos_x += card.WIDTH/2 + half_gap
                for put_card in self.hand[0:i]:
                    put_card.rect.centerx -= put_card.WIDTH/2 + half_gap

            card.rect.centerx = spawn_pos_x
            card.rect.centery = self.center.y