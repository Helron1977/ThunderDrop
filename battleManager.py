
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

class BattleManager:
    BONUS = {
        'archer': {'target': 'infantry', 'bonus': 0.2},
        'infantry': {'target': 'cavalry', 'bonus': 0.2},
        'cavalry': {'target': 'archer', 'bonus': 0.2}
    }

    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
       

    def calculate_damage(self):
        # Initialize variables
        attack_order = ['archer', 'cavalry', 'infantry']
        for troop_type in attack_order:
            attacker_troops = getattr(self.attacker, troop_type)
            if attacker_troops <= 0:
                continue  # Skip if no troops of this type

            target_types = ['infantry', 'cavalry', 'archer']
            for target in target_types:
                if attacker_troops <= 0:
                    break
                if troop_type == 'archer' and target == 'archer':
                    damage = attacker_troops // 3
                else:
                    damage = attacker_troops // 3

                # Apply bonus if applicable
                if self.BONUS[troop_type]['target'] == target:
                    damage += damage * self.BONUS[troop_type]['bonus']

                # Inflict damage
                self.apply_damage(damage, target)

                attacker_troops -= damage

    def apply_damage(self, damage, target):
        defender_troops = getattr(self.defender, target)
        if defender_troops >= damage:
            setattr(self.defender, target, defender_troops - damage)
        else:
            wounded = damage - defender_troops
            setattr(self.defender, target, 0)
            setattr(self.defender, f'wounded_{target}', getattr(self.defender, f'wounded_{target}') + wounded)

    def start_battle(self):       
        while self.attacker.infantry > 0 or self.attacker.archer > 0 or self.attacker.cavalry > 0:
            if self.defender.infantry <= 0 and self.defender.archer <= 0 and self.defender.cavalry <= 0:
                break
            self.calculate_damage()
            # Swap attacker and defender roles for the next round
            self.attacker, self.defender = self.defender, self.attacker


    async def generate_battle_image(self, player1_avatar_url, player2_avatar_url, result_player1, result_player2, troop_percentage_player1, troop_percentage_player2, player1_name, player2_name):
        # Charger l'image de fond (chemin local)
        base_image = Image.open("C:\\Users\\rolan\\OneDrive\\Documents\\TD\\battlebackground.png")
        
        # Créer un contexte de dessin
        draw = ImageDraw.Draw(base_image)

        # Charger les avatars des joueurs
        player1_avatar = Image.open(BytesIO(requests.get(player1_avatar_url).content))
        player2_avatar = Image.open(BytesIO(requests.get(player2_avatar_url).content))

        # Redimensionner les avatars à 175*175 pixels
        player1_avatar = player1_avatar.resize((175, 175))
        player2_avatar = player2_avatar.resize((175, 175))
        
        # Coller les avatars à 30 pixels des coins respectifs
        base_image.paste(player1_avatar, (30, 30))
        base_image.paste(player2_avatar, (base_image.width - 230, 30))

        # Charger la police Village
        font = ImageFont.truetype("C:\\Users\\rolan\\OneDrive\\Documents\\TD\\Village.ttf", 50)
        
        # Couleur du texte pour les résultats
        text_color = (113, 82, 42)  # Couleur spécifiée pour le texte

        # Calculer les positions du texte pour qu'il soit centré
        text_width_player1 = draw.textlength(result_player1, font=font)
        text_width_player2 = draw.textlength(result_player2, font=font)
        
        # Largeur de la moitié de l'image
        half_width = base_image.width // 2

        # Positionnement pour centrer le texte dans la moitié gauche
        x_player1 = (half_width - text_width_player1) // 2

        # Positionnement pour centrer le texte dans la moitié droite
        x_player2 = half_width + (half_width - text_width_player2) // 2

        # Dessiner les résultats (Victoire/Défaite)
        draw.text((x_player1, 272), result_player1, fill=text_color, font=font)
        draw.text((x_player2, 272), result_player2, fill=text_color, font=font)

        # Dessiner les noms des joueurs
        name_font = ImageFont.truetype("C:\\Users\\rolan\\OneDrive\\Documents\\TD\\Village.ttf", 30)  # Police plus petite pour les noms
        name_color = text_color

        def draw_text_with_left_corner(draw, text, left_x, y, font, fill):
            text_width = draw.textlength(text, font=font)
            x = left_x
            draw.text((x, y), text, fill=fill, font=font)

        def draw_text_with_right_corner(draw, text, right_x, y, font, fill):
            text_width = draw.textlength(text, font=font)
            x = right_x - text_width
            draw.text((x, y), text, fill=fill, font=font)

        # Positionnement du nom du joueur 1 (coin gauche du texte)
        draw_text_with_left_corner(draw, player1_name.upper(), 220, 120, name_font, name_color)

        # Positionnement du nom du joueur 2 (coin droit du texte)
        draw_text_with_right_corner(draw, player2_name.upper(), 2485, 120, name_font, name_color)

        # Paramètres de couleur pour les jauges
        fill_color = (173, 40, 24)  # Rouge défini
        dark_color = (123, 28, 17)  # Ombre (plus sombre)
        light_color = (223, 52, 31)  # Lumière (plus clair)
        border_color = (139, 69, 19)  # Marron

        # Calculer les largeurs des jauges en fonction des pourcentages
        fill_width_player1 = int(1000 * (troop_percentage_player1 / 100))
        fill_width_player2 = int(1000 * (troop_percentage_player2 / 100))

        # Dessiner la jauge pour le premier joueur
        draw.rectangle([155, 360, 1155, 388], outline=border_color, width=2)  # Cadre marron

        # Dégradé vertical symétrique pour l'effet bombé
        for i in range(28):  # Ajuster la hauteur du dégradé pour correspondre à la hauteur du rectangle
            ratio = i / 28.0
            if ratio <= 0.5:
                gradient_color = tuple(
                    int(dark_color[j] * (0.5 - ratio) * 2 + light_color[j] * ratio * 2) for j in range(3)
                )
            else:
                gradient_color = tuple(
                    int(light_color[j] * (1 - ratio) * 2 + dark_color[j] * (ratio - 0.5) * 2) for j in range(3)
                )
            draw.line([(157, 362 + i), (157 + fill_width_player1, 362 + i)], fill=gradient_color)

        # Dessiner la jauge pour le deuxième joueur (symétrique)
        draw.rectangle([base_image.width - 1155, 360, base_image.width - 155, 388], outline=border_color, width=2)  # Cadre marron
        for i in range(28):  # Ajuster la hauteur du dégradé pour correspondre à la hauteur du rectangle
            ratio = i / 28.0
            if ratio <= 0.5:
                gradient_color = tuple(
                    int(dark_color[j] * (0.5 - ratio) * 2 + light_color[j] * ratio * 2) for j in range(3)
                )
            else:
                gradient_color = tuple(
                    int(light_color[j] * (1 - ratio) * 2 + dark_color[j] * (ratio - 0.5) * 2) for j in range(3)
                )
            draw.line([(base_image.width - 1155 + (1000 - fill_width_player2), 362 + i), 
                    (base_image.width - 1155 + 1000, 362 + i)], fill=gradient_color)

        # Sauvegarder l'image dans un objet BytesIO
        img_bytes = BytesIO()
        base_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
    
    async def send_battle_result( self,player1,player1_avatar_url, player2_avatar_url, result_player1, result_player2, troop_percentage_player1, troop_percentage_player2, player1_name, player2_name):
        # Generate the battle image
        member1 = await self.bot.fetch_user(player1.user_id)

        battle_image = await BattleManager.generate_battle_image(self,player1_avatar_url, player2_avatar_url, result_player1, result_player2, troop_percentage_player1, troop_percentage_player2, player1_name, player2_name)

        # Send image to both players
        await member1.send(file=discord.File(battle_image, "battle_result.png"))
        print(f"Battle result sent to {member1.name}.") # Debug line



