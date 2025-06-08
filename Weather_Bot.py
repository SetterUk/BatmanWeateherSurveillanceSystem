import re
import requests
import time
import sys
import os
from datetime import datetime
from typing import Dict, Optional



class WeatherBot:
    def __init__(self):
        self.user_sessions = {}
        self.user_location = None

        self.weather_api_base = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_api_base = "https://geocoding-api.open-meteo.com/v1/search"
        
        self.batman_logo = """
⠀⠀⠀⢀⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡀⠀⠀⠀
⠀⠀⠀⣼⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣷⡀⠀⠀
⠀⠀⢠⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣇⠀⠀
⠀⠀⣾⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⡀⠀
⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⡟⠋⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠛⢿⣿⣿⣿⣿⡇
⢸⣿⣿⣿⣿⡀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀ ⣿⣿⣿⣿⡇
⠸⣿⣿⣿⣿⣷⣦⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⣠⣴⣿⣿⣿⣿⡇
⠀⢿⣿⣿⡟⠛⠛⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠛⢻⣿⣿⣿⠁
⠀⠘⢿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠋⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠏⠀
⠀⠀⠀⠙⠧⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣸⠿⠋⠀⠀
⠀⠀⠀⠀⠀⠀⠉⠓⠢⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡤⠴⠒⠋⠉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⡤⠒⠙⠿⣿⣿⣿⣿⣶⣶⣾⣿⣿⣿⡿⠟⠓⠢⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠉⣉⠁⠀⠀⠈⢉⠉⠀⠀⠀⠀⠀⠈⠑⢄⠀⠀⠀⠀⠀
⠀⣄⠀⡴⠁⠀⠀⠀⡆⠀⠀⠀⠾⠿⣶⣾⣷⣶⡿⠷⠀⠀⠀⢀⠇⠀⠀⠀⠳⡀⠀⠀⠀
⢰⣿⡿⣱⣦⣄⡀⣠⣷⠀⠀⠀⠀⠀⠀⠈⠃⠀⠀⠀⠀⠀⠀⢸⣄⡀⠀⣀⣤⣜⣶⣃⠀
⢳⣿⣱⣿⣿⣿⣿⣿⣿⣆⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣿⣿⣿⣿⣿⣿⣿⡞⣯⠆
⢀⣇⣿⣿⣿⣿⣿⣿⣿⡇⠀⢸⠀⠉⡏⣟⣿⡏⠏⠉⢹⠉⠈⣿⣿⣿⣿⣿⣿⣿⣿⢡⠀
⠸⣜⡿⣿⣿⢹⣿⣿⡿⠛⠻⠿⣿⣿⣿⣶⣶⣾⣷⣿⡿⠟⠛⢿⣿⣿⣿⡫⣿⣿⢿⣫⠀
⠀⠈⣽⣶⣾⣿⣿⡿⠁⠀⠀⠀⠀⠙⢿⣿⣿⣟⠋⠁⠀⠀⠀⠀⠻⣿⣿⣿⣮⣷⡏⠁⠀
⠀⢠⣿⣿⣿⣿⡿⢁⣀⣄⡀⠀⠀⢀⣾⣿⣿⣿⣧⠀⠀⠀⣀⣀⡀⢹⣿⣿⣿⣿⣿⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣼⣿⣿⣿⣿⣿⣤⣶⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⠀⠀
⠀⢸⠟⠉⠈⢙⣿⣿⣿⣿⣿⣿⣿⣿⠙⠻⣿⠟⢹⣿⣿⣿⣿⣿⣿⣿⣿⠛⠉⠙⢿⡆⠀
⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠁⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠁⠀
⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠛⠛⠉⠉⠉⠁⠀⠀⠀"""

        self.weather_icons = {
            "clear": "☀️",
            "cloudy": "☁️",
            "rain": "🌧️",
            "snow": "❄️",
            "storm": "⛈️",
            "fog": "🌫️",
            "windy": "💨"
        }

        self.weather_codes = {
            0: "clear", 1: "cloudy", 2: "partly_cloudy",
            3: "Overcast", 45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            56: "Light freezing drizzle", 57: "Dense freezing drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            66: "Light freezing rain", 67: "Heavy freezing rain",
            71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            85: "Slight snow showers", 86: "Heavy snow showers",
            95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
        }

        self.weather_rules = {
            'current_weather': {
                'patterns': [
                    r'\b(current|now|today|present)\b.*\b(weather|temperature|temp|condition)\b',
                    r'\bhow.*\b(weather|hot|cold|warm|cool)\b.*\b(today|now|currently)\b',
                    r'\bwhat.*\b(weather|temperature)\b.*\b(like|now|today)\b',
                    r'\bis it\b.*\b(hot|cold|warm|cool|raining|sunny|cloudy)\b',
                    r'\bweather\b.*\b(right now|currently|today)\b',
                    r'^\s*weather\s*$',
                    r'^\s*todays?\s+weather\s*$',
                    r'\bweather\s+(in|of|for|at)\s+[a-z]+',
                    r'\bweather\b.*\b[a-z]+\b',
                    r'\b[a-z]+\s+weather\b'
                ],
                'context_set': "current_weather"
            },
            'forecast': {
                'patterns': [
                    r'\b(tomorrow|next|future|forecast|upcoming)\b.*\b(weather|temperature|rain|snow)\b',
                    r'\bweather\b.*\b(tomorrow|next week|this week|weekend)\b',
                    r'\bwill it\b.*\b(rain|snow|be hot|be cold|be sunny)\b',
                    r'\b(7|seven|week|5|five|3|three)\b.*\b(day|days)\b.*\b(forecast|weather)\b',
                    r'\bforecast\b',
                    r'\bwhat.*weather.*\b(be like|expect)\b'
                ],
                'context_set': "forecast"
            }
        }

        self.faqs = {
            "working hours": "I patrol Gotham 24/7. The night never sleeps, and neither do I.",
            "hours": "I patrol Gotham 24/7. The night never sleeps, and neither do I.",
            "where are you": "I operate from the Batcave, but my surveillance covers the entire world.",
            "batcave": "I operate from the Batcave, but my surveillance covers the entire world.",
            "version": "I'm Batman Weather System v1.0 - constantly upgrading my crime-fighting capabilities.",
            "what can you do": "I provide weather intelligence and protect citizens with accurate forecasts. Justice never rests!",
            "capabilities": "I provide weather intelligence and protect citizens with accurate forecasts. Justice never rests!",
            "my capabilities": "I provide weather intelligence and protect citizens with accurate forecasts. Justice never rests!",
            "your capabilities": "I provide weather intelligence and protect citizens with accurate forecasts. Justice never rests!"
        }

        self.timepattern = {
            'today': [r'\btoday\b', r'\bnow\b', r'\bcurrently\b', r'\bpresent\b', r'\bcurrent\b'],
            'tomorrow': [r'\btomorrow\b', r'\btommorow\b', r'\bnext day\b'],
            'forecast': [r'\bforecast\b', r'\bweek\b', r'\bdays\b', r'\bfuture\b', r'\bupcoming\b', r'\bnext\b'],
            'this_week': [r'\bthis week\b', r'\bcurrent week\b'],
            'next_week': [r'\bnext week\b', r'\bupcoming week\b'],
            'weekend': [r'\bweekend\b', r'\bthis weekend\b', r'\bnext weekend\b'],
            'specific_day': [r'\bmonday|tuesday|wednesday|thursday|friday|saturday|sunday\b']
        }

        self.location = [
            r'\b(in|at)\s+([a-z]+(?:\s+[a-z]+)*)\b',
            r'\bweather\s+in\s+([a-z]+(?:\s+[a-z]+)*)\b',
            r'\bweather\s+of\s+([a-z]+(?:\s+[a-z]+)*)\b',
            r'\bweather\s+for\s+([a-z]+(?:\s+[a-z]+)*)\b',
            r'\b([a-z]+(?:\s+[a-z]+)*)\s+weather\b',
            r'\bchange location\b',
            r'\bdifferent city\b'
        ]

        self.temperature_units = {
            'celsius': ['c', 'celsius', '°c'],
            'fahrenheit': ['f', 'fahrenheit', '°f']
        }
        
    
        self.colors = {
            'RESET': '\033[0m',
            'BOLD': '\033[1m',
            'DIM': '\033[2m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'PURPLE': '\033[95m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'GRAY': '\033[90m'
        }

    def clear_screen(self):
        
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def typingeffect(self, text, delay=0.03):
        
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def printwthborder(self, text, border_char="═", color="CYAN"):
        
        border_length = len(text) + 4
        border = border_char * border_length
        
        print(f"{self.colors[color]}{border}{self.colors['RESET']}")
        print(f"{self.colors[color]}  {text}  {self.colors['RESET']}")
        print(f"{self.colors[color]}{border}{self.colors['RESET']}")
    
    def print_status(self, message, status_type="INFO"):
        
        icons = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "LOADING": "⏳"
        }
        colors = {
            "INFO": "CYAN",
            "SUCCESS": "GREEN", 
            "WARNING": "YELLOW",
            "ERROR": "RED",
            "LOADING": "PURPLE"
        }
        
        icon = icons.get(status_type, "ℹ️")
        color = colors.get(status_type, "CYAN")
        
        print(f"{self.colors[color]}{icon} {message}{self.colors['RESET']}")
    
    def loading(self, message, duration=2):
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                if time.time() >= end_time:
                    break
                sys.stdout.write(f"\r{self.colors['PURPLE']}{frame} {message}...{self.colors['RESET']}")
                sys.stdout.flush()
                time.sleep(0.1)
        
        sys.stdout.write(f"\r{self.colors['GREEN']}✅ {message} complete!{self.colors['RESET']}\n")
    
    def progressbar(self, current, total, width=30):
        
        percent = current / total
        filled = int(width * percent)
        bar = "█" * filled + "░" * (width - filled)
        
        sys.stdout.write(f"\r{self.colors['CYAN']}[{bar}] {percent:.1%}{self.colors['RESET']}")
        sys.stdout.flush()
        
        if current == total:
            print()
    
    def batmanintro(self):
        
        self.clear_screen()
        

        print(f"{self.colors['GRAY']}The night is dark...{self.colors['RESET']}")
        time.sleep(1)
        print(f"{self.colors['GRAY']}Gotham needs protection...{self.colors['RESET']}")
        time.sleep(1)
        print(f"{self.colors['YELLOW']}A shadow emerges...{self.colors['RESET']}")
        time.sleep(1)
        
        self.loading("Initializing Batman Weather System", 3)
        
        self.clear_screen()
        print(f"{self.colors['YELLOW']}{self.batman_logo}{self.colors['RESET']}")
        
        time.sleep(0.5)
        self.printwthborder("BATMAN WEATHER SURVEILLANCE SYSTEM", "═", "YELLOW")
        print()
        
        self.print_status("Batcave connection established", "SUCCESS")
        self.print_status("Weather satellites online", "SUCCESS") 
        self.print_status("Gotham surveillance active", "SUCCESS")
        print()
        
        welcome_msg = "🦇 Greetings, citizen. I am Batman, protector of Gotham and guardian of weather intel."
        self.typingeffect(f"{self.colors['CYAN']}{welcome_msg}{self.colors['RESET']}")
        print()

    def normalizeinput(self, input_text: str) -> str:
        processed = input_text.lower().strip()
        processed = re.sub(r'\s+', ' ', processed)

        contractions = {
            "can't": "cannot",
            "won't": "will not",
            "don't": "do not",
            "isn't": "is not",
            "aren't": "are not",
            "doesn't": "does not",
            "wasn't": "was not",
            "weren't": "were not",
            "hasn't": "has not",
            "haven't": "have not",
            "hadn't": "had not"
        }
        for contraction, full_form in contractions.items():
            processed = processed.replace(contraction, full_form)

        return processed

    def show_batman_logo(self):
        return self.batman_logo

    def batweatheradvice(self, temp, condition, wind_speed, precipitation=0):
        advice = []
        if temp >= 35:
            advice.append(f"🦇 Batman: It's scorching hot out there, citizen! Even the Batsuit's cooling system is working overtime.")
            advice.append(f"🦇 Batman: Apply sunscreen like you're suiting up for battle - SPF 30+ minimum!")
            advice.append(f"🦇 Batman: Stay hydrated. Even Batman needs his fluids to fight crime effectively.")
        elif temp >= 25:
            advice.append(f"🦇 Batman: Perfect weather for patrol. Light clothing recommended, citizen.")
            advice.append(f"🦇 Batman: Don't forget sunglasses - protect your eyes like I protect Gotham!")
        elif temp >= 15:
            advice.append(f"🦇 Batman: Mild weather detected. A light jacket should suffice for your mission.")
            advice.append(f"🦇 Batman: Perfect temperature for outdoor activities - just like my rooftop surveillance!")
        elif temp >= 5:
            advice.append(f"🦇 Batman: It's getting chilly, citizen. Layer up like the Dark Knight's armor!")
            advice.append(f"🦇 Batman: A warm coat is your shield against the cold - don't leave the cave without it!")
        else:
            advice.append(f"🦇 Batman: Freezing conditions detected! Bundle up like you're heading to the Arctic Batcave.")
            advice.append(f"🦇 Batman: Gloves, scarf, and thermal wear - essential gear for surviving this cold!")
        
        condition_lower = condition.lower()
        if any(word in condition_lower for word in ['rain', 'drizzle', 'shower']):
            advice.append(f"🦇 Batman: Rain detected! Grab your umbrella - it's your portable Bat-shelter.")
            advice.append(f"🦇 Batman: Waterproof gear recommended. Stay dry, citizen - soggy heroes are ineffective!")
            if precipitation > 10:
                advice.append(f"🦇 Batman: Heavy rainfall incoming! Consider postponing non-essential missions.")
        elif any(word in condition_lower for word in ['snow', 'blizzard']):
            advice.append(f"🦇 Batman: Snow alert! Wear boots with good grip - even Batman needs traction.")
            advice.append(f"🦇 Batman: Drive carefully, citizen. The roads are more treacherous than Gotham's alleys!")
        elif any(word in condition_lower for word in ['storm', 'thunder']):
            advice.append(f"🦇 Batman: Thunderstorm approaching! Seek shelter immediately - not even Batman fights lightning!")
            advice.append(f"🦇 Batman: Avoid tall objects and open areas. Stay indoors until the storm passes.")
        elif any(word in condition_lower for word in ['fog', 'mist']):
            advice.append(f"🦇 Batman: Foggy conditions detected! Visibility is limited - drive with extra caution.")
            advice.append(f"🦇 Batman: Use headlights even during the day. Be the beacon Gotham needs!")
        elif any(word in condition_lower for word in ['clear', 'sunny']):
            advice.append(f"🦇 Batman: Clear skies ahead! Perfect weather for your daily heroic activities.")
            advice.append(f"🦇 Batman: Excellent visibility for surveillance... I mean, sightseeing!")
        
        if wind_speed > 30:
            advice.append(f"🦇 Batman: High winds detected! Secure loose objects - even my cape needs extra attention!")
            advice.append(f"🦇 Batman: Be cautious with umbrellas - they might become projectiles!")
        elif wind_speed > 15:
            advice.append(f"🦇 Batman: Moderate winds present. Hold onto your hat, citizen!")
        
        batman_wisdom = [
            f"🦇 Batman: Remember, citizen - preparation is the key to victory, whether fighting crime or weather!",
            f"🦇 Batman: Stay alert, stay alive. Weather can be as unpredictable as Gotham's villains!",
            f"🦇 Batman: A wise citizen checks the weather before leaving their cave... I mean, home!",
            f"🦇 Batman: Weather preparedness is just another form of justice - protecting yourself and others!",
            f"🦇 Batman: The night may be dark, but your weather knowledge should always be bright!"
        ]
        
        import random
        advice.append(random.choice(batman_wisdom))
        
        return advice

    def show_creator_info(self):
        creator_info = f"""
{self.colors['CYAN']}🦇 Batman: Allow me to introduce my brilliant creator...{self.colors['RESET']}

{self.colors['YELLOW']}═══════════════════════════════════════════════════════════════════════════════{self.colors['RESET']}
{self.colors['BOLD']}{self.colors['CYAN']}                           🦇 KOUSHIK UPADHYAY 🦇{self.colors['RESET']}
{self.colors['BOLD']}{self.colors['CYAN']}                        AI/ML ENGINEER & INNOVATOR{self.colors['RESET']}
{self.colors['YELLOW']}═══════════════════════════════════════════════════════════════════════════════{self.colors['RESET']}

{self.colors['GREEN']}📧 Contact: Koushik4067@gmail.com{self.colors['RESET']}
{self.colors['GREEN']}📱 Phone: +91-{self.colors['RESET']}

{self.colors['PURPLE']}🎯 MISSION STATEMENT:{self.colors['RESET']}
{self.colors['WHITE']}Motivated and results-driven AI/ML Engineer seeking challenging roles within dynamic 
organizations to leverage expertise in machine learning, deep learning, and data-driven 
solutions. Passionate about driving innovation, enhancing system efficiency, and 
collaborating with cross-functional teams to deliver impactful AI solutions.{self.colors['RESET']}

{self.colors['BLUE']}🛠️ CORE TECHNOLOGIES & SKILLS:{self.colors['RESET']}
{self.colors['CYAN']}• Machine Learning & Deep Learning (TensorFlow, LLMs){self.colors['RESET']}
{self.colors['CYAN']}• AI Model Deployment (AWS, load balancing, auto-scaling){self.colors['RESET']}
{self.colors['CYAN']}• Programming Languages (Python, C++, Django){self.colors['RESET']}
{self.colors['CYAN']}• Cloud Platforms & Database Management{self.colors['RESET']}

{self.colors['PURPLE']}🎓 EDUCATION:{self.colors['RESET']}
{self.colors['WHITE']}• Bachelor of Technology - Shri Rmadeobaba College of Engineering and Management{self.colors['RESET']}
{self.colors['WHITE']}• 12th Grade - Modern School Dungarpur (Raj) - 91.4%{self.colors['RESET']}
{self.colors['WHITE']}• 10th Grade - Modern School Dungarpur (Raj) - 90.6%{self.colors['RESET']}

{self.colors['GREEN']}🏆 CERTIFICATIONS:{self.colors['RESET']}
{self.colors['CYAN']}• AI on Public Cloud Platforms{self.colors['RESET']}
{self.colors['CYAN']}• Generative AI: Tools, Techniques and Applications{self.colors['RESET']}

{self.colors['YELLOW']}🚀 KEY PROJECTS & ACHIEVEMENTS:{self.colors['RESET']}
{self.colors['WHITE']}• AWS Cloud Deployment - Successfully deployed multiple websites with scalability, 
  load balancing, and auto-scaling for optimized performance{self.colors['RESET']}

{self.colors['WHITE']}• AI & Machine Learning Projects:{self.colors['RESET']}
{self.colors['CYAN']}  - Spam Detection: ML model using NLP techniques{self.colors['RESET']}
{self.colors['CYAN']}  - Object Classification: AI system using image processing{self.colors['RESET']}
{self.colors['CYAN']}  - Generative Adversarial Networks (GANs): Synthetic image generation{self.colors['RESET']}

{self.colors['WHITE']}• Technical Expertise: Proficient in C++, Python, DBMS, AWS Cloud, 
  GitHub version control, and TensorFlow deep learning{self.colors['RESET']}

{self.colors['YELLOW']}═══════════════════════════════════════════════════════════════════════════════{self.colors['RESET']}
{self.colors['BOLD']}{self.colors['PURPLE']}🦇 Batman: This brilliant mind created me to serve and protect Gotham's citizens 
   with advanced weather intelligence. Together, we fight crime... and bad weather! 🦇{self.colors['RESET']}
{self.colors['YELLOW']}═══════════════════════════════════════════════════════════════════════════════{self.colors['RESET']}
"""
        return creator_info

    def extractlocation(self, user_input: str) -> Optional[str]:
        for pattern in self.location:
            match = re.search(pattern, user_input)
            if match:
                return match.group(2) if len(match.groups()) > 1 else match.group(1)
        return None

    def extracttime(self, user_input: str) -> Optional[str]:
        for time_key, patterns in self.timepattern.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    return time_key
        return None

    def greetings(self, user_input: str) -> Optional[str]:
        greetings = [
            r'\b(hi|hello|hey|greetings)\b',
            r'\b(how are you|how is it going|what\'s up)\b',
            r'\b(welcome|good to see you)\b'
        ]
        
        greeting_responses = [
            "Greetings, citizen. I am Batman. How can I assist you with weather surveillance today?",
            "The Dark Knight acknowledges your presence. What weather intel do you require?",
            "Gotham's protector is here. How may I serve your weather needs?",
            "Citizen, you have reached Batman's weather command center. State your request."
        ]
        
        for pattern in greetings:
            if re.search(pattern, user_input, re.IGNORECASE):
                import random
                return random.choice(greeting_responses)
        return None

    def farewell(self, user_input: str) -> Optional[str]:
        farewells = [
            r'\b(bye|goodbye|see you later|take care)\b',
            r'\b(thank you|thanks for your help)\b',
            r'\b(have a great day|have a nice day)\b'
        ]
        
        farewell_responses = [
            "Stay safe, citizen. Gotham's weather is under my protection. Call if you need me.",
            "The Dark Knight watches over Gotham's skies. Until we meet again, citizen.",
            "Your weather intel mission is complete. Batman out. 🦇",
            "Gotham's weather remains secure. The night calls, but I'll return when needed."
        ]
        
        for pattern in farewells:
            if re.search(pattern, user_input, re.IGNORECASE):
                import random
                return random.choice(farewell_responses)
        return None

    def checkfaq(self, user_input: str) -> str:
        user_input = user_input.lower()
        
       
        if any(phrase in user_input for phrase in ["system creator", "creator info", "who created", "who made you", "your creator", "creator", "created", "made"]):
            return self.show_creator_info()
        
        if any(phrase in user_input for phrase in ["change location", "set location", "my location", "update location"]):
            print("\n🦇 Batman: Let me fire up the Batmobile and head to your new location...")
            print("🦇 Batman: *Starting Bat-vehicle engines* 🚗💨")
            if self.askforlocation():
                arrival_message = f"🦇 Batman: I've arrived at {self.user_location}! *Bat-vehicle parked* 🦇\n🦇 Weather surveillance is now active for this location!"
                print(f"\n{self.colors['CYAN']}🦇 Batman:{self.colors['RESET']} {arrival_message}")
                
                
                self.loading("Accessing weather satellites", 1.5)
                weather_info = self.weatherinfo(None, "current_weather", show_travel=False)
                return weather_info
            else:
                return "🦇 Batman: Location patrol setup complete! Ask me about the weather."
        
        if any(phrase in user_input for phrase in ["batman", "bat logo", "show logo", "dark knight", "logo"]):
            return f"🦇 Here's the Batman logo for you!\n{self.show_batman_logo()}\n\n🦇 The Dark Knight protects Gotham... and your weather!"
        
        for keyword, answer in self.faqs.items():
            if keyword in user_input:
                return answer
        
        if "help" in user_input:
            return ("🦇 BATMAN WEATHER SURVEILLANCE SYSTEM - AVAILABLE COMMANDS:\n"
                   "• Weather intelligence (say 'weather' or 'today weather')\n" 
                   "• Weather forecast (say 'forecast' or 'weather tomorrow')\n"
                   "• Change patrol location (say 'change location' or 'set location')\n"
                   "• My patrol hours\n"
                   "• Batcave location\n"
                   "• System creator\n"
                   "• System version\n"
                   "• My capabilities\n"
                   "• Show Batman logo (say 'batman' or 'logo')\n"
                   "🦇 Gotham's weather is under my protection!")
        
        return ""

    def getlocationcoordinates(self, location_name):
        try:
            url = f"{self.geocoding_api_base}?name={location_name}&count=1&format=json"
            response = requests.get(url)
            data = response.json()
            
            if data.get('results'):
                result = data['results'][0]
                return {
                    'latitude': result['latitude'],
                    'longitude': result['longitude'],
                    'name': result['name'],
                    'country': result.get('country', '')
                }
            return None
        except:
            return None

    def askforlocation(self):
        print(f"\n{self.colors['YELLOW']}🦇 ═══════════════════════════════════════════════════════════════ 🦇{self.colors['RESET']}")
        print(f"{self.colors['YELLOW']}🦇                    LOCATION SETUP REQUIRED                    🦇{self.colors['RESET']}")
        print(f"{self.colors['YELLOW']}🦇 ═══════════════════════════════════════════════════════════════ 🦇{self.colors['RESET']}")
        
        self.typingeffect(f"{self.colors['CYAN']}🦇 Batman: I need to establish your coordinates for precise weather surveillance.{self.colors['RESET']}")
        print(f"{self.colors['WHITE']}🦇 Batman: What city requires my protection? {self.colors['GRAY']}(e.g., Nagpur, Mumbai, Delhi){self.colors['RESET']}")
        
        user_location = input(f"{self.colors['YELLOW']}🦇 Enter location: {self.colors['RESET']}")
        
        if user_location.strip():
            self.loading("Scanning global coordinates", 2)
            coords = self.getlocationcoordinates(user_location.strip())
            if coords:
                self.user_location = user_location.strip()
                self.print_status(f"Location locked: {coords['name']}, {coords.get('country', '')}", "SUCCESS")
                self.typingeffect(f"{self.colors['GREEN']}🦇 Batman: Excellent! Weather surveillance network activated for your location.{self.colors['RESET']}")
                return True
            else:
                self.print_status(f"Location '{user_location}' not found in database", "WARNING")
                self.typingeffect(f"{self.colors['YELLOW']}🦇 Batman: Setting Nagpur as default patrol zone.{self.colors['RESET']}")
                self.user_location = "Nagpur"
                return True
        else:
            self.typingeffect(f"{self.colors['CYAN']}🦇 Batman: No problem, citizen. Nagpur, Maharashtra will be your default location.{self.colors['RESET']}")
            self.user_location = "Nagpur"
            return True

    def weatherinfo(self, location, query_type, show_travel=True):
        if not location and not self.user_location:
            self.askforlocation()
        
        location_to_use = location or self.user_location or "Nagpur"
        
        
        if location and location != self.user_location and show_travel:
            print(f"\n🦇 Batman: Let me fire up the Batmobile and head to {location}...")
            print("🦇 Batman: *Starting Bat-vehicle engines* 🚗💨")
            
            print(f"\n{self.colors['YELLOW']}🦇 ═══════════════════════════════════════════════════════════════ 🦇{self.colors['RESET']}")
            print(f"{self.colors['YELLOW']}🦇                    LOCATION RECONNAISSANCE                     🦇{self.colors['RESET']}")
            print(f"{self.colors['YELLOW']}🦇 ═══════════════════════════════════════════════════════════════ 🦇{self.colors['RESET']}")
            
            self.typingeffect(f"{self.colors['CYAN']}🦇 Batman: Deploying surveillance to {location}...{self.colors['RESET']}")
            self.loading("Scanning global coordinates", 2)
        
        coords = self.getlocationcoordinates(location_to_use)
        if not coords:
            return f"🦇 Batman: I couldn't locate '{location_to_use}' in my surveillance network. Please try a different city."
        
        
        if location and location != self.user_location and show_travel:
            self.print_status(f"Target location: {coords['name']}, {coords.get('country', '')}", "SUCCESS")
            self.typingeffect(f"{self.colors['GREEN']}🦇 Batman: I've arrived at {coords['name']}! *Bat-vehicle parked* 🦇{self.colors['RESET']}")
            print(f"{self.colors['GRAY']}🦇 *Batman deploys weather monitoring equipment* 🛰️{self.colors['RESET']}")
            self.typingeffect(f"{self.colors['GREEN']}🦇 Weather surveillance is now active for this location!{self.colors['RESET']}")
            self.loading("Accessing weather satellites", 1.5)
        
        try:
            if query_type == "current_weather":
                weather_url = f"{self.weather_api_base}?latitude={coords['latitude']}&longitude={coords['longitude']}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
                response = requests.get(weather_url)
                
                if response.status_code == 200:
                    data = response.json()
                    current = data.get('current_weather', {})
                    
                    temp = current.get('temperature', 'N/A')
                    wind_speed = current.get('windspeed', 'N/A')
                    weather_code = current.get('weathercode', 0)
                    condition = self.weather_codes.get(weather_code, 'Unknown')
                    
                    location_name = f"{coords['name']}, {coords.get('country', '')}"
                    
                    weather_info = f"\n{self.colors['CYAN']}╔══════════════════════════════════════════════════════════════╗{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['CYAN']}║{self.colors['YELLOW']}                    BATMAN WEATHER INTEL                     {self.colors['CYAN']}║{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['CYAN']}╠══════════════════════════════════════════════════════════════╣{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['CYAN']}║{self.colors['WHITE']} 📍 Location: {location_name:<44} {self.colors['CYAN']}║{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['CYAN']}║{self.colors['WHITE']} 🌡️  Temperature: {temp}°C{' ' * (39 - len(str(temp)))} {self.colors['CYAN']}║{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['CYAN']}║{self.colors['WHITE']} 🌤️  Condition: {condition:<42} {self.colors['CYAN']}║{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['CYAN']}║{self.colors['WHITE']} 💨 Wind Speed: {wind_speed} km/h{' ' * (35 - len(str(wind_speed)))} {self.colors['CYAN']}║{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['CYAN']}║{self.colors['GRAY']} ⏰ Last Updated: {datetime.now().strftime('%H:%M:%S')}{' ' * (32)} {self.colors['CYAN']}║{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['CYAN']}╚══════════════════════════════════════════════════════════════╝{self.colors['RESET']}\n"
                    
                    
                    advice_list = self.batweatheradvice(temp, condition, wind_speed)
                    
                    weather_info += f"\n{self.colors['YELLOW']}╔══════════════════════════════════════════════════════════════╗{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['YELLOW']}║{self.colors['PURPLE']}                    BATMAN'S TACTICAL ADVICE                 {self.colors['YELLOW']}║{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['YELLOW']}╚══════════════════════════════════════════════════════════════╝{self.colors['RESET']}\n"
                    
                    for advice in advice_list:
                        weather_info += f"{self.colors['CYAN']}{advice}{self.colors['RESET']}\n"
                    
                    weather_info += f"\n{self.colors['CYAN']}╚══════════════════════════════════════════════════════════════╝{self.colors['RESET']}\n"
                    weather_info += f"{self.colors['GREEN']}🦇 Gotham's weather surveillance complete. Stay vigilant, citizen!{self.colors['RESET']}"
                    
                    return weather_info
            
            elif query_type == "forecast":
                weather_url = f"{self.weather_api_base}?latitude={coords['latitude']}&longitude={coords['longitude']}&daily=temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum,wind_speed_10m_max&timezone=auto&forecast_days=7"
                response = requests.get(weather_url)
                
                if response.status_code == 200:
                    data = response.json()
                    daily = data.get('daily', {})
                    
                    if daily:
                        dates = daily.get('time', [])
                        max_temps = daily.get('temperature_2m_max', [])
                        min_temps = daily.get('temperature_2m_min', [])
                        weather_codes = daily.get('weathercode', [])
                        precipitation = daily.get('precipitation_sum', [])
                        wind_speeds = daily.get('wind_speed_10m_max', [])
                        
                        forecast_info = f"{self.colors['CYAN']}🦇 Batman: 7-day weather forecast for {coords['name']}, {coords.get('country', '')}:{self.colors['RESET']}\n\n"
                        
                        day_names = ['Today', 'Tomorrow', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
                        
                        for i in range(min(7, len(dates))):
                            day_name = day_names[i]
                            date = dates[i]
                            max_temp = max_temps[i] if i < len(max_temps) else 'N/A'
                            min_temp = min_temps[i] if i < len(min_temps) else 'N/A'
                            weather_code = weather_codes[i] if i < len(weather_codes) else 0
                            rain = precipitation[i] if i < len(precipitation) else 0
                            wind = wind_speeds[i] if i < len(wind_speeds) else 'N/A'
                            
                            condition = self.weather_codes.get(weather_code, 'Unknown')
                            
                            forecast_info += f"{self.colors['YELLOW']}╔══════════════════════════════════════════════════════════════╗{self.colors['RESET']}\n"
                            forecast_info += f"{self.colors['YELLOW']}║{self.colors['WHITE']} 📅 {day_name} ({date}){' ' * (50 - len(day_name) - len(date))} {self.colors['YELLOW']}║{self.colors['RESET']}\n"
                            forecast_info += f"{self.colors['YELLOW']}╠══════════════════════════════════════════════════════════════╣{self.colors['RESET']}\n"
                            forecast_info += f"{self.colors['YELLOW']}║{self.colors['WHITE']} 🌡️ High: {max_temp}°C | Low: {min_temp}°C{' ' * (35 - len(str(max_temp)) - len(str(min_temp)))} {self.colors['YELLOW']}║{self.colors['RESET']}\n"
                            forecast_info += f"{self.colors['YELLOW']}║{self.colors['WHITE']} 🌤️ Condition: {condition}{' ' * (45 - len(str(condition)))} {self.colors['YELLOW']}║{self.colors['RESET']}\n"
                            forecast_info += f"{self.colors['YELLOW']}║{self.colors['WHITE']} �️ Precipitation: {rain}mm{' ' * (40 - len(str(rain)))} {self.colors['YELLOW']}║{self.colors['RESET']}\n"
                            forecast_info += f"{self.colors['YELLOW']}║{self.colors['WHITE']} 💨 Max Wind: {wind} km/h{' ' * (40 - len(str(wind)))} {self.colors['YELLOW']}║{self.colors['RESET']}\n"
                            forecast_info += f"{self.colors['YELLOW']}╚══════════════════════════════════════════════════════════════╝{self.colors['RESET']}\n"
                            
                            
                            avg_temp = (max_temp + min_temp) / 2 if isinstance(max_temp, (int, float)) and isinstance(min_temp, (int, float)) else max_temp
                            if i < 2:  
                                advice_list = self.batweatheradvice(avg_temp, condition, wind, rain)
                                forecast_info += f"{self.colors['PURPLE']}🦇 Batman's Tactical Advice for {day_name}:{self.colors['RESET']}\n"
                                for advice in advice_list[:2]:  
                                    forecast_info += f"{self.colors['CYAN']}{advice}{self.colors['RESET']}\n"
                            
                            forecast_info += "\n"
                        
                        forecast_info += f"{self.colors['GREEN']}🦇 Batman: Stay prepared, citizen. Weather can change as quickly as Gotham's criminal activity!{self.colors['RESET']}"
                        
                        return forecast_info
                    
            return "🦇 Batman: Weather surveillance systems are temporarily offline.Try again later."
                
        except Exception as e:
            return f"🦇 Batman: Error in weather surveillance: {str(e)}"

    def userinput(self, user_input: str) -> str:
        user_input_clean = self.normalizeinput(user_input)

        greeting_response = self.greetings(user_input_clean)
        if greeting_response:
            return greeting_response
        
        farewell_response = self.farewell(user_input_clean)
        if farewell_response:
            return farewell_response
        
        faq_response = self.checkfaq(user_input_clean)
        if faq_response:
            return faq_response

        location = self.extractlocation(user_input_clean)
        time = self.extracttime(user_input_clean)

        forecast_keywords = ['tomorrow', 'tommorow', 'forecast', 'week', 'days', 'future', 'upcoming', 'next day']
        weather_keywords = ['weather', 'temperature', 'temp', 'forecast', 'climate']
        
        is_forecast_request = (
            time in ['tomorrow', 'forecast', 'this_week', 'next_week', 'weekend', 'specific_day'] or
            any(word in user_input_clean for word in forecast_keywords) or
            (any(word in user_input_clean for word in weather_keywords) and 
             any(word in user_input_clean for word in forecast_keywords))
        )
        
        is_weather_request = (
            any(word in user_input_clean for word in weather_keywords) or
            any(word in user_input_clean for word in forecast_keywords) or
            time is not None
        )

        if is_weather_request:
            if is_forecast_request:
                return self.weatherinfo(location, "forecast")
            else:
                return self.weatherinfo(location, "current_weather")

        for rule, data in self.weather_rules.items():
            for pattern in data['patterns']:
                if re.search(pattern, user_input_clean):
                    context_set = data['context_set']
                    return self.weatherinfo(location, context_set)

        return "Sorry, I don't know that yet. Try asking about weather, my working hours, or type 'help' for more options."

    def run(self):
       
        self.batmanintro()
        
        
        print(f"{self.colors['CYAN']}╔══════════════════════════════════════════════════════════════╗{self.colors['RESET']}")
        print(f"{self.colors['CYAN']}║{self.colors['WHITE']}                        MISSION BRIEFING                        {self.colors['CYAN']}║{self.colors['RESET']}")
        print(f"{self.colors['CYAN']}╠══════════════════════════════════════════════════════════════╣{self.colors['RESET']}")
        print(f"{self.colors['CYAN']}║{self.colors['WHITE']} • Ask about weather: 'weather', 'forecast'                   {self.colors['CYAN']}║{self.colors['RESET']}")
        print(f"{self.colors['CYAN']}║{self.colors['WHITE']} • Set location: 'set location', 'change location'            {self.colors['CYAN']}║{self.colors['RESET']}")
        print(f"{self.colors['CYAN']}║{self.colors['WHITE']} • Get help: 'help', 'what can you do'                       {self.colors['CYAN']}║{self.colors['RESET']}")
        print(f"{self.colors['CYAN']}║{self.colors['WHITE']} • Exit system: 'quit', 'exit', 'bye'                        {self.colors['CYAN']}║{self.colors['RESET']}")
        print(f"{self.colors['CYAN']}╚══════════════════════════════════════════════════════════════╝{self.colors['RESET']}")
        print()
        
        conversation_count = 0
        
        while True:
           
            print(f"{self.colors['GRAY']}{'─' * 60}{self.colors['RESET']}")
            user_input = input(f"{self.colors['YELLOW']}🦇 Citizen: {self.colors['WHITE']}")
            print(f"{self.colors['RESET']}", end="")
            
            if user_input.lower().strip() in ['exit', 'quit', 'bye']:
                print(f"\n{self.colors['PURPLE']}🦇 ═══════════════════════════════════════════════════════════════ 🦇{self.colors['RESET']}")
                print(f"{self.colors['PURPLE']}🦇                    MISSION COMPLETE                           🦇{self.colors['RESET']}")
                print(f"{self.colors['PURPLE']}🦇 ═══════════════════════════════════════════════════════════════ 🦇{self.colors['RESET']}")
                
                farewell_messages = [
                    "Gotham's weather is secure. Stay safe, citizen!",
                    "The Dark Knight's watch continues. Until next time, citizen.",
                    "Weather surveillance complete. Gotham sleeps safely tonight.",
                    "Your mission is complete. The night calls, but I'll return when needed."
                ]
                
                import random
                farewell = random.choice(farewell_messages)
                self.typingeffect(f"{self.colors['CYAN']}🦇 Batman: {farewell}{self.colors['RESET']}")
                
                self.loading("Returning to Batcave", 2)
                print(f"{self.colors['GRAY']}🦇 *Batman disappears into the shadows*{self.colors['RESET']}")
                break

            if not user_input.strip():
                print(f"{self.colors['GRAY']}🦇 Batman: *Waiting in the shadows for your command...*{self.colors['RESET']}")
                continue

            try:
                response = self.userinput(user_input)
                
             
                print(f"\n{self.colors['CYAN']}🦇 Batman:{self.colors['RESET']} {response}")
                
                conversation_count += 1
                
                
                if conversation_count % 5 == 0:
                    flavor_texts = [
                        f"\n{self.colors['GRAY']}🦇 *The Dark Knight continues his vigilant watch over Gotham's weather...*{self.colors['RESET']}",
                        f"\n{self.colors['GRAY']}🦇 *Batman's weather surveillance network remains active...*{self.colors['RESET']}",
                        f"\n{self.colors['GRAY']}🦇 *Gotham's protector stands ready for your next weather inquiry...*{self.colors['RESET']}"
                    ]
                    import random
                    print(random.choice(flavor_texts))
                
            except Exception as e:
                self.print_status(f"System error detected: {str(e)}", "ERROR")
                print(f"{self.colors['RED']}🦇 Batman: Something's wrong in Gotham's weather system. Let me recalibrate...{self.colors['RESET']}")
                self.loading("Recalibrating systems", 1)
                print(f"{self.colors['GREEN']}🦇 Batman: Systems restored. Please try your request again.{self.colors['RESET']}")
            
            print() 

if __name__ == "__main__":
    bot = WeatherBot()
    bot.run()
