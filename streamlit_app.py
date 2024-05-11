import streamlit as st
import sqlite3

# Function to create the database table
def create_table():
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS survey (
                 id INTEGER PRIMARY KEY,
                 name TEXT,
                 phone_number TEXT,
                 fruit_preference_1 TEXT,
                 fruit_preference_2 TEXT,
                 fruit_preference_3 TEXT)''')
    conn.commit()
    conn.close()

# Function to save responses to the database
def save_responses(name, phone_number, fruit_preferences):
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute('''INSERT INTO survey (name, phone_number, fruit_preference_1, fruit_preference_2, fruit_preference_3) 
                 VALUES (?, ?, ?, ?, ?)''', (name, phone_number, *fruit_preferences))
    conn.commit()
    conn.close()

# Function to fetch and print saved responses from the database
def print_saved_responses():
    conn = sqlite3.connect('survey_responses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM survey")
    rows = c.fetchall()
    conn.close()

    if rows:
        st.subheader("Saved Survey Responses:")
        for row in rows:
            st.write(f"Name: {row[1]}")
            st.write(f"Phone Number: {row[2]}")
            st.write("Fruit Preferences:")
            for i in range(3, len(row)):
                st.write(f"Fruit {i-2}: {row[i]}")
            st.write("---")
    else:
        st.subheader("No saved survey responses.")

def main():
    # Page title
    st.title("Weekly Fruit Preference Survey")

    # User login
    name = st.text_input("Name:")
    phone_number = st.text_input("Phone Number:")

    # Question 1: Fruit Preference
    st.header("Question 1:")
    st.write("Please write down 3 fruits you would like to eat this week")

    fruit_preferences = []
    for i in range(3):
        fruit = st.text_input(f"Fruit {i+1}:", key=f"fruit_{i}")
        fruit_preferences.append(fruit)

    # Submit button
    if st.button("Submit"):
        # Check if all responses are provided
        if not all(fruit_preferences) or not name or not phone_number:
            st.error("Please provide responses for all fields.")
        else:
            # Create table if not exists
            create_table()

            # Save responses to the database
            save_responses(name, phone_number, fruit_preferences)
            st.success("Survey submitted successfully!")

            # Print saved responses
            print_saved_responses()

if __name__ == "__main__":
    main()
