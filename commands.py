import os
import inspect
import nextcord
import datetime

from nextcord.ext import commands

from src.extra.scripts.colored_printing import colorized_print
from src.extra.scripts.openai_manager import OpenAIManager
from src.bot import DiscordBot

from .components.scripts import tasks
from .components.scripts import recipe_embed
from .components.scripts import parser
from .components.scripts import json_manager

class SousChefCog(commands.Cog):
    IDX_REACTIONS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
    OPTIONS_REACTIONS = ["💾", "⭐", "♥️"]

    def __init__(self, bot):
        self.recipe_embedding = recipe_embed.RecipeEmbedding()
        self.bot: DiscordBot = bot
        self.name = "Admin Commands"
        self.open_ai = OpenAIManager()
        colorized_print("COG", "SousChefCog connected")

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="contains", description="Sous Chef: type an ingredient or list of ingredients")
    async def contains(self, interaction: nextcord.Interaction, ingredient: str, allergies: str=None) -> None:
        print("INFO", f"{interaction.user.name} used {self}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        await interaction.response.defer()
        embed_title = f"Recipes that contain {ingredient}."
        embed = nextcord.Embed(title=embed_title)

        user_message = f"Create a list of 5 recipe names that contain {ingredient}, list only the names"
        if allergies:
            embed.description = f"Excluding: {allergies}"
            user_message += f" exclude recipes that contain {allergies}"

        messages = [
                {"role": "system", "content": "You are a helpful sous chef."},
                {"role": "user", "content":  user_message}
            ]

        response = self.open_ai.generate_response(messages, 150)

        embed.add_field(name="="*len(embed_title), value=response)
        embed.set_footer(text="Click the numbers below to view recipe details")

        message = await interaction.followup.send(embed=embed)

        # Add reactions to the message
        for reaction in SousChefCog.IDX_REACTIONS:
            await message.add_reaction(reaction)

        # Start a background task to watch for reactions
        self.bot.loop.create_task(tasks.wait_for_idx_reaction(self, interaction, response, message))
        

    # =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="get_recipe", description="Sous Chef: use AI to find recipes that contain certain ingredients")
    async def get_recipe(self, interaction: nextcord.Interaction, dish_name: str, serving_count: int = 1) -> None:
        colorized_print("COMMAND", f"{interaction.user.name} used {self.__cog_name__}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")

        try:
            await interaction.response.defer()
        except nextcord.errors.InteractionResponded:
            pass

        if f"{dish_name}.json" in os.listdir(f"{self.bot.paths['temp']}/recipes"):
            recipe_info = json_manager.open_json(f"{self.bot.paths['temp']}/recipes/{dish_name}.json")
            messages = []
            response = ""
        else:
            messages = [
                {"role": "system", "content": f"You are a helpful sous chef preparing a concise recipe.\n===\nPart 1: List the Ingredients for {serving_count} servings\n- ingredient 1\n- ingredient 2\n===\nPart 2: Write concise Instructions\n1.\n2.\n3.\n===\nPart 3: short Description of dish\nPart 4: carefully consider a spice factor integer between one and ten"},
                {"role": "user", "content": f'Generate a step by step recipe for {dish_name}'}
            ]
            response = self.open_ai.generate_response(messages, 1000)
            recipe_info = parser.recipe_parser(dish_name, response)
            json_manager.save_json(f"{self.bot.paths['temp']}/recipes/{dish_name}.json", recipe_info)

        difficulty = parser.determine_difficulty(recipe_info)

        head_embed, instructions_embed = self.recipe_embedding.create_embeds(dish_name, recipe_info)

        head_embed.description = f"Difficulty: **{difficulty}**"

        await interaction.followup.send(embed=head_embed)
        message = await interaction.followup.send(embed=instructions_embed)

        # Add reactions to the message
        for reaction in SousChefCog.OPTIONS_REACTIONS:
            await message.add_reaction(reaction)

        # Start a background task to watch for reactions
        self.bot.loop.create_task(tasks.wait_for_options_reaction(self.bot, interaction, recipe_info, message, SousChefCog.OPTIONS_REACTIONS))


# =====================================================================================================
    @nextcord.slash_command(dm_permission=False, name="help", description="Sous Chef: use AI to find solutions to your culinary problems")
    async def help(self, interaction: nextcord.Interaction, query:str) -> None:
        colorized_print("COMMAND", f"{interaction.user.name} used {self.__cog_name__}.{inspect.currentframe().f_code.co_name} at {datetime.datetime.now()}")
        """use AI to find solutions to your culinary problems"""
        await interaction.response.defer()

        messages = [
                {"role": "system", "content": "You are a helpful sous chef. Please help me with my culinary problem. do not respond to non culinary questions"},
                {"role": "user", "content":  query + "do not respond to non culinary questions"}
            ]
        response = self.open_ai.generate_response(messages, 500, 0)

        embed = nextcord.Embed(title=query.capitalize(), description=response, color=nextcord.Color.blurple())

        await interaction.followup.send(embed=embed)



def setup(bot: commands.Bot):    
    os.makedirs(f'{DiscordBot.paths["temp"]}/recipes', exist_ok=True)
    bot.add_cog(SousChefCog(bot))

