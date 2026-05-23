from urllib.parse import urlparse
import validators
import re

# Validate URL
def is_valid_url(url):
    return validators.url(url)

# Extract domain name
def get_domain(url):
    parsed = urlparse(url)
    return parsed.netloc

# Count words in text
def count_words(text):
    words = re.findall(r'\w+', text)
    return len(words)

# Clean text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Separate internal and external links
def classify_links(links, base_domain):
    internal_links = []
    external_links = []

    for link in links:
        parsed = urlparse(link)

        # relative links = internal
        if parsed.netloc == "" or parsed.netloc == base_domain:
            internal_links.append(link)
        else:
            external_links.append(link)

    return internal_links, external_links

# Count keyword density
def keyword_density(text):
    words = re.findall(r'\w+', text.lower())
    total_words = len(words)

    if total_words == 0:
        return {}

    freq = {}
    for word in words:
        if len(word) > 3:  # ignore small words
            freq[word] = freq.get(word, 0) + 1

    density = {
        word: round((count / total_words) * 100, 2)
        for word, count in freq.items()
    }

    # Return top 10 keywords
    sorted_keywords = dict(
        sorted(density.items(), key=lambda x: x[1], reverse=True)[:10]
    )

    return sorted_keywords
