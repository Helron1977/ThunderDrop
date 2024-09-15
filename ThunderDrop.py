import discord

from discord.ext import commands
from discord import app_commands
from cogs.playerCog import PlayerCog
from cogs.listenersCog import ListenersCog
from cogs.paramCog import ParamCog  
from player import Player
from typeDef.hopistal  import Hospital


import logging

#Activer le logging
logging.basicConfig(level=logging.INFO)

# Configuration des intents
intents = discord.Intents.default()
intents.message_content = True  # Activer l'accès au contenu des messages
intents.members = True  # Nécessaire pour obtenir des informations sur les membres

# Définir le menu contextuel à l'extérieur des classes
async def check_troops(interaction: discord.Interaction, user: discord.Member):
    # Exemple de réponse simple pour vérifier la fonctionnalité
        # Affiche le nombre de troupes blessées par type
    player = Player.load(user.id)
    embed, view = Hospital.toEmbed(player)  # Obtient l'embed et les boutons à partir de la classe Hopital
    await interaction.response.send_message(embed=embed, view=view)


# Initialisation du bot avec les intents
bot = commands.Bot(command_prefix="!", intents=intents)
bot.tree.add_command(app_commands.ContextMenu(name="Check your troops", callback=check_troops))



# Ajouter les cogs
@bot.event
async def on_ready():
    try:
        # Synchroniser les commandes du bot
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

async def main():
    # Ajouter les cogs
    await bot.add_cog(PlayerCog(bot))
    await bot.add_cog(ListenersCog(bot))
    await bot.add_cog(ParamCog(bot))  # Ajoutez d'autres cogs de la même manière
    print('Logged in')
    import os
    from dotenv import load_dotenv

    load_dotenv()
    token = os.getenv('TOKEN')


    # Démarrer le bot
    await bot.start(token)  # Remplace 'YOUR_BOT_TOKEN' par le vrai token

import asyncio
asyncio.run(main())

# Run the main function
asyncio.run(main())


# Initialiser le bot et ajouter le cog
bot = commands.Bot(command_prefix="!")



