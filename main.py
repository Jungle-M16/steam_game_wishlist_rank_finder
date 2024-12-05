import urllib.request
import json
import threading
from html.parser import HTMLParser
import sys
import os
from collections import OrderedDict

# Prompt the user for the game name
game_name = input("Enter the game name to search: ").strip().lower()

cache_file = 'game_list_cache.json'

# Shared variables
found_rank = None
lock = threading.Lock()
results = {}  # To store titles per start index

def load_cache():
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            items = json.load(f)
        # Reconstruct the OrderedDict with lowercased keys
        game_titles = OrderedDict((key.lower(), value) for key, value in items)
        total_count = len(game_titles)
        print(f"Loaded {total_count} games from cache.")
        return game_titles
    except Exception as e:
        print(f"Failed to load cache file: {e}")
        if os.path.exists(cache_file):
            os.remove(cache_file)
            print("Corrupted cache file deleted.")
        return None  # Indicate that we need to fetch data

def fetch_and_cache_data():
    # Initial URL to get the total count
    initial_url = 'https://store.steampowered.com/search/results/?query&start=1150&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_popularwishlist_7&filter=popularwishlist&infinite=1'
    
    try:
        # Fetch the initial page to get the total_count
        response = urllib.request.urlopen(initial_url)
        data = response.read().decode('utf-8')
        json_data = json.loads(data)
        total_count = json_data['total_count']
        print(f"Total games in the wishlist: {total_count}")
    except Exception as e:
        print(f"Failed to fetch initial data: {e}")
        sys.exit(1)
    
    print("Fetching all pages in parallel...")
    
    # Base URL without the 'start' parameter
    base_url = 'https://store.steampowered.com/search/results/?query&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_popularwishlist_7&filter=popularwishlist&infinite=1'
    
    # Generate list of 'start' values
    starts = list(range(0, total_count, 50))
    
    # Define the HTML Parser
    class GameHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.in_title = False
            self.titles = []
            self.current_title = ''

        def handle_starttag(self, tag, attrs):
            if tag == 'span':
                for attr in attrs:
                    if attr[0] == 'class' and 'title' in attr[1]:
                        self.in_title = True

        def handle_endtag(self, tag):
            if tag == 'span' and self.in_title:
                self.in_title = False
                self.titles.append(self.current_title.strip())
                self.current_title = ''

        def handle_data(self, data):
            if self.in_title:
                self.current_title += data

    def fetch_and_parse(start):
        page_url = base_url + f'&start={start}'
        try:
            response = urllib.request.urlopen(page_url)
            data = response.read().decode('utf-8')
            json_data = json.loads(data)
            results_html = json_data['results_html']

            parser = GameHTMLParser()
            parser.feed(results_html)
            titles = parser.titles

            with lock:
                results[start] = titles

        except Exception as e:
            print(f"Failed to fetch or parse page starting at {start}: {e}")

    # Start threads to fetch and parse pages
    threads = []
    for start in starts:
        t = threading.Thread(target=fetch_and_parse, args=(start,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Combine results in order based on start index
    # Build an OrderedDict mapping from lowercased game titles to their ranks
    game_titles = OrderedDict()
    current_rank = 1
    for start in sorted(results.keys()):
        titles = results[start]
        for title in titles:
            lower_title = title.strip().lower()
            if lower_title not in game_titles:
                game_titles[lower_title] = current_rank
                current_rank += 1
            else:
                # If the same game title appears again, increment rank to maintain order
                current_rank += 1

    # After fetching all titles, save to cache
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            # Save as list of tuples to preserve order
            json.dump(list(game_titles.items()), f)
        print(f"Saved {len(game_titles)} games to cache.")
    except Exception as e:
        print(f"Failed to save cache file: {e}")
        sys.exit(1)

    return game_titles

# Try to load cache
game_titles = load_cache()

if game_titles is None:
    # Cache was corrupted or missing, fetch data and cache it
    game_titles = fetch_and_cache_data()

# Now, search for the game in the OrderedDict using lowercased key
found_rank = game_titles.get(game_name)

if found_rank is None:
    # Game not found in cache, delete cache and fetch data again
    print(f"The game '{game_name}' was not found in the cache. Fetching data again...")
    if os.path.exists(cache_file):
        os.remove(cache_file)
    # Clear results and fetch data again
    results.clear()
    game_titles = fetch_and_cache_data()
    # Search again
    found_rank = game_titles.get(game_name)

    if found_rank is not None:
        print(f"The game '{game_name}' is ranked #{found_rank}. 🚀")
    else:
        print(f"The game '{game_name}' was not found in the popular wishlist.")
else:
    print(f"The game '{game_name}' is ranked #{found_rank}. 🚀")
