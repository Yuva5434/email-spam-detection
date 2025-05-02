from flask import Flask, request, render_template, jsonify
import joblib
import sqlite3
from utils import mask_text

app = Flask(__name__)

# Load the trained model and vectorizer
model = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('sms_db.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database and create table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sms_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            label TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the text input from the frontend
    text = request.form.get('text', '').strip()

    if not text:
        # Return error response if text is empty
        return jsonify({'error': 'Empty input text'}), 400

    # Mask sensitive information in the text
    masked_text = mask_text(text)

    # Preprocess the masked text using the loaded vectorizer
    X_test = vectorizer.transform([masked_text])

    # Perform prediction using the model
    prediction = model.predict(X_test)[0]

    # Save the original message and prediction to the database
    conn = get_db_connection()
    conn.execute('INSERT INTO sms_data (text, label) VALUES (?, ?)', (text, prediction))
    conn.commit()
    conn.close()

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction})

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM sms_data ORDER BY id DESC').fetchall()
    conn.close()
    messages_list = [{'id': msg['id'], 'text': msg['text'], 'label': msg['label']} for msg in messages]
    return jsonify(messages_list)

@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    conn = get_db_connection()
    conn.execute('DELETE FROM sms_data')
    conn.commit()
    conn.close()
    return jsonify({'message': 'All messages cleared successfully'})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
