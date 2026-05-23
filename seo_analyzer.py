import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import get_domain, count_words, clean_text, classify_links, keyword_density


def analyze_website(url):
    result = {}

    try:
        response = requests.get(url, timeout=10)
        html = response.text
        soup = BeautifulSoup(html, "lxml")

        # ---------------- TITLE ----------------
        title = soup.title.string.strip() if soup.title else "Missing"
        result["title"] = title
        result["title_length"] = len(title) if title != "Missing" else 0

        # ---------------- META DESCRIPTION ----------------
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = (
            meta_desc.get("content").strip()
            if meta_desc and meta_desc.get("content")
            else "Missing"
        )
        result["meta_description"] = description
        result["description_length"] = len(description) if description != "Missing" else 0

        # ---------------- HEADINGS ----------------
        result["h1_count"] = len(soup.find_all("h1"))
        result["h2_count"] = len(soup.find_all("h2"))
        result["h3_count"] = len(soup.find_all("h3"))

        # ---------------- TEXT + KEYWORDS ----------------
        text = clean_text(soup.get_text())
        result["word_count"] = count_words(text)
        result["keywords"] = keyword_density(text)

        # ---------------- LINKS ----------------
        links = []
        broken_links = 0

        for a in soup.find_all("a", href=True):
            full_link = urljoin(url, a["href"])
            links.append(full_link)

            try:
                check = requests.get(full_link, timeout=5)
                if check.status_code >= 400:
                    broken_links += 1
            except:
                broken_links += 1

        domain = get_domain(url)
        internal_links, external_links = classify_links(links, domain)

        result["total_links"] = len(links)
        result["internal_links"] = len(internal_links)
        result["external_links"] = len(external_links)
        result["broken_links"] = broken_links

        # ---------------- IMAGES ----------------
        images = soup.find_all("img")
        missing_alt = 0

        for img in images:
            if not img.get("alt"):
                missing_alt += 1

        result["total_images"] = len(images)
        result["missing_alt"] = missing_alt

        # ---------------- ROBOTS.TXT ----------------
        robots_url = urljoin(url, "/robots.txt")
        robots = requests.get(robots_url)

        result["robots_txt"] = robots.status_code == 200

        # ---------------- SITEMAP.XML ----------------
        sitemap_url = urljoin(url, "/sitemap.xml")
        sitemap = requests.get(sitemap_url)

        result["sitemap_xml"] = sitemap.status_code == 200

        # ---------------- SEO SCORE ----------------
        score = 100

        if result["title"] == "Missing":
            score -= 15

        if result["meta_description"] == "Missing":
            score -= 15

        if result["h1_count"] == 0:
            score -= 10

        if result["missing_alt"] > 0:
            score -= 10

        if result["broken_links"] > 0:
            score -= 10

        if not result["robots_txt"]:
            score -= 10

        if not result["sitemap_xml"]:
            score -= 10

        if result["word_count"] < 300:
            score -= 10

        score = max(score, 0)
        result["seo_score"] = score

        return result

    except Exception as e:
        return {"error": str(e)}
