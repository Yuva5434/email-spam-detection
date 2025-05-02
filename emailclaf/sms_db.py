import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('your_file.db')  # Make sure to use the correct file path

# Create the sms_data table
create_table_query = '''
CREATE TABLE IF NOT EXISTS sms_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    label TEXT NOT NULL
);
'''

conn.execute(create_table_query)
conn.commit()

print("sms_data table created (if it didn't exist).")

# Close the connection
conn.close()
import sqlite3

# Connect (or create) the database file
conn = sqlite3.connect('sms_data.db')  # You can rename this if needed

# Create the sms_data table
conn.execute('''
CREATE TABLE IF NOT EXISTS sms_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    label TEXT NOT NULL
)
''')

# Insert some sample rows
sample_data = [
    ("Congratulations! You've won a free ticket to Bahamas. Text WIN to 8888!", "spam"),
    ("Hi, are we still meeting for lunch today?", "ham")
]

conn.executemany("INSERT INTO sms_data (text, label) VALUES (?, ?)", sample_data)
conn.commit()
print("sms_data table created and populated.")

conn.close()
