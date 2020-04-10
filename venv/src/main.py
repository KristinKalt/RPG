from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

def check_and_delete(person, list):
    if person.get_hp() == 0:
        print(person.name.replace(" ", ""), "has died.")
        list.remove(person)

print("\n\n")

#create black magic
fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 840, "black")

#create white magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1200, "white")
curaga = Spell("Curaga", 50, 6000, "white")

#create some items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of pne party member", 9999)
megaElixer = Item("Mega Elixer", "elixer", "Fully restores party's HP/MP ", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_magic = [fire, thunder, blizzard, meteor, cure, cura]
enemy_magic = [ fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15},
                {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5},
                {"item": elixer, "quantity": 5},
                {"item": megaElixer, "quantity": 2},
                {"item": grenade, "quantity": 5}]

#Instantiate people
player1 = Person("Kristin:", 3550, 172, 300, 34, player_magic, player_items)
player2 = Person("Jens   :", 4680, 128, 312, 34, player_magic, player_items)
player3 = Person("Becci  :", 3070, 198, 289, 34, player_magic, player_items)

enemy1 = Person("DOOM", 13200, 701, 567, 25, enemy_magic, [])
enemy2 = Person("Imp ", 1250, 130, 560, 324, enemy_magic, [])
enemy3 = Person("Imp ", 1250, 130, 560, 324, enemy_magic, [])

players= [player1, player2, player3]
enemies = [enemy2, enemy1, enemy3]
running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("==========================")
    print("\n")
    print("NAME                       HP                                           MP")
    for player in players:
        player.get_stats()
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(bcolors.OKBLUE + "You attacked", enemies[enemy].name.replace(" ", ""), "for", dmg, "points of damage." + bcolors.ENDC)
            check_and_delete(enemies[enemy], enemies)

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage to " + enemies[enemy].name.replace(" ", "") + "." + bcolors.ENDC)
                check_and_delete(enemies[enemy], enemy)
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.OKBLUE + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1


            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":
                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.get_max_hp()
                        i.mp = i.get_max_mp()
                player.hp = player.get_max_hp()
                player.mp = player.get_max_mp()
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage to", enemies[enemy].name.replace(" ", ""), "." + bcolors.ENDC)
                check_and_delete(enemies[enemy], enemies)

    #check if battle is over
    defeated_enemies = 0
    defeated_players = 0
    #check if enemy won
    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
    #check if player won
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your enemy has defeated you!" + bcolors.ENDC)
        running = False


    #Enemy attack phase
    print("\n")
    for enemy in enemies:
        enemy_choice = random.randrange(0,2)
        target = random.randrange(0, 3)
        if enemy_choice == 0:
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemy.name.replace(" ", ""), "attacks", players[target].name.replace(" ", "").replace(":", "") +
                  " for", str(enemy_dmg) + bcolors.ENDC)
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.FAIL + spell.name + " heals " + enemy.name.replace(" ", "") +  " for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + enemy.name.replace(" ", "") + "'s " + spell.name + " deals " +
                      str(magic_dmg) + " points of damage to " + players[target].name.replace(" ", "").replace(":","") + "." + bcolors.ENDC)
                check_and_delete(players[target], players)
