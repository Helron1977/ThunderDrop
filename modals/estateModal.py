import discord
from discord.ext import commands

class EstateModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Multi-field Modal")

        # Ajouter cinq champs de texte au modal
        self.field1 = discord.ui.TextInput(label="Field 1", placeholder="Enter text here...", style=discord.TextStyle.short)
        self.field2 = discord.ui.TextInput(label="Field 2", placeholder="Enter text here...", style=discord.TextStyle.short)
        self.field3 = discord.ui.TextInput(label="Field 3", placeholder="Enter text here...", style=discord.TextStyle.short)
        self.field4 = discord.ui.TextInput(label="Field 4", placeholder="Enter text here...", style=discord.TextStyle.short)
        self.field5 = discord.ui.TextInput(label="Field 5", placeholder="Enter text here...", style=discord.TextStyle.short)

        self.add_item(self.field1)
        self.add_item(self.field2)
        self.add_item(self.field3)
        self.add_item(self.field4)
        self.add_item(self.field5)

    async def on_submit(self, interaction: discord.Interaction):
        # Traitement des valeurs des champs
        data = {
            "Field 1": self.field1.value,
            "Field 2": self.field2.value,
            "Field 3": self.field3.value,
            "Field 4": self.field4.value,
            "Field 5": self.field5.value,
        }
        await interaction.response.send_message(f"Received data: {data}")