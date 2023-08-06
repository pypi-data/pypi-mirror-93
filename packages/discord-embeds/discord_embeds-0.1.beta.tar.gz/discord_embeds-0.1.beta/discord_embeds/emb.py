import discord

class emb:


	def confirmed(*, description):
		embed = discord.Embed(title = "**Успешно!**", description = description, colour = discord.Color.green())
		return embed