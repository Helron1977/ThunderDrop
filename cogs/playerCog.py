from asyncio import tasks
import threading
import time
import discord
from discord.ext import tasks, commands
from discord.ui import Button, View
from translationManager import TranslationManager
from player import Player  # Assurez-vous que c'est bien la classe que vous importez
from battleManager import BattleManager
from typeDef.hopistal import Hospital
from typeDef.army import Army


class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_ids = [123456789012345678, 987654321098765432]
        self.heal_jobs = {}  # Dictionnaire pour stocker les joueurs et leurs choix
        self.start_healing.start()  # Démarrer le timer de soin
        self.poll_message = None
        self.heal_jobs = {}  # Dictionnaire pour suivre les tâches de soin en cours
        self.healing_in_progress = False


    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def points(self, ctx):
        print("Commande points exécutée")  # Log pour vérifier l'exécution de la commande
        player = Player.load(ctx.author.id)
        if player:
            print(f"Points de l'utilisateur {ctx.author.id}: {player.points}")  # Log des points
            message = TranslationManager.gettext(ctx.author.id, 'POINTS_MESSAGE', points=player.points)
            print(f"Message traduit: {message}")  # Log du message traduit
            await ctx.send(f"{ctx.author.mention}, {message}")
        else:
            await ctx.send(f"{ctx.author.mention}, vous n'avez pas encore de score.")

    @commands.command()
    async def buy(self, ctx, troop_type: str, quantity: int):
        player = Player.load(ctx.author.id)
        cost = 10

        if player:
            if troop_type in ["infantry", "archer", "cavalry"]:
                total_cost = cost * quantity
                if player.points >= total_cost:
                    player.points -= total_cost
                    setattr(player, troop_type, getattr(player, troop_type) + quantity)
                    player.save()
                    msg = TranslationManager.gettext(ctx.author.id, 'BUY_SUCCESS', quantity=quantity, troop_type=troop_type)
                    await ctx.send(f"{ctx.author.mention} {msg}")
                else:
                    msg = TranslationManager.gettext(ctx.author.id, 'BUY_FAILURE')
                    await ctx.send(f"{ctx.author.mention}, {msg}")
            else:
                msg = TranslationManager.gettext(ctx.author.id, 'INVALID_TROOP_TYPE')
                await ctx.send(msg)
        else:
            await ctx.send(f"{ctx.author.mention}, vous n'avez pas encore de score.")

    @commands.command()
    async def attack(self, ctx, target: discord.Member):
        attacker = Player.load(ctx.author.id)
        defender = Player.load(target.id)

        if not attacker or not defender:
            await ctx.send(f"{ctx.author.mention}, l'attaqué ou l'attaquant n'a pas encore de score.")
            return

        # Mise à jour de Rich Presence
        self.update_rich_presence(attacker.user_id, defender.user_id)
        
        battle = BattleManager(attacker, defender)
        battle.start_battle()

        attacker.save()
        defender.save()

        # Fetch discord.Member objects directly using the member ID from the Player object
        player1_member = ctx.guild.get_member(attacker.user_id)
        player2_member = ctx.guild.get_member(defender.user_id)

        # Fetch avatar URLs
        player1_avatar_url = str(player1_member.avatar.url)
        player2_avatar_url = str(player2_member.avatar.url)

        await BattleManager.send_battle_result(self, attacker, player1_avatar_url, player2_avatar_url, "Victory", "Defeat", 50,50,player1_member.global_name, player2_member.global_name)

        # Déterminer le résultat en fonction des troupes restantes
        if attacker.infantry + attacker.archer + attacker.cavalry > 0:
            msg = TranslationManager.gettext(ctx.author.id, 'ATTACK_VICTORY')
        elif defender.infantry + defender.archer + defender.cavalry > 0:
            msg = TranslationManager.gettext(ctx.author.id, 'ATTACK_DEFEAT')
        else:
            msg = TranslationManager.gettext(ctx.author.id, 'DRAW')

        await ctx.send(f"{ctx.author.mention} {msg} {target.mention}!")
        

    def update_rich_presence(self, attacker_name, defender_name):
        try:
            details = f"Attaque de {attacker_name} contre {defender_name}"
            state = "Attaque en cours"

            def update_rpc():
                try:
                    self.RPC.update(
                        details=details,
                        state=state,
                        large_image="fight",  # Nom du large asset configuré sur Discord Developer Portal
                        large_text="En combat",
                        small_image="swords",  # Nom du small asset configuré sur Discord Developer Portal
                        small_text="En phase d'attaque",
                        start=time.time()
                    )

                    # Attendre 15 secondes avant de mettre à jour à nouveau
                    time.sleep(15)
                except Exception as e:
                    print(f"Erreur lors de la mise à jour de Rich Presence: {e}")

            # Exécuter la mise à jour dans un thread séparé
            thread = threading.Thread(target=update_rpc)
            thread.start()

        except Exception as e:
            print(f"Erreur lors de la mise à jour de Rich Presence: {e}")

    @commands.command()
    async def buritoattack(self, ctx, target: discord.Member):
        attacker = Player.load(ctx.author.id)
        defender = Player.load(target.id)

        if not attacker or not defender:
            await ctx.send(f"{ctx.author.mention}, l'attaqué ou l'attaquant n'a pas encore de score.")
            return
        
        attacker.infantry = attacker.infantry + defender.infantry
        attacker.archer = attacker.archer + defender.archer
        attacker.cavalry = attacker.cavalry + defender.cavalry
        defender.infantry = 0
        defender.archer = 0
        defender.cavalry = 0

        attacker.save()
        defender.save()

        await ctx.send("The King has rise a new army.. who is the burito now ?")

        # Déterminer le résultat en fonction des troupes restantes
        if attacker.infantry + attacker.archer + attacker.cavalry > 0:
            msg = TranslationManager.gettext(ctx.author.id, 'ATTACK_VICTORY')
        elif defender.infantry + defender.archer + defender.cavalry > 0:
            msg = TranslationManager.gettext(ctx.author.id, 'ATTACK_DEFEAT')
        else:
            msg = TranslationManager.gettext(ctx.author.id, 'DRAW')

        await ctx.send(f"{ctx.author.mention} {msg} {target.mention}!")



    @commands.command()
    async def army(self, ctx):
        player = Player.load(ctx.author.id)
        
        if not player:
            await ctx.send(f"{ctx.author.mention}, vous n'avez pas encore de score.")
            return

        embed, view = Army.toEmbed(player)  # Obtient l'embed et les boutons à partir de la classe Army

        # Envoyer le message avec l'embed et la vue
        await ctx.send(embed=embed, view=view)

    @commands.command()
    async def hospital(self, ctx):
        player = Player.load(ctx.author.id)
        
        if not player:
            await ctx.send(f"{ctx.author.mention}, vous n'avez pas encore de score.")
            return

        embed, view = Hospital.toEmbed(player)  # Obtient l'embed et les boutons à partir de la classe Army

        # Envoyer le message avec l'embed et la vue
        await ctx.send(embed=embed, view=view)
    
    @commands.command()
    async def estate(self, ctx):
        # Créer un bouton pour ouvrir le modal
        button = Button(label="Open Estate Modal", style=discord.ButtonStyle.primary, custom_id="open_estate_modal")
        view = View()
        view.add_item(button)

        # Envoyer un message avec le bouton
        await ctx.send("Click the button to open the modal.", view=view)


    @commands.command()
    async def show_scores(self, ctx):
        # Récupérer les joueurs depuis la base de données
        players = Player.get_all(self=self)

        players.sort(key=lambda p: p.points, reverse=True)

        # Limiter aux 5 premiers joueurs
        players = players[:3]

        # Initialiser un message
        message = "Top 5 Scores:\n"

        # Itérer sur les joueurs et construire le message
        for player in players:
            try:
                member = ctx.guild.get_member(player.user_id)  # Récupérer l'objet Member à partir de l'ID
                if member:
                    username = member.display_name  # Utiliser display_name pour obtenir le nom affiché
                else:
                    username = "Unknown"
                
                # Ajouter les détails du joueur au message
                message += f"{username}: Points: {player.points}, Army: {int(player.infantry)+ int(player.archer)+int(player.cavalry)}\n"
            
            except Exception as e:
                message += f"Error retrieving data for user ID {player.user_id}: {str(e)}\n"

        # Envoyer le message dans le canal où la commande a été appelée
        await ctx.send(message)

    @commands.command(name='heal')
    async def start_poll(self, ctx):
        # Envoyer le sondage
        self.poll_message = await ctx.send("Quel type de troupes voulez-vous soigner ? Réagissez pour choisir.")
        reactions = ['🏹', '🐴', '🛡️']  # Archers, Cavaliers, Infanterie
        for reaction in reactions:
            await self.poll_message.add_reaction(reaction)
        
        # Réinitialisez les tâches de soin et le statut
        self.healing_in_progress = False
        self.heal_jobs = {}
    


    @tasks.loop(minutes=1)
    async def start_healing(self):
        if not self.healing_in_progress:
            return

        # Drapeau pour savoir si un soin a été effectué dans cette boucle
        any_healing_done = False

        for user_id, troop_type in self.heal_jobs.items():
            player = Player.load(user_id)
            if player.points > 0:
                if troop_type == 'archer':
                    to_heal = min(player.wounded_archer, player.points * 2)
                    player.wounded_archer -= to_heal
                    any_healing_done = True
                elif troop_type == 'cavalry':
                    to_heal = min(player.wounded_cavalry, player.points * 2)
                    player.wounded_cavalry -= to_heal
                    any_healing_done = True
                elif troop_type == 'infantry':
                    to_heal = min(player.wounded_infantry, player.points * 2)
                    player.wounded_infantry -= to_heal
                    any_healing_done = True

                # Assurez-vous que les valeurs ne tombent pas en dessous de zéro
                player.wounded_archer = max(player.wounded_archer, 0)
                player.wounded_cavalry = max(player.wounded_cavalry, 0)
                player.wounded_infantry = max(player.wounded_infantry, 0)

                # Sauvegardez les données du joueur après le soin
                player.save()

                # Envoyer un message de mise à jour à l'utilisateur
                user = self.bot.get_user(user_id)
                await user.send(f"{troop_type.capitalize()} ont été soignés. Points restants: {player.points}")
                
                # Vérifier si toutes les troupes sont complètement soignées
                if (player.wounded_archer == 0 and troop_type == 'archer') or \
                (player.wounded_cavalry == 0 and troop_type == 'cavalry') or \
                (player.wounded_infantry == 0 and troop_type == 'infantry'):
                    # Arrêter le soin pour ce joueur
                    del self.heal_jobs[user_id]
                    await user.send(f"Le soin des {troop_type} est terminé.")

            else:
                # Arrêter le soin quand il n'y a plus de points
                del self.heal_jobs[user_id]
                user = self.bot.get_user(user_id)
                await user.send("Vous n'avez plus de points pour soigner. Le soin a été arrêté.")

        # Si aucun soin n'a été effectué et qu'il n'y a plus de tâches de soin en cours, arrêter la tâche
        if not self.heal_jobs and not any_healing_done:
            self.healing_in_progress = False
            self.start_healing.stop()
            # Optionnel : Envoyer un message pour informer que tous les soins sont terminés
            channel = self.bot.get_channel(self.poll_message.channel.id)
            await channel.send("Tous les soins sont terminés.")


    @start_healing.before_loop
    async def before_heal_task(self):
        print("Check if bot is  ready. Prepare Healing task")
        await self.bot.wait_until_ready()
        print("Bot is ready. Healing task will start.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if self.poll_message and reaction.message.id == self.poll_message.id:
            troop_types = {
                '🏹': 'archer',
                '🐴': 'cavalry',
                '🛡️': 'infantry'
            }
        
            if reaction.emoji in troop_types:
                troop_type = troop_types[reaction.emoji]

                if self.healing_in_progress:
                    await reaction.message.channel.send("Un soin est déjà en cours.")
                    return

                player = Player.load(user.id)
                self.heal_jobs[user.id] = troop_type

                if not self.healing_in_progress:
                    self.healing_in_progress = True
                    self.start_healing.start()

                await reaction.message.channel.send(
                    f"Le sondage est terminé. Vous avez choisi de soigner les {troop_type}. Soin en cours...")
                await reaction.message.edit(content=f"Soin en cours pour {troop_type}. Réactions seront ignorées.")
                self.poll_message = None


    # Enregistrement de la commande slash hello
    @discord.app_commands.command(name="hello", description="Says hello!")
    async def hello(self, interaction: discord.Interaction):
        button = discord.ui.Button(label="Click Me!", style=discord.ButtonStyle.primary)
        view = discord.ui.View()
        view.add_item(button)

        await interaction.response.send_message('Hello! Click the button below:', view=view)



    

    



