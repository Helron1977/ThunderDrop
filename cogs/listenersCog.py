import threading
import time
from discord.ext import commands
from pypresence import Presence
from player import Player
import discord
from modals.estateModal import EstateModal


class ListenersCog(commands.Cog):
    # Assurez-vous de remplacer par votre propre Application ID
    CLIENT_ID = '1277743389315436636'
    RPC = Presence(CLIENT_ID)
    try:
        RPC.connect()
    except Exception as e:
        print(f"Erreur lors de la connexion à Rich Presence: {e}")



    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        try:
            await self.RPC.clear()
        except Exception as e:
            print(f"Erreur lors de la déconnexion de Rich Presence: {e}")

    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     print(f"Réaction reçue de {user}: {reaction.emoji}")  # Log de la réaction reçue
    #     if user.bot:
    #         print("Réaction ignorée: auteur est un bot")
    #         return

    #     # Charge les données du joueur qui a reçu la réaction (l'auteur du message)
    #     actor = reaction.message.author.id
    #     player = Player.load(actor)  # Charge les données du joueur depuis la base de données

    #     # Vérifie si l'ID du message est dans la liste des messages ciblés
    #     if reaction.message.id in self.message_ids:
    #         print(f"Réaction sur un message spécifique détectée (ID: {reaction.message.id})")
    #         player.add_points(2)  # Ajoute 2 points au joueur
    #     else:
    #         # Ajoute 1 point au joueur
    #         player.add_points(1)

    #     # Le save est fait dans la fonction add_points, donc aucun besoin de save ici
    
    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"Message reçu de {message.author}: {message.content}")  # Log du message reçu
        if message.author.bot:
            print("Message ignoré: auteur est un bot")
            return

        player = Player.load(message.author.id)  # Charge les données du joueur depuis la base de données

        # Mise à jour des points du joueur qui a envoyé le message
        player.add_points(1)  # Ajoute 1 point au joueur
        print(f"Points de {message.author.id} mis à jour (message): {player.points}")  # Log des points mis à jour

    
    @commands.Cog.listener()
    async def on_message_reply(self, message):
        print(f"Réponse reçue par {message.author}: {message.content}")  # Log de la réponse reçue
        if message.author.bot:
            print("Réponse ignorée: auteur est un bot")
            return

        # Mise à jour des points du joueur qui a reçu la réponse
        if message.reference and message.reference.message_id:
            original_message = await message.channel.fetch_message(message.reference.message_id)
            if original_message.author:
                player = Player.load(original_message.author.id)
                player.points += 1
                player.save()
                print(f"Points de {original_message.author.id} mis à jour (réponse): {player.points}")  

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        if interaction.type == discord.InteractionType.component and interaction.data['custom_id'] == "open_estate_modal":
            modal = EstateModal()
            await interaction.response.send_modal(modal) 