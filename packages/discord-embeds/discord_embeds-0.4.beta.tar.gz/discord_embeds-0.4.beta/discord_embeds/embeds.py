import discord

class emb:


	def confirmed(*, description):
		embed = discord.Embed(title = "**Успешно!**", description = description, colour = discord.Color.green())
		return embed

	def rejected(*, description):
		embed = discord.Embed(title = "**Отклонено!**", description = description, colour = discord.Color.red())
		return embed

	def error(*, reason):
		embed = discord.Embed(title = "**Ошибка!**", description = reason, colour = discord.Color.red())
		return embed