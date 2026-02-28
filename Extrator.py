import re
from collections import Counter
from urllib.parse import urljoin, urlparse

import click
import requests
from bs4 import BeautifulSoup

def get_links_and_words(url):
    try:
        # Added a timeout so the script doesn't hang forever on bad links
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return set(), []
    except requests.RequestException:
        return set(), []

    soup = BeautifulSoup(resp.content.decode('utf-8', 'ignore'), 'html.parser')
    
    # Extract words
    raw_text = soup.get_text(separator=' ')
    words = re.findall(r'\w+', raw_text)

    # Extract links and keep them in-scope (same domain)
    links = set()
    base_netloc = urlparse(url).netloc
    
    for a_tag in soup.find_all('a', href=True):
        full_url = urljoin(url, a_tag['href'])
        if urlparse(full_url).netloc == base_netloc:
            links.add(full_url)
            
    return links, words

def generate_mutations(word):
    base = word.lower()
    casing_variants = {base, base.upper(), base.capitalize()}
    
    # Common password appendages
    suffixes = ['', '!', '1!', '123', '2025', '2026', '01']
    
    mutations = []
    for variant in casing_variants:
        for suffix in suffixes:
            mutations.append(f"{variant}{suffix}")
            
    return mutations

@click.command()
@click.option('--url', '-u', prompt='Web URL', help='URL of webpage to extract from.')
@click.option('--length', '-l', default=0, help='Minimum word length (default: 0).')
@click.option('--output', '-o', help='Output file to save the wordlist (e.g., wordlist.txt).')
@click.option('--depth', '-d', default=0, help='Crawl depth for finding new pages (default: 0).')
@click.option('--mutate', '-m', is_flag=True, help='Generate common password mutations.')
def main(url, length, output, depth, mutate):
    visited = set()
    queue = [(url, 0)]
    all_words = []
    
    # Breadth-first search for crawling
    while queue:
        curr_url, curr_depth = queue.pop(0)
        
        if curr_url in visited or curr_depth > depth:
            continue
            
        visited.add(curr_url)
        print(f"[*] Crawling: {curr_url}")
        
        links, words = get_links_and_words(curr_url)
        all_words.extend(words)
        
        if curr_depth < depth:
            for link in links:
                if link not in visited:
                    queue.append((link, curr_depth + 1))
                    
    # Filter by length and count frequencies
    valid_words = [w for w in all_words if len(w) >= length]
    word_counts = Counter(valid_words)
    
    # Sort by frequency (most common first)
    top_words = [word for word, count in word_counts.most_common()]
    
    # Apply mutations if the flag was passed
    results = []
    for word in top_words:
        if mutate:
            results.extend(generate_mutations(word))
        else:
            results.append(word)
            
    # Deduplicate while preserving the frequency order
    final_list = list(dict.fromkeys(results))
    
    if output:
        with open(output, 'w') as f:
            for w in final_list:
                f.write(f"{w}\n")
        print(f"\n[*] Success: Saved {len(final_list)} words to {output}")
    else:
        print("\n--- Top Results ---")
        # FIX: Using slice notation prevents the IndexError if there are <10 words
        for word in final_list[:10]:
            print(word)

if __name__ == '__main__':
    main()
