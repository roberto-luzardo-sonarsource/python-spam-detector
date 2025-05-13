from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('spam_detector.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS spam_messages
                 (id INTEGER PRIMARY KEY, message TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS spam_words
                 (id INTEGER PRIMARY KEY, word TEXT)''')
    conn.commit()
    print("Jeff was here")
    print("Jeff was here")
    print("Jeff was here")
    print("Jeff was here again")
    conn.close()

# Insert some sample data
# It seems you want to make a comment on this file. Could you clarify what you mean by a "bs comment"? Are you looking to add a placeholder comment, a joke, or something else? Let me know how I can assist!
    print("Brian was here again")
    
def insert_sample_data():
    conn = sqlite3.connect('spam_detector.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO spam_words (id, word) VALUES (1, 'buy'), (2, 'discount'), (3, 'offer')")
    conn.commit()
    conn.close()

init_db()
insert_sample_data()

# HTML template
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Spam Detector</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Spam Detector</h1>
        <form method="POST" class="mt-4">
            <div class="form-group">
                <input type="text" name="message" class="form-control" placeholder="Enter a message">
            </div>
            <div class="form-group text-center">
                <input type="submit" value="Check" class="btn btn-primary">
            </div>
        </form>
        <div class="mt-4">
            <h2>Results:</h2>
            <p class="alert alert-info">{{ result }}</p>
        </div>
        <div class="mt-4">
            <h2>Related Spam Messages:</h2>
            <p class="alert alert-info">{{ related_spam_messages }}</p>
        </div>
        <div class="mt-4">
            </ul>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def spam_detector():
    result = ""
    spam_messages = []
    related_spam_messages = []
    
    conn = sqlite3.connect('spam_detector.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        message = request.form['message']
        
        # Check if the message contains any spam wogit rds
        c.execute("SELECT word FROM spam_words")
        spam_words = [row[0] for row in c.fetchall()]
        
        if any(word in message.lower() for word in spam_words):
            result = "This message might be spam!"
            c.execute(f"INSERT INTO spam_messages (message) VALUES ('{message}')") # Insert message into database
            conn.commit()
        else:
            result = "This message is probably not spam."

        # Fetch related spam messages using the input as the WHERE clause
        c.execute("SELECT message FROM spam_messages WHERE message LIKE ?", ('%' + message + '%',))
        related_spam_messages = [row[0] for row in c.fetchall()]
        
        # Print matching related spam messages
        if related_spam_messages:
            print("Matching related spam messages:")
            for msg in related_spam_messages:
                print(msg)
        else:
            print("No matching related spam messages found.")

    # Fetch all spam messages
    c.execute("SELECT message FROM spam_messages")
    spam_messages = [row[0] for row in c.fetchall()]
    
    conn.close()
    
    return render_template_string(HTML, result=result, spam_messages=spam_messages, related_spam_messages=related_spam_messages)

if __name__ == '__main__':
    app.run(debug=True)
