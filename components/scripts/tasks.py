import asyncio
import nextcord

from src.bot import DiscordBot
from . import save_pdf


async def wait_for_idx_reaction(cog, interaction, response, message):
    def check(reaction, user):
        return user == interaction.user and str(reaction.emoji) in cog.IDX_REACTIONS and reaction.message.id == message.id

    try:
        reaction, user = await cog.bot.wait_for('reaction_add', timeout=180.0, check=check)
        await handle_idx_reaction(cog, interaction, response, reaction)
    except asyncio.TimeoutError:
        # Handle the timeout, e.g., remove the reactions from the message
        for reaction in cog.IDX_REACTIONS:
            await message.remove_reaction(reaction, cog.bot.user)


async def handle_idx_reaction(cog, interaction, response, reaction):
    """Handle the reaction pressed by the user"""
    response = response.split("\n")
    if str(reaction.emoji) == "1️⃣":
        # handle first recipe
        await cog.get_recipe(interaction, response[0].replace("1. ", ""))
    elif str(reaction.emoji) == "2️⃣":
        # handle second recipe
        await cog.get_recipe(interaction, response[1].replace("2. ", ""))
    elif str(reaction.emoji) == "3️⃣":
        # handle second recipe
        await cog.get_recipe(interaction, response[2].replace("3. ", ""))
    elif str(reaction.emoji) == "4️⃣":
        # handle second recipe
        await cog.get_recipe(interaction, response[3].replace("4. ", ""))
    elif str(reaction.emoji) == "5️⃣":
        # handle second recipe
        await cog.get_recipe(interaction, response[4].replace("5. ", ""))


async def wait_for_options_reaction(bot, interaction, recipe_info, message, reactions):
        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in reactions and reaction.message.id == message.id

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=180.0, check=check)
            await handle_options_reaction(bot, interaction, reaction, recipe_info)
        except asyncio.TimeoutError:
            # Handle the timeout, e.g., remove the reactions from the message
            for reaction in bot.OPTIONS_REACTIONS:
                await message.remove_reaction(reaction, bot.user)


async def handle_options_reaction(bot:DiscordBot, interaction, reaction, recipe_info):
    print(reaction)
    output_path = f"{bot.paths['temp']}/recipes/{recipe_info['name']}.pdf"
    if str(reaction.emoji) == "💾":
        # handle save file
        save_pdf.create_recipe_doc(recipe_info, output_path)
        save_pdf.stamp_image_to_pdf(output_path, output_path, f"{bot.paths['cogs']}/sousChef/components/img/Logo1_printer.png")
        
        await interaction.user.send(file=nextcord.File(output_path))
        
    elif str(reaction.emoji) == "⭐":
        # handle rating
        pass
        
    elif str(reaction.emoji) == "♥️":
        # handle favorite
        pass