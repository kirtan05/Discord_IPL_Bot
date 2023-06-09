import discord
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from tabulate import tabulate
#from IPython.display import HTML
import pandas as pd
#from sklearn.datasets import load_iris
import requests
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
#from table2ascii import table2ascii as t2a, PresetStyle
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
bot = discord.Client()
#print(DISCORD_TOKEN)
def convert(s):
    new = ""
    for x in s:
        new += x 
    return new
def convertx(s):
    new = ""
    for x in s[1:]:
        new += x 
    return new
def converted(s):
    new=""
    for x in range(len(s)-1):
        new+=s[x]
    return new
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
@bot.event
async def on_message(message):
    if message.author == bot.user:
            return
    elif message.content.startswith('$ipl points table') or message.content.startswith('$ipl pt'):
        raw= requests.get('https://ipl-stats-sports-mechanic.s3.ap-south-1.amazonaws.com/ipl/feeds/stats/60-groupstandings.js')
        soup = bs(raw.content, 'html.parser')
        txt = raw.text
        status = raw.status_code
        count1=txt.count("TeamName")
        substr="TeamName"
        indix=[]
        indix2=[]
        indix3=[]
        notded=1
        teams=[]
        nrr=[]
        points=[]
        sno=[]
        #GET THE TEAM NAMES
        for i in range(len(txt)):
          if txt.startswith(substr, i):
            indix.append(i)
        for i in indix:
          templ=[]
          for i in range(i+11,i+50):
            
            if txt[i]!='"':
              templ.append(txt[i])
            else:
              teams.append(convert(templ))
              break
        #GET THE NRR
        for i in range(len(txt)):
          if txt.startswith("NetRunRate", i):
            indix2.append(i)
        for i in indix2:
          templ=[]
          for i in range(i+13,i+20):
            
            if txt[i]!='"':
              templ.append(txt[i])
            else:
              nrr.append(convert(templ))
              break
        #GET THE POINTS
        for i in range(len(txt)):
          if txt.startswith("Points", i):
            indix3.append(i)
        for i in indix3:
          templ=[]
          for i in range(i+9,i+12):
            
            if txt[i]!='"':
              templ.append(txt[i])
            else:
              points.append(convert(templ))
              break
        for i in range(10):
          sno.append(i+1)
        table=pd.DataFrame(columns=['SNo','Team Name','NRR','Points'])
        for i in range(10):
          xx=sno[i]
          yy=teams[i]
          zz=nrr[i]
          zzz=points[i]
          table.loc[len(table.index)]=[xx,yy,zz,zzz]
        blankIndex=[''] * len(table)
        table.index=blankIndex
        table.style.set_properties(**{'text-align': 'right'})
        
        await message.channel.send('`'+tabulate(table, showindex=False, headers=table.columns)+'`')


  
    elif message.content.startswith('$ipl orange cap') or message.content.startswith('$ipl oc'):
        indi=[]
        indi2=[]
        team=[]
        name2=[]
        name=[]
        matches=[]
        sirat=[]
        runss=[]
        sizeoftn=[]
        import urllib.request, urllib.error, urllib.parse
        url = 'https://www.sportskeeda.com/go/ipl/orange-cap?ref=carousel'
        response = urllib.request.urlopen(url)
        webc = response.read()
        webc="".join(map(chr, webc))
        #GET THE NAMES
        for i in range(len(webc)):
            if webc.startswith('<a href="/player/',i):
                indi.append(i)
        for i in indi:
            i=i+20
            found=0
            flag=1
            templ=[]
            for i in range(i,i+30):
                if(webc[i]=='>'):
                    found=1
                if(webc[i]=='<'):
                   flag=0
                if(found+flag==2):
                    templ.append(webc[i])
                if(flag==0):
                    name.append(convertx(templ))
                    break
        #GET THE TEAMS
        for i in range(len(webc)):
            if webc.startswith('<a href="/team/',i):
                indi2.append(i)
        for i in indi2:
            i=i+20
            found=0
            flag=1
            templ=[]
            for i in range(i,i+55):
                if(webc[i]=='>'):
                    found=1
                if(webc[i]=='<'):
                   flag=0
                if(found+flag==2):
                    templ.append(webc[i])
                if(flag==0):
                    sizeoftn.append(len(templ)-1)
                    team.append(convertx(templ))
                    break
        #GET THE MATCHES PLAYED
        for i in range(10):
            indi2[i]+=139
            indi2[i]=indi2[i]+sizeoftn[i]+sizeoftn[i]+sizeoftn[i]
        for i in indi2:
            templ=[]
            flag=1
            for i in range(i,i+12):
                #print(webc[i],end="")
                if(webc[i] >= '0' and webc[i] <= '9'):
                    templ.append(webc[i])
                    matches.append(convert(templ))
                    break
        #GET THE RUNS SCORED
        for i in indi2:
            templ=[]
            i=i+105
            for i in range(i+8,i+19):
                if(webc[i] >= '0' and webc[i] <= '9'):
                    templ.append(webc[i])
            runss.append(convert(templ))
                
        #GET THE STRIKE RATE
        for i in range(10):
            indi2[i]=indi2[i]+140
            x=indi2[i]
        
        for i in indi2:
            templ=[]
            for i in range(i,i+20):
                if((webc[i] >= '0' and webc[i] <= '9') or webc[i]=='.'):
                    templ.append(webc[i])
            sirat.append(convert(templ))
        purple=pd.DataFrame(columns=['SNo','Player Name','Team','No Of Matches','Runs Scored','Strike Rate'])
        snoo=[]
        for i in range(10):
          snoo.append(i+1)
        for i in name:
            name2.append(converted(i))
                
        for i in range(10):
          purple.loc[len(purple.index)]=[snoo[i],name2[i],team[i],matches[i],runss[i],sirat[i]]
        blankIndex=[''] * len(purple)
        purple.index=blankIndex
        await message.channel.send('`'+tabulate(purple, showindex=False, headers=purple.columns)+'`')





  
    elif message.content.startswith('$ipl purple cap') or message.content.startswith('$ipl pc'):  
        indi=[]
        indi2=[]
        team=[]
        name2=[]
        name=[]
        matches=[]
        sirat=[]
        runss=[]
        sizeoftn=[]
        import urllib.request, urllib.error, urllib.parse
        url = 'https://www.sportskeeda.com/go/ipl/purple-cap?ref=carousel'
        response = urllib.request.urlopen(url)
        webc = response.read()
        webc="".join(map(chr, webc))
        #GET THE NAMES
        for i in range(len(webc)):
            if webc.startswith('<a href="/player/',i):
                indi.append(i)
        for i in indi:
            i=i+20
            found=0
            flag=1
            templ=[]
            for i in range(i,i+50):
                if(webc[i]=='>'):
                    found=1
                if(webc[i]=='<'):
                   flag=0
                if(found+flag==2):
                    templ.append(webc[i])
                if(flag==0):
                    name.append(convertx(templ))
                    break
        #GET THE TEAMS
        for i in range(len(webc)):
            if webc.startswith('<a href="/team/',i):
                indi2.append(i)
        for i in indi2:
            i=i+20
            found=0
            flag=1
            templ=[]
            for i in range(i,i+55):
                if(webc[i]=='>'):
                    found=1
                if(webc[i]=='<'):
                   flag=0
                if(found+flag==2):
                    templ.append(webc[i])
                if(flag==0):
                    sizeoftn.append(len(templ)-1)
                    team.append(convertx(templ))
                    break
        #GET THE MATCHES PLAYED
        for i in range(10):
            indi2[i]+=139
            indi2[i]=indi2[i]+sizeoftn[i]+sizeoftn[i]+sizeoftn[i]
        for i in indi2:
            templ=[]
            flag=1
            for i in range(i,i+12):
                #print(webc[i],end="")
                if(webc[i] >= '0' and webc[i] <= '9'):
                    templ.append(webc[i])
                    matches.append(convert(templ))
                    break
        #GET THE RUNS SCORED
        for i in indi2:
            templ=[]
            i=i+105
            for i in range(i+8,i+19):
                if(webc[i] >= '0' and webc[i] <= '9'):
                    templ.append(webc[i])
            runss.append(convert(templ))
                
        #GET THE STRIKE RATE
        for i in range(10):
            indi2[i]=indi2[i]+170
            x=indi2[i]
            #print(webc[x-5:x+10])
        
        for i in indi2:
            templ=[]
            for i in range(i+20,i+36):
                print(webc[i],end="")
                if(webc[i]=='.'):
                    templ.append(webc[i-1:i+3])
            sirat.append(convert(templ))
        purple=pd.DataFrame(columns=['SNo','Player Name','Team','No Of Matches','Wickets Taken','Economy'])
        snoo=[]
        for i in range(10):
          snoo.append(i+1)
        for i in name:
            name2.append(converted(i))
               
        for i in range(10):
          purple.loc[len(purple.index)]=[snoo[i],name2[i],team[i],matches[i],runss[i],sirat[i]]
        blankIndex=[''] * len(purple)
        purple.index=blankIndex
        await message.channel.send('`'+tabulate(purple, showindex=False, headers=purple.columns)+'`')   
                



# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.

      
    elif message.content.startswith('$ipl live') or message.content.startswith('$ipl l'):
        import urllib.request, urllib.error, urllib.parse
        url = 'https://www.sportskeeda.com/go/ipl?ref=homepage&page=1'
        response = urllib.request.urlopen(url)
        webc = response.read()
        webc="".join(map(chr, webc))
        raw= requests.get('https://www.sportskeeda.com/go/ipl?ref=homepage&page=1')
        soup = bs(raw.content, 'html.parser')
        txt = raw.text
        status = raw.status_code
        indi=0
        live=[]
        scores=[]
        for i in       range(len(txt)):
            if txt.startswith('<div class="keeda_widget_live_info">LIVE</div>',i):
                indi=i
                break
        #print(txt[indi+52:indi+150])
        templ=[]
        for i in range(indi+53,indi+150):
            if txt[i]!='<':
              templ.append(txt[i])
              #print(txt[i],end="")
            else:
              live.append(convert(templ))
              break 
        for i in range(len(txt)):
            templ=[]
            if txt.startswith('<span class="keeda_widget_score cricket">',i):
                #print(txt[i+41:i+57])
                for i in range(i+41,i+57):
                    #print(txt[i],end="")
                    if txt[i]=='<':
                      scores.append(convert(templ))
                      break
                    templ.append(txt[i])
        scorex=[]
        scorea=scores
        #print(len(scores))
        scoreb = [i for i in scorea if i]
        if(len(scoreb)%2==0):
            scorex.append(scoreb[len(scoreb)-1])
            scorex.append(scoreb[len(scoreb)-1])
        else:
            scorex.append(scoreb[len(scoreb)-1])
        templ=[]
        play=[]
        teams=[]
        #print(txt[indi-310:indi-288])
        #for i in scoreb:
            #print(i)
        rt=len(scoreb)
        #print(txt[indi-612:indi-607])
        for i in range(len(txt)):
            templ=[]
            if txt.startswith('<div class="keeda_widget_team" data-team-name="',i):
                for i in range(i+47,i+52):
                    if txt[i]!='"':
                      templ.append(txt[i])
                    else:
                      teams.append(convert(templ))
                      break
        templ=[]
        for i in range(indi-305,indi-297):
            if txt[i]!='"':
              templ.append(txt[i])
              #print(txt[i],end="")
            else:
              play.append(convert(templ))
              break 
        #print(play[0])
        matchup=teams[rt]+"               vs         "+teams[rt+1]
        #print(matchup)
        #print(len(scorex))
        if(len(scorex)%2==1):
            scorebo=scoreb[rt-1]
        else:
            scorebo=scoreb[rt-1]+"              "+scoreb[rt-1]
        print(scorebo)
        print(*scoreb)
        await message.channel.send('```'+"Latest Match"+"\n"+matchup+"\n"+scorebo+'```')
keep_alive()
bot.run(DISCORD_TOKEN)
  
    
    
