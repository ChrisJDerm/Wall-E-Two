from __future__ import print_function

from discord.ext.commands import bot

import quickstart
import discord
import gspread

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

dirname = os.path.dirname("main.py")
gc = gspread.service_account(filename=os.path.join(dirname, 'nasasortbot-ffaff37331c8.json'))
names = quickstart.main()
roles = quickstart.getRoles()
wks = gc.open_by_key('19MIoeRmY2K4TtKBvvUHtY9XZeDOE6vSy').sheet1  # sheets id
wks.format('A1:B1', {'backgroundColor': {"red": 0.5, "green": 0.5, "blue": 0.5}});

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

guildID = 933859797235818506

@client.event
async def on_ready():
    await client.get_channel(id=937604710259626034).send("Hello World " + client.get_guild(guildID).name)
    guild = client.get_guild(guildID)
    memberList = guild.members
    memberNick = []
    for m in memberList:
        if m.nick is None:
            memberNick.append(m.name.lower())
            print("Nick: " + m.name)
        else:
            memberNick.append(m.nick.lower())
            print("Nick: " + m.nick)
    for mNick in memberNick:
        if mNick in names:
            print("Match: " + mNick)
            index = names.index(mNick.lower())
            await updateCell(index, False)
            await client.get_channel(id=979147101302849577).send(mNick)
            rolesLower = []
            for role in memberList[memberNick.index(mNick)].roles:
                rolesLower.append(role.name.lower().strip())
            for j in rolesLower:
                print(j)
            print(roles[index].lower())
            print(roles[index].lower().strip() in rolesLower)
            if roles[index].lower().strip() in rolesLower:
                print("Working " + roles[index])
                await updateCell(index, True)
                wks.update_cell(index + 2, 4, "DONE")
                await client.get_channel(id=979147101302849577).send(roles[index])



async def updateCell(index, bool):
    if (bool):
        wks.format('A' + str(index + 2) + ':D' + str(index + 2),
                   {'backgroundColor': {"red": 1, "green": 1, "blue": 0.0}})
    else:
        wks.format('A' + str(index + 2) + ':D' + str(index + 2),
                   {'backgroundColor': {"red": 0.71, "green": 0.78, "blue": 0.91}})


@client.event
async def on_member_update(before, after):
    nickname = after.nick
    if (after.nick is None):
        nickname = after.name
    if nickname.lower() in names:
        index = names.index(nickname.lower())
        await updateCell(index, False)
        #await client.get_channel(id=979147101302849577).send(nickname)
        rolesLower = []
        for role in after.roles:
            rolesLower.append(role.name.lower().strip())
        for j in rolesLower:
            print(j)
        print(roles[index].lower())
        print(roles[index].lower().strip() in rolesLower)
        if roles[index].lower().strip() in rolesLower:
            print("Working " + roles[index])
            await updateCell(index, True)
            wks.update_cell(index + 2, 4, "DONE")
            await client.get_channel(id=979147101302849577).send(roles[index])


@client.event
async def on_message(message):
    #print(message.content)
    if(message.content == "$update"):
        await on_ready()


def printAll():
    index = 0
    for row in names:
        print(row + ", " + roles[index])
        index = index + 1


#printAll()
client.run('OTc5MTQ5NzExNTA2MzA5MTgw.G4ldN8.G-A4_Ixg30hAc-u-wnBMIJ_0XCWu0glA8NxLGw')  # bot token
