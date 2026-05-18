import sqlite3


class DatabaseManager:
    def __init__(self, db_path='astana_bot.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        self.seed_data_if_empty()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Places storage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS places (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                name TEXT UNIQUE,
                description TEXT,
                rating TEXT,
                average_receipt TEXT,
                link_2gis TEXT,
                lat REAL,
                lon REAL,
                photo_url TEXT
            )
        ''')
        # Persistent User Reviews
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_name TEXT,
                feedback TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_review(self, place_name, feedback):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reviews (place_name, feedback) VALUES (?, ?)", (place_name, feedback))
        self.conn.commit()

    def get_reviews_by_place(self, place_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT feedback FROM reviews WHERE place_name = ?", (place_name,))
        return [row[0] for row in cursor.fetchall()]

    def get_places_by_category(self, category):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT name, description, rating, average_receipt, link_2gis, lat, lon, photo_url FROM places WHERE category = ?",
            (category,))
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_all_places(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, description, rating, average_receipt, link_2gis, lat, lon, photo_url FROM places")
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def seed_data_if_empty(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM places")
        if cursor.fetchone()[0] > 0:
            return  # Already populated

        # 20 Restaurants
        restaurants = [
            ("Line Brew Astana", "Steakhouse, grills, premium meat", "4.8", "15000 KZT",
             "https://2gis.kz/astana/search/Line%20Brew", 51.1605, 71.4242),
            ("Saksaul", "Traditional Kazakh cuisine", "4.7", "8000 KZT", "https://2gis.kz/astana/search/Saksaul",
             51.1261, 71.4334),
            ("Qazaq Gourmet", "Modern Kazakh fine dining", "4.9", "25000 KZT",
             "https://2gis.kz/astana/search/Qazaq%20Gourmet", 51.1190, 71.4250),
            ("The Kitchen", "International cuisine", "4.5", "7000 KZT", "https://2gis.kz/astana/search/The%20Kitchen",
             51.1444, 71.4211),
            ("Roastbeef", "Steak & European menu", "4.6", "12000 KZT", "https://2gis.kz/astana/search/Roastbeef",
             51.1550, 71.4420),
            ("Wall Street", "Fusion / European", "4.4", "9000 KZT", "https://2gis.kz/astana/search/Wall%20Street",
             51.1285, 71.4310),
            ("La Rivière", "Premium European dining", "4.8", "20000 KZT", "https://2gis.kz/astana/search/La%20Riviere",
             51.1640, 71.4190),
            ("MÖKKI", "Fine dining / Scandinavian style", "4.7", "18000 KZT", "https://2gis.kz/astana/search/MOKKI",
             51.1242, 71.4265),
            ("Zina", "Modern restaurant & brunch", "4.5", "6500 KZT", "https://2gis.kz/astana/search/Zina", 51.1390,
             71.4150),
            ("Ocean Basket Kazakhstan", "Seafood specialist chain", "4.6", "8500 KZT",
             "https://2gis.kz/astana/search/Ocean%20Basket", 51.1331, 71.4225),
            ("Cafestar", "European café-restaurant", "4.4", "6000 KZT", "https://2gis.kz/astana/search/Cafestar",
             51.1270, 71.4340),
            ("Вечное небо Eternal sky", "Panoramic restaurant over Astana", "4.7", "11000 KZT",
             "https://2gis.kz/astana/search/Eternal%20sky", 51.1311, 71.4180),
            ("Cafe Momona", "Authentic Japanese cuisine", "4.5", "7500 KZT", "https://2gis.kz/astana/search/Momona",
             51.1480, 71.4390),
            ("Felice", "Elegant Italian restaurant", "4.7", "13000 KZT", "https://2gis.kz/astana/search/Felice",
             51.1210, 71.4290),
            ("NaNe Panasian Cuisine", "Flavorful Pan-Asian cuisine", "4.3", "5500 KZT",
             "https://2gis.kz/astana/search/NaNe", 51.1590, 71.4610),
            ("Osoba", "Rich Georgian cuisine", "4.6", "7000 KZT", "https://2gis.kz/astana/search/Osoba", 51.1620,
             71.4280),
            ("Focaccia", "Pizza & classic Italian", "4.5", "5000 KZT", "https://2gis.kz/astana/search/Focaccia",
             51.1150, 71.4080),
            ("Monte Bianco Nursaya", "European comfort food", "4.2", "6500 KZT",
             "https://2gis.kz/astana/search/Monte%20Bianco", 51.1277, 71.4366),
            ("Nasha Dacha", "Cozy Country-style restaurant", "4.6", "9500 KZT",
             "https://2gis.kz/astana/search/Nasha%20Dacha", 51.1820, 71.4010),
            ("Mari (ex. Marcello)", "Italian & European bistro", "4.5", "8000 KZT",
             "https://2gis.kz/astana/search/Mari", 51.1350, 71.4270)
        ]

        # 20 Parks
        parks = [
            ("Astana Central Park", "One of the oldest parks along the Ishim River with attractions.", "4.6",
             "Free Entry", "https://2gis.kz/astana/search/Central%20Park", 51.1632, 71.4145),
            ("Presidential Park", "Massive green park near Ak Orda with beautiful fountains.", "4.5", "Free Entry",
             "https://2gis.kz/astana/search/Presidential%20Park", 51.1245, 71.4485),
            ("Zheruyyq Park", "Beautiful landscaped park with thousands of trees and features.", "4.4", "Free Entry",
             "https://2gis.kz/astana/search/Zheruyyk", 51.1561, 71.4722),
            ("Zhetisu Park", "Modern thematic park inspired by the Zhetysu region.", "4.7", "Free Entry",
             "https://2gis.kz/astana/search/Zhetisu", 51.1382, 71.4410),
            ("Lovers Park", "Romantic urban park right near Khan Shatyr.", "4.6", "Free Entry",
             "https://2gis.kz/astana/search/Lovers%20Park", 51.1305, 71.4032),
            ("Linear Park", "Long modern pedestrian corridor connecting left bank spaces.", "4.6", "Free Entry",
             "https://2gis.kz/astana/search/Linear%20Park", 51.1250, 71.4210),
            ("Triathlon Park", "Sports-oriented park popular among runners and cyclists.", "4.7", "Free Entry",
             "https://2gis.kz/astana/search/Triathlon%20Park", 51.1490, 71.4450),
            ("Atatürk Park", "Compact, very clean, and calm neighborhood park.", "4.8", "Free Entry",
             "https://2gis.kz/astana/search/Ataturk", 51.1620, 71.4310),
            ("Bauyrzhan Momyshuly Park", "Large public park with playgrounds and shaded seating.", "4.5", "Free Entry",
             "https://2gis.kz/astana/search/Momyshuly%20Park", 51.1520, 71.4650),
            ("Expo 2017 park", "Modern landscaped park near the futuristic EXPO complex.", "4.6", "Free Entry",
             "https://2gis.kz/astana/search/Expo%20Park", 51.0910, 71.4180),
            ("Peace and Unity Alley", "Peaceful alley-park area near the Pyramid structure.", "4.6", "Free Entry",
             "https://2gis.kz/astana/search/Peace%20Alley", 51.1220, 71.4440),
            ("Park of the Birches", "Small but scenic natural-style park known for birch trees.", "4.9", "Free Entry",
             "https://2gis.kz/astana/search/Birch%20Park", 51.1710, 71.4550),
            ("Central Fountain", "Popular city relaxation area centered around custom lights.", "4.7", "Free Entry",
             "https://2gis.kz/astana/search/Central%20Fountain", 51.1610, 71.4190),
            ("Botanical Garden", "Largest botanical park in Astana with beautiful lakes and greenhouses.", "4.8",
             "Free Entry", "https://2gis.kz/astana/search/Botanical%20Garden", 51.1110, 71.4150),
            ("Green Belt Park", "Part of the eco-project forest belt around the city limits.", "4.5", "Free Entry",
             "https://2gis.kz/astana/search/Green%20Belt", 51.0500, 71.3800),
            ("Family Park Astana", "Family-oriented setup containing children's playgrounds.", "4.3", "Free Entry",
             "https://2gis.kz/astana/search/Family%20Park", 51.1420, 71.4810),
            ("River Embankment Park", "Long riverside walking strip with excellent skyline views.", "4.7", "Free Entry",
             "https://2gis.kz/astana/search/Embankment", 51.1680, 71.4110),
            ("Ethno Park", "Cultural setup with traditional structures and decor.", "4.4", "Free Entry",
             "https://2gis.kz/astana/search/Ethno%20Park", 51.1010, 71.4300),
            ("Student Park", "Calm green area near universities, popular among students.", "4.3", "Free Entry",
             "https://2gis.kz/astana/search/Student%20Park", 51.1550, 71.4990),
            ("Akbulak Riverside Park", "Riverside zone presenting modern urban configurations.", "4.5", "Free Entry",
             "https://2gis.kz/astana/search/Akbulak", 51.1510, 71.4520)
        ]

        # 20 Libraries
        libraries = [
            ("National Academic Library", "One of the largest libraries in KZ with 32 halls, located near Bayterek.",
             "4.9", "Free Access", "https://2gis.kz/astana/search/National%20Academic%20Library", 51.1275, 71.4241),
            ("NU Library", "Main library of Nazarbayev University with top-tier research collections.", "4.9",
             "Students/Permit", "https://2gis.kz/astana/search/NU%20Library", 51.0905, 71.3985),
            ("M. O. Auezov Central Library", "Historic public library offering reading halls and events.", "4.5",
             "Free Access", "https://2gis.kz/astana/search/Auezov%20Library", 51.1690, 71.4280),
            ("KAZGUU Library", "Academic library focusing on legal, social, and digital assets.", "4.6",
             "Students/Permit", "https://2gis.kz/astana/search/KAZGUU%20Library", 51.1180, 71.3690),
            ("Republican Scientific Library", "Specialized tech library serving STEM requirements.", "4.4",
             "Free Access", "https://2gis.kz/astana/search/Scientific%20Library", 51.1420, 71.4320),
            ("Central Youth Library", "Children and youth literary configuration with local clubs.", "4.5",
             "Free Access", "https://2gis.kz/astana/search/Youth%20Library", 51.1510, 71.4110),
            ("Eagilik Books & Coffee", "Cozy coffeehouse setting mixed with study resources.", "4.8", "Purchase Based",
             "https://2gis.kz/astana/search/Eagilik", 51.1622, 71.4215),
            ("Biblioteka Dlya Nezryachikh", "Specialized system setup optimized for visually impaired readers.", "4.7",
             "Free Access", "https://2gis.kz/astana/search/Biblioteka%20Nezryachikh", 51.1710, 71.3910),
            ("A.Gaidar Children's Library", "Children's literature focal point managing educational meets.", "4.4",
             "Free Access", "https://2gis.kz/astana/search/Gaidar%20Library", 51.1650, 71.4340),
            ("Biblioteka Pervogo Prezidenta", "Archives mapping historical development items.", "4.6", "Free Access",
             "https://2gis.kz/astana/search/Prezident%20Library", 51.1210, 71.4420),
            ("International Turkic Academy", "Research library focused on Turkic studies and historic timelines.",
             "4.7", "Research Permit", "https://2gis.kz/astana/search/Turkic%20Academy", 51.1195, 71.4390),
            ("Kitapkhana №5", "Local community library asset addressing neighborhood reads.", "4.1", "Free Access",
             "https://2gis.kz/astana/search/Kitapkhana%205", 51.1810, 71.4410),
            ("Massovaya Biblioteka №1", "Neighborhood public library serving the old center.", "4.2", "Free Access",
             "https://2gis.kz/astana/search/Massovaya%201", 51.1720, 71.4190),
            ("Massovaya Biblioteka №12", "Local district branch supporting general fiction.", "4.0", "Free Access",
             "https://2gis.kz/astana/search/Massovaya%2012", 51.1390, 71.4720),
            ("Massovaya Biblioteka General", "Public reading asset for regional citizens.", "4.1", "Free Access",
             "https://2gis.kz/astana/search/Massovaya%20General", 51.1550, 71.4480),
            ("Massovaya Biblioteka №2", "District library providing classic works and publications.", "4.2",
             "Free Access", "https://2gis.kz/astana/search/Massovaya%202", 51.1610, 71.4620),
            ("Centralized Library System", "Headquarters uniting 25 library arrays across the capital.", "4.5",
             "Free Access", "http://astana-library.kz", 51.1490, 71.4220),
            ("American Corner Astana", "English resource asset inside the National Academic library.", "4.8",
             "Free Access", "https://2gis.kz/astana/search/American%20Corner", 51.1275, 71.4241),
            ("Museum of Book", "Rare printings and historic publishing assets context.", "4.7", "Free Access",
             "https://2gis.kz/astana/search/Museum%20of%20Book", 51.1275, 71.4241),
            ("National Electronic Library", "KAZNEB operational physical station for digital archiving.", "4.6",
             "Online/Free", "http://kazneb.kz", 51.1275, 71.4241)
        ]

        # Dummy Image URL used across targets
        default_photo = "https://images.unsplash.com/photo-1549693578-d683be217e58?q=80&w=600&auto=format&fit=crop"

        for row in restaurants:
            cursor.execute(
                "INSERT OR IGNORE INTO places (category, name, description, rating, average_receipt, link_2gis, lat, lon, photo_url) VALUES ('rest', ?, ?, ?, ?, ?, ?, ?, ?)",
                (*row, default_photo))
        for row in parks:
            cursor.execute(
                "INSERT OR IGNORE INTO places (category, name, description, rating, average_receipt, link_2gis, lat, lon, photo_url) VALUES ('park', ?, ?, ?, ?, ?, ?, ?, ?)",
                (*row, default_photo))
        for row in libraries:
            cursor.execute(
                "INSERT OR IGNORE INTO places (category, name, description, rating, average_receipt, link_2gis, lat, lon, photo_url) VALUES ('lib', ?, ?, ?, ?, ?, ?, ?, ?)",
                (*row, default_photo))

        self.conn.commit()