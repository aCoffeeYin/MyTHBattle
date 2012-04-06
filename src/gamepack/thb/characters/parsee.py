# -*- coding: utf-8 -*-
from baseclasses import *
from ..actions import *
from ..cards import *
from ..skill import *

class Envy(TreatAsSkill):
    treat_as = DemolitionCard
    def check(self):
        cards = self.associated_cards
        if len(cards) != 1: return False
        c = cards[0]
        if c.suit not in (Card.SPADE, Card.CLUB): return False
        if c.resides_in.type == CardList.FATETELL: return False
        return True

@register_character
class Parsee(Character):
    skills = [Envy]
    eventhandlers_required = []
    maxlife = 4
