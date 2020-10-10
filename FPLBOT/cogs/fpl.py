from discord.ext import commands
import discord
import requests,json
import aiohttp
import asyncio

class FPL_commands(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    
    @commands.command(name='fixtures',help=' :shows fixturers of the gameweek')
    async def fixtures(self,ctx,gameweek = 1):
        FPL_URL = "https://fantasy.premierleague.com/api/"
        Fixture= "fixtures/?event="
        ALL = "bootstrap-static/"

        FPL_FIXTURES_DATA=FPL_URL+Fixture
        FPL_ALL_DATA=FPL_URL+ALL
        r=requests.get(FPL_ALL_DATA)
        response=r.json()

        scores=[]

        try:
            session=aiohttp.ClientSession()
            await ctx.trigger_typing()
            URL=FPL_FIXTURES_DATA+str(gameweek)
            matchdata=requests.get(URL)
            fix=matchdata.json()
            for num in range(0,len(fix)):  
                hometeam=fix[num]['team_h']
                hometeam_score=fix[num]['team_h_score']
                for i in response['teams']:
                    if i['id']==hometeam:
                        hometeam_name=i['name']
    
                awayteam=fix[num]['team_a']
                awayteam_score=fix[num]['team_a_score']
                for i in response['teams']:
                    if i['id']==awayteam:
                        awayteam_name=i['name']
                msg=hometeam_name+':'+str(hometeam_score) +' | '+ awayteam_name+':'+str(awayteam_score)
                scores.append(msg)
            embedmsg = discord.Embed(title="Results",colour=discord.Colour.blue())
            count=0
            for i in scores:
                count=count+1
                embedmsg.add_field(name=count,value=i,inline=True)
            await session.close()
            await ctx.send(embed=embedmsg)
        except:
            await ctx.send('Something is wrong')
def setup(bot):
    bot.add_cog(FPL_commands(bot))
