from bs4 import BeautifulSoup


def get_seo_data(text: str) -> str:
    """Extracts SEO data (h1, title, description) from HTML text."""
    html = BeautifulSoup(text, 'html.parser')
    h1 = html.h1.get_text() if html.h1 else ''
    title = html.title.get_text() if html.title else ''
    description = html.find('meta', {'name': 'description'})
    content = description['content'] if description else ''

    return h1, title, content
