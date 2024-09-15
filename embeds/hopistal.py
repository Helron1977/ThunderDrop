import discord

from translationManager import TranslationManager
from discord.ui import Button, View

class Hospital:

    def toEmbed(player):
        msg = TranslationManager.gettext(
                player.user_id,
                'HOSPITAL_STATUS', 
                wounded_infantry=player.wounded_infantry,
                wounded_archer=player.wounded_archer,
                wounded_cavalry=player.wounded_cavalry
            )

        # Créer un embed pour le rapport d'hôpital
        embed = discord.Embed(title="🩺 Hospital Report", color=0x3498db)
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/RLyWj8N8myPeqxUcCEPWmkRIvj89VlUpvDhfNDct0HY/https/idata.over-blog.com/1/28/66/98/chevalier-blesse.jpg?format=webp&width=418&height=270")
        embed.set_footer(text="Stay safe on the battlefield!")
        embed.description = msg

        view = MyView()

        return embed,view

class MyView(View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Soigner les troupes", style=discord.ButtonStyle.primary, custom_id="heal")
    async def heal_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Vous avez choisi de soigner les troupes.")

    @discord.ui.button(label="Détails", style=discord.ButtonStyle.secondary, custom_id="details")
    async def details_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Voici les détails.")