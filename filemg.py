import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import aiohttp

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Инициализация бота
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Событие при запуске бота
@bot.event
async def on_ready():
    print(f'{bot.user} успешно запущен!')

# Команда для списка файлов
@bot.command()
async def list_files(ctx, path='.'):
    if not os.path.exists(path):
        await ctx.send("Указанная директория не существует.")
        return
    try:
        items = os.listdir(path)
        files = [f for f in items if os.path.isfile(os.path.join(path, f))]
        folders = [f for f in items if os.path.isdir(os.path.join(path, f))]
        response = "**Файлы:**\n" + "\n".join(files) if files else "Файлы отсутствуют."
        response += "\n\n**Папки:**\n" + "\n".join(folders) if folders else "\nПапки отсутствуют."
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

# Команда для загрузки файла на Discord
@bot.command()
async def upload(ctx, filename: str):
    if not os.path.isfile(filename):
        await ctx.send("Файл не найден.")
        return
    try:
        with open(filename, 'rb') as f:
            await ctx.send(file=discord.File(f, filename))
    except Exception as e:
        await ctx.send(f"Ошибка при загрузке: {e}")

# Команда для скачивания файла с Discord
@bot.command()
async def download(ctx, url: str, filename: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(filename, 'wb') as f:
                        f.write(await resp.read())
                    await ctx.send(f"Файл {filename} успешно сохранён.")
                else:
                    await ctx.send("Не удалось скачать файл.")
    except Exception as e:
        await ctx.send(f"Ошибка: {e}")

# Запуск бота
bot.run(TOKEN)