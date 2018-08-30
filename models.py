from utils import message, messageDirect, formatHPString, generateUID, boolPrompt, stringPrompt
from abilities import AbilityManager

class Character(object):

    def __init__(self, name, lvl=1, hp=10, race='Gnome', charType='Tunneler'):
        self.id = generateUID() #id currently isnt used for anything, but I thought it might be useful to have a unique id in the future incase need to do character lookups
        self.player = False
        self.name = name #does not have to be unique
        self.race = race
        self.charType = charType #this is basically the class
        self.lvl = lvl
        self.hp_max = hp
        self.hp_current = hp
        self.ap_max = lvl
        self.ap_current = lvl
        self.spellbook = AbilityManager()
        self.abilities = [self.spellbook.yieldAbility('damage', 0), self.spellbook.yieldAbility('healing', 0)]
        self.dead = False
        self.retaliates = False #this determines if a monster (or player) will automatically attack back after being attacked. This is essentially a free attack, so is pretty strong
        self.weapon = None #this should be a weapon object
        self.armor_score = 0 #currently this is just implemented as a flat reduction on damage taken
        self.strength = 1 #currently only strength is implemented, will expand to other  RPG stats later
        self.intelligence = 1
        self.constitution = 1
        self.dexterity = 1
        self.wisdom = 1
        self.charisma = 1


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
        totalDamage = (damage - self.armor_score)
        if totalDamage > 0:
            self.hp_current -= totalDamage

        #this dead check is also done after attacks, which is redudant. can be removed from attacks at some point
        if self.hp_current <= 0:
            self.dead = True

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

    def takeHealing(self, healAmmount):
        self.hp_current += healAmmount
        if self.hp_current > self.hp_max:
            self.hp_current = self.hp_max

    def lvlUp(self):
        self.lvl += 1
        self.hp_max += (5 + self.constitution)
        self.hp_current = self.hp_max
        self.ap_max += (1 + self.wisdom)
        self.ap_current = self.ap_max
        self.strength += 1
        self.intelligence += 1
        self.constitution += 1
        self.dexterity += 1
        self.wisdom += 1
        self.charisma += 1

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
        message('It is ' + self.name + 's turn, what would you like to do?\n1: Attack\n2: Heal\n3: Inspect Enemies - NOT IMPLEMENTED\n4: Use an ability')
        message(self.name + ' currently has ' + formatHPString(self.hp_current, self.hp_max) + 'HP')
        turnAction = stringPrompt('What action would you like to take?', 'number next to action')
        if turnAction not in ['1', '2', '3', '4']:
            self.getTurnAction(game_state)
        elif turnAction == '1':
            self.attackTurn(game_state)
        elif turnAction == '2':
            self.heal()
        elif turnAction == '3':
            message('Inspecting is not implemented yet!', 'red')
            self.getTurnAction(game_state)
        elif turnAction == '4':
            self.abilityTurn(game_state)

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

    def abilityTurn(self, game_state):
        #get the player to select an ability
        message(self.name + ' currently has these abilities:')
        x=0
        for ability in self.abilities:
            messageDirect(str(x) + ': ' + str(ability.name))
            x += 1
        ability_id = stringPrompt('Which ability would you like to use?', 'number next to ability')
        try:
            ability_id = int(ability_id)
            if ability_id >= x or ability_id < 0:
                raise Exception()
        except:
            message('You must choose a valid ability.', 'red')
            self.getTurnAction(game_state)

        if self.abilities[ability_id].ap_cost > self.ap_current:
            message('Not enough AP to use this ability!', 'red')
            self.getTurnAction(game_state)

        #if the ability requires a target, select one
        if self.abilities[ability_id].target_required:
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

            self.abilities[ability_id].activate(monsters[monster_id], self)
        else:
            self.abilities[ability_id].activate(None, self)

    def lvlUp(self):
        self.lvl += 1
        self.hp_max += (5 + self.constitution)
        self.hp_current = self.hp_max
        self.ap_max += (1 + self.wisdom)
        self.ap_current = self.ap_max
        self.strength += 1
        self.intelligence += 1
        self.constitution += 1
        self.dexterity += 1
        self.wisdom += 1
        self.charisma += 1
        message(self.name + ' lvls up!')
        message(self.name + ' is now lvl ' + str(self.lvl))
        message('Stats Gained:', 'green')
        message('Strength: 1\nIntelligence: 1\nConstitution: 1\nDexterity: 1\nWisdom: 1\nCharisma: 1', 'green')
        message('Gain ' + str(5 + self.constitution) + 'HP and ' + str(1 + self.intelligence) + 'AP', 'green')

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
        





