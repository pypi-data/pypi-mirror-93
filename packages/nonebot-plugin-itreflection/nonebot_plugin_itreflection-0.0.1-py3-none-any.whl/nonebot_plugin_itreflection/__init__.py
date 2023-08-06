# import nonebot
from os import stat
from nonebot import get_driver
from nonebot import on_command
from nonebot.permission import Permission
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State

from nonebot.log import logger

import sys

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())


itreflection = on_command("开始交互反射")


@itreflection.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args == "q":
        await itreflection.finish("已退出交互反射流程")
    elif "receivingMethod" in state:
        if state["receivingMethod"] == "消息":
            state["newFuncSourceText"] = args
        if state["receivingMethod"] == "链接":
            state["newFuncSourceURL"] = args
        if state["receivingMethod"] == "文件":
            state["newFuncSourceFile"] = args

    elif "rawFuncName" in state:
        state["receivingMethod"] = args

    elif "rawModuleName" in state:
        state["rawFuncName"] = args

    elif args:
        state["rawModuleName"] = args


@itreflection.got("rawModuleName", prompt="请输入需被反射的模块名：")
async def handle_rawModuleName(bot: Bot, event: Event, state: T_State):
    rawModuleName = state["rawModuleName"]
    if rawModuleName not in sys.modules:
        await itreflection.reject("未import该模块！")
    logger.debug("rawModuleName state recorded")


@itreflection.got("rawFuncName", prompt="请输入该模块中的方法名：")
async def handle_rawFuncName(bot: Bot, event: Event, state: T_State):
    rawModuleName = state["rawModuleName"]
    rawFuncName = state["rawFuncName"]
    if not hasattr(__import__(rawModuleName), rawFuncName):
        await itreflection.send(dir(__import__(rawModuleName)))
        await itreflection.reject("模块内只有以上方法！！")
    logger.debug("rawFuncName state recorded")


@itreflection.got("receivingMethod", prompt="请输入接收代码的方法（消息/链接/文件）：")
async def handle_reflectMethod(bot: Bot, event: Event, state: T_State):
    pass


@itreflection.got("newFuncSourceText", prompt="已选择消息模式，请直接发送代码")
async def handle_newFuncSourceText(bot: Bot, event: Event, state: T_State):
    rawModuleName = state["rawModuleName"]
    rawFuncName = state["rawFuncName"]
    newFuncSourceText = state["newFuncSourceText"]

    rawModule=__import__(rawModuleName)
    fileFuncDict = dict()
    exec(newFuncSourceText, globals(), fileFuncDict)
    newFunc, = fileFuncDict.values()
    print("DEBUG!!!!",getattr(rawModule, rawFuncName))
    setattr(rawModule, rawFuncName, newFunc)
    print("DEBUG!!!!",dir(rawModule))
    print("DEBUG!!!!",getattr(rawModule, rawFuncName))
    await itreflection.finish("反射完成")
