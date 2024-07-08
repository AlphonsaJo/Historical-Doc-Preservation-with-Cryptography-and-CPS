import streamlit as st
from stegano import lsb
import hashlib
import os

# Function to calculate SHA-256 hash of a string
def calculate_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

# Function to save hashed password to a text file
def save_password_hash(password):
    hashed_password = calculate_hash(password)
    with open("password_hash.txt", 'w') as file:
        file.write(hashed_password)

# Function to save original hashed plain text to a text file
def save_original_hashed_plain_text(hashed_plain_text):
    with open("original_hashed_plain_text.txt", 'w') as file:
        file.write(hashed_plain_text)

# Function to encode data into an image using LSB steganography
def encode_data_into_image(image_filename, plain_text, password):
    if image_filename and plain_text and password:
        # Encrypt the plain text with SHA-256
        hashed_plain_text = calculate_hash(plain_text)

        # Save the hashed plain text to a file
        save_original_hashed_plain_text(hashed_plain_text)

        # Encode the plain text into the image
        secret = lsb.hide(image_filename, plain_text)

        # Save the password hash
        save_password_hash(password)

        # Save the encoded image with the text
        secret.save("encoded_image.png")
        st.success("Data encoded successfully!")

# Function to decode data from an image using LSB steganography
def decode_data_from_image(image_filename, password):
    # Check if password is set
    if not os.path.exists("password_hash.txt"):
        st.error("Password not set. Data cannot be decoded.")
        return
    
    # Load the saved password hash from file
    with open("password_hash.txt", 'r') as file:
        saved_password_hash = file.read().strip()

    # Calculate hash of the entered password and compare with the saved password hash
    if calculate_hash(password) != saved_password_hash:
        st.error("Authentication failed. Please enter the correct password.")
        return

    # Load the original hashed plain text from file
    with open("original_hashed_plain_text.txt", 'r') as file:
        original_hashed_plain_text = file.read().strip()

    if image_filename:
        # Extract the plain text from the image
        plain_text = lsb.reveal(image_filename)

        # Print the plaintext
        st.info("Plain Text: " + plain_text)

        # Calculate the hash of the extracted plain text
        hashed_plain_text = calculate_hash(plain_text)

        # Check if the calculated hash of the plain text matches the original hashed plain text
        if hashed_plain_text != original_hashed_plain_text:
            st.error("Data integrity check failed. The hash of the plaintext does not match the original hash.")
        else:
            st.success("Data integrity check passed. The hash of the plaintext matches the original hash.")


# Streamlit app
st.title("LSB Steganography")

plain_text = st.text_area("Enter Text to Encode:")
password = st.text_input("Set a password to protect data decoding:", type="password")
image_file = st.file_uploader("Select Cover Image", type=["png", "jpg", "jpeg"])

if st.button("Encode Data"):
    encode_data_into_image(image_file, plain_text, password)

if st.button("Decode Data"):
    decode_data_from_image(image_file, password)
