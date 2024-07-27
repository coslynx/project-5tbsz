import discord

def create_embed(title, description, fields=None):
    """Creates a Discord embed object with the given title, description, and optional fields.

    Args:
        title (str): The title of the embed.
        description (str): The description of the embed.
        fields (list[dict], optional): A list of field dictionaries. 
            Each dictionary should have the following keys:
                - name (str): The name of the field.
                - value (str): The value of the field.
                - inline (bool, optional): Whether the field should be inline. Defaults to False.

    Returns:
        discord.Embed: The created embed object.
    """
    embed = discord.Embed(title=title, description=description)
    if fields:
        for field in fields:
            embed.add_field(name=field['name'], value=field['value'], inline=field.get('inline', False))
    return embed

def format_timestamp(timestamp):
    """Formats a timestamp into a human-readable string.

    Args:
        timestamp (datetime.datetime): The timestamp to format.

    Returns:
        str: The formatted timestamp string.
    """
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def get_user_from_mention(mention):
    """Gets a user object from a mention in a message.

    Args:
        mention (str): The mention string.

    Returns:
        discord.Member: The user object, or None if the mention is invalid.
    """
    try:
        user_id = int(mention.replace("<@!", "").replace(">", ""))
        return discord.utils.get(mention.guild.members, id=user_id)
    except ValueError:
        return None

def get_user_from_id(user_id):
    """Gets a user object from a user ID.

    Args:
        user_id (int): The user ID.

    Returns:
        discord.Member: The user object, or None if the user is not found.
    """
    return discord.utils.get(mention.guild.members, id=user_id)

def get_server_from_id(server_id):
    """Gets a server object from a server ID.

    Args:
        server_id (int): The server ID.

    Returns:
        discord.Guild: The server object, or None if the server is not found.
    """
    return discord.utils.get(bot.guilds, id=server_id)