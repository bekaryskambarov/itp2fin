# ITP2FIN
# Astana Guide Bot

## Project Description
This is our final course project for the programming class. We developed an interactive Telegram bot that serves as a digital city guide for Astana. The main goal of this project is to help university students, tourists, and locals quickly discover popular city locations, get directions, and read or submit user feedback directly within Telegram.

## Main Functionalities
- Categorized Search: Users can browse locations sorted into specific types such as restaurants, parks, entertainment spots, and libraries.
- Distance Calculation: The bot prompts the user to share their live location. It then calculates the physical distance to nearby spots using the geopy library and sorts them so the closest ones appear first.
- Bilingual Support: The entire user interface, including buttons, information panels, and instructions, is fully localized in both Kazakh and Russian.
- Feedback and Ratings: Users can rate any location on a scale and type out text reviews. These submissions are processed and stored persistently in a database.
- External Maps Integration: Each place profile includes a direct 2GIS link, allowing users to build navigation routes instantly.

## Technologies and Tools
- Language: Python 3.13
- Core Framework: Aiogram 3.x (used for handling asynchronous updates and bot menus)
- Database System: SQLite3 (integrated engine for data storage)
- Hosting Platform: Railway Cloud Service (used for deployment and live operations)

## Python and OOP Concepts Applied
1. Object-Oriented Programming (Inheritance): To fulfill the OOP requirements of the assignment, we implemented class inheritance in our database structure. We built a parent class called `BaseDataManager` which sets up the database file path. The actual worker class, `DatabaseManager`, inherits from it and calls `super().__init__()` to reuse the setup code before running SQL commands.
2. Decorators: We used native framework decorators like `@dp.message()` and `@dp.callback_query()` across the main module. These handle incoming messages and button clicks seamlessly.
3. Environment Management (Security): For security reasons, we kept the Telegram bot token hidden. Instead of putting it in the plain text code where it could be leaked on GitHub, we used `os.getenv("BOT_TOKEN")` to fetch it securely from the host server.

## Local Installation and Setup
1. Clone the repository from GitHub:
   git clone https://github.com/bekaryskambarov/ITP2FIN.git
2. Navigate to the project folder:
   cd ITP2FIN
3. Install all required dependencies:
   pip install -r requirements.txt
4. Configure your Telegram bot token in your system environment.
5. Launch the application:
   python ITP2FIN/main.py
