# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import random
import asyncio
import os
from database import DatabaseManager


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  #asegura que el bot pueda leer mensajes
intents.guilds = True  # Para detectar servidores

bot = commands.Bot(command_prefix="!", intents=intents, description="Soy Terra Bot 🌿, tu amiga ecológica en Discord.")

@bot.event
async def on_ready():
    print(f"Terra Bot está conectada como {bot.user}")
    await bot.change_presence(activity=discord.Game("Cuidando el planeta 🌱"))
    
    # Registrar servidores en los que está el bot
    for guild in bot.guilds:
        await DatabaseManager.add_or_update_server(str(guild.id), guild.name)
        print(f"📊 Servidor registrado: {guild.name}")
    
    #extensiones
    try:
        await bot.load_extension("utilities")
        print("✅ Extensión utilities cargada correctamente")
    except Exception as e:
        print(f"❌ Error al cargar utilities: {e}")

@bot.event
async def on_message(message):
    """Registra usuarios cada vez que envían un mensaje"""
    if message.author == bot.user:
        return
    
    # Registrar usuario y servidor
    try:
        await DatabaseManager.add_or_update_user(str(message.author.id), message.author.name)
        await DatabaseManager.add_or_update_server(str(message.guild.id), message.guild.name)
        await DatabaseManager.add_connection(str(message.author.id), str(message.guild.id))
    except Exception as e:
        print(f"Error registrando usuario: {e}")
    
    # Procesar comandos
    await bot.process_commands(message)


# commands!
@bot.command(name="commands", aliases=["comandos", "helpme"])
async def show_commands(ctx):
    """Lista todos los comandos disponibles."""
    embed = discord.Embed(
        title="🌿 Lista de comandos disponibles",
        description="Aquí tienes todos los comandos que Terra Bot puede usar:",
        color=0x2ecc71
    )

    # 🌿 Comandos del main.py
    embed.add_field(name="📌 !hola", value="El bot te saluda.", inline=False)
    embed.add_field(name="📌 !consejo", value="Te da un consejo ecológico 🌱", inline=False)
    embed.add_field(name="📌 !8ball <pregunta>", value="Haz una pregunta a la bola mágica 🎱", inline=False)

    # 🧩 Comandos del módulo utilities
    embed.add_field(name="🧮 !calculadora <op> <n1> <n2>",
                    value="Calculadora básica. Operaciones: +, -, *, /, **",
                    inline=False)

    embed.add_field(name="🎲 !dado <caras>",
                    value="Lanza un dado con la cantidad de caras que quieras. Ej: !dado 20",
                    inline=False)

    embed.add_field(name="🪙 !moneda",
                    value="Lanza una moneda (Cara o Cruz).",
                    inline=False)

    embed.add_field(name="🌍 !traductor <idioma> <texto>",
                    value="Traduce palabras a: es, en, fr, de, it, pt. Ej: !traductor en hola",
                    inline=False)

    embed.add_field(name="🌤️ !clima",
                    value="Muestra un clima simulado.",
                    inline=False)

    # Información del propio comando
    embed.add_field(name="📘 !commands / !comandos / !helpme",
                    value="Muestra este mensaje de ayuda.",
                    inline=False)

    embed.set_footer(text="🌿 Terra Bot - Cuidemos el planeta juntos 💚")

    try:
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Error al mostrar los comandos: {e}")



@bot.command()
async def hola(ctx):
    await ctx.send("🌿 ¡Hola! Soy Terra Bot, lista para ayudarte a cuidar el planeta 💚")

@bot.command()
async def consejo(ctx):
    consejos = [
        "🌱 Usa menos plástico y lleva tu propia botella reutilizable.",
        "💧 Cierra el grifo mientras te cepillas los dientes.",
        "🚲 Usa transporte sostenible cuando puedas.",
        "🌿 Planta un árbol o cuida una planta.",
        "🔌 Desconecta los aparatos que no estés usando para ahorrar energía."
        "🛍️ Lleva tu propia bolsa reutilizable cuando vayas de compras."
        "🥕 Apoya los productos locales, reducen transporte y contaminación."
        "🧴 Prefiere envases reciclables o rellenables."
    ]
    await ctx.send(random.choice(consejos))

@bot.command(name="8ball")
async def magic_ball(ctx, *, pregunta=None):
    """Haz una pregunta a la bola 8 mágica"""
    respuestas = [
        "Sí 🎱",
        "No 🎱",
        "Por supuesto 🎱",
        "Tal vez 🎱",
        "Nunca 🎱",
        "Absolutamente 🎱",
        "Definitivamente no 🎱",
        "Probablemente 🎱",
        "Seguro que sí 🎱",
        "De ninguna manera 🎱"
    ]
    
    if pregunta is None:
        await ctx.send("❌ Por favor, haz una pregunta. Uso: `!8ball ¿Tu pregunta?`")
        return
    
    respuesta = random.choice(respuestas)
    await ctx.send(f"🔮 Pregunta: *{pregunta}*\n\n✨ La bola 8 dice: **{respuesta}**")


# Ejecuta el bot
try:
    print("Iniciando el bot...")
    bot.run("MTQzNjc3ODg4OTkzNzU1MTM3MA.Gpldg6.pg0Evv8hdUN8Y96-r3JIKJ--4dwR84FO1TLyvA") 
except Exception as e:
    print(f"Error al iniciar el bot: {e}")
