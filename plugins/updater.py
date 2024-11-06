#mrismanaziz

import os
import sys
from os import environ, execle, system
import subprocess
from bot import Bot
from git import Repo
from git.exc import InvalidGitRepositoryError
from pyrogram import Client, filters
from pyrogram.types import Message

from config import ADMINS, LOGGER


def gen_chlog(repo, diff):
    up_repo = Repo().remotes[0].config_reader.get("url").replace(".git", "")
    ac_br = repo.active_branch.name
    ch_log = ""
    tldr_log = ""
    ch = f"Update for <a href={up_repo}/tree/{ac_br}>[{ac_br}]</a>:"
    ch_tl = f"Updates for {ac_br}:"
    d_form = "%d/%m/%y | %H:%M"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"\n{c.count()} [{c.committed_datetime.strftime(d_form)}]\n"
            f"<a href={up_repo.rstrip('/')}/commit/{c}>[{c.summary}]</a> {c.author}"
        )
        tldr_log += f"\n{c.count()} [{c.committed_datetime.strftime(d_form)}]\n[{c.summary}] {c.author}"
    if ch_log:
        return str(ch + ch_log), str(ch_tl + tldr_log)
    return ch_log, tldr_log


def updater():
    try:
        repo = Repo()
    except InvalidGitRepositoryError:
        repo = Repo.init()
        origin = repo.create_remote("upstream", UPSTREAM)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if "upstream" in repo.remotes:
        ups_rem = repo.remote("upstream")
    else:
        ups_rem = repo.create_remote("upstream", UPSTREAM)
    ups_rem.fetch(ac_br)
    changelog, tl_chnglog = gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    return bool(changelog)


@Bot.on_message(filters.command("update") & filters.user(ADMINS))
async def update(client, message):
    try:
        out = subprocess.check_output(["git", "pull"]).decode("UTF-8")
        if "Already up to date." in str(out):
            return await message.reply_text("Its already up-to date!")
        await message.reply_text(f"{out}")
    except Exception as e:
        return await message.reply_text(str(e))
    await message.reply_text("<b>Updated with default branch, restarting now.</b>")
    os.system(f"kill -9 {os.getpid()} && python3 main.py")


@Bot.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply_text("...")
        LOGGER(__name__).info("Bot Restarted!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("Bot Restarted!")
    os.system(f"kill -9 {os.getpid()} && python main.py")
