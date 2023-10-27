from nextcord import Color


def heat_color_scale(idx:int) -> Color:
    heat_scale = [
        Color.dark_grey(),
        Color.dark_blue(),
        Color.blue(),
        Color.teal(),
        Color.dark_green(),
        Color.green(),
        Color.yellow(),
        Color.orange(),
        Color.dark_orange(),
        Color.red(),
        Color.dark_red()
    ]
    if idx == None:
        return 0
    
    if idx > len(heat_scale) - 1:
        idx = 10
    elif idx < 0:
        idx = 0

    return heat_scale[idx]