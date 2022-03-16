from numpy import isin
import pygame
import random
import settings
import time

from card import NumCard, AddCard, MissCard, ReverseCard, WildCard, FourCard, AnyColour
from player import Player
from bot import Bot

class Board():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.draw_cards = []
        self.makeCards()

        self.player = Player(self.getCards(7), 100)
        self.bot = Bot(self.getCards(7), 0)

        self.face_card = self.getCards(1)[0]
        while isinstance(self.face_card, WildCard):
            self.face_card = self.getCards(1)[0]
        self.face_card.rect.center = (settings.WIDTH//2, settings.HEIGHT//2)

        self.empty_card = NumCard(None, -1)
        self.empty_card.rect.center = (settings.WIDTH-self.empty_card.WIDTH//2-10, settings.HEIGHT//2)

    def makeCards(self) -> None:
        """makes all the cards at the start of the game"""
        # red, green, blue, yellow
        for colour in ["#c42b25", "#5aa142", "#057bad", "#f0db1f"]:
            for i in range(2):
                for i in range(0,10):
                    self.draw_cards.append(NumCard(colour, i))
                self.draw_cards.append(AddCard(colour, 2))
                self.draw_cards.append(MissCard(colour))
                self.draw_cards.append(ReverseCard(colour))
            self.draw_cards.append(FourCard())
            self.draw_cards.append(WildCard())

    def getCards(self, number: int) -> list:
        """gets a set number of random cards from draw cards"""
        add = []
        for i in range(number):
            card = random.choice(self.draw_cards)
            add.append(card)
            self.draw_cards.remove(card)
        return add

    def update(self) -> None:
        """called once per frame"""
        if self.player.is_turn: pygame.draw.circle(self.display_surface, 'white', (20, settings.HEIGHT-100), 10)
        else: pygame.draw.circle(self.display_surface, 'white', (20, 100), 10)

        self.face_card.drawCard(self.display_surface)
        self.empty_card.drawBack(self.display_surface)

        self.bot.update()
        self.player.update()

        if len(self.player.hand) == 0 or len(self.bot.hand) == 0:
            return True

        if self.bot.is_turn == True:
            card = self.bot.turn(self.isValid)
            if card != None:
                self.validTurn(card, self.bot, self.player)
            elif self.bot.turn_timer <= 0: # pick up card
                self.bot.turn_timer = self.bot.turn_time
                self.bot.hand.extend(self.getCards(1))
                self.switchTurns()

            if isinstance(card, WildCard):
                self.face_card = card.botUse(random.choice(["#c42b25", "#5aa142", "#057bad", "#f0db1f"]), self.face_card)

        elif self.player.is_turn == True:
            card, clicked = self.player.turn()
            if clicked and self.isValid(card):
                self.validTurn(card, self.player, self.bot)
            
            if clicked and isinstance(card, WildCard):
                self.player.centreCards()
                self.face_card = card.playerUse(self.face_card, self.player.hand)
            
            card, clicked = self.empty_card.click() # pick up card
            if clicked: 
                self.player.hand.extend(self.getCards(1))
                self.switchTurns()

    def switchTurns(self):
        self.bot.is_turn = not self.bot.is_turn
        self.player.is_turn = not self.player.is_turn
    
    def isValid(self, card):
        if isinstance(card, WildCard):
            return True
        if isinstance(card, FourCard):
            return True
        elif isinstance(card, NumCard) and ((isinstance(self.face_card, NumCard) and card.number == self.face_card.number) or card.colour == self.face_card.colour):
            return True
        elif isinstance(card, AddCard) and ((isinstance(self.face_card, AddCard) and card.add == self.face_card.add) or card.colour == self.face_card.colour):
            return True
        elif isinstance(card, MissCard) and (isinstance(self.face_card, MissCard) or card.colour == self.face_card.colour):
            return True
        elif isinstance(card, ReverseCard) and (isinstance(self.face_card, ReverseCard) or card.colour == self.face_card.colour):
            return True
        return False
    
    def validTurn(self, card, turn_person, opponent) -> None:
        turn_person.hand.remove(card)
        card.rect.center = self.face_card.rect.center
        self.faceToDraw()
        self.face_card = card
        self.switchTurns()
        card.effect(turn_person, opponent, self.getCards)
    
    def faceToDraw(self):
        if isinstance(self.face_card, AnyColour):
            return
        self.draw_cards.insert(random.randint(10,len(self.draw_cards)), self.face_card)