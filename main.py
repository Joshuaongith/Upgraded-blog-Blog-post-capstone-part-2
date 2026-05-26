from flask import Flask, render_template, request
from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime
import requests
import smtplib
import os

# Initialize environment variables
load_dotenv()

# Email and application configuration
my_email = os.getenv("MY_EMAIL")
password = os.getenv("MY_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")
SMTP_SERVER = "smtp.gmail.com"
PORT = 465

current_year = datetime.now().year
api_endpoint = os.getenv("API_ENDPOINT")

# Fetch and cache blog data on server startup to minimize external API calls
response = requests.get(api_endpoint)
blog_data = response.json()
POSTS_MAP = {item["id"]: item for item in blog_data}

app = Flask(__name__)


@app.route('/')
def home():
    """Render the main blog feed."""
    return render_template('index.html', posts=blog_data, current_year=current_year)


@app.route('/about')
def about():
    """Render the static about page."""
    return render_template('about.html', current_year=current_year)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Handle contact form rendering and secure email transmission."""
    if request.method == "GET":
        return render_template('contact.html', current_year=current_year)

    if request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        message = request.form.get("message")

        # Validate required fields
        if not name or not email or not message:
            return render_template("contact.html", current_year=current_year, success="error")

        else:
            # Construct the email payload
            success = "success"
            msg = EmailMessage()
            msg["Subject"] = "New Contact Form Submission"
            msg["From"] = my_email
            msg["To"] = receiver_email
            msg.set_content(f"""\
                    Name: {name}
                    Email: {email}
                    Phone number: {request.form.get("phone_number")}
                    Message: {message}
                    """)

            # Open a secure connection and transmit
            try:
                with smtplib.SMTP_SSL(SMTP_SERVER, PORT) as connection:
                    connection.login(user=my_email, password=password)
                    connection.send_message(msg)

                print("Email sent successfully!")
                return render_template('contact.html', current_year=current_year, success=success)

            except Exception as e:
                print(f"An error occurred: {e}")
                return render_template('contact.html', current_year=current_year)


@app.route('/post/<int:post_id>')
def post(post_id):
    """Render an individual blog post via direct dictionary lookup."""
    post_content = POSTS_MAP.get(post_id)
    return render_template('post.html', post_body=post_content)


if __name__ == '__main__':
    app.run(debug=True)