import discord
from discord.ext import commands

import discord
from discord.ext import commands

# Classe pour les paramètres, avec un sélecteur de langue
class Settings:

    @staticmethod
    def toEmbed():
        # Créer un embed pour la sélection de la langue
        embed = discord.Embed(title="Settings", color=0x3498db)

        # Créer des options pour le menu déroulant de sélection de langue
        options = [
            discord.SelectOption(label="English", value="en", emoji="🇬🇧"),
            discord.SelectOption(label="Français", value="fr", emoji="🇫🇷")
        ]

        # Créer un objet Select avec les options
        language_select = LanguageSelect(options=options)

        # Créer une instance de View et ajouter le Select
        view = discord.ui.View()
        view.add_item(language_select)

        return embed, view

# Classe pour gérer le sélecteur de langue
class LanguageSelect(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder="Choose your language...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_language = self.values[0]
        
        # Sauvegarde la langue sélectionnée dans la base de données (logique à implémenter)
        # db_manager.set_user_language(interaction.user.id, selected_language)

        if selected_language == "en":
            await interaction.response.send_message("Language set to English.", ephemeral=True)
        elif selected_language == "fr":
            await interaction.response.send_message("Langue définie sur le Français.", ephemeral=True)
