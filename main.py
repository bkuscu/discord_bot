import discord
import os
import random
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

groupList = []
groupSize = 0
grpBool = False

now = datetime.now()
current_time = now.strftime("[ %d.%m.%y | %H:%M:%S ] ")


class MyClient(discord.Client):

    async def on_ready(self):
        f = open("logs.txt", "a")
        print("{} logged in.".format(client.user.name))
        f.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        f.write('\n')
        f.write(str(current_time) + "{} is online now..".format(client.user.name))
        f.write('\n')
        f.close()

    async def on_message(self, message):
        f = open("logs.txt", "a")
        global groupSize, grpBool, allGroups
        if message.content.startswith("grp"):
            await message.delete()
            grpBool = True
            groupSize = message.content.split(' ')[1]

            if int(groupSize) > 0:
                print("--------------------------------------------------------------------------------------")
                print("Groupsize for each group: " + str(groupSize))
                f.write("------------------------------------------------------------------------------------")
                f.write('\n')
                f.write(str(current_time) + "Group size for each group: " + str(groupSize))
                f.write('\n')

                await message.channel.send("Group Shuffler Bot: type: [$in] to enter OR [$out] to delete the entry"
                                           , delete_after=10)
                await message.channel.send("To end the selection and get the groups type [$end]"
                                           , delete_after=10)
            else:
                await message.channel.send("Please enter a group size >0 ", delete_after=4)

        if message.content.startswith("in"):
            await message.delete()
            if grpBool.__eq__(True):
                if not groupList.__contains__(str(message.author)):
                    groupList.append(str(message.author))
                    print("Added " + str(message.author) + " to list")
                    print("Current group pool: " + str(groupList))
                    await message.channel.send("Added: " + str(message.author), delete_after=10)
                    f.write(str(current_time) + "Added:" + str(message.author))
                    f.write('\n')
            else:
                await message.channel.send("Please create a group selection first.", delete_after=10)
                f.write(str(current_time) + "Please create a group selection first. @" + str(message.author))
                f.write('\n')

        if message.content.startswith("$out"):
            await message.delete()
            if grpBool.__eq__(True):
                if groupList.__contains__(str(message.author)):
                    groupList.remove(str(message.author))
                    print("Removed " + str(message.author) + "from list")
                    await message.channel.send("Removed " + str(message.author) + " from list", delete_after=10)
                    f.write(str(current_time) + "Removed:" + str(message.author) + " from list")
                    f.write('\n')
            else:
                await message.channel.send("Please create a group selection first.", delete_after=10)

        if message.content.startswith("end"):
            await message.delete()

            groupListFinal = groupList.copy()
            random.shuffle(groupListFinal)
            count = 1
            f.write(str(current_time) + "Shuffling...")
            f.write('\n')

            groupDict = {}

            while len(groupListFinal) >= int(groupSize):
                pair = groupListFinal[0:int(groupSize)]

                for x in pair:
                    groupListFinal.remove(x)
                await message.channel.send("Group " + str(count) + ": " + str(pair))

                groupDict[count] = str(pair)

                f.write(str(current_time) + "Group " + str(count) + ": " + str(pair))
                f.write('\n')
                pair.clear()
                count = count + 1

            print(groupDict)
            groupList.clear()
            grpBool = False
            f.write("------------------------------------------------------------------------------------")
            f.write('\n')
            print("--------------------------------------------------------------------------------------")

        f.close()


client = MyClient()
client.run(TOKEN)
