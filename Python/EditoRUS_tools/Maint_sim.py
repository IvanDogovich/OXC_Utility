# Author: EditoRUS
# Thread: https://openxcom.org/forum/index.php/topic,4194.0.html
#Author comment: 
'''First version of maint_sim.py devoted to calculate the ideal 
setup and profit of any manufacturable item possible. You punch 
in all the values and get what needed. Be aware that TFTD rules for 
most part follow easy rule: more engineers = more profit, so you might b
e using it just to evaluate your average profit.'''

''' It simulates the whole process of manufacturing throughout a virtual month.
The reason of that is because UFO: EU uses a very weird system of manufacturing 
and calculating it mathematically would require using some special means. 
Simulating is just overall easier to implement.'''

from math import ceil, floor

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
        
AVG_MONTH   = 30
MONTH       = 24*AVG_MONTH
YEAR        = 24*365
ENG_COST    = persistent_input('Engineer hire cost (1000s): ', 'float', NOT_NEGATIVE)*1000
ENG_SAL     = persistent_input('Engineer salary (1000s): ', 'float', NOT_NEGATIVE)*1000
WORK_COST   = persistent_input('Workshop cost (1000s): ', 'float', NOT_NEGATIVE)*1000
LIVI_COST   = persistent_input('Living quarters cost (1000s): ', 'float', NOT_NEGATIVE)*1000
WORK_MAIN   = persistent_input('Workshop maintenance cost (1000s): ', 'float', NOT_NEGATIVE)*1000
LIVI_MAIN   = persistent_input('Living quarters maintenance cost (1000s): ', 'float', NOT_NEGATIVE)*1000
MAX_WORKSHOPS = floor((6*6-1) / 2)
TFTD = False

while True:
    answer = input("TFTD rules? Y/N: ")
    if answer.upper() == "Y":
        TFTD = True
        break
    if answer.upper() == "N":
        TFTD = False
        break

print()

while True:
    man_hours = persistent_input("Man-hours: ", 'int', POSITIVE)
    man_cost  = persistent_input("Manufacture cost (1000s): ", 'float', POSITIVE)*1000
    man_sell  = persistent_input("Selling cost (1000s): ", 'float', POSITIVE)*1000
    man_space = persistent_input("Workshop space: ", 'int', POSITIVE)
    man_sanity = persistent_input("Max amount of workshops: ", 'int', POSITIVE)
    
    max_workshops_needed = ceil(man_hours+man_space / 50)
    higher_limit_of_engineers = man_hours

    best_engineers = 0
    best_workshops = 0
    best_living_space = 0
    best_profit = 0
    best_product = 0
    best_setup = 0

    max_workshops_needed = min(MAX_WORKSHOPS, man_sanity)
    
    for workshops in range(1, max_workshops_needed+1):
        max_engineers = workshops*50-man_space
        min_engineers = (workshops-1)*50
        for engineers in range(min_engineers, max_engineers+1):
            reqLS = ceil(engineers / 50)
            hours_to_do = man_hours
            product_made = 0
            for hour in range(MONTH):
                hours_to_do = hours_to_do - engineers
                while hours_to_do <= 0:
                    product_made += 1
                    if TFTD:
                        hours_to_do += man_hours
                    else:
                        hours_to_do = man_hours
            income = product_made * man_sell
            maint  = workshops * WORK_MAIN +\
                     reqLS * LIVI_MAIN +\
                     engineers * ENG_SAL
            expend = product_made * man_cost
            expend = expend + maint
            profit = income - expend
            setup = workshops*WORK_COST +\
                    reqLS*LIVI_COST +\
                    engineers*ENG_COST
            if profit > best_profit:
                best_engineers = engineers
                best_living_space = reqLS
                best_workshops = workshops
                best_profit = profit
                best_setup = setup
                best_product = product_made

    print()
    print('Best setup')
    print('\tMonthly profit: {0}$'.format(best_profit))
    print('\tEngineers needed: {0}'.format(best_engineers))
    print('\tLiving quartes needed: {0}'.format(best_living_space))
    print('\tWorkshops needed: {0}'.format(best_workshops))
    print('\tSetup cost: {0}$'.format(best_setup))
    if best_profit <= 0:
        print('\tPayoff in: NEVER')
    else:
        print('\tPayoff in: {0} days'.format(ceil(24 * (best_setup / best_profit))))
    print('\tProduct made: {0}'.format(best_product))
    print()
