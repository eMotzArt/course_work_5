from .unit import Hero, Enemy
from .utils import singleton
from .informer import Informer


@singleton
class Arena:
    def __init__(self):
        self.restored_stamina = 1
        self.hero: Hero = None
        self.enemy: Enemy = None
        self.is_game_active = False

    # Для повторной игры без перезаупска
    def clear(self):
        self.__init__()

    @property
    def heroes(self):
        return {
            'player': self.hero,
            'enemy': self.enemy
        }

    def add_character(self, character):
        if not self.hero:
            self.hero = character
        else:
            self.enemy = character

    def start_game(self):
        Informer().add_note('LET MORTAL KOMBAT BEGIN!!!')
        self.hero.enemy = self.enemy
        self.enemy.enemy = self.hero
        self.is_game_active = True

    def next_move(self):
        self.check_health()
        self.enemy.attack()
        self.check_health()
        self.restore_stamina()

    def restore_stamina(self):
        self.hero.stamina_points += self.restored_stamina * self.hero.unit_class.stamina_multiplier
        self.enemy.stamina_points += self.restored_stamina * self.enemy.unit_class.stamina_multiplier

    def check_health(self):
        if self.hero.is_dead or self.enemy.is_dead:
            self.end_game()

    def end_game(self):
        self.is_game_active = False
        if not self.hero.is_dead and not self.enemy.is_dead:
            Informer().add_note('Бойцы в какой то момент решили остановиться, '
                                'и обсудить конфликт за столом переговоров.'
                                'Поговаривают, что они всё уладили и создали совместную компанию и стали '
                                'лучшими друзяьми')
            return
        for character in [self.hero, self.enemy]:
            if character.is_dead:
                Informer().add_note(f'{character.name} был повержен. {character.enemy.name} победитель! Игра окончена!')
                return

    def hit(self):
        if self.is_game_active:
            self.hero.attack()
            self.next_move()

    def skill_use(self):
        if self.is_game_active:
            self.hero.use_skill()
            self.next_move()

    def skip_move(self):
        if self.is_game_active:
            Informer().add_note(f"{self.hero.name} решил пропустить ход и поднакопить выносливости")
            self.next_move()
