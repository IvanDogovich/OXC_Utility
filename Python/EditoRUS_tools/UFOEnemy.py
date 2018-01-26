# Author: EditoRUS
# Thread: https://openxcom.org/forum/index.php/topic,4194.0.html
#Author comment: 
'''Advanced version of older UFOEnemy.py. It is supposed to evaluate 
efficiency of any given weapon against any given enemy.

Now it supports mass evaluation and can easily and quite reliably be 
used by modders who want to balance things out. Or by common players 
seeking to know what weapon deals with what enemy best.'''

''' It also simulates the whole process of killing virtual enemies. 
It collects statistical data and outputs it in readable form.

The tab in the screenshot consists of three values: 
first is average amount of shots needed to kill some enemy, 
second is standard deviation and 
third is the absolute minimum of shots needed to kill an enemy.
'''


import random
import copy
from math import ceil

data = [ [], [] ]

#CONST section
TRIES = 10000
MAIN_MENU = 0
WEAP_MENU = 1
ENEM_MENU = 2

WEAPONS = 0
ENEMIES = 1

WEAPON_NAME = 0
WEAPON_POWER = 1
BULLETS = 2
DEVIATION = 3

ENEMY_NAME = 0
HEALTH = 1
FRONT = 2
SIDE = 3
REAR = 4
UNDER = 5
SUSCEPT = 6

STATE = MAIN_MENU

# Format strings section
STR_SIMPLE_TRY_AVERAGE = "It would take on average {0} +- {1} shot/s to kill that enemy"
STR_SIMPLE_TRY_MINIMUM = "Minimum amount of {0} shot/s is needed to kill that enemy. {1:2%} of enemies were killed that way"
STR_SIMPLE_TRY_INVINCIBLE_STATUS = "It appears the enemy is almost/completely invincible to that weapon (at least {0} shots were done)"
STR_ADVANCED_TRY_DATA = "{0:>4} +- {1:>4} | {2:>2}"
STR_ADVANCED_TRY_WEAPON_DAM = "({0} DAM)"
STR_ADVANCED_TRY_ENEMY_DATA = "({0} HP) ({1}):"
STR_SHOW_WEAPONS_TAB_ARRANGE = "{0:>3}|{1:>20}|{2:>5}|{3:>5}|{4:>7}|"
STR_SHOW_WEAPONS_TAB_ARRANGE_LEN = 3+20+5+5+7+5
STR_BORDER_OF_DATA_AND_NAMES = "="
STR_SHOW_ENEMIES_SUSCEPT_NAME = "{0:>20}|"
STR_SHOW_ENEMIES_SUSCEPT_LEN  = 3+3+19
STR_SHOW_ENEMIES_ENEMY_DATA = "{0:>3}|{1:>20}|{2:>5}|{3:>5}|{4:>5}|{5:>5}|{6:>5}"
STR_SHOW_ENEMIES_ENEMY_DATA_LEN = 3+20+5+5+5+5+5+6

# Service
NOT_NEGATIVE = 2**0
POSITIVE     = 2**1
BOUNDARY      = 2**2

def persistent_input(question, the_type, rules=0, boundary=[]):
    val = 0
    while True:
        try:
            val = eval('{0}(input(\'{1}\'))'.format(the_type, question))     # Metacode
        except ValueError:
            continue
        else:
            try:
                if (rules & NOT_NEGATIVE) and val < 0: continue
                if (rules & POSITIVE) and val <= 0: continue
                if (rules & BOUNDRY) and val in range(boundary[0], boundary[1]+1): continue
            except:
                pass # Not appliable
            return val

# Main simulation
def perform(armor, weapon, susp, health, bullets_shot, deviation):
    result_data = []
    # 0 - average shots
    # 1 - deviation
    # 2 - kills
    # 3 - best shots
    # 4 - chance of best shots
    
    higher_mul = 1 + deviation/100
    lower_mul  = max(1 - deviation/100, 0)
    
    minimum = ceil(health / (bullets_shot*(higher_mul*weapon*susp-armor)))
    
    kills = 0

    curHP = health
    curAP = armor
    statistical_data = []
    shots = 0
    best_kills = 0
    
    for attempt in range(TRIES):
        for bullet in range(bullets_shot):
            rolled_damage = random.randint(int(weapon*lower_mul), int(weapon*higher_mul))
            rolled_damage = int(rolled_damage * susp)
            curHP -= max(rolled_damage - curAP, 0)
            curAP -= max(0.1 * (rolled_damage - curAP), 0)
            curAP = max(curAP, 0)
        shots += 1
        if shots > 0.01 * TRIES: # If it requires more than 1/100 of TRIES it is probably impossible
            return result_data # Blank data
        if curHP <= 0:
            kills += 1
            if shots <= minimum:
                best_kills += 1
            curHP = health
            curAP = armor
            statistical_data.append(shots)
            shots = 0
        

    standard_deviation = 0
    median = 0
    if len(statistical_data):
        median = 0
        for data in statistical_data:
            median += data
        median = median / len(statistical_data)

        standard_deviation = 0
        for data in statistical_data:
            standard_deviation += (data - median)**2
        standard_deviation = standard_deviation / len(statistical_data)
        standard_deviation = standard_deviation**0.5
        
    result_data.append(round(TRIES / kills, 1))
    result_data.append(round(standard_deviation, 1))
    result_data.append(kills)

    result_data.append(minimum)
    result_data.append(best_kills / kills)
    
    return result_data

# Simulation section
def simple_try():
    armor = persistent_input('Armor: ', 'int', NOT_NEGATIVE)
    weapon = persistent_input('Weapon power: ', 'int', POSITIVE)
    susp  = persistent_input('Susceptibility: ', 'float', NOT_NEGATIVE)
    health = persistent_input('Health: ', 'int', POSITIVE)
    bullets_shot = persistent_input('Projectiles shot at once: ', 'int', POSITIVE)
    expl = persistent_input("Maximum damage deviation from 100% in percents (100% -> 0%-200%): ", 'int', NOT_NEGATIVE)

    simple_data = perform(armor, weapon, susp, health, bullets_shot, expl)
    if len(simple_data):
        print(STR_SIMPLE_TRY_AVERAGE.format(simple_data[0], simple_data[1]))
        print(STR_SIMPLE_TRY_MINIMUM.format(simple_data[3], simple_data[4]))
    else:
        print(STR_SIMPLE_TRY_INVINCIBLE_STATUS.format(ceil(0.01 * TRIES)))
    print()

def advanced_try():
    # Data
    # [0] = weapons[]
    #       [weapon name, weapon power, bullets_shot, deviation of damage]
    # [1] = enemy list[]
    #       [enemy name, health, front armor, side armor, rear armor, under armor, susceptibility[]]

    sim_data = []

    # For each weapon a list
    # The list has A lists
    # A = amount of enemies
    # Each list consists of 12 entries
    # 1 + 4X - Average
    # 2 + 4X - Deviation
    # 3 + 4X - Minimum

    basic_entry = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # Basic list, 12 entries
    weapon_entry = [] # Data of affecting each weapon on each enemy
    for alpha in range(len(data[ENEMIES])):
        weapon_entry.append(copy.deepcopy(basic_entry))
    for alpha in range(len(data[WEAPONS])):
        sim_data.append(copy.deepcopy(weapon_entry))

    for alpha in range(len(data[WEAPONS])):
        for beta in range(len(data[ENEMIES])):
            weapon = data[WEAPONS][alpha]
            enemy  = data[ENEMIES][beta]

            HP = enemy[HEALTH]
            FA = enemy[FRONT]
            SA = enemy[SIDE]
            RA = enemy[REAR]
            UA = enemy[UNDER]
            S  = enemy[SUSCEPT][alpha]

            P  = weapon[WEAPON_POWER]
            B  = weapon[BULLETS]
            D  = weapon[DEVIATION]

            FAData = perform(FA, P, S, HP, B, D)
            SAData = perform(SA, P, S, HP, B, D)
            RAData = perform(RA, P, S, HP, B, D)
            UAData = perform(UA, P, S, HP, B, D)

            if len(FAData) > 0:
                sim_data[alpha][beta][0] = round(FAData[0], 1)
                sim_data[alpha][beta][1] = round(FAData[1], 1)
                sim_data[alpha][beta][2] = round(FAData[3], 1)
            if len(SAData) > 0:
                sim_data[alpha][beta][3] = round(SAData[0], 1)
                sim_data[alpha][beta][4] = round(SAData[1], 1)
                sim_data[alpha][beta][5] = round(SAData[3], 1)
            if len(RAData) > 0:
                sim_data[alpha][beta][6] = round(RAData[0], 1)
                sim_data[alpha][beta][7] = round(RAData[1], 1)
                sim_data[alpha][beta][8] = round(RAData[3], 1)
            if len(UAData) > 0:
                sim_data[alpha][beta][9] = round(UAData[0], 1)
                sim_data[alpha][beta][10] = round(UAData[1], 1)
                sim_data[alpha][beta][11] = round(UAData[3], 1)

    for alpha in range(len(data[WEAPONS])):
        for beta in range(len(data[ENEMIES])):
            CurWDT = data[WEAPONS][alpha]
            CurEDT = data[ENEMIES][beta]
            
            if CurWDT[WEAPON_NAME] != "":
                print(CurWDT[WEAPON_NAME], end=' ')
            else:
                print('Weapon #', alpha, end=' ', sep='')
            print(STR_ADVANCED_TRY_WEAPON_DAM.format(CurWDT[WEAPON_POWER]), end='')
            print('vs ', end='')
            if CurEDT[ENEMY_NAME] != "":
                print(CurEDT[ENEMY_NAME], end=' ')
            else:
                print('enemy #', beta, end='', sep='')
            print(STR_ADVANCED_TRY_ENEMY_DATA.format(CurEDT[ENEMY_NAME], CurEDT[SUSCEPT][alpha]))

            CurSD = sim_data[alpha][beta]
            
            print('\tFront armor ({0:>9}'.format(str(CurEDT[FRONT])+'AP'+'):| '), end='')
            if CurSD[0] > 0:
                print(STR_ADVANCED_TRY_DATA.format(CurSD[0], CurSD[1], CurSD[2]))
            else:
                print('INVINCIBLE')
            
            print('\tSide armor  ({0:>9}'.format(str(CurEDT[SIDE])+'AP'+'):| '), end='')
            if CurSD[3] > 0:
                print(STR_ADVANCED_TRY_DATA.format(CurSD[3], CurSD[4], CurSD[5]))
            else:
                print('INVINCIBLE')

            print('\tRear armor  ({0:>9}'.format(str(CurEDT[REAR])+'AP'+'):| '), end='')
            if CurSD[6] > 0:
                print(STR_ADVANCED_TRY_DATA.format(CurSD[6], CurSD[7], CurSD[8]))
            else:
                print('INVINCIBLE')

            print('\tUnder armor ({0:>9}'.format(str(CurEDT[UNDER])+'AP'+'):| '), end='')
            if CurSD[9] > 0:
                print(STR_ADVANCED_TRY_DATA.format(CurSD[9], CurSD[10], CurSD[11]))
            else:
                print('INVINCIBLE')
            print()
            print()

# Weapon section
def add_weapon():
    weapon_name = persistent_input('Weapon name (leave blank if none): ', 'str')
    damage = persistent_input('Weapon damage: ', 'int', POSITIVE)
    bullets = persistent_input('Projectiles in one shot: ', 'int', POSITIVE)
    deviati = persistent_input('Deviation of damage in percents: ', 'int', NOT_NEGATIVE)
    arrange_data = [weapon_name, damage, bullets, deviati]
    data[WEAPONS].append(arrange_data)
    
    print('{0} enemies are in base.'.format(len(data[ENEMIES])))
    for beta in range(len(data[ENEMIES])):
        print('Susceptability of ', end='')
        if data[ENEMIES][beta][ENEMY_NAME] != "":
            print(data[ENEMIES][beta][ENEMY_NAME], end='')
        else:
            print('enemy #{0}'.format(beta), end='')
        print('; HP = {0}'.format(data[ENEMIES][beta][HEALTH]), end='')
        value = persistent_input(': ', 'float', NOT_NEGATIVE)
        data[ENEMIES][beta][SUSCEPT].append(value)

def show_weapons():
    # Arrange a tab
    if len(data[WEAPONS]):
        print(STR_SHOW_WEAPONS_TAB_ARRANGE.format('ID', 'Weapon name', 'Dam', 'Shot', 'Dev'))
        for x in range(STR_SHOW_WEAPONS_TAB_ARRANGE_LEN):
            print(STR_BORDER_OF_DATA_AND_NAMES, end='')
        print()
        indx = 0
        for weapon in data[WEAPONS]:
            print(STR_SHOW_WEAPONS_TAB_ARRANGE.format(indx, weapon[WEAPON_NAME], weapon[WEAPON_POWER], weapon[BULLETS], weapon[DEVIATION]))
            indx += 1
        return True
    return False
        
def rem_weapon():
    global data
    if show_weapons():
        while True:
            ids = persistent_input('Weapon ID (negative to cancel): ', 'int')
            if ids < 0:
                return False
            if ids > len(data[WEAPONS])-1:
                continue
            del data[WEAPONS][ids]
            return True
    else:
        print('Nothing to delete')
        return False

# Enemy section
def add_enemy():
        name = persistent_input('Enemy name (leave blank if none): ', 'str')
        health = persistent_input('Health: ', 'int', POSITIVE)
        front = persistent_input('Front armor: ', 'int', NOT_NEGATIVE)
        side = persistent_input('Side armor: ', 'int', NOT_NEGATIVE)
        rear = persistent_input('Rear armor: ', 'int', NOT_NEGATIVE)
        under = persistent_input('Under armor: ', 'int', NOT_NEGATIVE)
        
        susp = []
        print('{0} weapons are in base.'.format(len(data[WEAPONS])))
        for delta in range(len(data[WEAPONS])):
            while True:
                print('Susceptability to ', end='')
                if data[WEAPONS][delta][WEAPON_NAME] != "":
                    print(data[WEAPONS][delta][WEAPON_NAME], end='')
                else:
                    print('weapon #{0}'.format(delta), end='')
                print('; Damage = {0}'.format(data[WEAPONS][delta][WEAPON_POWER]), end='')
                value = persistent_input(': ', 'float', NOT_NEGATIVE)
                susp.append(value)
                break
            
        arrange_data = [name, health, front, side, rear, under, susp]
        data[ENEMIES].append(arrange_data)

def show_enemies():
    if len(data[ENEMIES]):
    # [1] = enemy list[]
    #       [enemy name, front armor, side armor, rear armor, under armor, susceptibility]
    #                                                                      []
        print() 
        print('{0:>4}'.format('ID|'), end='') # ID column
        print(STR_SHOW_ENEMIES_SUSCEPT_NAME.format('Weapon name'), end='') # Name column
        for enemy in data[ENEMIES]:
            print(STR_SHOW_ENEMIES_SUSCEPT_NAME.format(enemy[ENEMY_NAME]), end='') # Enemy names
        print()
        for m in range(STR_SHOW_ENEMIES_SUSCEPT_LEN+21*len(data[ENEMIES])):
            print(STR_BORDER_OF_DATA_AND_NAMES, end='')
        for alpha in range(len(data[WEAPONS])):
            print()
            print('{0:>3}|'.format(alpha), end='')
            print(STR_SHOW_ENEMIES_SUSCEPT_NAME.format(data[WEAPONS][alpha][WEAPON_NAME]), end='')
            for delta in range(len(data[ENEMIES])):
                print(STR_SHOW_ENEMIES_SUSCEPT_NAME.format(data[ENEMIES][delta][SUSCEPT][alpha]), end='')
        print()
        print()
        print(STR_SHOW_ENEMIES_ENEMY_DATA.format('ID', 'Enemy name', 'HP', 'FA', 'SA', 'RA', 'UA'))
        for m in range(STR_SHOW_ENEMIES_ENEMY_DATA_LEN):
            print(STR_BORDER_OF_DATA_AND_NAMES, end='')
        print()
        indx = 0
        for enemy in data[ENEMIES]:
            print(STR_SHOW_ENEMIES_ENEMY_DATA.format(indx, enemy[ENEMY_NAME], enemy[HEALTH], enemy[FRONT], enemy[SIDE], enemy[REAR], enemy[UNDER]))
            indx += 1
        return True
    return False

def rem_enemy():
    global data
    if show_enemies():
        while True:
            ids = persistent_input('ID (negative to cancel): ', 'int')
            if ids < 0:
                return False
            if ids > len(data[ENEMIES])-1:
                continue
            del data[ENEMIES][ids]
            return True
    print('Nothing to delete')
    return False

# Debug section
def purge():
    data = [ [], [] ]

def debug():
    data0 = ['Heavy Plasma', 115, 1, 100]
    data1 = ['Laser Rifle', 60, 1, 100]
    data2 = [data0, data1]
    data3 = ['Sectoid', 60, 70, 60, 50, 40, [0.8, 0.6]]
    data4 = ['Sectopod', 120, 145, 130, 100, 90, [0.8, 1.5]]
    data5 = [data3, data4]
    c = copy.deepcopy(data2)
    d = copy.deepcopy(data5)
    data[WEAPONS] = c
    data[ENEMIES] = d

# Interface section
def main_menu():
    global STATE, TRIES
    choice = 0
    print()
    print('1: Simple evaluation')
    print('2: Multiple evaluations')
    print('3: Change TRIES const (make simulation more accurate or faster)')
    print('0: Exit')
    print()
    choice = persistent_input('>>> ', 'int', BOUNDARY, [0, 3])
    print()
    if choice == 0:
        return True
    if choice == 1:
        simple_try()
    if choice == 2:
        STATE = WEAP_MENU
    if choice == 3:
        print('Current TRIES: ', TRIES)
        while True:
            new_val = persistent_input('New value (negative to cancel): ', 'int')
            if new_val < 0:
                break
            if new_val == 0:
                continue
            TRIES = new_val
            break
        
def weapon_menu():
    global STATE
    choice = 0
    print()
    print('1: Add weapon')
    print('2: Show weapons')
    print('3: Remove weapon')
    print('4: Next step')
    print('0: Back to main menu')
    print()
    choice = persistent_input('>>> ', 'int', BOUNDARY, [0, 4])
    print()
    if choice == 0:
        STATE = MAIN_MENU
    if choice == 1:
        add_weapon()
    if choice == 2:
        if not show_weapons():
            print('Nothing to show')
    if choice == 3:
        rem_weapon()
    if choice == 4:
        STATE = ENEM_MENU

def enemy_menu():
    global STATE
    choice = 0
    print()
    print('1: Add enemy')
    print('2: Show enemies')
    print('3: Remove enemy')
    print('4: Previous step')
    print('5: Start simulation')
    print('0: Back to main menu')
    print()
    choice = persistent_input('>>> ', 'int', BOUNDARY, [0, 5])
    print()
    if choice == 0:
        STATE = MAIN_MENU
    if choice == 1:
        add_enemy()
    if choice == 2:
        if not show_enemies():
            print('Nothing to show')
    if choice == 3:
        rem_enemy()
    if choice == 4:
        STATE = WEAP_MENU
    if choice == 5:
        advanced_try()
        STATE = MAIN_MENU

# Main iterator
while True:
    if STATE == MAIN_MENU:
        if main_menu(): # To exit
            break
    if STATE == WEAP_MENU:
        weapon_menu()
    if STATE == ENEM_MENU:
        enemy_menu()
