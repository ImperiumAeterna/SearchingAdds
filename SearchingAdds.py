#! /usr/bin/env python3

import requests
import datetime

def CheckDate(str, currentTime):  # check if post published in last 24 hours
    postDate = ''''''
    tmp = '''"date":'''
    i = str.find(tmp)+7
    while (str[i] != ','):
        postDate += str[i]
        i += 1
    return ((int(postDate)+60*60*24) > currentTime)


def SearchRepost(str):
    result = ''''''
    if (str.find("copy_history") > 0):  # if copy_history founded
        i = str.find('''id":''')+4  # find postId in publicId[i] group
        while (str[i] != ','):
            result += str[i]  # write postId
            i += 1
        return result  # & return it
    else:
        return False


def SearchSource(str):
    result = ''''''
    if (str.find('''"link":"''') > 0):
        i = str.find('''"link":"''')+8  # search start of copyright link
        while (str[i] != '''"'''):
            result += str[i]  # write copyright link
            i += 1
        return (result)  # & return it
    else:
        return False


def CheckBlackList(blackList, tmp):
    notFound = True
    for i in range(0, len(blackList)):
        if tmp.find(blackList[i]):
            notFound = False
    return notFound

def WallPost(accessToken, text):
    print(accessToken)
    wallPost="https://api.vk.com/method/wall.post?access_token="
    owner = '&owner_id=-197501499&v=5.92' #here print you public ID
    message='&message="'
    requests.get(wallPost+accessToken+owner+message+text+'"')
    print()

def FiscusWall(accessToken,tmp):
    WallPost(accessToken,tmp)
    
# not used #correcting currentIndex after searching copyright link
def RectificationIndex(str, currentIndex):
    return str.find('''"link":"''', currentIndex)


currentTime = datetime.datetime.now().timestamp()
wallGet = "https://api.vk.com/method/wall.get?access_token="
ownerId = '&owner_id=-'
offsetValue = "&offset="
otherPar = '&count=1&v=5.92'
accessToken = 'd7efca0f6a0cb54f2274bf19b17c58212dae26fbd147c7069aa0364363a990546c8830323e62026a462b9'
PublicId = ['133624651', '110310316', '166931460',
            '86559535', '52808290', '39695140', '100157872', '26406986', '50957736', '37428214', '146246673',
            '112964810', '104417315', '111182922', '104202061', '102334909', '104083566',
            '81668509', '161578115', '130360681', '53529984', '69961', '40207369', '27989623', '7768848',
            '43747253', '78915110', '42452438', '50270185', '117827457', '27669439', '49883792', '30015237',
            '4327437', '151878956', '158803926', '72163745', '151729282', '129762621', '75115271', '36047336',
            '72100530', '68812734', '99569653', '59740949', '46381558', '49372824', '73921861', '38753481',
            '68995594', '97446391', '140265408', '124111152', '148648595',  '133325750', '137065294',
            '132945788', '117640405', '107844627', '173752134', '147000793', '52399827', '60426665',
            '138813913', '84673469', '49597300', '41887171']
blackList = ['114689011', '110310316']
lastDay = True

for i in range(0, len(PublicId)):
    lastDay = True
    offset = 0
    while (lastDay):
        req = requests.get(wallGet+accessToken+ownerId +
                           PublicId[i]+offsetValue+(str(offset))+otherPar)
        res = req.text
        if (CheckDate(res,currentTime)):
            tmp=SearchSource(res)
            if (tmp and CheckBlackList(blackList,tmp)): #if source founded & not blacklisted
                print (tmp)
                FiscusWall(accessToken,tmp)
            tmp=SearchRepost(res)
            if (tmp): #if repost founded
                print ('''https://vk.com/wall-'''+PublicId[i]+"_"+tmp) 
                FiscusWall(accessToken,('''https://vk.com/wall-'''+PublicId[i]+"_"+tmp))
            offset += 1
        else:
            lastDay = False
