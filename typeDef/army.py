import discord
from translationManager import TranslationManager

class Army:
    @staticmethod
    def toEmbed(player):
        # Créer un message traduit avec gettext pour le statut de l'armée
        message = TranslationManager.gettext(
            player.user_id, 
            'ARMY_STATUS', 
            infantry=player.infantry, 
            archer=player.archer, 
            cavalry=player.cavalry
        )

        # Créer un embed pour le statut des troupes
        embed = discord.Embed(title="🏰 Army Status", color=0x2ecc71)
        embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/6/6d/Armored_Knight_Mounted_on_Cloaked_Horse.JPG")
        embed.set_footer(text=message)

        # Créer des boutons pour l'interaction
        buttons = [
            discord.ui.Button(label="Upgrade Troops", style=discord.ButtonStyle.primary, custom_id="upgrade_troops"),
            discord.ui.Button(label="Troop Details", style=discord.ButtonStyle.secondary, custom_id="troop_details")
        ]

        # Créer une instance de View
        view = discord.ui.View()
        for button in buttons:
            view.add_item(button)
        
        return embed, view