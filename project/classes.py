from dataclasses import dataclass
from .skills import BaseSkill, Kick, Sting


@dataclass
class Character:
    name: str
    max_health: float
    max_stamina: float
    attack_multiplier: float
    stamina_multiplier: float
    armor_multiplier: float
    skill: BaseSkill


warrior = Character(name='воин',
                    max_health=60.0,
                    max_stamina=30.0,
                    attack_multiplier=0.8,
                    stamina_multiplier=0.9,
                    armor_multiplier=1.2,
                    skill=Kick())

thief = Character(name='вор',
                  max_health=50.0,
                  max_stamina=25.0,
                  attack_multiplier=1.5,
                  stamina_multiplier=1.2,
                  armor_multiplier=1.0,
                  skill=Sting())

class_list = {'воин': warrior, 'вор': thief}
