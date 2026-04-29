import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from geopy.distance import geodesic

# 1. SETUP
BOT_TOKEN = "8734845651:AAFU9kfnMn5g1f8fvd_DLTJCmzj34SsbBrc"
ADMIN_HANDLES = "@qallmen, @arabek127, @bzglnazerke"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class BotStates(StatesGroup):
    waiting_for_help = State()
    waiting_for_feedback = State()

# 2. DATA STORAGE
RESTAURANTS = [
    {"name": "Line Brew Astana", "desc": "One of the city’s most famous steakhouses. Known for premium meat, grilled dishes, and house beer.", "link": "https://2gis.kz/astana/search/Line%20Brew", "lat": 51.1491, "lon": 71.4241, "photo": "https://2gis.kz/astana/gallery/geo/70000001030035728/photoId/30258560193956857", "feeds": []},
    {"name": "Saksaul", "desc": "Classic Kazakh and Central Asian restaurant with traditional interior, plov, horse meat dishes, and shashlik.", "link": "https://2gis.kz/astana/search/Saksaul", "lat": 51.1272, "lon": 71.4334, "photo": "https://sxodim.com/uploads/posts/2023/05/15/original.jpg", "feeds": []},
    {"name": "Felice", "desc": "Upscale Italian restaurant with elegant atmosphere, pasta, seafood, and fine dining service.", "link": "https://2gis.kz/astana/search/Felice", "lat": 51.1250, "lon": 71.4250, "photo": "https://images.unsplash.com/photo-1559339352-11d035aa65de", "feeds": []},
    {"name": "The Kitchen", "desc": "Modern European restaurant popular for breakfasts, steaks, and business dinners.", "link": "https://2gis.kz/astana/search/The%20Kitchen", "lat": 51.1211, "lon": 71.4289, "photo": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4", "feeds": []},
    {"name": "Qazaq Gourmet", "desc": "Luxury modern Kazakh cuisine with national dishes presented in contemporary style.", "link": "https://2gis.kz/astana/search/Qazaq%20Gourmet", "lat": 51.1092, "lon": 71.4328, "photo": "https://qazaqgourmet.kz/img/gallery/1.jpg", "feeds": []},
    {"name": "Eternal sky (Вечное небо)", "desc": "Panoramic restaurant with skyline views and Asian-European menu.", "link": "https://2gis.kz/astana/search/Eternal%20sky", "lat": 51.1322, "lon": 71.4111, "photo": "https://images.unsplash.com/photo-1504674900247-0877df9cc836", "feeds": []},
    {"name": "On The Roof", "desc": "Rooftop restaurant known for atmosphere, cocktails, and city views.", "link": "https://2gis.kz/astana/search/On%20The%20Roof", "lat": 51.1280, "lon": 71.4310, "photo": "https://images.unsplash.com/photo-1533777857889-4be7c70b33f7", "feeds": []},
    {"name": "Kishlak", "desc": "Popular Uzbek restaurant with large portions, plov, and traditional Eastern cuisine.", "link": "https://2gis.kz/astana/search/Kishlak", "lat": 51.1550, "lon": 71.4100, "photo": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b", "feeds": []},
    {"name": "GINZA ASTANA", "desc": "Luxury restaurant and lounge with stylish interior and nightlife atmosphere.", "link": "https://2gis.kz/astana/search/GINZA", "lat": 51.1100, "lon": 71.4400, "photo": "https://images.unsplash.com/photo-1550966842-28ca260840bc", "feeds": []},
    {"name": "Portofino", "desc": "Elegant Italian restaurant often chosen for celebrations and romantic dinners.", "link": "https://2gis.kz/astana/search/Portofino", "lat": 51.1400, "lon": 71.4200, "photo": "https://images.unsplash.com/photo-1515003197210-e0cd71810b5f", "feeds": []},
    {"name": "Restaurant FARHI", "desc": "Well-known local restaurant with Kazakh and European dishes.", "link": "https://2gis.kz/astana/search/FARHI", "lat": 51.1600, "lon": 71.4300, "photo": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0", "feeds": []},
    {"name": "Grand Hall Astana", "desc": "Large upscale restaurant for banquets, family events, and traditional cuisine.", "link": "https://2gis.kz/astana/search/Grand%20Hall", "lat": 51.1520, "lon": 71.4250, "photo": "https://images.unsplash.com/photo-1519225421980-715cb0215aed", "feeds": []},
    {"name": "Astana Nury", "desc": "Popular restaurant with live music and traditional Kazakh-style atmosphere.", "link": "https://2gis.kz/astana/search/Astana%20Nury", "lat": 51.1650, "lon": 71.4210, "photo": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5", "feeds": []},
    {"name": "Roastbeef", "desc": "Highly rated steakhouse with premium meat and modern interior.", "link": "https://2gis.kz/astana/search/Roastbeef", "lat": 51.1200, "lon": 71.4300, "photo": "https://images.unsplash.com/photo-1544025162-d76694265947", "feeds": []},
    {"name": "Take Eat Easy", "desc": "Modern café-restaurant known for breakfasts and international dishes.", "link": "https://2gis.kz/astana/search/Take%20Eat%20Easy", "lat": 51.1350, "lon": 71.4450, "photo": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085", "feeds": []},
    {"name": "La Rivière", "desc": "Luxury Italian and Mediterranean fine dining restaurant.", "link": "https://2gis.kz/astana/search/La%20Riviere", "lat": 51.1450, "lon": 71.4180, "photo": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4", "feeds": []},
    {"name": "Salter's", "desc": "One of the best steak restaurants in the city according to reviews.", "link": "https://2gis.kz/astana/search/Salters", "lat": 51.1050, "lon": 71.4350, "photo": "https://images.unsplash.com/photo-1532592391327-9c18fd842702", "feeds": []},
    {"name": "Daredzhani", "desc": "Popular Georgian restaurant with khinkali and khachapuri.", "link": "https://2gis.kz/astana/search/Daredzhani", "lat": 51.1300, "lon": 71.4400, "photo": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38", "feeds": []},
    {"name": "Mökki", "desc": "Premium Italian restaurant with modern Scandinavian-inspired interior.", "link": "https://2gis.kz/astana/search/Mokki", "lat": 51.1150, "lon": 71.4250, "photo": "https://images.unsplash.com/photo-1543007630-9710e4a00a20", "feeds": []},
    {"name": "Cafe Momona", "desc": "Top-rated sushi and Pan-Asian restaurant. Popular among younger visitors and families.", "link": "https://2gis.kz/astana/search/Momona", "lat": 51.1290, "lon": 71.4220, "photo": "https://images.unsplash.com/photo-1553621042-f6e147245754", "feeds": []},
]

