import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Easy Verify || use !help"))
    print('Bot is ready.')


@client.command(name="verification")
async def verification(ctx, verification_channel: discord.TextChannel, verification_role: discord.Role):
    # Make every channel private except for the verification channel
    for channel in ctx.guild.channels:
        if channel != verification_channel:
            await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        await channel.set_permissions(verification_role, read_messages=True)
    
    # Set verification channel permissions
    await verification_channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await verification_channel.set_permissions(verification_role, read_messages=True)

    # Send verification message and add reaction role
    verification_message = await verification_channel.send("React to get verified!")
    await verification_message.add_reaction("✅")
    
    def check(reaction, user):
        return user != client.user and str(reaction.emoji) == "✅" and reaction.message == verification_message

    while True:
        reaction, user = await client.wait_for('reaction_add', check=check)
        await user.add_roles(verification_role)
        await verification_channel.set_permissions(verification_role, read_messages=True)
        await verification_channel.set_permissions(ctx.guild.default_role, read_messages=False)


@client.command(name="invite")
async def invite(ctx):
    embed = discord.Embed(
        title="Bot Invite Link",
        description="[Click here to invite the bot to your server!](https://discord.com/api/oauth2/authorize?client_id=1087022739325468693&permissions=8&scope=bot%20applications.commands)",
        color=0x00ff00
    )
    await ctx.send(embed=embed)


@client.command(name="help")
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="Here are the commands for this bot:",
        color=0x00ff00
    )

    embed.add_field(
        name="!verification",
        value="Starts the verification process in the specified channel with the specified role."
    )

    embed.add_field(
        name="!invite",
        value="Returns the invite link for this bot."
    )

    await ctx.send(embed=embed)


client.run('token)
