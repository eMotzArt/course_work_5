from abc import ABC, abstractmethod


class BaseSkill(ABC):
    name: str
    stamina_required: int
    damage: int

    @abstractmethod
    def skill_effect(self, target):
        pass

    def use(self, user, target):
        if user.max_stamina >= self.stamina_required:
            return self.skill_effect(target)
        else:
            return 'Not enough stamina'


class Kick(BaseSkill):
    name = 'Свирепый пинок'
    stamina_required = 6
    damage = 12

    def skill_effect(self, target):
        target.max_health -= self.damage


class Sting(BaseSkill):
    name = 'Мощный укол'
    stamina_required = 5
    damage = 15

    def skill_effect(self, target):
        target.max_health -= self.damage
