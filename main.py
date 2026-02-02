import feedparser
import json
import os
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

if __name__ == "__main__":
    main()
