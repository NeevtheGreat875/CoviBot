import os
import discord
from discord.ext import commands
from discord import embeds
import os
from covid import Covid
from covid_india import states
import urllib
import INDICovid19
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import ARIMA

ctxCommand = "c!"
client = commands.Bot(command_prefix=ctxCommand, help_command=None)

@client.event
async def on_ready():
    print("Ready")


@client.command()
async def info(ctx):
    covid = Covid()
    covid.get_data()
    active = covid.get_total_active_cases()
    confirmed = covid.get_total_confirmed_cases()
    recovered = covid.get_total_recovered()
    deaths = covid.get_total_deaths()
    em = discord.Embed(title="Covid Information", color=discord.Color.red())
    em.add_field(name="Total Active Cases :space_invader: :", value=active)
    em.add_field(name="Total Confirmed Cases :hot_face: :", value=confirmed)
    em.add_field(name="Total Recovered Cases :muscle: :", value=recovered)
    em.add_field(name="Total Deaths :skull: :", value=deaths)
    await ctx.send(embed=em)


@client.command()
async def safezone(ctx, *, place=None):
    try:

        e = states.getdata(place)
        f = int(e["Active"])
        if f > 1000:
            issafe= "No"
        elif f < 1000:
            issafe = "Yes"

        em = discord.Embed(title=f"Information for {place}",
                           color=discord.Color.red())
        em.add_field(name="Active Cases :space_invader: : ", value=e['Active'])
        em.add_field(name="Total Cured Cases :muscle: :", value=e["Cured"])
        em.add_field(name="Total Deaths :skull: :", value=e["Death"])
        em.add_field(name="Safe to go? :thinking: :", value=issafe)

        await ctx.send(embed=em)
    except:
        em = discord.Embed(
            title="Try That Again",
            description=
            "Write a name after c!safezone <state_name> and with first letter capital."
        )
        await ctx.send(embed=em)


@client.command()
async def hospital(ctx, *, city=None):
    try:
        x = INDICovid19.TotalHospitalCountState()

        print(x[0])
        for y in x:

            if y['state'] == city:
                z = y
        emb = discord.Embed(title=f"Hospital Information for {city}",
                            color=discord.Color.green())
        emb.add_field(name="Total Hospitals :hospital:",
                      value=z['totalHospitals'])
        emb.add_field(name="Total Beds :bed: :", value=z['totalBeds'])

        await ctx.send(embed=emb)
    except:
        em = discord.Embed(
            title="Try That Again",
            description=
            "Write a name after c!hospital <state_name> and with first letter capital.",
            color=discord.Color.red())
        await ctx.send(embed=em)


@client.command()
async def test(ctx, *, symptoms=None):
    with open("symptoms.json", "r") as file:
        data = json.load(file)
    availible = []
    messageToSend = ""
    for i in data:
        availible.append(i["name"])
    have = []
    threshhold = 0
    if symptoms == None:
        em = discord.Embed(title="Please Enter Symptoms After The c!test!")
        em.add_field(name="Symptoms we evaluate:", value=availible)
        await ctx.send(embed=em)
        return

    for x in data:
        if x["name"] in symptoms:
            have.append(x["name"])
            threshhold += x["corr"]

    threshhold = round(threshhold, 1)
    if threshhold > 50 and threshhold < 76:
        messageToSend = "You should probably go and get tested!"
    elif threshhold > 75 and threshhold < 91:
        messageToSend = "You should become isolated and go get tested!"
    elif threshhold > 90:
        messageToSend = "GO GET CHECKED RIGHT NOW, AND DONT TOUCH ANYBODY"
    else:
        messageToSend = "No need to worry, just go on with daily life and ENJOY!"

    em = discord.Embed(
        title="Your Calculated Report",
        description=
        "This may not be the most accurate but may help you be more aware",
        color=discord.Color.green())
    em.add_field(name="Result", value=messageToSend)
    em.add_field(name="Threshold:", value=threshhold)
    em.set_footer(text="All our evaluation symptoms: " + str(availible))
    await ctx.send(embed=em)


@client.command()
async def predict(ctx):
    value_to_display, chart = ARIMA.get_results()
    chart.write_image("chart.png", width=1200, height=300, scale=2)
    file = discord.File("chart.png")
    await ctx.send(file=file)
    em = discord.Embed(
        title="ARIMA Model Forcast",
        description=
        "The machine learning model is of type ARIMA(autoregressive integrated moving average) Time Series Forcasting by statsmodels.",
        color=discord.Color.green())
    em.add_field(name="Predicted Tomorrow's:", value=int(value_to_display))
    await ctx.send(embed=em)

@client.command()
async def help(ctx):
  em = discord.Embed(title="Help for CoviBot", color = discord.Color.green())
  em.add_field(name = "c!help", value = "Sends this message")
  em.add_field(name ="c!safezone <state name>", value = "Sends the current covid data of a particular state and tells whether it is safe to visit or not")
  em.add_field(name ="c!hospital <state name>", value ="Sends the number of hospitals and beds available of a state")
  em.add_field(name ="c!predict",value = "Predicts the number of covid cases in India")
  em.add_field(name ="c!test",value = "Tests whether you have covid or not depending on your symptoms")
  em.add_field(name ="c!info",value = "Sends worldwide information of covid cases.")
  await ctx.send(embed = em)

def detection():
    covid_words = [
        "corona",
        "covid",
    ]

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        msg = message.content
        if any(word in msg.lower() for word in covid_words):
            em = discord.Embed(
                title="I heard you were talking about COVID 19",
                description="Check out covid info by typing c!info",
                color=discord.Color.green())
            await message.channel.send(embed=em)
        await client.process_commands(message)


detection()
client.run("secret_token")
