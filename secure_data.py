import streamlit as st
import hashlib
from cryptography.fernet import Fernet

# Generate a key (in production, store securely)
KEY = Fernet.generate_key()
cipher = Fernet(KEY)

# In-memory data storage
stored_data = {}  # {"encrypted_text": {"encrypted_text": ..., "passkey": ...}}
failed_attempts = 0

# Function to hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Function to encrypt data
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Function to decrypt data
def decrypt_data(encrypted_text, passkey):
    global failed_attempts
    hashed_passkey = hash_passkey(passkey)

    if encrypted_text in stored_data:
        if stored_data[encrypted_text]["passkey"] == hashed_passkey:
            failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()

    failed_attempts += 1
    return None

# Streamlit UI
st.title("\U0001F512 Secure Data Encryption System")

# Navigation
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("\U0001F3E0 Welcome to the Secure Data System")
    st.write("Use this app to **securely store and retrieve data** using unique passkeys.")

elif choice == "Store Data":
    st.subheader("\U0001F4C2 Store Data Securely")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            hashed_passkey = hash_passkey(passkey)
            encrypted_text = encrypt_data(user_data)
            stored_data[encrypted_text] = {"encrypted_text": encrypted_text, "passkey": hashed_passkey}
            st.success("\u2705 Data stored securely!")
            st.text_area("Encrypted Text", encrypted_text)
        else:
            st.error("\u26A0\uFE0F Both fields are required!")

elif choice == "Retrieve Data":
    st.subheader("\U0001F50D Retrieve Your Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            decrypted_text = decrypt_data(encrypted_text, passkey)

            if decrypted_text:
                st.success(f"\u2705 Decrypted Data: {decrypted_text}")
            else:
                st.error(f"\u274C Incorrect passkey! Attempts remaining: {3 - failed_attempts}")

                if failed_attempts >= 3:
                    st.warning("\U0001F512 Too many failed attempts! Redirecting to Login Page.")
                    st.experimental_rerun()
        else:
            st.error("\u26A0\uFE0F Both fields are required!")

elif choice == "Login":
    st.subheader("\U0001F511 Reauthorization Required")
    login_pass = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if login_pass == "admin123":
            failed_attempts = 0
            st.success("\u2705 Reauthorized successfully! Redirecting to Retrieve Data...")
            st.experimental_rerun()
        else:
            st.error("\u274C Incorrect password!")
