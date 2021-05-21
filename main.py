import discord
import os
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

groupList = []
groupListFinal = []
groupSize = 0

class MyClient(discord.Client):

    async def on_ready(self):
        print("Group shuffler bot is active...")

    async def on_message(self, message):
        global groupSize, x
        if message.content.startswith("$grp"):
            groupSize = message.content.split(' ')[1]

            if int(groupSize) > 0:
                print("-------------------------------------------")
                print("Groupsize for each group: " + str(groupSize))


                await message.channel.send("Group Shuffler Bot: type: [$in] to enter OR [$out] to delete the entry"
                                           , delete_after=60)
            else:
                await message.channel.send("Please enter a group size >0 ", delete_after=4)


        if message.content.startswith("$in"):
            if not groupList.__contains__(str(message.author)):
                groupList.append(str(message.author))
                print("Added " + str(message.author) + " to list")
                print("Current group pool: " + str(groupList))
                await message.channel.send("Added: " + str(message.author), delete_after=4)

        if message.content.startswith("$out"):
            if groupList.__contains__(str(message.author)):
                groupList.remove(str(message.author))
                print("Removed " + str(message.author) + "from list")
                await message.channel.send("Removed " + str(message.author) + " from list", delete_after=4)


        if message.content.startswith("$end"):

            groupListFinal = groupList.copy()
            random.shuffle(groupListFinal)
            count = 1

            while len(groupListFinal) > 0:

                pair = groupListFinal[0:int(groupSize)]

                for x in pair:
                    groupListFinal.remove(x)

                await message.channel.send("Group " + str(count) + ": " + str(pair))
                pair.clear()
                count = count+1
            groupList.clear()
            print("-------------------------------------------")

client = MyClient()
client.run(TOKEN)