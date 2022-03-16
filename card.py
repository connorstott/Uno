import pygame
import settings

class Card():
    def __init__(self,  colour: str):
        self.colour = colour
        self.rect = None

        self.z = 0

        # self.is_being_dragged = False
        # self.prev_pressed = False
        # self.drag_offset = pygame.math.Vector2()

        self.WIDTH = 100
        self.HEIGHT = 175

        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rad = 10

        self.font = pygame.font.Font(None, 30)

        self.back_image = pygame.image.load("assets/logo.png").convert_alpha()
        self.back_image = pygame.transform.rotozoom(self.back_image, 0, 0.2)
        self.back_image_rect = self.back_image.get_rect()

    def click(self) -> tuple:
        """check if card was clicked\n
        returns the card and if it was clicked"""
        mouses_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if mouses_pressed[0] and self.rect.collidepoint(mouse_pos):
            return self, True
        return None, False

    # def drag(self) -> None:
    #     """logic for dragging cards"""
    #     mouses_pressed = pygame.mouse.get_pressed()
    #     mouse_pos = pygame.mouse.get_pos()

    #     if mouses_pressed[0] and not self.prev_pressed and self.rect.collidepoint(mouse_pos): # mouse down
    #         self.drag_offset.x = mouse_pos[0] - self.rect.centerx
    #         self.drag_offset.y = mouse_pos[1] - self.rect.centery
    #         self.is_being_dragged = True
    #         self.z = 1
    #     elif mouses_pressed[0] and self.is_being_dragged: # mouse held down
    #         self.rect.centerx = mouse_pos[0] - self.drag_offset.x
    #         self.rect.centery = mouse_pos[1] - self.drag_offset.y
    #     elif not mouses_pressed[0]: # mouse up
    #         self.drag_offset = pygame.math.Vector2()
    #         self.is_being_dragged = False
    #         self.z = 0

    #     self.prev_pressed = mouses_pressed[0]
        
    def drawCard(self, surface) -> None:
        colour = 'black' if self.colour == None else self.colour
        if colour == "black": pygame.draw.rect(surface, 'white', self.rect.inflate(2,2), border_radius=self.rad)
        pygame.draw.rect(surface, colour, self.rect, border_radius= self.rad)
    
    def drawBack(self, surface) -> None:
        pygame.draw.rect(surface, 'white', self.rect.inflate(2,2), border_radius=self.rad)
        pygame.draw.rect(surface, 'black', self.rect, border_radius= self.rad)
        self.back_image_rect.center = self.rect.center
        surface.blit(self.back_image, self.back_image_rect)
    
    def drawCardText(self, text: str, surface) -> None:
        txt = self.font.render(text, True, 'white')
        txt_rect = txt.get_rect()
        txt_rect.center = self.rect.center
        surface.blit(txt, txt_rect)
    
    def effect(self, user, opponent, addCards):
        pass

class NumCard(Card):
    def __init__(self, colour: str, number: int):
        super().__init__(colour)
        self.number = number
    
    def drawCard(self, surface) -> None:
        super().drawCard(surface)
        super().drawCardText(str(self.number), surface)

class AddCard(Card):
    def __init__(self, colour: str, add: int):
        super().__init__(colour)
        self.add = add
    
    def drawCard(self, surface) -> None:
        super().drawCard(surface)
        super().drawCardText("+"+str(self.add), surface)
    
    def effect(self, user, opponent, addCards):
        opponent.hand.extend(addCards(self.add))

class MissCard(Card):
    def __init__(self, colour: str):
        super().__init__(colour)
        self.image = pygame.image.load("assets/miss_turn.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.03)
        self.image_rect = self.image.get_rect()
    
    def drawCard(self, surface) -> None:
        super().drawCard(surface)
        self.image_rect.center = self.rect.center
        surface.blit(self.image, self.image_rect)
    
    def effect(self, user, opponent, addCards):
        user.is_turn = True
        opponent.is_turn = False

class ReverseCard(Card):
    def __init__(self, colour: str):
        super().__init__(colour)
        self.image = pygame.image.load("assets/reverse.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
        self.image_rect = self.image.get_rect()
    
    def drawCard(self, surface) -> None:
        super().drawCard(surface)
        self.image_rect.center = self.rect.center
        surface.blit(self.image, self.image_rect)
    
    def effect(self, user, opponent, addCards):
        user.is_turn = True
        opponent.is_turn = False

class WildCard(Card):
    def __init__(self, *args):
        super().__init__(None)
        self.image = pygame.image.load("assets/wildcard.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.22)
        self.image_rect = self.image.get_rect()
    
    def drawCard(self, surface) -> None:
        super().drawCard(surface)
        self.image_rect.center = self.rect.center
        surface.blit(self.image, self.image_rect)
    
    def botUse(self, colour, face_card) -> object:
        colour_card = AnyColour(colour)
        colour_card.rect.center = face_card.rect.center
        return colour_card
    
    def playerUse(self, face_card, player_hand) -> object:
        surface = pygame.display.get_surface()
        clock = pygame.time.Clock()

        red = AnyColour("#c42b25")
        red.rect.centerx = settings.WIDTH//2 -3*(10+red.WIDTH//2)
        green = AnyColour("#5aa142")
        green.rect.centerx = settings.WIDTH//2 -(10+green.WIDTH//2)
        blue = AnyColour("#057bad")
        blue.rect.centerx = settings.WIDTH//2 +(10+blue.WIDTH//2)
        yellow = AnyColour("#f0db1f")
        yellow.rect.centerx = settings.WIDTH//2 +3*(10+yellow.WIDTH//2)
        options = [red, green, blue, yellow]
        for card in options: card.rect.centery = settings.HEIGHT//2
        
        while True:
            clock.tick(settings.FPS)
            pygame.event.get()
            pygame.display.update()
            surface.fill('black')

            for card in options: 
                card.drawCard(surface)
                card, clicked = card.click()
                if clicked:
                    card.rect.center = face_card.rect.center
                    return card
            
            for card in player_hand:
                card.drawCard(surface)
    
class FourCard(AddCard, WildCard):
    def __init__(self):
        super().__init__(None, 4)
    
    def drawCard(self, surface) -> None:
        super().drawCard(surface)

class AnyColour(Card):
    def __init__(self, colour):
        super().__init__(colour)
    
    def drawCard(self, surface) -> None:
        super().drawCard(surface)
        super().drawCardText("any", surface)