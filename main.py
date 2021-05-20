import discord
import os
from random import *
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

groupList = []
groupListFinal = []
groupSize = 0
random = 0

class MyClient(discord.Client):

    async def on_ready(self):
        print("Group shuffler bot is active...")

    async def on_message(self, message):
        global groupSize
        if message.content.startswith("g"):
            groupSize = message.content.split(' ')[1]
            print("groupsize is: " + str(groupSize))

            await message.channel.send("Group Shuffler Bot: React on this message to enter group selection pool...")


        if message.content.startswith("in"):
            if not groupList.__contains__(str(message.author)):
                groupList.append(str(message.author))
                print(groupList)

        if message.content.startswith("out"):
            if groupList.__contains__(str(message.author)):
                groupList.remove(str(message.author))
                print("removed " + str(message.author))
                await message.channel.send("Removed " + str(message.author) + " from list")
                await asyncio.sleep(3)
                await message.delete()


        if message.content.startswith("end"):
            groupListFinal = groupList.copy()

            pair = []

            while groupListFinal.__sizeof__() != 0:
                #x is the groupID counter
                for x in range(0, int(((len(groupListFinal) // int(groupSize))))):

                    #y is the group size counter
                    for y in range(0, int(groupSize)):
                        random = randint(0, len(groupListFinal) -1)



                        holder = (groupListFinal[random])
                        pair.append(holder)
                        groupListFinal.remove(holder)

                        print("PAIR: ", pair)
                        print("List of members", groupListFinal)

                    await message.channel.send("Group " + str(x) + " : " + str(pair))
                    pair.clear()

client = MyClient()
client.run(TOKEN)