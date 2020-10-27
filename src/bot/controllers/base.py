class Controller:
    
    @staticmethod
    async def send_embed_message(ctx, embed):
        return await ctx.message.channel.send(embed=embed)