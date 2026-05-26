from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import datetime
import requests
import os


load_dotenv()

current_year = datetime.now().year
api_endpoint = os.getenv("API_ENDPOINT")

response = requests.get(api_endpoint)
blog_data = response.json()

POSTS_MAP = {item["id"]: item for item in blog_data}



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', posts=blog_data, current_year=current_year)

@app.route('/about')
def about():
    return render_template('about.html', current_year=current_year)

@app.route('/contact')
def contact():
    return render_template('contact.html', current_year=current_year)

@app.route('/post/<int:post_id>')
def post(post_id):
    post_content = POSTS_MAP.get(post_id)
    return render_template('post.html', post_body=post_content)

if __name__ == '__main__':
    app.run(debug=True)


