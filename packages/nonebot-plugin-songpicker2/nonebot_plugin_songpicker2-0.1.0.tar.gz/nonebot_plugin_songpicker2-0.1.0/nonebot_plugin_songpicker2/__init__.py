# import nonebot
from .data_source import dataGet, dataProcess
from nonebot.permission import Permission
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot import on_command

from nonebot import get_driver
from .config import Config
global_config = get_driver().config
config = Config(**global_config.dict())

dataget = dataGet()

songpicker = on_command(
    "点歌", permission=Permission(), priority=5)


@songpicker.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["songName"] = args


@songpicker.got("songName", prompt="歌名是？")
async def handle_songName(bot: Bot, event: Event, state: T_State):
    songName = state["songName"]
    songIdList = await dataget.songIds(songName=songName)
    if not songIdList:
        await songpicker.reject("没有找到这首歌，请发送其它歌名！")
    songInfoList = list()
    for songId in songIdList:
        songInfoDict = await dataget.songInfo(songId)
        songInfoList.append(songInfoDict)
    songInfoMessage = await dataProcess.mergeSongInfo(songInfoList)
    await songpicker.send(songInfoMessage)
    state["songIdList"] = songIdList


@songpicker.receive()
async def handle_songNum(bot: Bot, event: Event, state: T_State):
    songIdList = state["songIdList"]
    songNum = str(event.get_message()).strip()
    if not songNum.isdigit():
        await songpicker.finish()
    selectedSongId = songIdList[int(songNum)]
    
    songContent = [
        {
            "type": "music",
            "data": {
                "type": 163,
                "id": selectedSongId
            }
        }
    ]
    await songpicker.send(songContent)

    songCommentsDict = await dataget.songComments(songId=selectedSongId)
    songCommentsMessage = await dataProcess.mergeSongComments(songCommentsDict)
    commentContent = [
        {
            "type": "text",
            "data": {
                "text": "下面为您播送热评：\n"
            }
        },
        {
            "type": "text",
            "data": {
                "text": songCommentsMessage
            }
        }
    ]
    
    await songpicker.finish(commentContent)
