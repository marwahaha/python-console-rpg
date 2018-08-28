from utils import *
from config import Config
from models import Player, Monster, Weapon


class Game(object):

    def __init__(self):
        self.players = []
        self.monsters = []
        self.getPlayer()
        self.createMonster()
        while True:
            self.turnLoop()

    def turnLoop(self):
        for player in self.players:
            game_state = {'players':self.players, 'monsters':self.monsters}
            player.getTurnAction(game_state)
            self.deadCheck()

        for monster in self.monsters:
            game_state = {'players':self.players, 'monsters':self.monsters}
            monster.turnAction(game_state)
            self.deadCheck()

    def deadCheck(self):
        for player in self.players:
            if player.dead:
                self.players.pop(self.players.index(player))

        if not self.players:
            message('All players are dead! Game over!')
            exit()

        for monster in self.monsters:
            if monster.dead:
                self.monsters.pop(self.monsters.index(monster))

        if not self.monsters:
            self.createMonster()

    def getPlayer(self):
        name = stringPrompt('What is your name?', 'your Name')
        player = Player(name, race = 'Human', charType = 'Warrior')
        player.weapon = Weapon()
        self.players.append(player)
        messageDirect(player)

    def createMonster(self):
        monster = Monster('Rabid Gnome')
        self.monsters.append(monster)
        messageDirect('A new monster joins the fray!\n', monster)


enableVTWindows()

game = Game()