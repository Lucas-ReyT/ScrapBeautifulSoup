import requests
from bs4 import BeautifulSoup
import re

#Pour tester avec un seul article = False, sinon false pour scrap à l'infini (mais fini par crash)
def scrape_articles(url, Test=False):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find('main').find_all('article')

    if Test:
        articles = [articles[0]] if articles else []

    for article in articles:
        img = article.find('img')
        thumbnail = img.get('data-lazy-src') or img.get('src') if img else None
        
        meta = article.find('div', class_='entry-meta')
        subcategory = meta.find('span', class_='favtag').get_text().strip()
        date = meta.find('span', class_='posted-on').get_text().strip()
        
        a_tag = meta.find('a')
        title = a_tag.find('h3').get_text().strip()
        article_url = a_tag['href']
        
        summary = meta.find('div', class_='entry-excerpt').get_text().strip()
        
        # Aller chercher le contenu complet
        article_response = requests.get(article_url, headers=headers)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        # Auteur
        for a in article_soup.find_all('a', href=True):
         if "/auteur/" in a['href']:
             auteur2 = a.get_text().strip()
             break
        
        # Contenu
        content_div = article_soup.find('div', class_='entry-content')
        content = content_div.get_text().strip() if content_div else None
        
        # Date au format AAAAMMJJ
        date_match = re.search(r'(\d{1,2})\s+(\w+)\s+(\d{4})', date.lower())
        if date_match:
            day, month, year = date_match.groups()
            months = {'janvier':'01','février':'02','mars':'03','avril':'04','mai':'05','juin':'06',
                     'juillet':'07','août':'08','septembre':'09','octobre':'10','novembre':'11','décembre':'12'}
            format_date = f"{year}{months.get(month,'01')}{day.zfill(2)}"
        else:
            format_date = date
            
        # Images dans l'article (j'ai eu un problème de scrapping sur cette partie)
        images = {}
        image_index = 1

        if content_div:
            for img in content_div.find_all('img'):
                img_url = img.get('src') or img.get('data-lazy-src')
                if not img_url or img_url.startswith("data:image"):
                    continue

                caption = img.get('alt', '') or img.get('title', '')
                images[f'image_{image_index}'] = {'url': img_url, 'caption': caption}
                image_index += 1

        # Afficher les résultats
        format_date = f"{format_date[:4]}-{format_date[4:6]}-{format_date[6:]}"

        print(f"\nTitre: {title}")
        print(f"Miniature: {thumbnail}")
        print(f"Sous-catégorie: {subcategory}")
        print(f"Résumé: {summary}")
        print(f"Date: {format_date}")
        print(f"Auteur: {auteur2}")
        #Tester avec un contenu limité pour ne pas déborder
        print(f"Contenu: {content[:200]}...")
        #print(f"Contenu: {content}...")
        print(f"Images: {len(images)} trouvées")
        for key, img_data in images.items():
            print(f"  - {key}:")
            print(f"      URL: {img_data['url']}")
            print(f"      Légende: {img_data['caption']}")

        print(f"URL: {article_url}")
        print("-" * 50)

# Utilisation
scrape_articles("https://www.blogdumoderateur.com/web/")
