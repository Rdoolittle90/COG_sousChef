from nextcord import Embed
import json

from . import colors
from src.bot import DiscordBot


def get_spice_meter_img()->dict:
    with open(f"{DiscordBot.paths['cogs']}/sousChef/components/img/spice_meter/spice_meter.json", "r") as fin:
        return json.load(fin)


class RecipeEmbedding:
    spice_meter = get_spice_meter_img()

    def create_embeds(self, name, recipe_info:dict=None) -> Embed:

        ingredients = "\n".join(recipe_info["ingredients"])
        instructions = "\n".join(recipe_info["instructions"])
        
        r_embed = Embed(title=f"Recipe for {name}", description=recipe_info["description"], color=colors.heat_color_scale(recipe_info["spice"]))
        r_embed.add_field(name="Ingredients", value=ingredients, inline=False)
        r_embed.set_thumbnail(url=self.spice_meter[f"spice_meter_{recipe_info['spice']}"])

        if len(instructions) > 1000:
            instructions = instructions[:1000] + "\n\nOUTPUT TOO LONG\n..."
        i_embed = Embed(title=f"{name}", color=colors.heat_color_scale(recipe_info["spice"]))
        i_embed.add_field(name="The Instructions", value=instructions, inline=False)
        i_embed.set_footer(text="CREATED BY AI - click the reaction below to save a pdf")


        return r_embed, i_embed
