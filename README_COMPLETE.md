# Demeter - AI-Powered Agricultural Assistant

Demeter is an **offline-first**, AI-powered mobile application for farmers, built with **React Native** (frontend) and **Flask** (backend). It delivers personalized agricultural insights without constant internet, with multilingual voice support.

## 🚀 Features

### Current Features ✅
- **AI-Powered Crop Recommendations**: Soil and climate-based crop suggestions with confidence scores
- **Market Price Predictions**: Real-time price forecasting and yield estimates  
- **Risk Assessment**: Weather and agricultural risk analysis with actionable recommendations
- **Pest Detection**: Image-based pest identification with treatment suggestions
- **Financial Advisory**: Government scheme eligibility and loan recommendations
- **Natural Language Processing**: Query any agricultural question in plain language
- **Multilingual Support**: Translation services for local languages
- **Offline Capabilities**: Core functionality works without internet

### Planned Features 🔄
- Voice input/output capabilities
- Camera integration for pest detection
- Weather forecasting integration
- Advanced offline data synchronization
- Push notifications for alerts

---

## 🏗️ Architecture

### Backend (Flask)
- **Orchestrator System**: Routes queries to specialized AI agents
- **ML Agents**: 5 specialized agents (crop, market, risk, pest, finance)
- **Intent Classification**: Natural language understanding
- **Translation Service**: Multi-language support with mT5
- **RESTful API**: Clean, documented endpoints

### Frontend (React Native + Expo)
- **Cross-Platform**: iOS and Android support
- **Modern UI**: Clean, accessible interface
- **TypeScript**: Type-safe development
- **Offline-First**: Local data storage and sync

---

## 📦 Prerequisites

### General Requirements
- [Git](https://git-scm.com/downloads)
- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js (LTS)](https://nodejs.org/en/download/)
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/)

### For Mobile Development
- [Expo CLI](https://docs.expo.dev/get-started/installation/): `npm install -g @expo/cli`
- **Android**: [Android Studio](https://developer.android.com/studio) (for emulator)
- **iOS**: [Xcode](https://developer.apple.com/xcode/) (Mac only)
- **Physical Device**: [Expo Go](https://expo.dev/go) app

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Sukesh-2006-cse/demeter.git
cd demeter
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create ML models (for development)
python create_dummy_models.py

# Start Flask server
python main.py
```

✅ **Backend will run on**: `http://127.0.0.1:5000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment configuration
cp .env.example .env

# Start Expo development server
npx expo start
```

### 4. Run the App

**Options to run:**
- 📱 **Phone**: Scan QR code with Expo Go app
- 🤖 **Android Emulator**: Press `a` in terminal
- 🍎 **iOS Simulator**: Press `i` in terminal (Mac only)
- 🌐 **Web**: Press `w` in terminal

---

## 🔗 API Documentation

### Available Endpoints

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/health` | GET | System health check | ✅ |
| `/crop-recommendation` | POST | Soil-based crop suggestions | ✅ |
| `/market-prediction` | POST | Price and yield forecasts | ✅ |
| `/risk-assessment` | POST | Agricultural risk analysis | ✅ |
| `/pest-detection` | POST | Image-based pest identification | ✅ |
| `/query` | POST | Natural language queries | ✅ |
| `/languages` | GET | Supported languages | ✅ |

### Example API Usage

```bash
# Health Check
curl http://localhost:5000/health

# Crop Recommendation
curl -X POST http://localhost:5000/crop-recommendation \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90, "P": 42, "K": 43,
    "temperature": 25, "humidity": 80,
    "ph": 6.5, "rainfall": 200
  }'

# Natural Language Query
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"text": "What crop should I plant in sandy soil?"}'
```

---

## 🧪 Testing the System

### Backend Testing
```bash
cd backend

# Test individual agents
python -c "
from agents.crop_agent import CropAgent
agent = CropAgent('models')
result = agent.predict({'context': {'N': 90, 'P': 42, 'K': 43, 'temperature': 25, 'humidity': 80, 'ph': 6.5, 'rainfall': 200}})
print('Result:', result)
"

# Test API endpoints
curl http://localhost:5000/health
```

### Frontend Testing
1. Start the backend (port 5000)
2. Start the frontend (`npx expo start`)
3. Use Expo Go to scan QR code
4. Navigate through the app features

---

## ⚙️ Configuration

### Backend Configuration
- **Models**: Located in `backend/models/` (auto-generated dummy models)
- **Environment**: Configure via environment variables
- **Port**: Default 5000 (change in `main.py`)

### Frontend Configuration
- **API URL**: Set in `frontend/.env` (`EXPO_PUBLIC_API_URL`)
- **Features**: Enable/disable features via environment variables
- **Debug**: Set `EXPO_PUBLIC_DEBUG_MODE=true` for development

### Environment Variables
```bash
# Frontend (.env)
EXPO_PUBLIC_API_URL=http://localhost:5000
EXPO_PUBLIC_APP_NAME=Demeter
EXPO_PUBLIC_DEBUG_MODE=true
```

---

## 🏃‍♂️ Development Workflow

### Backend Development
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
python main.py           # Start development server
```

### Frontend Development
```bash
cd frontend
npx expo start           # Start Expo development server
```

### Key Development Files
- **Backend**: `main.py`, `agents/`, `orchestrator/`
- **Frontend**: `app/`, `services/api.ts`, `components/`

---

## 🛑 Stopping the Application

1. **Stop Frontend**: Press `Ctrl+C` in frontend terminal
2. **Stop Backend**: Press `Ctrl+C` in backend terminal
3. **Deactivate Python Environment**: Run `deactivate`

---

## 🔧 Troubleshooting

### Common Issues

**Backend won't start:**
- ✅ Check Python virtual environment is activated
- ✅ Verify all dependencies installed: `pip install -r requirements.txt`
- ✅ Ensure port 5000 is available

**Frontend connection issues:**
- ✅ Check backend is running on port 5000
- ✅ Verify API URL in `.env` file
- ✅ For physical device, use computer's IP address instead of `localhost`

**Mobile device connection:**
- ✅ Ensure computer and device on same WiFi network
- ✅ Update `EXPO_PUBLIC_API_URL` to use computer's IP address
- ✅ Example: `http://192.168.1.100:5000`

### Getting Help
- Check the `backend/server.log` for backend errors
- Use Expo development tools for frontend debugging
- Enable debug mode: `EXPO_PUBLIC_DEBUG_MODE=true`

---

## 📱 Current App Status

### ✅ Working Features
- Backend API with all 5 AI agents functional
- Natural language query processing
- Comprehensive agricultural recommendations
- Error handling and logging
- Basic frontend structure and navigation

### 🔄 In Development
- Complete frontend screen implementations
- Mobile-specific features (camera, offline storage)
- UI/UX polish and accessibility
- Comprehensive testing suite

### 🎯 Production Ready
- Backend API is production-ready
- ML models can be replaced with real trained models
- Frontend foundation is solid for rapid development

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

---

## 📞 Support

For questions or support:
- 📧 Create an issue in the GitHub repository
- 💬 Check existing issues for solutions
- 📖 Refer to this README for setup instructions

---

**🌱 Happy Farming with Demeter! 🌱**