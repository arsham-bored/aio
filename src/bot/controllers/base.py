class Controller:
    
    @staticmethod
    async def send_embed_message(ctx, embed):
        return await ctx.message.channel.send(embed=embed)

    @staticmethod
    def is_same_message(user, ctx):
        return user == ctx.author