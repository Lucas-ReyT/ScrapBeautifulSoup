from pymongo import MongoClient

def get_articles_by_subcategory(subcategory):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["BlogDuModerateur"]  
    collection = db["articles"]        

    query = {"subcategory": subcategory}
    articles = list(collection.find(query))

    return articles

if __name__ == "__main__":
    subcat = input("Entrez la sous-catégorie recherchée : ").strip()
    results = get_articles_by_subcategory(subcat)

    print(f"\nArticles trouvés dans la sous-catégorie '{subcat}' : {len(results)}\n")
    for article in results:
        print(f"- {article.get('title')} (URL: {article.get('url')})")
