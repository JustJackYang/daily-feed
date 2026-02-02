import feedparser
import json
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import time

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_feed(url, max_entries):
    print(f"Fetching {url}...")
    try:
        feed = feedparser.parse(url)
        if feed.bozo:
            print(f"Warning: Issue parsing {url}: {feed.bozo_exception}")
        return feed.entries[:max_entries]
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def format_date(date_struct):
    if not date_struct:
        return ""
    # date_struct is a time.struct_time
    dt = datetime.fromtimestamp(time.mktime(date_struct))
    return dt.strftime('%Y-%m-%d %H:%M')

def send_email(html_content, subject):
    print("Preparing to send email...")
    email_user = os.environ.get('EMAIL_USER', '').strip()
    email_pass = os.environ.get('EMAIL_PASS', '').strip()
    email_to = os.environ.get('EMAIL_TO', '').strip()
    
    # Debug logging (masking password)
    print(f"DEBUG: EMAIL_USER={'Found' if email_user else 'Missing'}")
    print(f"DEBUG: EMAIL_PASS={'Found' if email_pass else 'Missing'}")
    print(f"DEBUG: EMAIL_TO={'Found' if email_to else 'Missing'}")
    
    if not email_user or not email_pass or not email_to:
        print("Email configuration missing (EMAIL_USER, EMAIL_PASS, EMAIL_TO). Skipping email.")
        return

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(html_content, 'html'))

    # Try Port 465 (SSL) first
    try:
        smtp_server = 'smtp.qq.com'
        smtp_port = 465
        print(f"Connecting to SMTP server: {smtp_server}:{smtp_port} (SSL)...")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            print("Logging in to SMTP server...")
            server.login(email_user, email_pass)
            print("Sending email...")
            server.sendmail(email_user, email_to, msg.as_string())
        print(f"Email sent successfully to {email_to} via Port 465!")
        return
    except Exception as e:
        print(f"Failed to send email via Port 465: {e}")
        print("Retrying with Port 587 (STARTTLS)...")

    # Retry Port 587 (STARTTLS)
    try:
        smtp_port = 587
        print(f"Connecting to SMTP server: {smtp_server}:{smtp_port} (STARTTLS)...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            print("Logging in to SMTP server...")
            server.login(email_user, email_pass)
            print("Sending email...")
            server.sendmail(email_user, email_to, msg.as_string())
        print(f"Email sent successfully to {email_to} via Port 587!")
    except Exception as e:
        print(f"Failed to send email via Port 587: {e}")

def main():
    # 1. Load Config
    config = load_config()
    
    # 2. Fetch Feeds
    feeds_data = {}
    for feed_config in config['feeds']:
        if 'example.com' in feed_config['url']:
            continue # Skip example
            
        entries = fetch_feed(feed_config['url'], config.get('max_entries_per_feed', 5))
        if entries:
            feeds_data[feed_config['name']] = entries

    # 3. Setup Template Environment
    env = Environment(loader=FileSystemLoader('templates'))
    env.filters['date_format'] = format_date
    template = env.get_template('index.html')

    # 4. Render Template
    now = datetime.now()
    html_content = template.render(
        site_title=config.get('site_title', 'My Daily Feed'),
        date=now.strftime('%Y年%m月%d日'),
        update_time=now.strftime('%H:%M:%S'),
        feeds_data=feeds_data
    )

    # 5. Write Output
    output_file = config.get('output_file', 'index.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Successfully generated {output_file}")

    # 6. Send Email
    send_email(html_content, f"每日信息汇总 - {now.strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
