from utils import message, messageDirect, formatHPString, generateUID, boolPrompt, stringPrompt

class Character(object):

    def __init__(self, name, lvl=1, hp=10, race='Gnome', charType='Tunneler'):
        self.id = generateUID() #id currently isnt used for anything, but I thought it might be useful to have a unique id in the future incase need to do character lookups
        self.name = name #does not have to be unique
        self.race = race
        self.charType = charType #this is basically the class
        self.lvl = lvl
        self.hp_max = hp
        self.hp_current = hp
        self.weapon = None #this should be a weapon object
        self.strength = 2 #currently only strength is implemented, will expand to other  RPG stats later
        self.retaliates = False #this determines if a monster (or player) will automatically attack back after being attacked. This is essentially a free attack, so is pretty strong
        self.dead = False

    def __str__(self):
        #this overwrites the classes default string method, so if you call message(player) this is what will print
        return(message(self.name, 'cyan', returnFormatted=True) + ' is a Lvl ' + message(self.lvl, 'cyan', returnFormatted=True) + ' ' + 
            message(self.race, 'green', returnFormatted=True) + ' ' + message(self.charType, 'green', returnFormatted=True) + ' with ' +
            formatHPString(self.hp_current, self.hp_max) + 'HP')
    
    def calculateDamage(self):
        #damage is currently always calculated the same. May implement some randomization or critical chance in the future
        if self.weapon:
            damage = self.strength + self.weapon.damage + self.lvl
        else:
            damage = self.strength + self.lvl    
        return damage

    def takeDamage(self, damage):
        #this can be overridden in the future for classes or monsters that have special abilities
        self.hp_current -= damage

    def attack(self, target):
        ownDamage = self.calculateDamage()
        target.takeDamage(ownDamage)
        message(self.name + ' attacks ' + target.name + ' dealing ' + str(ownDamage) + ' damage!')
        if target.hp_current <= 0:
            target.dead = True
            message(target.name + ' is dead!')
            self.lvlUp()
        if target.retaliates and target.dead == False:
            message(target.name + ' retaliates!')
            target.attack(self)

    def heal(self, healAmmount):
        self.hp_current += healAmmount
        if self.hp_current > self.hp_max:
            self.hp_current = self.hp_max

    def lvlUp(self):
        self.lvl += 1
        self.hp_max += 5
        self.hp_current = self.hp_max
        self.strength += 1
        message(self.name + ' lvls up!')
        message(self.name + ' is now lvl ' + str(self.lvl))
        message('Gain 5HP and 1 Strength!')

class Player(Character):

    def equipWeapon(self, weapon):
        if self.weapon:
            discard_current_weapon = boolPrompt('You currently have a weapon ' + self.weapon.name + ', would you like to exchange it for a ' + weapon.name + '?')
            if discard_current_weapon:
                self.weapon = weapon
            return discard_current_weapon
        else:
            self.weapon = weapon
            return True

    def getTurnAction(self, game_state):
        message('It is ' + self.name + 's turn, what would you like to do?\n1: Attack\n2: Heal\n3: Inspect Enemies - NOT IMPLEMENTED')
        message(self.name + ' currently has ' + formatHPString(self.hp_current, self.hp_max) + 'HP')
        turnAction = stringPrompt('What action would you like to take?', 'number next to action')
        if turnAction not in ['1', '2', '3']:
            self.getTurnAction(game_state)
        elif turnAction == '1':
            self.attackTurn(game_state)
        elif turnAction == '2':
            self.heal()
        elif turnAction == '3':
            message('Inspecting is not implemented yet!', 'red')
            self.getTurnAction(game_state)

    def heal(self):
        healAmmount = self.hp_max / 2
        if self.hp_current + healAmmount >= self.hp_max:
            self.hp_current = self.hp_max
            message(self.name + ' heals to full health, ' + str(self.hp_max), 'magenta')
        else:
            self.hp_current += healAmmount
            message(self.name + ' heals for ' + str(healAmmount) + ' leaving them at ' + str(self.hp_current), 'magenta')

    def attackTurn(self, game_state):
        monsters = sorted(game_state['monsters'], key=lambda x: x.hp_current)
        message('These monsters are currently in the room:', 'green')
        x = 0
        for monster in monsters:
            messageDirect(str(x) + ': ' + str(monster))
            x += 1
        monster_id = stringPrompt('Which would you like to fight?', 'number next to monster')
        try:
            monster_id = int(monster_id)
            if monster_id >= x or monster_id < 0:
                raise Exception()
        except:
            message('You must choose a valid monster.', 'red')
            self.getTurnAction(game_state)

        self.attack(monsters[monster_id])        

        

class Monster(Character):
    
    def turnAction(self, game_state):
        players = sorted(game_state['players'], key=lambda x: x.hp_current)
        self.attack(players[0])


class Weapon(object):
    
    def __init__(self, name='Rusty Sword', damage=4):
        self.name = name
        self.damage = damage #int

    def __str__(self):
        return('A ' + self.name + ' which deals ' + str(self.damage) + ' damage per hit.')
        