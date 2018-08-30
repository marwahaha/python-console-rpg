from utils import message

class AbilityManager(object):

    def __init__(self):
        self.damage_abilities = [Fireball()]
        self.healing_abilities = [GreaterHeal()]
        self.other_abilities = []

    def listAbilities(self):
        message('Damage Abilties:')
        for i in self.damage_abilities:
            message(i.name + ': ' + i.description)
        message('Healing Abilties:')
        for i in self.healing_abilities:
            message(i.name + ': ' + i.description)
        message('Other Abilties:')
        for i in self.other_abilities:
            message(i.name + ': ' + i.other_abilities)

    def yieldAbility(self, school, abilityIndex):
        #return ability based on school and the index. yes this is a really bad way, yes it has no error checking, yes it needs to be improved
        #im just really lazy right now
        if school.lower() not in ['damage', 'healing', 'other']:
            raise ValueError('Invalid ability school', school)
        if school == 'damage':
            return self.damage_abilities[abilityIndex]
        elif school == 'healing':
            return self.healing_abilities[abilityIndex]
        elif school == 'other':
            return self.other_abilities[abilityIndex]

class Ability(object):

    def __init__(self, name='Fireball', description='A targeted ball of fire.'):
        self.name = name
        self.description = description
        self.damage = 15
        self.ap_cost = 1
        self.range = 'room'
        self.target_required = True

    def deadCheck(self, target, caster):
        if target.hp_current <= 0:
            target.dead = True
            message(target.name + ' is dead!')
            caster.lvlUp()
        if target.retaliates and target.dead == False:
            message(target.name + ' retaliates!')
            target.attack(caster)

    def activate(self, target, caster):
        #all abilties should be initiated by the activate method, which should always take 'target' and 'caster' as its main inputs. target can be none if it is self casted, but must be included in the method
        #this can be overwritten by making a new activate method on child abilility classes
        totalDamage = caster.intelligence + self.damage
        target.takeDamage(totalDamage)
        caster.ap_current -= self.ap_cost
        message(caster.name + ' casts fireball! It deals ' + str(totalDamage) + ' to ' + target.name)
        #all activate methods where the target is taking damage should include deadcheck() at the end
        self.deadCheck(target, caster)

class Fireball(Ability):

    def __init__(self):
        super().__init__()


class GreaterHeal(Ability):

    def __init__(self):
        super().__init__('Greater Heal', 'A large heal, consuming several AP.')
        self.damage = 0
        self.heal_ammount = 10 #this isnt in the base ability model
        self.ap_cost = 4
        self.target_required = False

    def activate(self, target, caster): #here we are overwriting the base activate method.
        if target == None:
            target = caster
        total_heal_ammount = self.heal_ammount + caster.wisdom
        target.takeHealing(total_heal_ammount)
        caster.ap_current -= self.ap_cost
        message(caster.name + ' casts Greater Heal on ' + target.name + ', healing for ' +  str(total_heal_ammount))