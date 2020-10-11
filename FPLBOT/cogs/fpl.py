from discord.ext import commands
import discord
import requests,json
import aiohttp
import asyncio


class FPL_commands(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.FPL_URL = "https://fantasy.premierleague.com/api/"
        self.Fixture= "fixtures/?event="
        self.ALL = "bootstrap-static/"

        self.FPL_FIXTURES_DATA=self.FPL_URL+self.Fixture
        self.FPL_ALL_DATA=self.FPL_URL+self.ALL

        self.r=requests.get(self.FPL_ALL_DATA)
        self.response=self.r.json()

    @commands.command(name='fixtures',help=' :shows fixtures of the gameweek')
    async def fixtures(self,ctx,gameweek = 0):

        scores=[]

        try:
            session=aiohttp.ClientSession()
            await ctx.trigger_typing()
            if gameweek==0:
                temp=requests.get("https://fantasy.premierleague.com/api/entry/3604290/")
                temp=temp.json()
                gameweek=temp['current_event']
                gameweek=str(gameweek)
            URL=self.FPL_FIXTURES_DATA+str(gameweek)
            matchdata=requests.get(URL)
            fix=matchdata.json()
            for num in range(0,len(fix)):  
                hometeam=fix[num]['team_h']
                hometeam_score=fix[num]['team_h_score']
                for i in self.response['teams']:
                    if i['id']==hometeam:
                        hometeam_name=i['name']
    
                awayteam=fix[num]['team_a']
                awayteam_score=fix[num]['team_a_score']
                for i in self.response['teams']:
                    if i['id']==awayteam:
                        awayteam_name=i['name']
                msg='`'+hometeam_name+'`:**'+str(hometeam_score) +'** | '+ '`'+awayteam_name+'`:**'+str(awayteam_score)+'**'
                scores.append(msg)
            embedmsg = discord.Embed(title="Results",colour=discord.Colour.blue())
            count=0
            for i in scores:
                count=count+1
                val='Match '+str(count)
                embedmsg.add_field(name=val,value=i,inline=False)
            await session.close()
            await ctx.send(embed=embedmsg)
        except:
            await ctx.send('Something is wrong')
    

    
    @commands.command(name='teamfixtures',help=' :shows fixturers of the gameweek',aliases=['tf'])
    async def results_by_team(self,ctx,gameweek,*teamname):
        try:
            
            session=aiohttp.ClientSession()
            await ctx.trigger_typing()
            if gameweek=='0':
                temp=requests.get("https://fantasy.premierleague.com/api/entry/3604290/")
                temp=temp.json()
                gameweek=temp['current_event']
                gameweek=str(gameweek)
            
            
            URL=self.FPL_FIXTURES_DATA+str(gameweek)
            matchdata=requests.get(URL)
            fix=matchdata.json()

            teamname=" ".join(teamname[:])
            
            for i in self.response['teams']:
                if i['name']==teamname:
                    team_id=i['id']
            #score of match
            for num in range(0,len(fix)):
                if fix[num]['team_a']==team_id or fix[num]['team_h']==team_id:
                    matchid=fix[num]["id"]  #id of the particular match
                    awayteamid=fix[num]['team_a']
                    awayteam_score=fix[num]['team_a_score']
                    for i in self.response['teams']:
                        if i['id']==awayteamid:
                            awayteam_name=i['name']
                    hometeamid=fix[num]['team_h']
                    hometeam_score=fix[num]['team_h_score']
                    for i in self.response['teams']:
                        if i['id']==hometeamid:
                            hometeam_name=i['name']


            #stats of the match
            homescorers=[]
            awayscorers=[]

            homeassisters=[]
            awayassisters=[]

            homesavers=[]
            awaysavers=[]

            homeowngoals=[]
            awayowngoals=[]

            homeyellows=[]
            awayyellows=[]

            homereds=[]
            awayreds=[]

            homepenaltysaves=[]
            awaypenaltysaves=[]

            homepenaltymisses=[]
            awaypenaltymisses=[]

            homebonuses=[]
            awaybonuses=[]

            for num in range(0,len(fix)):
                if fix[num]['id']==matchid:
                    for stat in fix[num]["stats"]:  
                        if stat['identifier']=='goals_scored':  #goal scored stats
                            for homescorer in stat['h']:  #goal scorers of home team
                                homescorers.append(homescorer)
                            for awayscorer in stat['a']:   #goal scorers of away team
                                awayscorers.append(awayscorer)

                        if stat['identifier']=='assists':   #assists stats
                            for homeassister in stat['h']:  #assist players of home team
                                homeassisters.append(homeassister)
                            for awayassister in stat['a']:   #assist players of away team
                                awayassisters.append(awayassister)

                        if stat['identifier']=='saves':   #save stats
                            for homesave in stat['h']:     #saves for home team
                                homesavers.append(homesave)
                            for awaysave in stat['a']:     #saves for away team
                                awaysavers.append(awaysave)

                        if stat['identifier']=='own_goals':   #owngoal stats
                            for homeowngoal in stat['h']:     #owngoal for home team
                                homeowngoals.append(homeowngoal)
                            for awayowngoal in stat['a']:     #owngoal for away team
                                awayowngoals.append(awayowngoal)

                        if stat['identifier']=='yellow_cards':   #Yellow card stats
                            for homeyellow in stat['h']:     #Yellow card for home team
                                homeyellows.append(homeyellow)
                            for awayyellow in stat['a']:     #Yellow card for away team
                                awayyellows.append(awayyellow)
                        
                        if stat['identifier']=='red_cards':   #Red card stats
                            for homered in stat['h']:     #Red card for home team
                                homereds.append(homered)
                            for awayred in stat['a']:     #Red card for away team
                                awayreds.append(awayred)
                        
                        if stat['identifier']=='penalties_saved':   #Penalty save stats
                            for homepenaltysave in stat['h']:     #Penalty save for home team
                                homepenaltysaves.append(homepenaltysave)
                            for awaypenaltysave in stat['a']:     #penalty save for away team
                                awaypenaltysaves.append(awaypenaltysave)

                        if stat['identifier']=='penalties_missed':   #Penalty miss  stats
                            for homepenaltymiss in stat['h']:     #Penalty missf or home team
                                homepenaltymisses.append(homepenaltymiss)
                            for awaypenaltymiss in stat['a']:     #Penalty miss for away team
                                awaypenaltymisses.append(awaypenaltymiss)
                        if stat['identifier']=='bonus':   #bonus stats
                            for homebonus in stat['h']:     #bonus for home team
                                homebonuses.append(homebonus)
                            for awaybonus in stat['a']:     #bonus for away team
                                awaybonuses.append(awaybonus)
                            
            #for home team
                #for goals
            home_scorer_ids=[i['element'] for i in homescorers]
            home_scorer_values=[i['value'] for i in homescorers]
            homescorer_webnames=[]

            for player in home_scorer_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homescorer_webnames.append(i['web_name'])
                #for assists
            home_assist_ids=[i['element'] for i in homeassisters]
            home_assist_values=[i['value'] for i in homeassisters]
            homeassist_webnames=[]
            for player in home_assist_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homeassist_webnames.append(i['web_name'])

                #for saves
            home_save_ids=[i['element'] for i in homesavers]
            home_save_values=[i['value'] for i in homesavers]
            homesaver_webnames=[]
            for player in home_save_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homesaver_webnames.append(i['web_name'])

                #for owngoals
            home_og_ids=[i['element'] for i in homeowngoals]
            home_og_values=[i['value'] for i in homeowngoals]
            homeog_webnames=[]
            for player in home_og_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homeog_webnames.append(i['web_name'])

                #for Yellow cards
            home_yellow_ids=[i['element'] for i in homeyellows]
            home_yellow_values=[i['value'] for i in homeyellows]
            homeyellow_webnames=[]
            for player in home_yellow_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homeyellow_webnames.append(i['web_name'])
            
                #for Red cards
            home_red_ids=[i['element'] for i in homereds]
            home_red_values=[i['value'] for i in homereds]
            homered_webnames=[]
            for player in home_red_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homered_webnames.append(i['web_name'])
                #for penalty saves
            home_penaltysave_ids=[i['element'] for i in homepenaltysaves]
            home_penaltysave_values=[i['value'] for i in homepenaltysaves]
            homepenaltysave_webnames=[]
            for player in home_penaltysave_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homepenaltysave_webnames.append(i['web_name'])
                #for penalty miss
            home_penaltymiss_ids=[i['element'] for i in homepenaltymisses]
            home_penaltymiss_values=[i['value'] for i in homepenaltymisses]
            homepenaltymiss_webnames=[]
            for player in home_penaltymiss_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homepenaltymiss_webnames.append(i['web_name'])
                #for bonus points
            home_bonus_ids=[i['element'] for i in homebonuses]
            home_bonus_values=[i['value'] for i in homebonuses]
            homebonus_webnames=[]
            for player in home_bonus_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        homebonus_webnames.append(i['web_name'])
            
            #for away team
                #for goals
            away_scorer_ids=[i['element'] for i in awayscorers]
            away_scorer_values=[i['value'] for i in awayscorers]
            awayscorer_webnames=[]
            for player in away_scorer_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awayscorer_webnames.append(i['web_name'])

                #for assists
            away_assist_ids=[i['element'] for i in awayassisters]
            away_assist_values=[i['value'] for i in awayassisters]
            awayassist_webnames=[]
            for player in away_assist_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awayassist_webnames.append(i['web_name'])
                #for saves
            away_save_ids=[i['element'] for i in awaysavers]
            away_save_values=[i['value'] for i in awaysavers]
            awaysaver_webnames=[]
            for player in away_save_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awaysaver_webnames.append(i['web_name'])
                #for owngoals
            away_og_ids=[i['element'] for i in awayowngoals]
            away_og_values=[i['value'] for i in awayowngoals]
            awayog_webnames=[]
            for player in away_og_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awayog_webnames.append(i['web_name'])
                #for Yellow cards
            away_yellow_ids=[i['element'] for i in awayyellows]
            away_yellow_values=[i['value'] for i in awayyellows]
            awayyellow_webnames=[]
            for player in away_yellow_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awayyellow_webnames.append(i['web_name'])
        
                #for Red cards
            away_red_ids=[i['element'] for i in awayreds]
            away_red_values=[i['value'] for i in awayreds]
            awayred_webnames=[]
            for player in away_red_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awayred_webnames.append(i['web_name'])

                #for penalty saves
            away_penaltysave_ids=[i['element'] for i in awaypenaltysaves]
            away_penaltysave_values=[i['value'] for i in awaypenaltysaves]
            awaypenaltysave_webnames=[]
            for player in away_penaltysave_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awaypenaltysave_webnames.append(i['web_name'])
                #for penalty miss
            away_penaltymiss_ids=[i['element'] for i in awaypenaltymisses]
            away_penaltymiss_values=[i['value'] for i in awaypenaltymisses]
            awaypenaltymiss_webnames=[]
            for player in away_penaltymiss_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awaypenaltymiss_webnames.append(i['web_name'])
                #for bonus points
            away_bonus_ids=[i['element'] for i in awaybonuses]
            away_bonus_values=[i['value'] for i in awaybonuses]
            awaybonus_webnames=[]
            for player in away_bonus_ids:
                for i in self.response['elements']:
                    if i['id']==player:
                        awaybonus_webnames.append(i['web_name'])
            
            embedmsg = discord.Embed(title=teamname+' Gameweek '+gameweek,colour=discord.Colour.blue())
            #score display
            score=hometeam_name+':'+str(hometeam_score) +' | '+ awayteam_name+':'+str(awayteam_score)
            embedmsg.add_field(name='Score',value=score,inline=False)
            #hometeam stats display
            
            count=0
            home_finalgoalscore=''
            for player in homescorer_webnames:
                msg=player+' : '+str(home_scorer_values[count])+'\n'
                home_finalgoalscore=home_finalgoalscore+msg
                count=count+1
            home_finalgoalscore='\n'+'**`Goals`**'+'\n'+home_finalgoalscore
            
            count=0
            home_finalassist=''
            for player in homeassist_webnames:
                msg=player+' : '+str(home_assist_values[count])+'\n'
                home_finalassist=home_finalassist+msg
                count=count+1
            home_finalassist='\n**`Assist`**\n'+home_finalassist
            
            count=0
            home_finalsave=''
            for player in homesaver_webnames:
                msg=player+' : '+str(home_save_values[count])+'\n'
                home_finalsave=home_finalsave+msg
                count=count+1
            home_finalsave='\n**`Saves`**\n'+home_finalsave
            
            count=0
            home_finalog=''
            for player in homeog_webnames:
                msg=player+' : '+str(home_og_values[count])+'\n'
                home_finalog=home_finalog+msg
                count=count+1
            home_finalog='\n**`OwnGoals`**\n'+home_finalog
            
            count=0
            home_finalyc=''
            for player in homeyellow_webnames:
                msg=player+' : '+str(home_yellow_values[count])+'\n'
                home_finalyc=home_finalyc+msg
                count=count+1
            home_finalyc='\n**`Yellow cards`**\n'+home_finalyc

            count=0
            home_finalrc=''
            for player in homered_webnames:
                msg=player+' : '+str(home_red_values[count])+'\n'
                home_finalrc=home_finalrc+msg
                count=count+1
            home_finalrc='\n**`Red cards`**\n'+home_finalrc
          
            count=0
            home_finalps=''
            for player in homepenaltysave_webnames:
                msg=player+' : '+str(home_penaltysave_values[count])+'\n'
                home_finalps=home_finalps+msg
                count=count+1
            home_finalps='\n**`Penalty Saves`**\n'+home_finalps
            
            
            count=0
            home_finalpm=''
            for player in homepenaltymiss_webnames:
                msg=player+' : '+str(home_penaltymiss_values[count])+'\n'
                home_finalpm=home_finalpm+msg
                count=count+1
            home_finalpm='\n**`Penalty Miss`**\n'+home_finalpm
            
            
            count=0
            home_finalbp=''
            for player in homebonus_webnames:
                msg=player+' : '+str(home_bonus_values[count])+'\n'
                home_finalbp=home_finalbp+msg
                count=count+1
            home_finalbp='\n**`Bonus Points`**\n'+home_finalbp

            homefinalmsg=home_finalgoalscore+home_finalassist+home_finalsave+home_finalog+home_finalyc+home_finalrc+home_finalps+home_finalpm+home_finalbp
            embedmsg.add_field(name=hometeam_name,value=homefinalmsg,inline=False)

                
            #awayteam stats display
            
            count=0
            away_finalgoalscore=''
            for player in awayscorer_webnames:
                msg=player+' : '+str(away_scorer_values[count])+'\n'
                away_finalgoalscore=away_finalgoalscore+msg
                count=count+1
            away_finalgoalscore='\n**`Goals`**\n'+away_finalgoalscore
            
            count=0
            awayfinalassist=''
            for player in awayassist_webnames:
                msg=player+' : '+str(away_assist_values[count])+'\n'
                awayfinalassist=awayfinalassist+msg
                count=count+1
            awayfinalassist='\n**`Assists`**\n'+awayfinalassist
            
            count=0
            awaysaves=''
            for player in awaysaver_webnames:
                msg=player+' : '+str(away_save_values[count])+'\n'
                awaysaves=awaysaves+msg
                count=count+1
            awaysaves='\n**`Saves`**\n'+awaysaves
            
            count=0
            awayog=''
            for player in awayog_webnames:
                msg=player+' : '+str(away_og_values[count])+'\n'
                awayog=awayog+msg
                count=count+1
            awayog='\n**`Own Goals`**\n'+awayog
            
            count=0
            awayyc=''
            for player in awayyellow_webnames:
                msg=player+':'+str(away_yellow_values[count])+'\n'
                awayyc=awayyc+msg
                count=count+1
            awayyc='\n**`Yellow Cards`**\n'+awayyc
            
            count=0
            awayrc=''
            for player in awayred_webnames:
                msg=player+' : '+str(away_red_values[count])+'\n'
                awayrc=awayrc+msg
                count=count+1
            awayrc='\n**`Red Cards`**\n'+awayrc
            
            count=0
            awayps=''
            for player in awaypenaltysave_webnames:
                msg=player+' : '+str(away_penaltysave_values[count])+'\n'
                awayps=awayps+msg
                count=count+1
            awayps='\n**`Penalty Saves`**\n'+awayps
            
            count=0
            awaypm=''
            for player in awaypenaltymiss_webnames:
                msg=player+' : '+str(away_penaltymiss_values[count])+'\n'
                awaypm=awaypm+msg
                count=count+1
            awaypm='\n**`Penalty Misses`**\n'+awaypm
            
            count=0
            awaybp=''
            for player in awaybonus_webnames:
                msg=player+' : '+str(away_bonus_values[count])+'\n'
                awaybp=awaybp+msg
                count=count+1
            awaybp='\n**`Bonus Points`**\n'+awaybp

            awayfinalmsg=away_finalgoalscore+awayfinalassist+awaysaves+awayog+awayyc+awayrc+awayps+awaypm+awaybp
            embedmsg.add_field(name=awayteam_name,value=awayfinalmsg,inline=False)
            
            await session.close()
            # await ctx.send('Something is right')
            await ctx.send(embed=embedmsg)
        except:
            await ctx.send('Something is wrong')
    
    @commands.command(name='pstats',help=' :shows fantasy player data',aliases=['ps'])
    async def getplayerdata(self,ctx,playercode):
        try:
            session=aiohttp.ClientSession()
            await ctx.trigger_typing()
            URL=self.FPL_URL+'entry/'+str(playercode)+'/'
            r=requests.get(URL)
            playerdata=r.json()

            player_name=playerdata['player_first_name']+' '+playerdata['player_last_name']
            player_region=playerdata['player_region_name']
            player_total_points=playerdata['summary_overall_points']
            player_overall_global_rank=playerdata['summary_overall_rank']

            
            
            finalmsg=''
            for league in playerdata['leagues']['classic']:
                seperator='---------------------\n'
                leaguename=league['name']+'\n'
                rank='Rank: '+str(league['entry_rank'])+'\n'
                lastrank='Last Rank: '+str(league['entry_last_rank'])+'\n'
                msg=seperator+leaguename+rank+lastrank
                finalmsg=finalmsg+msg
            
            embedmsg = discord.Embed(title="Fantasy Player Data",colour=discord.Colour.blue())
            embedmsg.add_field(name='Name',value=player_name,inline=False)
            embedmsg.add_field(name='Region',value=player_region,inline=False)
            embedmsg.add_field(name='Total Points',value=player_total_points,inline=False)
            embedmsg.add_field(name='Global rank',value=player_overall_global_rank,inline=False)
            embedmsg.add_field(name='Classic Leagues',value=finalmsg,inline=False)
            await session.close()
            await ctx.send(embed=embedmsg)
        except:
            await ctx.send('something is wrong')

    
    @commands.command(name='gwpoints',help=' :shows point of the gameweek',aliases=['gp'])
    async def getplayer_gameweek_data(self,ctx,playercode,gameweek=0):
        try:
            session=aiohttp.ClientSession()
            await ctx.trigger_typing()
            if gameweek==0:
                temp=requests.get("https://fantasy.premierleague.com/api/entry/3604290/")
                temp=temp.json()
                gameweek=temp['current_event']
                gameweek=str(gameweek)
            
            URL=self.FPL_URL+'entry/'+str(playercode)+'/event/'+str(gameweek)+'/picks/'
            r=requests.get(URL)
            response=r.json()

            squadvalue=response['entry_history']['value']/10
            bankvalue=response['entry_history']['bank']/10

            picks=[]
            for i in range (0,len(response['picks'])):
                picks.append(response['picks'][i]['element'])

            
            URL=self.FPL_URL+'event/'+str(gameweek)+'/live/'
            r=requests.get(URL)
            response2=r.json()

            r=requests.get(self.FPL_ALL_DATA)
            response3=r.json()

            webnames={}
            playerstats={}
            finalstats={}

            for i in range (0,len(response2['elements'])):
                for playerid in picks:
                    if response2['elements'][i]['id']==playerid:
                        for a in response3['elements']:
                            if a["id"]==playerid:
                                webnames[a['id']]=a['web_name']

                        playerstats[playerid]=response2['elements'][i]['stats']

            for key,value in webnames.items():
                for key2,value2 in playerstats.items():
                        if key==key2:
                            finalstats[value]=value2

            embedmsg1 = discord.Embed(title='Gameweek '+str(gameweek),colour=discord.Colour.blue())
            point='Points: '+str(response['entry_history']['points'])+'\n'
            pointonbench='Points on Bench: '+str(response['entry_history']['points_on_bench'])+'\n'
            rank='GameweekRank: '+str(response['entry_history']['rank'])+'\n'
            # squadvalue='Squad Value: '+str(squadvalue)+'\n'
            # bank='Bank: '+str(bankvalue)+'\n'
            tmade='Transfers made: '+str(response['entry_history']['event_transfers'])+'\n'
            tcost='Transfers cost: '+str(response['entry_history']['event_transfers_cost'])+'\n'
            firstsection=point+pointonbench+rank+tmade+tcost
            embedmsg1.add_field(name='Overview',value=firstsection,inline=False)

            embedmsg2 = discord.Embed(title='Picks for gameweek '+str(gameweek),colour=discord.Colour.blue())
            secondsection=''
            for a in finalstats:
                name='`'+a+'`'+'\n'
                point='**Total Points: `'+str(finalstats[a]['total_points'])+'`**\n'
                minp='Minutes Played: '+str(finalstats[a]['minutes'])+'\n'
                gs='**Goal Scored: '+str(finalstats[a]['goals_scored'])+'**\n'
                asssist_made='**Assist: '+str(finalstats[a]['assists'])+'**\n'
                yc='Yellow_cards: '+str(finalstats[a]['yellow_cards'])+'\n'
                rc='Red cards: '+str(finalstats[a]['red_cards'])+'\n'
                saves='Baves: '+str(finalstats[a]['saves'])+'\n'
                bonus='Bonus: '+str(finalstats[a]['bonus'])+'\n'
                # indt='\tin_dreamteam: '+str(finalstats[a]['in_dreamteam'])+'\n'
                temp=name+point+minp+gs+asssist_made+yc+rc+saves+bonus
                secondsection=secondsection+temp
            res_first, res_second = secondsection[:len(secondsection)//2],secondsection[len(secondsection)//2:] 
            
            embedmsg2.add_field(name='Picks',value=res_first,inline=False)
            embedmsg2.add_field(name='Picks contd..',value=res_second,inline=False)
            await session.close()
            await ctx.send(embed=embedmsg1)
            await ctx.send(embed=embedmsg2)


        except:
            await ctx.send('Something wrong')

def setup(bot):
    bot.add_cog(FPL_commands(bot))
