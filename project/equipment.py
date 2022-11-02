from dataclasses import dataclass
import json


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_req: float


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_req: float


@dataclass
class EquipmentData:
    weapons: list[Weapon]
    armors: list[Armor]


class EquipHelper:
    def __init__(self):
        self.equipments = self._get_equipments()
        pass

    def _get_equipments(self) -> EquipmentData:
        with open('project/equipment.json') as file:
            equipments_raw = json.load(file)
        return EquipmentData(
            [Weapon(*weapon.values()) for weapon in equipments_raw.get('weapons')],
            [Armor(*armor.values()) for armor in equipments_raw.get('armors')]
        )

    def get_weapon(self, weapon_name: str) -> Weapon:
        try:
            return [weapon for weapon in self.equipments.weapons if weapon.name == weapon_name][0]
        except IndexError:
            raise Exception('Weapon not found')

    def get_armor(self, armor_name: str) -> Armor:
        try:
            return [armor for armor in self.equipments.armors if armor.name == armor_name][0]
        except IndexError:
            raise Exception('Armor not found')

    def get_weapon_names(self) -> list[str]:
        return [weapon.name for weapon in self.equipments.weapons]

    def get_armor_names(self) -> list[str]:
        return [armor.name for armor in self.equipments.armors]

equip_helper = EquipHelper()