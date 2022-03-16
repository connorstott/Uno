import pygame
import settings

class Bot():
    def __init__(self, start_hand: list, offset: int):
        self.center = pygame.Vector2(settings.WIDTH//2, offset)
        self.spawn_card_pos = self.center

        self.hand = start_hand

        self.display_surface = pygame.display.get_surface()

        self.is_turn = False

        self.turn_time = 1
        self.turn_timer = self.turn_time

    def update(self) -> None:
        self.centreCards()

        for card in sorted(self.hand, key = lambda card: card.z):
            card.drawBack(self.display_surface)
        
        if self.is_turn: self.turn_timer -= 1/settings.FPS
    
    def turn(self, isValid):
        if self.turn_timer > 0: return None
        for card in self.hand:
            if isValid(card):
                self.turn_timer = self.turn_time
                return card
    
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