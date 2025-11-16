# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import random
import math

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calculadora(self, ctx, operacion: str, num1: float, num2: float):
        """Realiza cálculos matemáticos básicos
        Operaciones: +, -, *, /, **
        Uso: !calculadora + 5 3"""
        try:
            if operacion == "+":
                resultado = num1 + num2
            elif operacion == "-":
                resultado = num1 - num2
            elif operacion == "*":
                resultado = num1 * num2
            elif operacion == "/":
                if num2 == 0:
                    await ctx.send("❌ No se puede dividir entre cero.")
                    return
                resultado = num1 / num2
            elif operacion == "**":
                resultado = num1 ** num2
            else:
                await ctx.send("❌ Operación no válida. Usa: +, -, *, /, **")
                return
            
            await ctx.send(f"🧮 **{num1} {operacion} {num2} = {resultado}**")
        except Exception as e:
            await ctx.send(f"❌ Error en el cálculo: {e}")

    @commands.command()
    async def dado(self, ctx, caras: int = 6):
        """Lanza un dado con el número de caras que especifiques
        Uso: !dado 20"""
        if caras < 2:
            await ctx.send("❌ El dado debe tener mínimo 2 caras.")
            return
        
        resultado = random.randint(1, caras)
        await ctx.send(f"🎲 Lanzaste un dado de {caras} caras y salió: **{resultado}**")

    @commands.command()
    async def moneda(self, ctx):
        """Lanza una moneda al aire"""
        resultado = random.choice(["Cara 🪙", "Cruz 🪙"])
        await ctx.send(f"Lanzaste la moneda y salió: **{resultado}**")

    @commands.command()
    async def traductor(self, ctx, idioma: str, *, texto: str):
        """Traduce texto a otro idioma
        Idiomas soportados: es, en, fr, de, it, pt
        Uso: !traductor en Hola mundo"""
        
        traducciones = {
            "hola": {
                "en": "Hello",
                "fr": "Bonjour",
                "de": "Hallo",
                "it": "Ciao",
                "pt": "Olá",
                "es": "Hola"
            },
            "mundo": {
                "en": "World",
                "fr": "Monde",
                "de": "Welt",
                "it": "Mondo",
                "pt": "Mundo",
                "es": "Mundo"
            },
            "gracias": {
                "en": "Thank you",
                "fr": "Merci",
                "de": "Danke",
                "it": "Grazie",
                "pt": "Obrigado",
                "es": "Gracias"
            },
            "por favor": {
                "en": "Please",
                "fr": "S'il vous plaît",
                "de": "Bitte",
                "it": "Per favore",
                "pt": "Por favor",
                "es": "Por favor"
            },
            "buenos días": {
                "en": "Good morning",
                "fr": "Bonjour",
                "de": "Guten Morgen",
                "it": "Buongiorno",
                "pt": "Bom dia",
                "es": "Buenos días"
            }
        }
        
        idiomas_validos = ["es", "en", "fr", "de", "it", "pt"]
        
        if idioma.lower() not in idiomas_validos:
            await ctx.send(f"❌ Idioma no válido. Usa: {', '.join(idiomas_validos)}")
            return
        
        texto_lower = texto.lower()
        
        if texto_lower in traducciones and idioma.lower() in traducciones[texto_lower]:
            traduccion = traducciones[texto_lower][idioma.lower()]
            await ctx.send(f"🌍 **Traducción a {idioma.upper()}:** {traduccion}")
        else:
            await ctx.send(f"⚠️ No tengo traducción para '{texto}' a {idioma}. Palabras disponibles: {', '.join(traducciones.keys())}")

    @commands.command()
    async def clima(self, ctx):
        """Muestra info sobre el clima (simulado)"""
        climas = [
            "☀️ Soleado - Temperatura: 28°C - Humedad: 45%",
            "⛅ Parcialmente nublado - Temperatura: 22°C - Humedad: 60%",
            "🌧️ Lluvioso - Temperatura: 18°C - Humedad: 85%",
            "❄️ Frío - Temperatura: 5°C - Humedad: 50%",
            "⛈️ Tormentoso - Temperatura: 20°C - Humedad: 90%"
        ]
        
        clima = random.choice(climas)
        await ctx.send(f"🌤️ **Clima actual:** {clima}\n\n💚 Recuerda: ¡Cuida el planeta!")

async def setup(bot):
    await bot.add_cog(Utilities(bot))
