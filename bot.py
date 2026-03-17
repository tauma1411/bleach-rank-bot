import discord
from discord.ext import commands
import json
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

characters = [
    "Giselle Gewelle",
    "Bazz-B",
    "Baraggan Louisenbairn",
    "Coyote Starrk",
    "Rukia Kuchiki",
    "Ulquiorra Cifer",
    "Mayuri Kurotsuchi",
    "Yoruichi Shihoin",
    "Gremmy Thoumeaux",
    "Toshiro Hitsugaya",
    "Uryu Ishida",
    "Royd Lloyd",
    "Tenjiro Kirinji",
    "Jugram Haschwalth",
    "Kisuke Urahara",
    "Byakuya Kuchiki",
    "Oetsu Nimaiya",
    "Askin Nakk Le Vaar",
    "Pernida Parnkgjas",
    "Shunsui Kyoraku",
    "Retsu Unohana",
    "Kenpachi Zaraki",
    "Lille Barro",
    "Senjumaru Shutara",
    "Gerard Valkyrie",
    "Sosuke Aizen",
    "Ichibe Hyosube",
    "Genryusai Yamamoto",
    "Ichigo Kurosaki",
    "Yhwach"
]

xp_levels = [
    0, 120, 260, 420, 600, 800, 1020, 1260, 1520, 1800,
    2100, 2420, 2760, 3120, 3500, 3900, 4320, 4760, 5220, 5700,
    6200, 6720, 7260, 7820, 8400, 9000, 9620, 10260, 10920, 11600
]

next_abilities = [
    "The Heat",
    "Arrogante",
    "Los Lobos",
    "Hakka no Togame",
    "Segunda Etapa",
    "Konjiki Ashisogi Jizo",
    "Shunko",
    "The Visionary",
    "Daiguren Hyorinmaru",
    "Antithesis",
    "The Yourself",
    "Kinpika",
    "The Balance",
    "Kannonbiraki Benihime Aratame",
    "Senbonzakura Kageyoshi",
    "Sayafushi",
    "The Deathdealing",
    "The Compulsory",
    "Katen Kyokotsu: Karamatsu Shinju",
    "Minazuki",
    "Nozarashi",
    "The X-Axis",
    "Shatatsu Karagara Shigarami no Tsuji",
    "The Miracle",
    "Kyoka Suigetsu",
    "Ichimonji",
    "Zanka no Tachi",
    "Tensa Zangetsu",
    "The Almighty",
    "Nível máximo"
]

image_files = {
    "Giselle Gewelle": "giselle.png",
    "Bazz-B": "bazzb.png",
    "Baraggan Louisenbairn": "baraggan.png",
    "Coyote Starrk": "starrk.png",
    "Rukia Kuchiki": "rukia.png",
    "Ulquiorra Cifer": "ulquiorra.png",
    "Mayuri Kurotsuchi": "mayuri.png",
    "Yoruichi Shihoin": "yoruichi.png",
    "Gremmy Thoumeaux": "gremmy.png",
    "Toshiro Hitsugaya": "hitsugaya.png",
    "Uryu Ishida": "uryu.png",
    "Royd Lloyd": "royd.png",
    "Tenjiro Kirinji": "tenjiro.png",
    "Jugram Haschwalth": "jugram.png",
    "Kisuke Urahara": "urahara.png",
    "Byakuya Kuchiki": "byakuya.png",
    "Oetsu Nimaiya": "oetsu.png",
    "Askin Nakk Le Vaar": "askin.png",
    "Pernida Parnkgjas": "pernida.png",
    "Shunsui Kyoraku": "shunsui.png",
    "Retsu Unohana": "unohana.png",
    "Kenpachi Zaraki": "zaraki.png",
    "Lille Barro": "lille.png",
    "Senjumaru Shutara": "senjumaru.png",
    "Gerard Valkyrie": "gerard.png",
    "Sosuke Aizen": "aizen.png",
    "Ichibe Hyosube": "ichibe.png",
    "Genryusai Yamamoto": "yamamoto.png",
    "Ichigo Kurosaki": "ichigo.png",
    "Yhwach": "yhwach.png"
}

def load_data():
    if not os.path.exists("database.json"):
        return {}

    try:
        with open("database.json", "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except:
        return {}

def save_data(data):
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_level(xp):
    level = 0
    for i in range(len(xp_levels)):
        if xp >= xp_levels[i]:
            level = i
    return level

def get_next_xp(level):
    if level + 1 < len(xp_levels):
        return xp_levels[level + 1]
    return None

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    data = load_data()
    user_id = str(message.author.id)

    if user_id not in data:
        data[user_id] = {"xp": 0}

    data[user_id]["xp"] += 20
    save_data(data)

    await bot.process_commands(message)

@bot.command()
async def rank(ctx):
    data = load_data()
    user_id = str(ctx.author.id)

    if user_id not in data:
        data[user_id] = {"xp": 0}
        save_data(data)

    xp = data[user_id]["xp"]
    level = get_level(xp)
    character = characters[level]
    next_ability = next_abilities[level]

    next_xp = get_next_xp(level)

    if next_xp is not None:
        xp_text = f"{xp} / {next_xp}"
        faltam = next_xp - xp
        next_text = f"**Próxima liberação:** {next_ability}\n**Falta para subir:** {faltam} XP"
    else:
        xp_text = f"{xp}"
        next_text = "**Status:** Rank máximo alcançado"

    embed = discord.Embed(
        title=f"Rank de {ctx.author.name}",
        color=0x2b2d31
    )

    embed.add_field(name="Personagem atual", value=character, inline=False)
    embed.add_field(name="XP", value=xp_text, inline=False)
    embed.add_field(name="Progresso", value=next_text, inline=False)

    image_filename = image_files.get(character)
    if image_filename:
        image_path = os.path.join("images", image_filename)
        if os.path.exists(image_path):
            file = discord.File(image_path, filename=image_filename)
            embed.set_thumbnail(url=f"attachment://{image_filename}")
            await ctx.send(file=file, embed=embed)
            return

    await ctx.send(embed=embed)

bot.run(TOKEN)