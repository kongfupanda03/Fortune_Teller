# ✨ Constellation Fortune Teller - Full Stack Edition

A beautiful, secure full-stack web application that provides personalized fortune readings based on zodiac constellations. Features include user authentication, static zodiac fortune displays, and a live AI-powered chatbot named Celestia!

## 🌟 Features

### 🔐 User Authentication
- **Secure Registration**: Create an account with username, email, and password
- **JWT-Based Login**: Secure token-based authentication
- **Session Management**: Persistent login with localStorage
- **MySQL Database**: Robust data storage for users and chat history

### 🔮 Zodiac Fortune Reading
- **12 Zodiac Signs**: Complete coverage with beautiful UI
- **Daily Fortunes**: Unique readings for each sign
- **Cosmic Energy Meters**: Visual Love, Career, Health, Finance energies
- **Lucky Numbers & Colors**: Personalized recommendations
- **Compatibility Insights**: Discover aligned zodiac signs

### 💬 AI Chat with Celestia
- **Live Conversations**: Chat with an AI fortune teller
- **Personalized Readings**: Context-aware responses
- **Chat History**: Saved conversations in database
- **Multi-Topic Guidance**: Love, career, health, finances

### 🎨 Beautiful Design
- **Modern UI**: Gradient designs with smooth animations
- **Responsive**: Works on desktop, tablet, and mobile
- **Secure**: Password hashing with bcrypt
- **Professional**: Organized backend and frontend structure

## 📁 Project Structure

```
fortune_teller/
│
├── backend/                # Python FastAPI backend
│   ├── server.py          # Main server with all endpoints
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── auth.py            # Authentication utilities
│   ├── init_db.py         # Database initialization script
│   └── requirements.txt   # (duplicate, can be removed)
│
├── frontend/              # Static frontend files
│   ├── index.html         # Main HTML with auth UI
│   ├── style.css          # Complete styling
│   └── script.js          # Client-side logic
│
├── run.py                 # ⭐ Main entry point - RUN THIS!
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this!)
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **MySQL 5.7+** or **MariaDB** - [Download MySQL](https://dev.mysql.com/downloads/)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

### Installation

#### 1. **Set Up MySQL Database**

First, create a MySQL database for the application:

```sql
-- Login to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE fortune_teller CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user (optional, recommended for production)
CREATE USER 'fortune_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON fortune_teller.* TO 'fortune_user'@'localhost';
FLUSH PRIVILEGES;

-- Exit MySQL
EXIT;
```

#### 2. **Install Python Dependencies**

```bash
cd fortune_teller
pip install -r requirements.txt
```

Or use a virtual environment (recommended):

```bash
cd fortune_teller
python -m venv venv

# Activate it:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

pip install -r requirements.txt
```

#### 3. **Configure Environment Variables**

Create a `.env` file in the **project root** (fortune_teller/):

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
PORT=3000

# JWT Secret Key - Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-generated-secret-key-here

# MySQL Database Configuration
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/fortune_teller
# Or with custom user:
# DATABASE_URL=mysql+pymysql://fortune_user:your_secure_password@localhost:3306/fortune_teller
```

**Important:**
- Get your OpenAI API key from https://platform.openai.com/api-keys
- Generate a secure SECRET_KEY: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- Update DATABASE_URL with your actual MySQL credentials

#### 4. **Initialize the Database**

```bash
cd backend
python init_db.py
cd ..
```

This will create all necessary tables (users, chat_sessions, chat_messages).

#### 5. **Start the Server**

Simply run from the project root:

```bash
python run.py
```

Or:

```bash
python3 run.py
```

You should see:
```
============================================================
🔮 Constellation Fortune Teller - Starting Server
============================================================
🚀 Server: http://localhost:3000
📚 API Docs: http://localhost:3000/docs
📡 Health Check: http://localhost:3000/api/health
============================================================

✨ Press CTRL+C to stop the server
```

#### 6. **Open Your Browser**

Navigate to: **http://localhost:3000**

## 📖 How to Use

### First Time Setup

1. **Register an Account**
   - Click the "Register" tab
   - Enter username, email, and password (min 6 characters)
   - Click "Create Account"
   - You'll be automatically logged in

2. **Or Login**
   - If you already have an account, use the "Login" tab
   - Enter your credentials
   - Your session will persist until logout

### Using the App

#### Zodiac Fortune Mode
1. Click "Zodiac Fortune" tab
2. Select your zodiac sign
3. View comprehensive reading with:
   - Daily fortune message
   - Energy levels for all life aspects
   - Lucky numbers and color
   - Compatibility insights
   - Personalized advice

#### Chat with Celestia
1. Click "Chat with Celestia" tab
2. Type your questions about fortunes, zodiac, life guidance
3. Celestia remembers conversation context
4. Your chat history is saved to the database

**Example Questions:**
- "I'm a Leo, what's in store for me this week?"
- "Can you give me guidance about my career?"
- "What should I focus on in my love life?"
- "Tell me my fortune for today"

## 🛠️ Technical Stack

### Backend
- **Python 3.8+**: Modern Python
- **FastAPI**: High-performance async framework
- **SQLAlchemy**: Powerful ORM
- **MySQL/PyMySQL**: Relational database
- **OpenAI API**: GPT-4o-mini for AI chat
- **JWT (python-jose)**: Secure authentication
- **Passlib**: Password hashing with bcrypt
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern styling with gradients/animations
- **Vanilla JavaScript**: No framework dependencies
- **LocalStorage**: Token persistence
- **Fetch API**: Async HTTP requests

### Security
- **Password Hashing**: bcrypt with salts
- **JWT Tokens**: Secure, stateless authentication
- **HTTPS Ready**: Production-ready security
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS**: Configurable cross-origin policies

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info (requires auth)

### Chat
- `POST /api/chat` - Send message to AI (requires auth)
- `POST /api/clear-history` - Clear chat history (requires auth)

### Health
- `GET /api/health` - Health check with database status
- `GET /docs` - Auto-generated API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## 💾 Database Schema

### Users Table
```sql
- id (INT, PRIMARY KEY)
- username (VARCHAR, UNIQUE)
- email (VARCHAR, UNIQUE)
- hashed_password (VARCHAR)
- created_at (DATETIME)
```

### Chat Sessions Table
```sql
- id (INT, PRIMARY KEY)
- user_id (INT, FOREIGN KEY)
- session_id (VARCHAR, UNIQUE)
- created_at (DATETIME)
```

### Chat Messages Table
```sql
- id (INT, PRIMARY KEY)
- session_id (INT, FOREIGN KEY)
- role (VARCHAR) # 'user' or 'assistant'
- content (TEXT)
- created_at (DATETIME)
```

## 🎯 Configuration

### Customize AI Behavior
Edit `backend/server.py`:
- `FORTUNE_TELLER_PROMPT` - Celestia's personality
- `model` parameter - Switch between GPT models
- `temperature` - Control response creativity (0-1)
- `max_tokens` - Response length limit

### Customize Fortune Data
Edit `frontend/script.js`:
- `zodiacData` - Add more fortunes, colors, compatible signs
- `adviceTemplates` - Add more advice messages

### Customize Styling
Edit `frontend/style.css`:
- Color schemes and gradients
- Animations and transitions
- Responsive breakpoints

## 🐛 Troubleshooting

### Database Connection Error
```
sqlalchemy.exc.OperationalError: (2003, "Can't connect to MySQL server")
```
**Solution:**
- Ensure MySQL is running: `sudo systemctl start mysql` (Linux) or start from MySQL Workbench
- Verify DATABASE_URL in `.env` has correct credentials
- Check MySQL is listening on port 3306: `netstat -an | grep 3306`

### "Invalid API Key" Error
**Solution:**
- Verify OPENAI_API_KEY in `.env` is correct
- No extra spaces or quotes around the key
- Check key is active at https://platform.openai.com/api-keys

### Frontend Can't Connect to Backend
**Solution:**
- Ensure backend server is running on port 3000
- Check for CORS errors in browser console (F12)
- Verify API_BASE_URL in `frontend/script.js` matches your setup

### Authentication Errors
**Solution:**
- Generate a strong SECRET_KEY in `.env`
- Clear browser localStorage and re-login
- Check JWT token hasn't expired (default: 7 days)

### Port Already in Use
```
ERROR: [Errno 48] error while attempting to bind on address ('0.0.0.0', 3000)
```
**Solution:**
```bash
# Find process using port 3000
lsof -ti:3000

# Kill the process
kill <PID>

# Or change PORT in .env
PORT=8000
```

## 💰 Cost Considerations

The AI chat uses OpenAI's API:
- **GPT-4o-mini**: ~$0.00015 per 1K tokens (very affordable)
- **GPT-3.5-turbo**: Alternative for even lower costs

A typical conversation costs less than $0.01. Monitor usage at [OpenAI Dashboard](https://platform.openai.com/usage).

## 🔒 Security Best Practices

### For Development
- ✅ Keep `.env` file secret (already in `.gitignore`)
- ✅ Use strong passwords for MySQL
- ✅ Generate secure SECRET_KEY

### For Production
- 🔐 Use HTTPS (Let's Encrypt)
- 🔐 Set secure CORS origins
- 🔐 Use environment variables, not .env file
- 🔐 Enable MySQL SSL connections
- 🔐 Set up rate limiting
- 🔐 Regular security updates
- 🔐 Use strong JWT secret (32+ bytes)
- 🔐 Set httpOnly cookies instead of localStorage

## 📱 Browser Support

Works on all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🚀 Deployment

### Backend Deployment (Example: Railway/Render/Heroku)
1. Set environment variables in hosting platform
2. Update DATABASE_URL to production MySQL
3. Set CORS allowed origins
4. Run database migrations
5. Deploy backend

### Frontend Deployment (Example: Netlify/Vercel)
1. Update API_BASE_URL in script.js to production backend
2. Deploy static files
3. Configure redirects for SPA routing

### Docker Deployment
Create `Dockerfile` in backend/:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

## 🌈 Future Enhancements

Potential features:
- Password reset functionality
- Email verification
- OAuth social login (Google, Facebook)
- User profile customization
- Favorite fortunes
- Share readings on social media
- Weekly/monthly horoscopes
- Tarot card readings
- Chinese zodiac integration
- Premium subscription tier
- Mobile app (React Native/Flutter)

## 📄 License

This project is free to use for personal and educational purposes.

## 🤝 Contributing

Feel free to fork and improve! Some ideas:
- Add more AI models (Claude, Gemini)
- Implement real-time notifications
- Add voice chat with Celestia
- Create admin dashboard
- Add analytics and insights
- Multilingual support

## 💡 Tips

- **Save API costs**: Clear chat history when starting new topics
- **Better readings**: Provide your zodiac sign for personalized responses
- **Security**: Change SECRET_KEY and use strong passwords
- **Performance**: Consider Redis for session storage in production
- **Backup**: Regularly backup your MySQL database

## 📧 Support

For issues:
1. Check Troubleshooting section above
2. Review [FastAPI Documentation](https://fastapi.tiangolo.com/)
3. Check [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
4. Review [OpenAI API Documentation](https://platform.openai.com/docs)

## 🎓 Learning Resources

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/14/orm/tutorial.html)
- [JWT Authentication](https://jwt.io/introduction)
- [MySQL Documentation](https://dev.mysql.com/doc/)

---

**May the stars guide your path!** ✨🔮⭐

*Built with ❤️ using Python FastAPI, MySQL, and OpenAI*

**Version 2.0.0** - Full Stack with Authentication
