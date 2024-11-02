from bs4 import BeautifulSoup


def get_seo_data(text: str):
    """Извлекает данные SEO (h1, title, description) из HTML текста."""
    html = BeautifulSoup(text, 'html.parser')
    h1 = html.h1.get_text() if html.h1 else ''
    title = html.title.get_text() if html.title else ''
    description = html.find('meta', {'name': 'description'})
    content = description['content'] if description else ''

    return h1, title, content
