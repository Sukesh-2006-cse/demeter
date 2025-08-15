# Demeter

Demeter is an **offline-first**, AI-powered mobile application for farmers, built with **React Native** (frontend) and **Flask** (backend). It delivers personalized agricultural insights without constant internet, with multilingual voice support.

---

## 🚀 Features
- Offline-first operation
- AI-driven advisories
- Local language and dialect support
- Lightweight for low-cost devices

---

## 📦 Prerequisites

### General
- [Git](https://git-scm.com/downloads)
- [Python 3.9+](https://www.python.org/downloads/)
- [Node.js (LTS)](https://nodejs.org/en/download/)
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/)
- [Expo CLI](https://docs.expo.dev/get-started/installation/)

### For React Native Development
- **Android Studio** (for Android emulator) or **Xcode** (for iOS, Mac only)
- Optional: Physical device with [Expo Go](https://expo.dev/go)

---

## 📥 Clone the Repository

```bash
git clone https://github.com/Sukesh-2006-cse/demeter.git
cd demeter
🖥 Backend Setup (Flask)
bash
Copy
Edit
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
The backend will run on:

cpp
Copy
Edit
http://127.0.0.1:5000
📱 Frontend Setup (React Native)
bash
Copy
Edit
cd frontend
npm install
# or
yarn install

# Start Expo development server
npx expo start
Run options:

Phone: Scan QR code with Expo Go

Emulator: Press a (Android) or i (iOS) in the terminal

🔗 Connecting Frontend & Backend
Update the API base URL in the frontend configuration file (e.g., config.js or .env):

javascript
Copy
Edit
export const API_URL = "http://127.0.0.1:5000";
For testing on a real phone, replace 127.0.0.1 with your computer’s local IP address.

🛑 Stopping the App
In each terminal, press:

objectivec
Copy
Edit
CTRL + C
To deactivate the Python virtual environment:

bash
Copy
Edit
deactivate
📄 License
This project is licensed under the MIT License — see the LICENSE file for details.

yaml
Copy
Edit

---

If you want, I can also **add installation screenshots and a folder structure diagram** so your README looks more professional and beginner-friendly. That way, even someone new to React Native or Flask can follow without guesswork.
