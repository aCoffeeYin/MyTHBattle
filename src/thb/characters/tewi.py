# -*- coding: utf-8 -*-


# -- stdlib --
# -- third party --
# -- own --
from game.autoenv import EventHandler
from thb.actions import DrawCards
from thb.cards.classes import Skill, t_None
from thb.characters.base import Character, register_character_to


# -- code --
class Luck(Skill):
    associated_action = None
    skill_category = ['character', 'passive', 'compulsory']
    target = t_None


class LuckDrawCards(DrawCards):
    pass


class LuckHandler(EventHandler):
    interested = ['card_migration']

    def handle(self, evt_type, arg):
        if evt_type != 'card_migration':
            return arg

        act, l, _from, to, is_bh = arg
        p = _from.owner

        if p and p.has_skill(Luck) and not p.dead:
            if _from not in (p.cards, p.showncards):
                return arg

            if not (p.cards or p.showncards):
                self.game.process_action(LuckDrawCards(p, 2))

        return arg


@register_character_to('common', '-kof')
class Tewi(Character):
    skills = [Luck]
    eventhandlers = [LuckHandler]
    maxlife = 4
