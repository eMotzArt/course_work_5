import random
from abc import ABC, abstractmethod

from .equipment import Weapon, Armor
from .classes import Character, class_list
from .equipment import EquipHelper
from .informer import Informer
from .ingame_exceptions import GameOverError


class BaseUnit(ABC):
    name: str
    unit_class: Character
    _health_points: float
    _stamina_points: float
    weapon: Weapon
    armor: Armor
    is_skill_used: bool
    enemy: object

    @property
    @abstractmethod
    def health_points(self):
        pass

    @health_points.setter
    @abstractmethod
    def health_points(self, value):
        pass

    @property
    @abstractmethod
    def stamina_points(self):
        pass

    @stamina_points.setter
    @abstractmethod
    def stamina_points(self, value):
        pass

    @abstractmethod
    def equip_weapon(self, weapon_name: str):
        pass

    @abstractmethod
    def equip_armor(self, armor_name: str):
        pass

    @abstractmethod
    def _calc_damage(self):
        pass

    @abstractmethod
    def use_skill(self):
        pass

    @abstractmethod
    def attack(self):
        pass


class Hero(BaseUnit):
    enemy: BaseUnit

    def __init__(self, name, role, weapon, armor):
        self.name = name
        self.unit_class = class_list[role]
        self._health_points = self.unit_class.max_health
        self._stamina_points = self.unit_class.max_stamina
        self.weapon = EquipHelper().get_weapon(weapon)
        self.armor = EquipHelper().get_armor(armor)
        self.is_skill_used = False
        self.is_dead = False

    @property
    def stamina_points(self):
        return self._stamina_points

    @stamina_points.setter
    def stamina_points(self, value):
        self._stamina_points = round(value, 1)

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, value):
        self._health_points = round(value, 1)
        if self._health_points <= 0:
            self.is_dead = True
            raise GameOverError

    def equip_weapon(self, weapon_name: str):
        self.weapon = EquipHelper().get_weapon(weapon_name)

    def equip_armor(self, armor_name: str):
        self.armor = EquipHelper().get_armor(armor_name)

    def _calc_damage(self):
        damage_raw = random.uniform(self.weapon.min_damage, self.weapon.max_damage)
        damage_from_hero = damage_raw*self.unit_class.attack_multiplier

        if self.enemy.stamina_points < self.enemy.armor.stamina_req:
            return round(damage_from_hero, 1)

        target_armor = self.enemy.armor.defence * self.enemy.unit_class.armor_multiplier

        final_damage = damage_from_hero - target_armor

        return round(final_damage, 1)

    def use_skill(self):
        if self.is_skill_used:
            Informer().add_note(f"{self.name} попытался использовать умение, но он уже делал это раньше.")
            return

        if self._stamina_points < self.unit_class.skill.stamina_required:
            Informer().add_note(f"{self.name} попытался использовать умение {self.unit_class.skill.name}, "
                                f"но выносливости не хватило")
            return

        Informer().add_note(f'{self.name} использовал умение и отнял у {self.enemy.name} '
                            f'{self.unit_class.skill.damage} очков здоровья')
        self.enemy.health_points -= self.unit_class.skill.damage
        self.stamina_points -= self.unit_class.skill.stamina_required

        self.is_skill_used = True

    def attack(self):
        if self._stamina_points < self.weapon.stamina_req:
            Informer().add_note(f'{self.name.title()} '
                                f'хотел было атаковать, но отсутствие сил для удара не позволило ему.')
            return

        if (damage := self._calc_damage()) <= 0:
            Informer().add_note(f'{self.name} атаковал с помощью {self.weapon.name}, '
                                f'но не смог пробить броню {self.enemy.name}')
            return

        self.enemy.health_points -= damage
        self.enemy.stamina_points -= self.enemy.armor.stamina_req
        self.stamina_points -= self.weapon.stamina_req

        Informer().add_note(f'{self.name} атаковал {self.enemy.name} и нанёс ему {damage} урона!')


class Enemy(Hero):
    def attack(self):
        skill_chance = 0.33
        # auto-use skill with 33% chance
        if (random.random() < skill_chance) and not self.is_skill_used:
            self.use_skill()
        else:
            super().attack()
