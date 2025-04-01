from flask import Flask, render_template, request, jsonify
import re
import random
import string

app = Flask(__name__)

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length check
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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_password():
    password = request.json.get('password')
    return jsonify(check_password_strength(password))

@app.route('/generate', methods=['POST'])
def generate_password():
    passwords = [generate_smart_password() for _ in range(3)]
    return jsonify({
        'passwords': [
            {
                'text': pwd,
                'score': check_password_strength(pwd)['score'],
                'memorability': 'High' if len(pwd) < 20 else 'Medium'
            }
            for pwd in passwords
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)