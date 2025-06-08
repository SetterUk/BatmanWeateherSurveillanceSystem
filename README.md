# 🦇 Batman Weather Surveillance System

A Batman-themed interactive weather bot that provides real-time weather information with the Dark Knight's signature style and personality. Get weather updates, forecasts, and tactical advice from Gotham's protector himself!

![Batman Weather Bot](https://img.shields.io/badge/Batman-Weather%20Bot-darkblue?style=for-the-badge&logo=batman)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🖼️ Batman Intro Preview

When you start the Weather Bot, you're greeted with an impressive Batman ASCII art:

```
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
⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠛⠛⠉⠉⠉⠁⠀⠀⠀
```

**"I am vengeance, I am the night, I am... your weather forecaster!"** 🦇

## 🌟 Features

### 🦇 Batman-Themed Experience
- **Immersive Batman persona** with authentic dialogue and responses
- **ASCII Batman logo** and themed visual elements
- **Gotham-style interface** with colored borders and formatting
- **Dynamic typing effects** for realistic conversation flow
- **Batman's tactical advice** based on weather conditions

### 🌤️ Weather Intelligence
- **Real-time weather data** using Open-Meteo API (no API key required!)
- **Current weather conditions** with temperature, humidity, and wind speed
- **7-day weather forecasts** for planning ahead
- **Global location support** with intelligent location detection
- **Weather code interpretation** with detailed condition descriptions

### 🎯 Smart Interaction
- **Natural language processing** for weather queries
- **Location extraction** from user input
- **Context-aware responses** based on conversation flow
- **FAQ system** for common questions
- **Session management** with user preferences

### 🛠️ Technical Features
- **Error handling** with graceful fallbacks
- **Progress indicators** and loading animations
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Clean, modular code structure**
- **No external API keys required**

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Internet connection for weather data

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Weather_Bot.git
   cd Weather_Bot
   ```

2. **Install dependencies**
   ```bash
   pip install requests
   ```

3. **Run the bot**
   ```bash
   python Weather_Bot.py
   ```

## 🎮 How to Use

### Starting the Bot
When you run the bot, Batman will introduce himself and provide a mission briefing with available commands.

### Basic Commands

#### Weather Queries
- `weather` - Get current weather for your location
- `weather in London` - Get weather for a specific city
- `forecast` - Get 7-day weather forecast
- `tomorrow weather` - Get tomorrow's weather

#### Location Management
- `set location` - Change your default location
- `change location` - Update your current location

#### Help & Information
- `help` - Get list of available commands
- `what can you do` - Learn about Batman's capabilities
- `version` - Check bot version information

#### Exit Commands
- `quit`, `exit`, or `bye` - End the session

### Example Interactions

```
🦇 Citizen: weather in New York
🦇 Batman: Let me fire up the Batmobile and head to New York...

╔══════════════════════════════════════════════════════════════╗
║                    BATMAN WEATHER INTEL                     ║
╠══════════════════════════════════════════════════════════════╣
║ 📍 Location: New York, United States                        ║
║ 🌡️  Temperature: 22°C                                       ║
║ 🌤️  Condition: Clear                                        ║
║ 💨 Wind Speed: 15 km/h                                      ║
║ ⏰ Last Updated: 14:30:25                                   ║
╚══════════════════════════════════════════════════════════════╝

╔══════════════════════════════════════════════════════════════╗
║                    BATMAN'S TACTICAL ADVICE                 ║
╚══════════════════════════════════════════════════════════════╝
🦇 Perfect weather for patrol. The streets are clear, citizen.
🦇 Comfortable temperature - no need for extra gear.
🦇 Light winds detected. Ideal conditions for surveillance.
```

## 🏗️ Project Structure

```
Weather_Bot/
│
├── Weather_Bot.py          # Main bot application
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies (optional)
```

## 🔧 Technical Details

### APIs Used
- **Open-Meteo Weather API** - Free weather data service
- **Open-Meteo Geocoding API** - Location coordinate resolution

### Key Components

#### WeatherBot Class
The main class that handles all bot functionality:

- **Weather Data Processing**: Fetches and formats weather information
- **Natural Language Processing**: Interprets user queries using regex patterns
- **Location Management**: Handles location detection and coordinate resolution
- **User Interface**: Manages colored output, animations, and formatting
- **Session Management**: Tracks user preferences and conversation state

#### Weather Intelligence
- Supports 70+ weather condition codes
- Provides temperature, humidity, wind speed, and precipitation data
- Offers tactical advice based on current conditions
- Includes weather icons and visual indicators

#### Batman Persona
- Authentic Batman dialogue and responses
- Gotham-themed terminology and references
- Dynamic flavor text and atmospheric elements
- Mission-oriented language and tactical advice

## 🎨 Customization

### Adding New Weather Responses
You can extend Batman's weather advice by modifying the `batweatheradvice()` method:

```python
def batweatheradvice(self, temp, condition, wind_speed, precipitation=0):
   
    advice = []
    
    if temp > 30:
        advice.append("🦇 Extreme heat detected. Stay hydrated, citizen!")
    
    return advice
```

### Customizing Batman's Personality
Modify the FAQ responses and dialogue in the `__init__` method:

```python
self.faqs = {
    "your custom question": "Batman's custom response here",
    
}
```

### Adding New Commands
Extend the natural language patterns in the `weather_rules` dictionary:

```python
'your_command': {
    'patterns': [
        r'your regex pattern here',
    ],
    'context_set': "your_context"
}
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Contribution Ideas
- Add more weather data sources
- Implement weather alerts and warnings
- Add support for different temperature units
- Create a GUI version
- Add weather maps and visualizations
- Implement weather history tracking
- Add more Batman dialogue variations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 About the Creator

**Koushik Upadhyay** - AI/ML Engineer & Innovator

🎯 **Mission**: Motivated and results-driven AI/ML Engineer passionate about driving innovation, enhancing system efficiency, and delivering impactful AI solutions.

🛠️ **Core Technologies**:
- Machine Learning & Deep Learning (TensorFlow, LLMs)
- AI Model Deployment (AWS, load balancing, auto-scaling)
- Programming Languages (Python, C++, Django)
- Cloud Platforms & Database Management

🎓 **Education**: Bachelor of Technology - Shri Rmadeobaba College of Engineering and Management

🏆 **Key Projects**:
- AWS Cloud Deployment with scalability and auto-scaling
- Spam Detection using NLP techniques
- Object Classification with AI image processing
- Generative Adversarial Networks (GANs) for synthetic image generation

📧 **Contact**: Koushik4067@gmail.com

---

## 🙏 Acknowledgments

- **Open-Meteo** for providing free weather API services
- **Batman/DC Comics** for the inspiration (this is a fan project)
- **Python Community** for excellent libraries and documentation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/Weather_Bot/issues) page
2. Create a new issue with detailed information
3. Include your Python version and operating system

## 🔮 Future Enhancements

- [ ] Weather alerts and notifications
- [ ] Historical weather data
- [ ] Weather maps integration
- [ ] Mobile app version
- [ ] Voice interaction support
- [ ] Multiple language support
- [ ] Weather-based activity suggestions
- [ ] Integration with smart home devices

---

**"I am vengeance, I am the night, I am... your weather forecaster!"** 🦇

*Made with ❤️ by Koushik Upadhyay - AI/ML Engineer & Batman fan*
