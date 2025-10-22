// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:3000/api';

// ===== STATE =====
let currentUser = null;
let authToken = null;
let chatSessionId = null;
let currentZodiacSign = null;

// Zodiac data with fortunes
const zodiacData = {
    aries: { name: "Aries", icon: "♈", element: "Fire", fortunes: ["Today's fiery energy brings new opportunities. Your courage will lead you to unexpected success.", "The stars align in your favor today. Take bold action and trust your instincts.", "Your natural leadership shines through. Others look to you for guidance and inspiration.", "A challenge presents itself, but your determination will see you through victoriously.", "Creative energy flows strongly. Express yourself boldly and authentically."], colors: ["Red", "Scarlet", "Crimson", "Orange"], compatibleSigns: ["Leo", "Sagittarius", "Gemini", "Aquarius"] },
    taurus: { name: "Taurus", icon: "♉", element: "Earth", fortunes: ["Patience and persistence pay off today. Your steady approach brings tangible rewards.", "Financial opportunities emerge. Trust your practical instincts about investments.", "Comfort and security are within reach. Focus on building lasting foundations.", "Your reliability makes you invaluable to others. Your help will be deeply appreciated.", "Indulge in life's pleasures today. You've earned a moment of luxury and relaxation."], colors: ["Green", "Pink", "Emerald", "Turquoise"], compatibleSigns: ["Virgo", "Capricorn", "Cancer", "Pisces"] },
    gemini: { name: "Gemini", icon: "♊", element: "Air", fortunes: ["Communication is your superpower today. Your words inspire and enlighten others.", "Curiosity leads to fascinating discoveries. Follow your interests wherever they take you.", "Social connections bring joy and opportunity. Network and share your brilliant ideas.", "Adaptability is your strength. Embrace change and flow with new circumstances.", "Your quick wit and charm open doors. Express yourself with confidence."], colors: ["Yellow", "Light Blue", "Silver", "White"], compatibleSigns: ["Libra", "Aquarius", "Aries", "Leo"] },
    cancer: { name: "Cancer", icon: "♋", element: "Water", fortunes: ["Trust your intuition today. Your emotional intelligence guides you to the right path.", "Home and family bring comfort and joy. Nurture your closest relationships.", "Your caring nature is deeply appreciated. Someone needs your compassionate support.", "Creative imagination flows freely. Express your feelings through artistic pursuits.", "Protect your energy while staying open to love. Balance is key to your wellbeing."], colors: ["Silver", "White", "Pearl", "Light Blue"], compatibleSigns: ["Scorpio", "Pisces", "Taurus", "Virgo"] },
    leo: { name: "Leo", icon: "♌", element: "Fire", fortunes: ["Your natural charisma is magnetic today. Step into the spotlight with confidence.", "Generosity of spirit brings unexpected blessings. Share your warmth with others.", "Creative projects flourish under your passionate guidance. Express your unique talents.", "Leadership opportunities arise. Your courage inspires others to follow your vision.", "Joy and celebration are in the air. Let your playful side shine through."], colors: ["Gold", "Orange", "Yellow", "Royal Purple"], compatibleSigns: ["Aries", "Sagittarius", "Gemini", "Libra"] },
    virgo: { name: "Virgo", icon: "♍", element: "Earth", fortunes: ["Your attention to detail solves complex problems. Your analytical skills are unmatched.", "Organization brings clarity and peace. Take time to create order in your environment.", "Service to others fulfills your soul. Your helpful nature makes a real difference.", "Health and wellness take priority. Your body appreciates your mindful care.", "Practical wisdom guides your decisions. Trust in your methodical approach."], colors: ["Navy Blue", "Grey", "Beige", "Forest Green"], compatibleSigns: ["Taurus", "Capricorn", "Cancer", "Scorpio"] },
    libra: { name: "Libra", icon: "♎", element: "Air", fortunes: ["Balance and harmony are within reach. Your diplomatic skills bring peace to conflicts.", "Beauty surrounds you today. Appreciate art, nature, and elegant solutions.", "Partnerships flourish under your fair and thoughtful guidance. Collaboration brings success.", "Your sense of justice guides important decisions. Stand up for what's right.", "Social grace opens doors. Your charm and tact create wonderful opportunities."], colors: ["Pink", "Light Blue", "Lavender", "Mint Green"], compatibleSigns: ["Gemini", "Aquarius", "Leo", "Sagittarius"] },
    scorpio: { name: "Scorpio", icon: "♏", element: "Water", fortunes: ["Intense focus brings breakthrough insights. Your determination is unstoppable.", "Hidden truths come to light. Your intuition reveals what others cannot see.", "Transformation is in the air. Embrace change and emerge stronger than before.", "Passionate energy drives your pursuits. Channel your intensity into meaningful goals.", "Loyalty and depth in relationships bring profound connections. Trust those who earn it."], colors: ["Deep Red", "Black", "Burgundy", "Dark Purple"], compatibleSigns: ["Cancer", "Pisces", "Virgo", "Capricorn"] },
    sagittarius: { name: "Sagittarius", icon: "♐", element: "Fire", fortunes: ["Adventure calls your name. Expand your horizons through travel or learning.", "Optimism attracts abundance. Your positive outlook creates wonderful opportunities.", "Truth and wisdom guide your path. Share your philosophical insights with others.", "Freedom and exploration fulfill your spirit. Break free from limiting routines.", "Your enthusiasm is contagious. Inspire others with your adventurous spirit."], colors: ["Purple", "Dark Blue", "Turquoise", "Red"], compatibleSigns: ["Aries", "Leo", "Libra", "Aquarius"] },
    capricorn: { name: "Capricorn", icon: "♑", element: "Earth", fortunes: ["Ambition drives you forward. Your disciplined approach leads to lasting success.", "Responsibility brings rewards. Your dedication does not go unnoticed.", "Strategic planning pays dividends. Take time to map out your long-term goals.", "Professional opportunities arise. Your reputation for excellence opens doors.", "Patience and persistence are your allies. Success comes to those who endure."], colors: ["Dark Green", "Brown", "Grey", "Black"], compatibleSigns: ["Taurus", "Virgo", "Scorpio", "Pisces"] },
    aquarius: { name: "Aquarius", icon: "♒", element: "Air", fortunes: ["Innovation and originality set you apart. Your unique perspective solves problems.", "Humanitarian efforts bring fulfillment. Make a difference in your community.", "Independent thinking leads to breakthroughs. Trust your unconventional ideas.", "Friendships and social networks flourish. Connect with like-minded visionaries.", "Future-focused vision guides your choices. You're ahead of your time."], colors: ["Electric Blue", "Silver", "Aqua", "Neon Green"], compatibleSigns: ["Gemini", "Libra", "Aries", "Sagittarius"] },
    pisces: { name: "Pisces", icon: "♓", element: "Water", fortunes: ["Intuition and dreams guide your path. Trust the whispers of your soul.", "Compassion opens hearts. Your empathetic nature heals those around you.", "Artistic expression flows naturally. Create beauty through your unique vision.", "Spiritual insights bring peace. Connect with your higher self through meditation.", "Imagination knows no bounds. Your creative dreams can become reality."], colors: ["Sea Green", "Lavender", "Purple", "Aquamarine"], compatibleSigns: ["Cancer", "Scorpio", "Taurus", "Capricorn"] }
};

const adviceTemplates = ["Stay true to your authentic self and trust your inner wisdom.", "Take time for self-care and recharge your spiritual batteries.", "Be open to unexpected opportunities that come your way.", "Listen carefully to what others are really saying beneath their words.", "Balance your ambitions with moments of rest and reflection.", "Trust the process, even when the path isn't clear.", "Your kindness today will create ripples of positivity.", "Focus on what you can control and release what you cannot.", "Embrace change as a pathway to growth and transformation.", "Connect with nature to ground yourself and find clarity."];

// ===== AUTHENTICATION =====

function saveAuth(token, user) {
    authToken = token;
    currentUser = user;
    localStorage.setItem('authToken', token);
    localStorage.setItem('currentUser', JSON.stringify(user));
}

function loadAuth() {
    authToken = localStorage.getItem('authToken');
    const userStr = localStorage.getItem('currentUser');
    if (userStr) {
        currentUser = JSON.parse(userStr);
    }
    return authToken && currentUser;
}

function clearAuth() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
}

async function register(username, email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Registration failed');
        }
        
        const data = await response.json();
        saveAuth(data.access_token, data.user);
        return data;
    } catch (error) {
        throw error;
    }
}

async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }
        
        const data = await response.json();
        saveAuth(data.access_token, data.user);
        return data;
    } catch (error) {
        throw error;
    }
}

function logout() {
    clearAuth();
    showAuthSection();
}

function showAuthSection() {
    document.getElementById('authSection').classList.remove('hidden');
    document.getElementById('mainApp').classList.add('hidden');
    document.getElementById('userInfo').classList.add('hidden');
}

function showMainApp() {
    document.getElementById('authSection').classList.add('hidden');
    document.getElementById('mainApp').classList.remove('hidden');
    document.getElementById('userInfo').classList.remove('hidden');
    document.getElementById('usernameDisplay').textContent = `Welcome, ${currentUser.username}!`;
}

// ===== ZODIAC FORTUNE =====

function getCurrentDate() {
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date().toLocaleDateString('en-US', options);
}

function randomInRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateLuckyNumbers() {
    const numbers = new Set();
    while (numbers.size < 5) {
        numbers.add(randomInRange(1, 99));
    }
    return Array.from(numbers).sort((a, b) => a - b);
}

function generateEnergyLevels() {
    return {
        love: randomInRange(60, 100),
        career: randomInRange(60, 100),
        health: randomInRange(60, 100),
        finance: randomInRange(60, 100)
    };
}

function displayFortune(sign) {
    const data = zodiacData[sign];
    const zodiacSelection = document.getElementById('zodiacSelection');
    const fortuneDisplay = document.getElementById('fortuneDisplay');
    
    zodiacSelection.classList.add('hidden');
    fortuneDisplay.classList.remove('hidden');
    
    document.getElementById('fortuneIcon').textContent = data.icon;
    document.getElementById('fortuneTitle').textContent = data.name;
    document.getElementById('fortuneDate').textContent = getCurrentDate();
    
    const randomFortune = data.fortunes[randomInRange(0, data.fortunes.length - 1)];
    document.getElementById('dailyFortune').textContent = randomFortune;
    
    const energy = generateEnergyLevels();
    setTimeout(() => {
        document.getElementById('loveMeter').style.width = energy.love + '%';
        document.getElementById('careerMeter').style.width = energy.career + '%';
        document.getElementById('healthMeter').style.width = energy.health + '%';
        document.getElementById('financeMeter').style.width = energy.finance + '%';
    }, 100);
    
    const luckyNumbers = generateLuckyNumbers();
    const luckyNumbersContainer = document.getElementById('luckyNumbers');
    luckyNumbersContainer.innerHTML = '';
    luckyNumbers.forEach(num => {
        const numberDiv = document.createElement('div');
        numberDiv.className = 'lucky-number';
        numberDiv.textContent = num;
        luckyNumbersContainer.appendChild(numberDiv);
    });
    
    const randomColor = data.colors[randomInRange(0, data.colors.length - 1)];
    document.getElementById('luckyColor').innerHTML = `
        <div class="color-circle" style="background-color: ${randomColor.toLowerCase().replace(' ', '')}"></div>
        <div class="color-name">${randomColor}</div>
    `;
    
    const compatibleSign = data.compatibleSigns[randomInRange(0, data.compatibleSigns.length - 1)];
    document.getElementById('compatibility').textContent = 
        `Today you have excellent cosmic alignment with ${compatibleSign}. Connections with this sign may bring unexpected joy and mutual understanding.`;
    
    const randomAdvice = adviceTemplates[randomInRange(0, adviceTemplates.length - 1)];
    document.getElementById('advice').textContent = randomAdvice;
    
    window.scrollTo(0, 0);
}

// ===== CHAT FUNCTIONALITY =====

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function addMessage(content, isUser = false) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = isUser ? '👤' : '🔮';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const paragraphs = content.split('\n').filter(p => p.trim());
    paragraphs.forEach(paragraph => {
        const p = document.createElement('p');
        p.textContent = paragraph;
        contentDiv.appendChild(p);
    });
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message';
    typingDiv.id = 'typingIndicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🔮';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    
    contentDiv.appendChild(indicator);
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(contentDiv);
    messagesContainer.appendChild(typingDiv);
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) indicator.remove();
}

function showError(message) {
    const messagesContainer = document.getElementById('chatMessages');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    messagesContainer.appendChild(errorDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

async function sendMessage(message) {
    const sendButton = document.getElementById('sendButton');
    const chatInput = document.getElementById('chatInput');
    
    try {
        sendButton.disabled = true;
        chatInput.disabled = true;
        
        showTypingIndicator();
        
        if (!chatSessionId) {
            chatSessionId = generateSessionId();
        }
        
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({
                message: message,
                sessionId: chatSessionId,
                zodiacSign: currentZodiacSign
            })
        });
        
        removeTypingIndicator();
        
        if (!response.ok) {
            if (response.status === 401) {
                throw new Error('Session expired. Please login again.');
            }
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get response');
        }
        
        const data = await response.json();
        chatSessionId = data.sessionId;
        addMessage(data.response, false);
        
    } catch (error) {
        removeTypingIndicator();
        console.error('Error:', error);
        showError(error.message || 'Unable to connect to fortune teller. Please try again.');
    } finally {
        sendButton.disabled = false;
        chatInput.disabled = false;
        chatInput.focus();
    }
}

function handleSendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (message) {
        addMessage(message, true);
        chatInput.value = '';
        sendMessage(message);
    }
}

async function clearChat() {
    if (!chatSessionId) return;
    
    try {
        await fetch(`${API_BASE_URL}/clear-history`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ sessionId: chatSessionId })
        });
        
        const messagesContainer = document.getElementById('chatMessages');
        while (messagesContainer.children.length > 1) {
            messagesContainer.removeChild(messagesContainer.lastChild);
        }
        
        chatSessionId = null;
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}

function switchTab(tabName) {
    const zodiacSelection = document.getElementById('zodiacSelection');
    const fortuneDisplay = document.getElementById('fortuneDisplay');
    const chatInterface = document.getElementById('chatInterface');
    const tabs = document.querySelectorAll('.nav-tab');
    
    tabs.forEach(tab => {
        if (tab.getAttribute('data-tab') === tabName) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
    
    if (tabName === 'zodiac') {
        zodiacSelection.classList.remove('hidden');
        fortuneDisplay.classList.add('hidden');
        chatInterface.classList.add('hidden');
    } else if (tabName === 'chat') {
        zodiacSelection.classList.add('hidden');
        fortuneDisplay.classList.add('hidden');
        chatInterface.classList.remove('hidden');
    }
    
    window.scrollTo(0, 0);
}

// ===== INITIALIZATION =====

document.addEventListener('DOMContentLoaded', () => {
    // Check if user is already logged in
    if (loadAuth()) {
        showMainApp();
    } else {
        showAuthSection();
    }
    
    // Auth tab switching
    const authTabs = document.querySelectorAll('.auth-tab');
    authTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabType = tab.getAttribute('data-auth-tab');
            authTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            if (tabType === 'login') {
                document.getElementById('loginForm').classList.remove('hidden');
                document.getElementById('registerForm').classList.add('hidden');
            } else {
                document.getElementById('loginForm').classList.add('hidden');
                document.getElementById('registerForm').classList.remove('hidden');
            }
        });
    });
    
    // Login form
    document.getElementById('loginSubmit').addEventListener('click', async () => {
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;
        const errorDiv = document.getElementById('loginError');
        
        errorDiv.classList.add('hidden');
        
        if (!username || !password) {
            errorDiv.textContent = 'Please fill in all fields';
            errorDiv.classList.remove('hidden');
            return;
        }
        
        try {
            await login(username, password);
            showMainApp();
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('hidden');
        }
    });
    
    // Register form
    document.getElementById('registerSubmit').addEventListener('click', async () => {
        const username = document.getElementById('registerUsername').value.trim();
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;
        const errorDiv = document.getElementById('registerError');
        
        errorDiv.classList.add('hidden');
        
        if (!username || !email || !password) {
            errorDiv.textContent = 'Please fill in all fields';
            errorDiv.classList.remove('hidden');
            return;
        }
        
        if (password.length < 6) {
            errorDiv.textContent = 'Password must be at least 6 characters';
            errorDiv.classList.remove('hidden');
            return;
        }
        
        try {
            await register(username, email, password);
            showMainApp();
        } catch (error) {
            errorDiv.textContent = error.message;
            errorDiv.classList.remove('hidden');
        }
    });
    
    // Logout button
    document.getElementById('logoutButton').addEventListener('click', logout);
    
    // Zodiac cards
    const zodiacCards = document.querySelectorAll('.zodiac-card');
    zodiacCards.forEach(card => {
        card.addEventListener('click', () => {
            const sign = card.getAttribute('data-sign');
            currentZodiacSign = zodiacData[sign].name;
            displayFortune(sign);
        });
    });
    
    // Back button
    document.getElementById('backButton').addEventListener('click', () => {
        document.getElementById('fortuneDisplay').classList.add('hidden');
        document.getElementById('zodiacSelection').classList.remove('hidden');
        window.scrollTo(0, 0);
    });
    
    // Navigation tabs
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
    
    // Chat send button
    document.getElementById('sendButton').addEventListener('click', handleSendMessage);
    
    // Chat input enter key
    document.getElementById('chatInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
    
    // Clear chat button
    document.getElementById('clearChatButton').addEventListener('click', () => {
        if (confirm('Are you sure you want to clear the conversation?')) {
            clearChat();
        }
    });
    
    // Allow Enter key on login/register forms
    document.getElementById('loginPassword').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            document.getElementById('loginSubmit').click();
        }
    });
    
    document.getElementById('registerPassword').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            document.getElementById('registerSubmit').click();
        }
    });
});

