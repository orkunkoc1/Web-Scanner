import os
from dotenv import load_dotenv
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import certifi
from bs4 import BeautifulSoup

def search_duckduckgo(query):
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers, verify=certifi.where())
    response.raise_for_status()
    return response.text

def parse_results(html, keywords):
    soup = BeautifulSoup(html, "html.parser")
    results = soup.select("div.result")
    found_results = []

    for result in results:
        link = result.select_one("a.result__url")
        title = result.select_one("h2.result__title")
        description = result.select_one("a.result__snippet")

        if link and title and description:
            link = link.get("href")
            title = title.get_text()
            description = description.get_text()

            if any(keyword.lower() in title.lower() or keyword.lower() in description.lower() for keyword in keywords):
                found_results.append({"title": title, "description": description, "link": link})

    return found_results

def send_email(results):
    # Email configuration
    sender_email = '_your_mail_'  # Sender's email address
    receiver_email = '_receiver_mail_'  # Recipient's email address
    subject = 'Search Results'  # Email subject

    # Construct email message
    message = 'Search Results:\n\n'
    for i, result in enumerate(results, 1):
        message += f"Result {i}:\n"
        message += f"Title: {result['title']}\n"
        message += f"Description: {result['description']}\n"
        message += f"Link: {result['link']}\n"
        message += "--------------------\n"

    # Create message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    #Load the enviroment variables from .env
    dotenv_path = Path('....\get.env')
    load_dotenv(dotenv_path=dotenv_path)
    
    #Get the SMTP password from the environment variable
    key="SMTP_PASSWORD"
    #smtp_password = os.getenv("SMTP_PASSWORD")
    
    # SMTP server configuration
    smtp_server = '_smtp_server_'  # SMTP server address
    smtp_port = 25  # SMTP server port
    smtp_port = int(smtp_port)
    smtp_username = '_your_username_'  # SMTP username
    smtp_password = os.getenv(key)

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print('Email sent successfully!')

def perform_search():
    keywords = ['Superligde bu hafta']  # Modify with your desired keywords
    query = "+".join(keywords)
    html = search_duckduckgo(query)
    results = parse_results(html, keywords)

    if results:
        send_email(results)
    else:
        print("No results found.")

# Schedule the search and email to be sent every day at a specific time
#schedule.every().day.at('09:00').do(perform_search)

# Keep the script running to execute scheduled tasks
#while True

perform_search()
