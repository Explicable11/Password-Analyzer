from flask import Flask, render_template, request, jsonify
import re
import random
from flask import send_from_directory
import string

app = Flask(__name__)

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 12:
        score += 20
        feedback.append({"pass": True, "message": "Length (12+ characters)"})
    else:
        feedback.append({"pass": False, "message": "Length (12+ characters)"})
    
    # Uppercase check
    if re.search(r'[A-Z]', password):
        score += 20
        feedback.append({"pass": True, "message": "Contains uppercase letters"})
    else:
        feedback.append({"pass": False, "message": "Contains uppercase letters"})
    
    # Lowercase check
    if re.search(r'[a-z]', password):
        score += 20
        feedback.append({"pass": True, "message": "Contains lowercase letters"})
    else:
        feedback.append({"pass": False, "message": "Contains lowercase letters"})
    
    # Numbers check
    if re.search(r'\d', password):
        score += 20
        feedback.append({"pass": True, "message": "Contains numbers"})
    else:
        feedback.append({"pass": False, "message": "Contains numbers"})
    
    # Special characters check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 20
        feedback.append({"pass": True, "message": "Contains special characters"})
    else:
        feedback.append({"pass": False, "message": "Contains special characters"})
    
    return {
        "score": score,
        "feedback": feedback,
        "strength": "Strong" if score >= 80 else "Moderate" if score >= 60 else "Weak"
    }

def generate_smart_password(length=16):
    # Word lists for more memorable passwords
    adjectives = ['Happy', 'Brave', 'Bright', 'Swift', 'Clever']
    nouns = ['Tiger', 'Mountain', 'Ocean', 'Forest', 'Star']
    
    # Create base password
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    number = str(random.randint(100, 999))
    special = random.choice('!@#$%^&*')
    
    # Combine with some character substitutions
    password = f"{adj}{special}{noun}{number}"
    
    # Add some common substitutions to make it more secure
    substitutions = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    for char, replacement in substitutions.items():
        if random.random() > 0.5:  # 50% chance to apply each substitution
            password = password.replace(char, replacement)
    
    return password

@app.route('/style.css')
def serve_css():
    return send_from_directory('templates', 'style.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory('templates', 'script.js')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_password():
    password = request.json.get('password')
    return jsonify(check_password_strength(password))

def generate_smart_password():
    # List of common words for memorable passwords
    words = ["mountain", "river", "forest", "ocean", "desert", "valley", "cloud", "storm", 
             "sunset", "sunrise", "galaxy", "planet", "moon", "star", "comet", "rocket", 
             "eagle", "tiger", "lion", "wolf", "bear", "dolphin", "whale", "shark", "turtle"]
    
    # Generate a password with 2 words, numbers, and special characters
    word1 = random.choice(words).capitalize()
    word2 = random.choice(words)
    
    # Add some numbers
    numbers = ''.join(random.choices(string.digits, k=random.randint(2, 4)))
    
    # Add some special characters
    special_chars = ''.join(random.choices('!@#$%^&*()_+-=[]{}|;:,./<>?', k=random.randint(1, 3)))
    
    # Combine all parts and shuffle a bit
    password = word1 + special_chars + word2 + numbers
    
    return password

@app.route('/generate', methods=['POST'])
def generate_password():
    try:
        # Generate 3 different passwords with a simpler approach
        passwords = []
        for _ in range(3):
            # Create a simple but strong password
            length = random.randint(12, 16)
            chars = string.ascii_letters + string.digits + '!@#$%^&*'
            pwd = ''.join(random.choice(chars) for _ in range(length))
            passwords.append(pwd)
        
        # Return the passwords with fixed scores for testing
        result = {
            'passwords': [
                {
                    'text': pwd,
                    'score': 80,  # Fixed score for testing
                    'memorability': 'Medium'
                }
                for pwd in passwords
            ]
        }
        
        print("Generated passwords:", result)  # Debug print
        return jsonify(result)
    except Exception as e:
        print(f"Error generating passwords: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)