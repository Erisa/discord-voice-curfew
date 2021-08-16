import asyncio
from asyncio.tasks import sleep
from datetime import time
import datetime
import discord
import aioschedule as schedule
import functools
import config
from discord.ext import tasks, commands

intents = discord.Intents.default()
intents.voice_states = True

textChannel = None
voiceChannel = None

lock_job = None
unlock_job = None

def isNowInTimePeriod(startTime, endTime, nowTime): 
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    else:
        return nowTime >= startTime or nowTime <= endTime 

async def send_message(target_channel_id, target_message = "", send_with_empty_channel = False):
    if (target_message == ""):
        print("requested to send message but skipping because no message was configured")
        return
    voiceChannel = client.get_channel(config.voicechannel_id)

    if (send_with_empty_channel == False and len(voiceChannel.members) == 0):
        print("requested to send message but skipping because no members are present to see it")
        return

    print("running send_message")
    target_channel = client.get_channel(target_channel_id)
    await target_channel.send(target_message)

async def lock():
    print("running lock")
    voiceChannel = client.get_channel(config.voicechannel_id)
    await voiceChannel.set_permissions(voiceChannel.guild.default_role, connect=False)
    for member in voiceChannel.members:
        await member.move_to(None)
    await send_message(config.textchannel_id, config.lock_message)

async def unlock():
    print("running unlock")
    voiceChannel = client.get_channel(config.voicechannel_id)
    await voiceChannel.set_permissions(voiceChannel.guild.default_role, connect=True)
    await send_message(config.textchannel_id, config.unlock_message, True)

async def task_test(string):
    print(string)

def checkManually():
    print("checking manually")

lock_job = schedule.every().day.at(config.lock_time_str).do(lock)
unlock_job = schedule.every().day.at(config.unlock_time_str).do(unlock)

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        voiceChannel = client.get_channel(config.voicechannel_id)
        overwrite = voiceChannel.overwrites_for(voiceChannel.guild.default_role)

        if (overwrite.connect == False):
            lock_state = True
        else:
            lock_state = False

        expected_lock_state = isNowInTimePeriod(lock_job.at_time, unlock_job.at_time, datetime.datetime.now().time())

        if (lock_state == False and expected_lock_state == True):
            print("Locking because state is inconsistent")
            await lock()
        elif (lock_state == True and expected_lock_state == False):
            print("Unlocking because state is inconsistent")
            await unlock()


    async def on_message(self, message):        
        if (message.author.id != config.owner):
            return

        if (message.content.startswith('!lock')):
            await lock()
            await message.reply("✅ I've locked the voice channel!")
        
        if message.content.startswith('!unlock'):
            await unlock()
            await message.reply("✅ I've unlocked the voice channel!")

    async def my_background_task(self):
        for key,value in config.warnings.items():
            schedule.every().day.at(key).do(send_message, config.textchannel_id, value)

        await self.wait_until_ready()
        while not self.is_closed():
            loop = asyncio.get_event_loop()
            await schedule.run_pending()
            await asyncio.sleep(3)

client = MyClient(intents=intents)

client.run(config.token)
