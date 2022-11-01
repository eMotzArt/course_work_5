from flask import Blueprint, render_template, request, redirect, url_for
from project import Informer, equip_helper, class_list, Hero, Enemy, Arena, GameOverError

main_blueprint = Blueprint('main', __name__, template_folder='./templates/')


@main_blueprint.get("/")
def index():
    Arena().clear()
    return render_template('index.html')


@main_blueprint.get("/choose-hero/")
def hero_choose():
    export_info = {
            'header': 'Выберите героя',
            'classes': class_list,
            'weapons': equip_helper.get_weapon_names(),
            'armors': equip_helper.get_armor_names()
    }
    return render_template('hero_chosing.html', result=export_info)


@main_blueprint.post("/choose-hero/")
def enemy_choose():
    if not Arena().hero:
        hero = request.values
        hero_compile = Hero(name=hero['name'], role=hero['unit_class'], weapon=hero['weapon'], armor=hero['armor'])
        Arena().add_character(hero_compile)
        export_info = {
            'header': 'Выберите соперника',
            'classes': class_list.keys(),
            'weapons': equip_helper.get_weapon_names(),
            'armors': equip_helper.get_armor_names()
        }
        return render_template('hero_chosing.html', result=export_info)

    enemy = request.values
    enemy_compile = Enemy(name=enemy['name'], role=enemy['unit_class'], weapon=enemy['weapon'],
                          armor=enemy['armor'])
    Arena().add_character(enemy_compile)
    return redirect(url_for('main.fight'))


@main_blueprint.get('/fight/')
def fight():
    Arena().start_game()
    export_info = Informer().get_message()
    return render_template('fight.html', heroes=Arena().heroes, result=export_info)


@main_blueprint.get('/fight/hit/')
def hit():
    Arena().hit()
    export_info = Informer().get_message()
    return render_template('fight.html', heroes=Arena().heroes, result=export_info)


@main_blueprint.get('/fight/use-skill/')
def use_skill():
    Arena().skill_use()
    export_info = Informer().get_message()
    return render_template('fight.html', heroes=Arena().heroes, result=export_info)


@main_blueprint.get('/fight/pass-turn/')
def pass_turn():
    Arena().skip_move()
    export_info = Informer().get_message()
    return render_template('fight.html', heroes=Arena().heroes, result=export_info)


@main_blueprint.get('/fight/end-fight/')
def end_fight():
    Arena().end_game()
    export_info = Informer().get_message()
    return render_template('fight.html', heroes=Arena().heroes, result=export_info)


@main_blueprint.errorhandler(GameOverError)
def game_over(e):
    return redirect(url_for('main.end_fight'))
