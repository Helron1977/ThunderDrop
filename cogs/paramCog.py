import discord
from discord.ext import commands
from DatabaseManager import DatabaseManager  # Import de DatabaseManager
from translationManager import TranslationManager
from typeDef.settings import Settings


class ParamCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.db_manager = DatabaseManager()  # Initialisation de DatabaseManager

    @commands.command(name='setlang')
    async def set_language(self, ctx, language: str):
        if language in ['en', 'fr']:
            self.db_manager.set_user_language(ctx.author.id, language)
            await ctx.send(f"Language set to {language}.")
        else:
            await ctx.send(TranslationManager.get_translation(language, 'LANG_UNSUPPORTED'))


    @commands.command(name='setlang')
    async def set_language(self, ctx, language: str):
        if language in ['en', 'fr']:
            self.db_manager.set_user_language(ctx.author.id, language)
            await ctx.send(f"Language set to {language}.")
        else:
            await ctx.send(TranslationManager.get_translation(language, 'LANG_UNSUPPORTED'))

    @commands.command(name="settings")
    async def open_settings(self, ctx):
        # Obtenir l'embed et la vue de Settings
        embed, view = Settings.toEmbed()
        
        # Envoyer le message avec l'embed et la vue
        await ctx.send(embed=embed, view=view)