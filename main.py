import systems.player as player
from systems.party import Party
import systems.monster as monster
from systems.battle import Battle
from systems.skills.knight import WIND_SWING, RISING_SHIELD, SHIELD_BASH, HEAL, BERSERK, INTIMIDATE
from systems.skills.mage import IGNITE, FLAME_STRIKE, HEALING, GREATER_HEALING

from systems.items.item import HEALTH_POTION, MANA_POTION, MANA_REGEN_POTION
from systems.equipments.armor import WOODEN_ARMOR
from systems.equipments.weapon import WOODEN_LONG_SWORD, LEGENDARY_LONG_SWORD, LEGENDARY_FIRE_STAFF
from systems.equipments.accessory import WOODEN_RING
# from systems.effects.effect import POISON, BUFF

p1 = player.Character("Arya", "Knight", level=2)
p2 = player.Character("Eris", "Mage", level=1)

m1 = monster.Monster("Goblin", level=1, drop_item=HEALTH_POTION)
m2 = monster.Monster("Slime", level=2, drop_item=MANA_POTION)
m3 = monster.Monster("Kobold", level=2, drop_item=HEALTH_POTION)

p1.learn_skill(RISING_SHIELD)
p1.learn_skill(WIND_SWING)
p1.learn_skill(SHIELD_BASH)
p1.learn_skill(HEAL)
p1.learn_skill(BERSERK)
p1.learn_skill(INTIMIDATE)

p2.learn_skill(IGNITE)
p2.learn_skill(FLAME_STRIKE)
p2.learn_skill(HEALING)
p2.learn_skill(GREATER_HEALING)

# p1.gain_experience(1000)
p1.info()
p2.info()

party = Party([p1, p2])
party.add_item(HEALTH_POTION)
party.add_item(MANA_POTION)
party.add_item(MANA_REGEN_POTION)
party.add_item(LEGENDARY_LONG_SWORD)
party.add_item(LEGENDARY_FIRE_STAFF)
party.add_item(WOODEN_RING)
# party.info()
# party.use_item(HEALTH_POTION, [p1])
# party.info()
# party.equip(p1, LEGENDARY_LONG_SWORD)
# party.unequip(p1, LEGENDARY_LONG_SWORD)
# party.show_inventory()


battle = Battle(party, [m1, m2, m3])
result = battle.battle()


# print("\nBattle finished!")
# p1.info()

