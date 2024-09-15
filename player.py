# player.py
from DatabaseManager import DatabaseManager

class Player:
    def __init__(self, user_id, points=0, infantry=0, archer=0, cavalry=0,wounded_infantry=0,wounded_archer=0,wounded_cavalry=0,):
        self.user_id = user_id
        self.points = points
        self.infantry = infantry
        self.archer = archer
        self.cavalry = cavalry
        self.wounded_infantry = wounded_infantry
        self.wounded_archer = wounded_archer
        self.wounded_cavalry = wounded_cavalry

    def save(self):
        db = DatabaseManager()
        db.save_player(self)
        del db

    @staticmethod
    def load(user_id):
        db = DatabaseManager()
        player = db.load_player(user_id)
        del db
        return player
    
    def add_points(self, points_to_add):
        self.points += points_to_add
        self.save()
        print(f"Points de {self.user_id} mis à jour (add): {self.points}")

    def get_all(self):
        db = DatabaseManager()
        players = db.get_all_players()
        del db
        return players
    
    def heal_troops(self, troop_type, points):
        if troop_type == 'Infantry':
            to_heal = min(points * 2, self.wounded_infantry)
            self.wounded_infantry -= to_heal
            self.infantry += to_heal
        elif troop_type == 'Archers':
            to_heal = min(points * 2, self.wounded_archers)
            self.wounded_archers -= to_heal
            self.archers += to_heal
        elif troop_type == 'Cavalry':
            to_heal = min(points * 2, self.wounded_cavalry)
            self.wounded_cavalry -= to_heal
            self.cavalry += to_heal
        self.points -= points

            