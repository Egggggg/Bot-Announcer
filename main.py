import asyncio
import discord
from discord.ext import commands
import sys
import threading
import tkinter as tk 
from tkinter.messagebox import showerror

message = ""
cid = ""
token = ""

send_button = ""

bot = commands.Bot(command_prefix="////")

async def send_message():
    global message
    global cid
    global token
    global send_button

    msg = message.get()
    id = cid.get()

    try:
        id = int(id)
    except(ValueError):
        showerror("Invalid ID", "Channel ID must be an int.")

        message.configure(state=tk.NORMAL)
        cid.configure(state=tk.NORMAL)
        token.configure(state=tk.NORMAL)
        send_button.configure(state=tk.NORMAL)

        return

    channel = bot.get_channel(id)

    #send to a text channel
    if channel == None:
        channel = bot.get_user(id)

        #dm a user
        if channel == None:
            showerror("Channel not found", f"Channel with ID {id} doesn't exist in a server your bot is in.")

            message.configure(state=tk.NORMAL)
            cid.configure(state=tk.NORMAL)
            token.configure(state=tk.NORMAL)
            send_button.configure(state=tk.NORMAL)
        else:
            try:
                await channel.send(msg)
            except(discord.errors.Forbidden):
                showerror("Blocked", "This user has blocked your bot. Do not try to get around it with another bot.")

            message.configure(state=tk.NORMAL)
            cid.configure(state=tk.NORMAL)
            token.configure(state=tk.NORMAL)
            send_button.configure(state=tk.NORMAL)
    else:
        try:
            await channel.send(msg)
        except(discord.errors.Forbidden):
            showerror("Blocked", "Your bot can't send messages in this channel.")

        message.configure(state=tk.NORMAL)
        cid.configure(state=tk.NORMAL)
        token.configure(state=tk.NORMAL)
        send_button.configure(state=tk.NORMAL)

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        global message
        global cid
        global token
        global send_button

        self.master.title("Bot Messenger")

        tk.Label(self.master, text="Message").grid(row=0)
        tk.Label(self.master, text="Channel ID").grid(row=1)
        tk.Label(self.master, text="Token").grid(row=2)

        message = tk.Entry(self.master, width=35)
        cid = tk.Entry(self.master, width=35)
        token = tk.Entry(self.master, width=35)
    
        send_button = tk.Button(self.master, text="Send", command=self.send)

        message.grid(row=0, column=1)
        cid.grid(row=1, column=1)
        token.grid(row=2, column=1)
        send_button.grid(row=3, column=0)

    def send(self):
        global message
        global cid
        global token
        global send_button
        global bot_thread

        #disables the entries and button while the message sends
        message.configure(state=tk.DISABLED)
        cid.configure(state=tk.DISABLED)
        token.configure(state=tk.DISABLED)
        send_button.configure(state=tk.DISABLED)

        asyncio.ensure_future(send_message())

def on_closing():
    sys.exit(0)

root = tk.Tk()
root.geometry("290x90")
root.resizable(0, 0)
app = Window(root)
root.protocol("WM_DELETE_WINDOW", on_closing)

def _bot():
    bot.run("BOT TOKEN GOES HERE")

bot_thread = threading.Thread(target=_bot)
bot_thread.daemon = True
bot_thread.start()

root.mainloop()