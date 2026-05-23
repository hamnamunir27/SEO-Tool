def generate_suggestions(data):
    suggestions = []

    if data.get("title") == "Missing":
        suggestions.append(
            "Add a proper SEO title tag (recommended 50–60 characters)."
        )
    elif data.get("title_length", 0) < 30:
        suggestions.append(
            "Title is too short. Make it more descriptive and keyword-focused."
        )
    elif data.get("title_length", 0) > 60:
        suggestions.append(
            "Title is too long. Keep it between 50–60 characters."
        )

    if data.get("meta_description") == "Missing":
        suggestions.append(
            "Add a meta description (recommended 150–160 characters)."
        )
    elif data.get("description_length", 0) < 70:
        suggestions.append(
            "Meta description is too short. Add more meaningful details."
        )
    elif data.get("description_length", 0) > 160:
        suggestions.append(
            "Meta description is too long. Keep it concise."
        )

    if data.get("h1_count", 0) == 0:
        suggestions.append(
            "No H1 heading found. Add one main H1 tag."
        )

    if data.get("missing_alt", 0) > 0:
        suggestions.append(
            f"{data['missing_alt']} images are missing ALT text."
        )

    if data.get("broken_links", 0) > 0:
        suggestions.append(
            f"Fix {data['broken_links']} broken links."
        )

    if not data.get("robots_txt", False):
        suggestions.append(
            "robots.txt not found. Add it for crawler guidance."
        )

    if not data.get("sitemap_xml", False):
        suggestions.append(
            "sitemap.xml not found. Add it for better indexing."
        )

    if data.get("word_count", 0) < 300:
        suggestions.append(
            "Content is short. Consider adding more useful text."
        )

    if not suggestions:
        suggestions.append("Great SEO health. No major issues found.")

    return suggestions


# Simple title generator
def generate_title_ideas(domain):
    return [
        f"Best SEO Strategy Guide for {domain}",
        f"Complete Website Optimization for {domain}",
        f"Improve Search Ranking with {domain}",
    ]


# Simple meta description generator
def generate_meta_ideas(domain):
    return [
        f"Discover SEO optimization tips and website improvements for {domain}.",
        f"Boost visibility, speed, and rankings with better SEO for {domain}.",
        f"Learn how {domain} can improve search performance and user experience.",
    ]
