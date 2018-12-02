# -*- coding: utf-8 -*-
import pycurl
import re
import io
import time
from html.parser import HTMLParser



def Curl(url):
    c = pycurl.Curl()
    c.setopt(pycurl.URL,url)
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36")
    c.setopt(pycurl.CUSTOMREQUEST,"GET")
    c.setopt(pycurl.TIMEOUT, 1000)
    body = io.BytesIO()
    c.setopt(pycurl.WRITEFUNCTION, body.write)
    c.perform()
    html = body.getvalue()
    result=str(html,encoding = "utf8")
    return result

def Curl_Post(url,data):
    c = pycurl.Curl()
    c.setopt(pycurl.URL,url)
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36")
    c.setopt(pycurl.CUSTOMREQUEST,"POST")
    c.setopt(pycurl.POSTFIELDS,  data)
    c.setopt(pycurl.TIMEOUT, 1000)
    body = io.BytesIO()
    c.setopt(pycurl.WRITEFUNCTION, body.write)
    c.perform()
    html = body.getvalue()
    result=str(html,encoding = "utf8")
    return result

def Curl_Auth(url):
    c = pycurl.Curl()
    c.setopt(pycurl.URL,url)
    c.setopt(pycurl.USERAGENT,"Mozilla/5.0 (Linux; U; Android 7.1.2; zh-Hans-CN; ONEPLUS A5010 Build/NJH47F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 Quark/2.4.2.986 Mobile Safari/537.36")
    c.setopt(pycurl.CUSTOMREQUEST,"GET")
    c.setopt(pycurl.HTTPHEADER,['Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwY2Q0YzhjMC01ZTVhLTAxMzYtOTQ3YS0wYTU4NjQ2MTRkYjUiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTMwMzM4OTU5LCJwdWIiOiJzZW1jIiwidGl0bGUiOiJ2YWluZ2xvcnkiLCJhcHAiOiJ2Z19xcV9ib3QiLCJzY29wZSI6ImNvbW11bml0eSIsImxpbWl0IjoxMH0.iR6ZXgiFlt9pRcHsjnlw0F-It_nl9lVTzXbAit02sNs','Accept: application/vnd.api+json'])
    body = io.BytesIO()
    c.setopt(pycurl.WRITEFUNCTION, body.write)
    c.perform()
    html = body.getvalue()
    result=str(html,encoding = "utf8")
    return result

def Write_Time_Log():
    path = r'/storage/emulated/0/.qqbot-tmp/message_time.log'
    file_name = open(path,'w',encoding='utf-8')
    file_name.write(str(int(time.time())))
    file_name.close()

def Read_Time_Log():
    path = r'/storage/emulated/0/.qqbot-tmp/message_time.log'
    file_name = open(path,'r',encoding='utf-8')
    message=file_name.read()
    return message

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
    def handle_starttag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        pass
    def handle_data(self, data):
        if data.count('\n') == 0:
            self.data.append(data)

def GetLevel(player_name):
    url="http://vgbox.cc/player/cn/%s/ranked" %(player_name)
    result=Curl(url)
    if re.search('游戏id不存在或没有数据',result):
        return('ID:%s不存在')  %(player_name)
    else:
        level_3v3=re.findall('3v3分：[0-9.]*',result)[0].strip("3v3分：").replace('\'','')
        ranked_3v3=re.findall('排行：[0-9.]*',result)[0].strip("排行：").replace('\'','')
        url="http://vgbox.cc/player/cn/%s/5v5_pvp_ranked" %(player_name)
        result=Curl(url)
        level_5v5=re.findall('5v5分：[0-9.]*',result)[0].strip("5v5分：").replace('\'','')
        ranked_5v5=re.findall('排行：[0-9.]*',result)[0].strip("排行：").replace('\'','')
        url="http://vgbox.cc/player/cn/%s/blitz_pvp_ranked" %(player_name)
        result=Curl(url)
        level_blitz=re.findall('闪电战分：[0-9.]*',result)[0].strip("闪电战分：").replace('\'','')
        ranked_blitz=re.findall('排行：[0-9.]*',result)[0].strip("排行：").replace('\'','')
        message="查询成功\n3v3段位分: %s\n3v3排名: %s\n\n5v5排位分: %s\n5v5排名: %s\n\n闪电战排位分: %s\n闪电战排名: %s" %(level_3v3,ranked_3v3,level_5v5,ranked_5v5,level_blitz,ranked_blitz)
        return message

def Legacy(player_name,mode,page):
    if int(page) > 4:
        realpage=int(page)//4
        part=int(page)%4
        if part != 0:
            realpage=(int(page)//4)+1
    else:
        realpage="1"
        part=page
    url="http://vgbox.cc/recentMatches/cn/%s/all/%s" %(player_name,realpage)
    result=Curl(url).replace('http://vgbox.oss-cn-shenzhen.aliyuncs.com/assets/images/heroes/','http://vgbox.oss-cn-shenzhen.aliyuncs.com/assets/images/heroes/" <b>英雄:').replace('" alt="${p.getActor()}"','<b>').replace('.gif','')
    if re.search('游戏id不存在或没有数据',result):
        return('ID:%s不存在')  %(player_name)
    else:
        parser = MyHTMLParser()
        parser.feed(result)
        info=" ".join(parser.data)
        info=(info.replace("KDA","KDA\n").replace("→","\n").replace("排位赛","R").replace("大","").replace("匹配赛","C").replace("胜利","赢").replace("失败","输")).replace("闪电战",'闪电').replace("好友对战-","")
        list=re.findall(".*?KDA",info)
        do_time=1
        time_needed_start=((int(part)-1)*5)+1
        time_needed_end=int(part)*5
        message=""
        print(part,realpage,time_needed_start,time_needed_end)
        for match in list:
            game_date=" ".join(re.findall('([0-99]*-[0-99]*)',match)).replace(" ","")
            game_time=" ".join(re.findall(' ([0-99]*:[0-99]*) ',match)).replace(" ","")
            ranke_change=" ".join(re.findall('( [↑↓][0-99]*.[0-99]*) ',match)).replace(" ","")
            game_type=" ".join(re.findall('[0-99]*-[0-99]* [0-99]*:[0-99]* (.*) [0-99]*.*秒',match.replace(" ".join(re.findall(' ([↑↓][0-99]*.[0-99]*) ',match)),""))).replace(" ","")
            game_last=" ".join(re.findall(' ([0-99]*分[0-99]*秒)',match)).replace(" ","").replace("分",":").replace("时",":").replace("秒","")
            game_result=" ".join(re.findall(' [0-99]*分[0-99]*秒 (.*) 英雄',match)).replace(" ","")
            game_hero=" ".join(re.findall('英雄:([A-Za-z]*)',match)).replace(" ","")
            game_score=" ".join(re.findall('评分 ([A-Za-z])',match)).replace(" ","")
            game_KDA=" ".join(re.findall('([0-99]* [0-99]* [0-99]* [0-99]*\.[0-99]*) KDA',match)).replace(" ","|").replace(" ","")
            if int(time_needed_start) <= do_time <= int(time_needed_end):
                if mode == "1":
                    message=message + "%s %s %s %s\n" %(game_type,game_result,game_KDA,game_hero)
                elif mode == "2":
                    message=message + "%s %s %s %s %s %s\n" %(game_date,game_time,game_result,game_score,game_type,game_last)
            do_time=do_time+1
        if mode == "1":
            all_message="id: %s\n类型 输赢 K|D|A|KDA 英雄\n%s" %(player_name,message)
        elif mode == "2":
            all_message="id: %s\n日期 时间 输赢/评分 类型 时长\n%s" %(player_name,message)
        return all_message

def Vg_Time(player_name):
    url="http://vghours.glitch.me/user?ign=%s" %(player_name)
    result=Curl_Post(url,"")
    if re.search('There was an error searching this IGN.',result):
        return('ID:%s不存在')  %(player_name)
    else:
        aral=" ".join(re.findall("aral:([0-99]*)",result.replace('\"',"").replace('\'','')))
        blitz=" ".join(re.findall("blitz:([0-99]*)",result.replace('\"',"").replace('\'','')))
        ranked=" ".join(re.findall("ranked:([0-99]*)",result.replace('\"',"").replace('\'','')))
        ranked_5v5=" ".join(re.findall("ranked_5v5:([0-99]*)",result.replace('\"',"").replace('\'','')))
        casual=" ".join(re.findall("casual:([0-99]*)",result.replace('\"',"").replace('\'','')))
        casual_5v5=" ".join(re.findall("casual_5v5:([0-99]*)",result.replace('\"',"").replace('\'','')))
        vg_time=" ".join(re.findall("time:([0-99]*)",result.replace('\"',"").replace('\'','')))
        rank=" ".join(re.findall("rank:([0-99]*)",result.replace('\"',"").replace('\'','')))
        rankpercentage=" ".join(re.findall("rankPercentage:([A-Z]* [0-9]*%)",result.replace('\"',"").replace('\'','').replace("[","")))
        message="查询成功\nid: %s\n大乱斗: %s\n闪电战: %s\n3v3排位: %s\n5v5排位: %s\n3v3匹配: %s\n5v5匹配: %s\n\n总共游戏时长: %s小时\n肝硬化排名: %s\n肝硬化金字塔: %s" %(player_name,aral,blitz,ranked,ranked_5v5,casual,casual_5v5,vg_time,rank,rankpercentage)
        return message

def Win_Rate(player_name):
    url='http://vgbox.cc/player/cn/%s/all'  %(player_name)
    result=Curl(url).replace('<span class="pull-left"> ','<span class="pull-left">').replace('负 </span>','负</span>')
    if re.search('游戏id不存在或没有数据',result):
        return('ID:%s不存在')  %(player_name)
    else:
        parser = MyHTMLParser()
        parser.feed(result)
        info=" ".join(parser.data)
        win_and_lose=" ".join(re.findall('[0-99\.]*%'," ".join(re.findall('[0-99]*胜.*[0-99]*%.*[0-99]负',info))))
        team_fight_rate=" ".join(re.findall('参团率:.*[0-99]*%',info)).strip('参团率:').strip(' ')
        KDA=" ".join(re.findall('平均KDA:[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*',info)).replace('平均KDA: ','').replace('  ','|').replace(' ','/').replace('|','  ')
        url='http://vgbox.cc/player/cn/%s/5v5_pvp_ranked'  %(player_name)
        result=Curl(url).replace('<span class="pull-left"> ','<span class="pull-left">').replace('负 </span>','负</span>')
        parser = MyHTMLParser()
        parser.feed(result)
        info=" ".join(parser.data)
        pvp_ranked_5v5_win_and_lose=" ".join(re.findall('[0-99\.]*%'," ".join(re.findall('[0-99]*胜.*[0-99]*%.*[0-99]负',info))))
        pvp_ranked_5v5_team_fight_rate=" ".join(re.findall('参团率:.*[0-99]*%',info)).strip('参团率:').strip(' ')
        pvp_ranked_5v5_KDA=" ".join(re.findall('平均KDA:[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*',info)).replace('平均KDA: ','').replace('  ','|').replace(' ','/').replace('|','  ')
        url='http://vgbox.cc/player/cn/%s/5v5_pvp_casual'  %(player_name)
        result=Curl(url).replace('<span class="pull-left"> ','<span class="pull-left">').replace('负 </span>','负</span>')
        parser = MyHTMLParser()
        parser.feed(result)
        info=" ".join(parser.data)
        pvp_casual_5v5_win_and_lose=" ".join(re.findall('[0-99\.]*%'," ".join(re.findall('[0-99]*胜.*[0-99]*%.*[0-99]负',info))))
        pvp_casual_5v5_team_fight_rate=" ".join(re.findall('参团率:.*[0-99]*%',info)).strip('参团率:').strip(' ')
        pvp_casual_5v5_KDA=" ".join(re.findall('平均KDA:[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*',info)).replace('平均KDA: ','').replace('  ','|').replace(' ','/').replace('|','  ')
        url='http://vgbox.cc/player/cn/%s/ranked'  %(player_name)
        result=Curl(url).replace('<span class="pull-left"> ','<span class="pull-left">').replace('负 </span>','负</span>')
        parser = MyHTMLParser()
        parser.feed(result)
        info=" ".join(parser.data)
        ranked_win_and_lose=" ".join(re.findall('[0-99\.]*%'," ".join(re.findall('[0-99]*胜.*[0-99]*%.*[0-99]负',info))))
        ranked_team_fight_rate=" ".join(re.findall('参团率:.*[0-99]*%',info)).strip('参团率:').strip(' ')
        ranked_KDA=" ".join(re.findall('平均KDA:[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*',info)).replace('平均KDA: ','').replace('  ','|').replace(' ','/').replace('|','  ')
        url='http://vgbox.cc/player/cn/%s/casual'  %(player_name)
        result=Curl(url).replace('<span class="pull-left"> ','<span class="pull-left">').replace('负 </span>','负</span>')
        parser = MyHTMLParser()
        parser.feed(result)
        info=" ".join(parser.data)
        casual_win_and_lose=" ".join(re.findall('[0-99\.]*%'," ".join(re.findall('[0-99]*胜.*[0-99]*%.*[0-99]负',info))))
        casual_team_fight_rate=" ".join(re.findall('参团率:.*[0-99]*%',info)).strip('参团率:').strip(' ')
        casual_KDA=" ".join(re.findall('平均KDA:[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*',info)).replace('平均KDA: ','').replace('  ','|').replace(' ','/').replace('|','  ')
        url='http://vgbox.cc/player/cn/%s/casual_aral'  %(player_name)
        result=Curl(url).replace('<span class="pull-left"> ','<span class="pull-left">').replace('负 </span>','负</span>')
        parser = MyHTMLParser()
        parser.feed(result)
        info=" ".join(parser.data)
        casual_aral_win_and_lose=" ".join(re.findall('[0-99\.]*%'," ".join(re.findall('[0-99]*胜.*[0-99]*%.*[0-99]负',info))))
        casual_aral_team_fight_rate=" ".join(re.findall('参团率:.*[0-99]*%',info)).strip('参团率:').strip(' ')
        casual_aral_KDA=" ".join(re.findall('平均KDA:[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*',info)).replace('平均KDA: ','').replace('  ','|').replace(' ','/').replace('|','  ')
        url='http://vgbox.cc/player/cn/%s/blitz_pvp_ranked'  %(player_name)
        result=Curl(url).replace('<span class="pull-left"> ','<span class="pull-left">').replace('负 </span>','负</span>')
        parser = MyHTMLParser()
        parser.feed(result)
        info=" ".join(parser.data)
        blitz_pvp_ranked_win_and_lose=" ".join(re.findall('[0-99\.]*%'," ".join(re.findall('[0-99]*胜.*[0-99]*%.*[0-99]负',info))))
        blitz_pvp_ranked_team_fight_rate=" ".join(re.findall('参团率:.*[0-99]*%',info)).strip('参团率:').strip(' ')
        blitz_pvp_ranked_KDA=" ".join(re.findall('平均KDA:[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*[ ]*[0-99\.]*',info)).replace('平均KDA: ','').replace('  ','|').replace(' ','/').replace('|','  ')
        message="id: %s\n分类   胜率   KDA    K / D / A\n全部  %s  %s\n5v5R %s  %s\n5v5C %s  %s\n3v3R %s  %s\n3v3C %s  %s\n乱斗  %s  %s\n闪电  %s  %s\n" %(player_name,win_and_lose,KDA,pvp_ranked_5v5_win_and_lose,pvp_ranked_5v5_KDA,pvp_casual_5v5_win_and_lose,pvp_casual_5v5_KDA,ranked_win_and_lose,ranked_KDA,casual_win_and_lose,casual_KDA,casual_aral_win_and_lose,casual_aral_KDA,blitz_pvp_ranked_win_and_lose,blitz_pvp_ranked_KDA)
        return message

def Info(player_name,shardid):
    url="https://api.dc01.gamelockerapp.com/shards/%s/players?filter[playerNames]=%s" %(shardid,player_name)
    result=Curl_Auth(url)
    if re.search('No players found matching criteria',result):
        return('服务器%s中不存在ID:%s')  %(shardid,player_name)
    else:
        shardid=" ".join(re.findall('\"shardId\":\"([a-z]*)\",',result))
        guildtag=" ".join(re.findall('\"guildTag\":\"([A-Za-z]*)\",',result))
        karmalevel=" ".join(re.findall('\"karmaLevel\":([0-9]*),',result))
        level=" ".join(re.findall('\"level\":([0-9]*),',result))
        wins=" ".join(re.findall('\"wins\":([0-9]*),',result))
        xp=" ".join(re.findall('\"xp\":([0-9]*)',result))
        if karmalevel == "1":
            display_karmalevel="善"
        elif karmalevel == "2":
            display_karmalevel="至善"
        else:
            display_karmalevel="恶"
        message="id: %s\n所在服务器: %s\n所在公会: %s\n游戏等级: %s\n业力等级: %s\n总胜场数: %s\n总经验值: %s" %(player_name,shardid,guildtag,level,display_karmalevel,wins,xp)
        return message

def Match(player_name,number):
    url="http://vgbox.cc/recentMatches/cn/%s/all/1" %(player_name)
    result=Curl(url)
    if re.search('游戏id不存在或没有数据',result):
        return('ID:%s不存在')  %(player_name)
    else:
        match_ids=re.findall("/matchDetail/cn/.*/[0-99]*-[0-99]*-[0-99]*/([a-z0-99]*-[a-z0-99]*-[a-z0-99]*-[a-z0-99]*-[a-z0-99]*)",result)
        do_time=1
        for match_id in match_ids:
            locals()['match_id'+str(do_time)] = match_id
            do_time=do_time+1
        chosenid=locals()['match_id'+str(number)]
        url="https://api.dc01.gamelockerapp.com/shards/cn/matches/%s" %(chosenid)
        result=Curl_Auth(url).replace("}}}}","}}}}\n").replace("patchVersion","patchVersion\n")
        info=re.findall('actor\":\"\*.*}}}}',result)
        match_type="".join(re.findall("gameMode\":\"(.*)\",\"patchVersion",result))
        info_number=(len(info))
        menbers_winner=""
        menbers_loser=""
        for ids in info:
            hero="".join(re.findall("actor\":\"\*([a-zA-Z]*)\*\"",ids))
            assists="".join(re.findall("assists\":([0-99]*),",ids))
            deaths="".join(re.findall("deaths\":([0-99]*),",ids))
            farm="".join(re.findall("farm\":([0-99]*),",ids))
            kills="".join(re.findall("kills\":([0-99]*),",ids))
            gold='%.1f'%(float("".join(re.findall("gold\":([0-99\.]*),",ids)))/1000)
            player_id="".join(re.findall("id\":\"(.*)\"}}}}",ids))
            findall_key="%s\",\"attributes\":{\"name\":\"(.*)\",\"patchVersion" %(player_id)
            match_player_name="".join(re.findall(findall_key,result))
            skilltier="".join(re.findall("\"skillTier\":([0-99]*)",ids))
            winner="".join(re.findall("\"winner\":([a-z]*)",ids))
            if winner == "true":
                if menbers_winner != "":
                    menbers_winner="%s\n%s    %s    %s\n%s/%s/%s         %s         %sK" %(menbers_winner,hero,match_player_name,skilltier,kills,deaths,assists,farm,gold)
                else:
                    menbers_winner="%s    %s    %s\n%s/%s/%s         %s         %sK" %(hero,match_player_name,skilltier,kills,deaths,assists,farm,gold)
            else:
                if menbers_loser != "":
                    menbers_loser="%s\n%s    %s    %s\n%s/%s/%s         %s         %sK" %(menbers_loser,hero,match_player_name,skilltier,kills,deaths,assists,farm,gold)
                else:
                    menbers_loser="%s    %s    %s\n%s/%s/%s         %s         %sK" %(hero,match_player_name,skilltier,kills,deaths,assists,farm,gold)
        message="英雄            ID            段位\nK/D/A         补刀        经济\n对局类型:  %s\n胜利方:\n%s\n失败方:\n%s" %(match_type,menbers_winner,menbers_loser)
        return message

def SkyTier(region,rank_type,start_rank):
    url="https://api.vgpro.gg/leaderboard/%s/%s?limit=10&offset=%s" %(rank_type,region,start_rank)
    result=Curl(url).replace(']}',']}\n')
    if result == "":
        return("服务器连接错误")
    elif result == "[]":
        return("未查询到数据")
    else:
        message=""
        info=re.findall('playerId.*]}',result)
        for playerinfo in info:
            playername=re.findall('name":"(.*)","region',playerinfo)[0]
            points='%.1f'%(float("".join(re.findall('points":"([0-99\.]*)",',playerinfo))))
            position=re.findall('position":([0-99]*),',playerinfo)[0]
            message="%s%s %s %s\n" %(message,position,points,playername)
        return message
            
        

def onQQMessage(bot, contact, member, content):
    if '@ME' in content:
        if int(time.time()) - int(Read_Time_Log()) < 3 :
            bot.SendTo(contact, "冷却中")
        else:
            word_to_send=content.replace("".join(re.findall('\[@ME\][ ]*',content)),'')
            if word_to_send == "":
                bot.SendTo(contact, "@我是没有用的哦。\n想要查询只要发送消息就行了呢.\n查询指令格式: \"-[指令] [id] [选项]\"\n指令支持:信息 段位 胜率 时光 战绩 比赛 对局\n开头那个是英文符号-,打错了我是不会查询的\n个别指令有选项参数,也可不写\n比如\"信息\"指令支持参数\"服务器\"可填sg等其他服")
            else:
                data='{"reqType":0,"perception":{"inputText":{"text":"%s"},"inputImage":{"url":""},"selfInfo":{"location":{"city":"","province":"","street":""}}},"userInfo":{"apiKey":"f4ffa9a048744dacb611c41f185ba2cb","userId":"123"}}' %(word_to_send)
                message_returned=Curl_Post('http://openapi.tuling123.com/openapi/api/v2',data.encode('utf-8'))
                message="".join(re.findall('{"text":"(.*)"}}',message_returned))
                if re.search('groupType',message):
                    message="".join(re.findall('(.*)"}},{"groupType',message))
                bot.SendTo(contact,message)
                Write_Time_Log()
    elif '-段位' in content:
        player_name=content.replace('-段位 ','')
        player_name=player_name.replace('-段位','')
        player_name=player_name.replace('-战绩 ','')
        player_name=player_name.replace('-战绩','')
        player_name=player_name.replace('-时光 ','')
        player_name=player_name.replace('-时光','')
        player_name=player_name.replace('-比赛 ','')
        player_name=player_name.replace('-比赛','')
        player_name=player_name.replace('-信息 ','')
        player_name=player_name.replace('-信息','')
        player_name=player_name.replace('-对局 ','')
        player_name=player_name.replace('-对局','')
        if int(time.time()) - int(Read_Time_Log()) < 5 :
            bot.SendTo(contact, "冷却中")
        else:
            if player_name == "":
                bot.SendTo(contact, "格式错误")
            else:
                message="正在查询id: %s" %(player_name)
                bot.SendTo(contact, message)
                message=GetLevel(player_name)
                bot.SendTo(contact, message)
            Write_Time_Log()
    elif '-战绩' in content:
        player_name=content.replace('-战绩 ','')
        player_name=player_name.replace('-战绩','')
        player_name=player_name.replace('-段位 ','')
        player_name=player_name.replace('-段位','')
        player_name=player_name.replace('-时光 ','')
        player_name=player_name.replace('-时光','')
        player_name=player_name.replace('-胜率 ','')
        player_name=player_name.replace('-胜率','')
        player_name=player_name.replace('-比赛 ','')
        player_name=player_name.replace('-比赛','')
        player_name=player_name.replace('-信息 ','')
        player_name=player_name.replace('-信息','')
        player_name=player_name.replace('-对局 ','')
        info_player_name=player_name.replace('-对局','')
        if int(time.time()) - int(Read_Time_Log()) < 5 :
            bot.SendTo(contact, "冷却中")
        else:
            if " " in info_player_name:
                player_name="".join(info_player_name.split(' ')[0])
                page="".join(info_player_name.split(' ')[1])
            else:
                player_name=info_player_name
                page="1"
            if player_name == "":
                bot.SendTo(contact, "格式错误")
            else:
                if page == "":
                    page="1"
                    message="正在查询id: %s的第%s页战绩\nR代表排位，C代表匹配" %(player_name,page)
                    bot.SendTo(contact, message)
                    message=Legacy(player_name,'1',page)
                    bot.SendTo(contact, message)
                else:
                    if 0 < int(page) <= 100:
                        message="正在查询id: %s的第%s页战绩\nR代表排位，C代表匹配" %(player_name,page)
                        bot.SendTo(contact, message)
                        message=Legacy(player_name,'1',page)
                        bot.SendTo(contact, message)
                    else:
                        message="页数%s不可用，只支持1-100页" %(page)
                        bot.SendTo(contact, message)
            Write_Time_Log()
    elif '-时光' in content:
        player_name=content.replace('-战绩 ','')
        player_name=player_name.replace('-战绩','')
        player_name=player_name.replace('-段位 ','')
        player_name=player_name.replace('-段位','')
        player_name=player_name.replace('-时光 ','')
        player_name=player_name.replace('-时光','')
        player_name=player_name.replace('-胜率 ','')
        player_name=player_name.replace('-胜率','')
        player_name=player_name.replace('-比赛 ','')
        player_name=player_name.replace('-比赛','')
        player_name=player_name.replace('-信息 ','')
        player_name=player_name.replace('-信息','')
        player_name=player_name.replace('-对局 ','')
        player_name=player_name.replace('-对局','')
        if int(time.time()) - int(Read_Time_Log()) < 5 :
            bot.SendTo(contact, "冷却中")
        else:
            if player_name == "":
                bot.SendTo(contact, "格式错误")
            else:
                message="正在查询id: %s\n不显示排名过一会儿再查一次就有了" %(player_name)
                bot.SendTo(contact, message)
                message=Vg_Time(player_name)
                bot.SendTo(contact, message)
            Write_Time_Log()
    elif '-胜率' in content:
        player_name=content.replace('-战绩 ','')
        player_name=player_name.replace('-战绩','')
        player_name=player_name.replace('-段位 ','')
        player_name=player_name.replace('-段位','')
        player_name=player_name.replace('-时光 ','')
        player_name=player_name.replace('-时光','')
        player_name=player_name.replace('-胜率 ','')
        player_name=player_name.replace('-胜率','')
        player_name=player_name.replace('-比赛 ','')
        player_name=player_name.replace('-比赛','')
        player_name=player_name.replace('-排行榜 ','')
        player_name=player_name.replace('-排行榜','')
        player_name=player_name.replace('-信息 ','')
        player_name=player_name.replace('-信息','')
        player_name=player_name.replace('-对局 ','')
        player_name=player_name.replace('-对局','')
        if int(time.time()) - int(Read_Time_Log()) < 5 :
            bot.SendTo(contact, "冷却中")
        else:
            if player_name == "":
                bot.SendTo(contact, "格式错误")
            else:
                message="正在查询id: %s\n胜率查询时间比较长，请耐心等候\nR代表排位 C代表匹配" %(player_name)
                bot.SendTo(contact, message)
                message=Win_Rate(player_name)
                bot.SendTo(contact, message)
            Write_Time_Log()
    elif '-比赛' in content:
        player_name=content.replace('-战绩 ','')
        player_name=player_name.replace('-战绩','')
        player_name=player_name.replace('-段位 ','')
        player_name=player_name.replace('-段位','')
        player_name=player_name.replace('-时光 ','')
        player_name=player_name.replace('-时光','')
        player_name=player_name.replace('-胜率 ','')
        player_name=player_name.replace('-胜率','')
        player_name=player_name.replace('-比赛 ','')
        player_name=player_name.replace('-比赛','')
        player_name=player_name.replace('-信息 ','')
        player_name=player_name.replace('-排行榜 ','')
        player_name=player_name.replace('-排行榜','')
        player_name=player_name.replace('-信息','')
        player_name=player_name.replace('-对局 ','')
        info_player_name=player_name.replace('-对局','')
        if int(time.time()) - int(Read_Time_Log()) < 5 :
            bot.SendTo(contact, "冷却中")
        else:
            if " " in info_player_name:
                player_name="".join(info_player_name.split(' ')[0])
                page="".join(info_player_name.split(' ')[1])
            else:
                player_name=info_player_name
                page="1"
            if player_name == "":
                bot.SendTo(contact, "格式错误")
            else:
                 if page == "":
                     page="1"
                     message="正在查询id: %s的第%s页比赛\nR代表排位，C代表匹配" %(player_name,page)
                     bot.SendTo(contact, message)
                     message=Legacy(player_name,'2',page)
                     bot.SendTo(contact, message)
                 else:
                     if 0 < int(page) <= 100:
                         message="正在查询id: %s的第%s页战绩\nR代表排位，C代表匹配" %(player_name,page)
                         bot.SendTo(contact, message)
                         message=Legacy(player_name,'2',page)
                         bot.SendTo(contact, message)
                     else:
                         message="页数%s不可用，只支持1-100页" %(page)
                         bot.SendTo(contact, message)
            Write_Time_Log()
    elif '-信息' in content:
        player_name=content.replace('-战绩 ','')
        player_name=player_name.replace('-战绩','')
        player_name=player_name.replace('-段位 ','')
        player_name=player_name.replace('-段位','')
        player_name=player_name.replace('-时光 ','')
        player_name=player_name.replace('-时光','')
        player_name=player_name.replace('-胜率 ','')
        player_name=player_name.replace('-胜率','')
        player_name=player_name.replace('-比赛 ','')
        player_name=player_name.replace('-比赛','')
        player_name=player_name.replace('-排行榜 ','')
        player_name=player_name.replace('-排行榜','')
        player_name=player_name.replace('-对局 ','')
        player_name=player_name.replace('-对局','')
        player_name=player_name.replace('-信息 ','')
        info_player_name=player_name.replace('-信息','')
        if int(time.time()) - int(Read_Time_Log()) < 5 :
            bot.SendTo(contact, "冷却中")
        else:
            if " " in info_player_name:
                player_name="".join(info_player_name.split(' ')[0])
                shardid="".join(info_player_name.split(' ')[1])
            else:
                player_name=info_player_name
                shardid="cn"
            if player_name == "":
                bot.SendTo(contact, "格式错误")
            else:
                if shardid == "":
                    shardid="cn"
                    message="正在查询%s服务器的id: %s" %(shardid,player_name)
                    bot.SendTo(contact, message)
                    message=Info(player_name,shardid)
                    bot.SendTo(contact, message)
                elif shardid != "":
                    if shardid in "cn na eu sa ea sg":
                        message="正在查询id: %s" %(player_name)
                        bot.SendTo(contact, message)
                        message=Info(player_name,shardid)
                        bot.SendTo(contact, message)
                    else:
                        message="服务器: %s不存在\n可用的服务器:cn na eu sa ea sg" %(shardid)
                        bot.SendTo(contact, message)
            Write_Time_Log()
    elif '-对局' in content:
        player_name=content.replace('-战绩 ','')
        player_name=player_name.replace('-战绩','')
        player_name=player_name.replace('-段位 ','')
        player_name=player_name.replace('-段位','')
        player_name=player_name.replace('-时光 ','')
        player_name=player_name.replace('-时光','')
        player_name=player_name.replace('-胜率 ','')
        player_name=player_name.replace('-胜率','')
        player_name=player_name.replace('-比赛 ','')
        player_name=player_name.replace('-比赛','')
        player_name=player_name.replace('-排行榜 ','')
        player_name=player_name.replace('-排行榜','')
        player_name=player_name.replace('-对局 ','')
        player_name=player_name.replace('-对局','')
        player_name=player_name.replace('-信息 ','')
        info_player_name=player_name.replace('-信息','')
        if int(time.time()) - int(Read_Time_Log()) < 5 :
            bot.SendTo(contact, "冷却中")
        else:
            if " " in info_player_name:
                player_name="".join(info_player_name.split(' ')[0])
                number="".join(info_player_name.split(' ')[1])
            else:
                player_name=info_player_name
                number="1"
            if player_name == "":
                bot.SendTo(contact, "格式错误")
            else:
                if number == "":
                    number="1"
                    message="正在查询id: %s的倒数第%s场对局" %(player_name,number)
                    bot.SendTo(contact, message)
                    message=Match(player_name,number)
                    bot.SendTo(contact, message)
                elif number != "":
                    if number in "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20":
                        message="正在查询id: %s的倒数第%s场对局" %(player_name,number)
                        bot.SendTo(contact, message)
                        message=Match(player_name,number)
                        bot.SendTo(contact, message)
                    else:
                        message="对局: %1不存在\n只可查询1-20" %(number)
                        bot.SendTo(contact, message)
            Write_Time_Log()
    elif '-排行榜' in content:
        player_name=content.replace('-战绩 ','')
        player_name=player_name.replace('-战绩','')
        player_name=player_name.replace('-段位 ','')
        player_name=player_name.replace('-段位','')
        player_name=player_name.replace('-时光 ','')
        player_name=player_name.replace('-时光','')
        player_name=player_name.replace('-胜率 ','')
        player_name=player_name.replace('-胜率','')
        player_name=player_name.replace('-比赛 ','')
        player_name=player_name.replace('-比赛','')
        player_name=player_name.replace('-对局 ','')
        player_name=player_name.replace('-对局','')
        player_name=player_name.replace('-信息 ','')
        player_name=player_name.replace('-信息','')
        player_name=player_name.replace('-排行榜 ','')
        info_player_name=player_name.replace('-排行榜','')
        if int(time.time()) - int(Read_Time_Log()) < 5 :
            bot.SendTo(contact, "冷却中")
        else:
            ok="yes"
            if " " in info_player_name:
                region="".join(info_player_name.split(' ')[0])
                print(len(info_player_name.split(' ')))
                if len(info_player_name.split(' ')) >= 2:
                    start_rank="".join(info_player_name.split(' ')[1])
                else:
                    start_rank=""
                if len(info_player_name.split(' ')) >= 3:
                    rank_type="".join(info_player_name.split(' ')[2])
                else:
                    rank_type=""
            else:
                region=info_player_name
                rank_type="ranked"
                start_rank="0"
            if region == "":
                region="cn"
            else:
                if region in "cn na eu sa ea sg":
                    region=region
                else:
                    message="服务器: %s不存在\n可用的服务器:cn na eu sa ea sg" %(region)
                    bot.SendTo(contact, message)
                    ok="no"
            if rank_type == "":
                rank_type="ranked"
            else:
                if rank_type in "ranked ranked5v5 blitz":
                    rank_type=rank_type
                else:
                    message="排位类型: %s不存在\n可用的排位类型:ranked ranked5v5 blitz" %(rank_type)
                    bot.SendTo(contact, message)
                    ok="no"
            if start_rank == "":
                start_rank="0"
            if ok != "no":
                message="正在查询%s服务器的%s排位赛第%s后的排名" %(region,rank_type,start_rank)
                bot.SendTo(contact, message)
                message=SkyTier(region,rank_type,start_rank)
                bot.SendTo(contact, message)
        Write_Time_Log()
  



