# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
# -- own --
from thb import cards, characters
from thb.ui.ui_meta.common import build_handcard, ui_meta_for, my_turn, passive_clickable
from thb.ui.ui_meta.common import passive_is_action_valid

# -- code --
ui_meta = ui_meta_for(characters.yuuka)


@ui_meta
class ReversedScales:
    # Skill
    name = '逆鳞'
    description = '每当你成为其他角色使用的单体符卡效果目标时，你可以将其视为|G弹幕战|r效果；你的回合外，你可以将一张手牌当做|G弹幕|r使用或打出。'

    def clickable(self, g):
        me = g.me
        if my_turn():
            return False

        if not (me.cards or me.showncards):
            return False

        try:
            act = g.action_stack[-1]
            return act.cond([build_handcard(cards.AttackCard)])
        except Exception:
            pass

        return False

    def is_complete(self, g, cl):
        skill = cl[0]
        acards = skill.associated_cards
        if len(acards) != 1:
            return (False, '请选择1张牌！')

        return (True, '反正这条也看不到，偷个懒~~~')

    def is_action_valid(self, g, cl, target_list, is_complete=is_complete):
        skill = cl[0]
        rst, reason = is_complete(g, cl)
        if not rst:
            return (rst, reason)
        else:
            return cards.AttackCard.ui_meta.is_action_valid(g, [skill], target_list)

    def effect_string(self, act):
        # for LaunchCard.ui_meta.effect_string
        return '|G【%s】|r用和善的眼神看了|G【%s】|r一眼。' % (
            act.source.ui_meta.name,
            act.target.ui_meta.name,
        )

    def sound_effect(self, act):
        return 'thb-cv-yuuka_flowerqueen'


@ui_meta
class Sadist:
    # Skill
    name = '施虐'
    description = '当你击坠一名角色时，你可以对攻击范围内一名其他角色造成1点伤害；你对体力值为1的其他角色造成的伤害+1。'

    clickable = passive_clickable
    is_action_valid = passive_is_action_valid


@ui_meta
class SadistKOF:
    # Skill
    name = '施虐'
    description = '|B锁定技|r，当你击坠对手后，你摸2张牌并对其下一名登场角色造成1点伤害。'

    clickable = passive_clickable
    is_action_valid = passive_is_action_valid


@ui_meta
class ReversedScalesAction:
    def effect_string_apply(self, act):
        return (
            '|G【%s】|r：“来正面上我啊！”'
        ) % (
            act.target.ui_meta.name,
        )

    def sound_effect(self, act):
        return 'thb-cv-yuuka_rs'


@ui_meta
class SadistAction:
    def effect_string_apply(self, act):
        return (
            '|G【%s】|r又看了看|G【%s】|r：“你也要尝试一下么！”'
        ) % (
            act.source.ui_meta.name,
            act.target.ui_meta.name,
        )

    def sound_effect(self, act):
        return 'thb-cv-yuuka_sadist'


@ui_meta
class SadistKOFDamageAction:
    def effect_string_apply(self, act):
        return (
            '|G【%s】|r又看了看|G【%s】|r：“你也要尝试一下么！”'
        ) % (
            act.source.ui_meta.name,
            act.target.ui_meta.name,
        )

    def sound_effect(self, act):
        return 'thb-cv-yuuka_sadist'


@ui_meta
class SadistHandler:
    # choose_card
    def choose_card_text(self, g, act, cards):
        if act.cond(cards):
            return (True, '发动【施虐】')
        else:
            return (False, '【施虐】：请弃置一张牌')

    def target(self, pl):
        if not pl:
            return (False, '【施虐】：请选择1名玩家')

        return (True, '发动【施虐】')


@ui_meta
class ReversedScalesHandler:
    # choose_option
    choose_option_buttons = (('发动', True), ('不发动', False))
    choose_option_prompt = '你要发动【逆鳞】吗？'


@ui_meta
class Yuuka:
    # Character
    name        = '风见幽香'
    title       = '四季的鲜花之主'
    illustrator = '霏茶'
    cv          = 'VV'

    port_image        = 'thb-portrait-yuuka'
    figure_image      = 'thb-figure-yuuka'
    miss_sound_effect = 'thb-cv-yuuka_miss'


@ui_meta
class YuukaKOF:
    # Character
    name        = '风见幽香'
    title       = '四季的鲜花之主'
    illustrator = '霏茶'
    cv          = 'VV'

    port_image        = 'thb-portrait-yuuka'
    figure_image      = 'thb-figure-yuuka'
    miss_sound_effect = 'thb-cv-yuuka_miss'

    notes = '|RKOF修正角色'