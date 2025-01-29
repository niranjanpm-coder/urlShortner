import hashlib
import string
import random
from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Dictionary to store short URLs
url_mapping = {}

# Function to generate a short hash
def generate_short_url(original_url):
    # Create a hash of the URL
    hash_object = hashlib.md5(original_url.encode())
    short_hash = hash_object.hexdigest()[:6]  # Shorten to the first 6 characters
    return short_hash

@app.route('/')
def home():
    return render_template_string("""
        <h1>URL Shortener</h1>
        <form method="POST" action="/shorten">
            <input type="text" name="url" placeholder="Enter URL" required>
            <button type="submit">Shorten</button>
        </form>
    """)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_url = generate_short_url(original_url)
    
    # Store the URL mapping
    url_mapping[short_url] = original_url
    
    return f"Short URL: <a href='/{short_url}'>/{short_url}</a>"

@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = url_mapping.get(short_url)
    if original_url:
        return redirect(original_url)
    return f"URL not found for {short_url}", 404

if __name__ == '__main__':
    app.run(debug=True)