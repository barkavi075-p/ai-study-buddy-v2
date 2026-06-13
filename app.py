from flask import Flask, request, jsonify, render_template
from groq import Groq
import json
import os

app = Flask(__name__)

client = Groq(api_key="YOUR_API_KEY_HERE")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explain', methods=['POST'])
def explain():
    try:
        data = request.json
        topic = data.get('topic', '')
        level = data.get('level', 'simple')
        
        prompt = f"""You are a friendly AI tutor for Indian students.
Explain: "{topic}", Level: {level}

Reply ONLY with this JSON, no extra text:
{{
    "explanation": "3-4 line simple explanation",
    "example": "One real Indian example",
    "quiz": [
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}},
        {{"question": "Question here?", "options": ["First option", "Second option", "Third option", "Fourth option"], "answer": "Exact correct option text here"}}
    ],
    "flashcards": [
        {{"front": "Term 1", "back": "Definition 1"}},
        {{"front": "Term 2", "back": "Definition 2"}},
        {{"front": "Term 3", "back": "Definition 3"}},
        {{"front": "Term 4", "back": "Definition 4"}},
        {{"front": "Term 5", "back": "Definition 5"}}
    ]
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        text = response.choices[0].message.content.strip()
        text = text.replace('```json', '').replace('```', '').strip()
        result = json.loads(text)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)