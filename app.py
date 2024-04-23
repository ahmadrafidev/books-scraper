from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    categories = fetch_categories()
    if request.method == 'POST':
        title = request.form.get('title', '')
        category_name = request.form.get('category', '')
        category_url = next((url for name, url in categories if name == category_name), None)
        books = scrape_books(title_filter=title, category_filter=category_url)
        save_books_to_csv(books)
        return render_template('results.html', books=books, categories=categories)
    return render_template('index.html', categories=categories)

# Fungsi untuk melakukan scraping data buku dari situs web
def scrape_books(max_pages=3, title_filter=None, category_filter=None):
    current_page = 1
    books = []
    total_books = 0 
    seen_titles = set()

    while current_page <= max_pages and total_books < 60:
        if category_filter and category_filter != "All Categories":
            url = category_filter 
        else:
            url = f"https://books.toscrape.com/catalogue/page-{current_page}.html"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for book in soup.find_all('article', class_='product_pod'):
            title = book.h3.a['title']
            
            if title_filter and title_filter.lower() not in title.lower():
                continue
            
            if title in seen_titles:
                continue 
            seen_titles.add(title)  
            
            rating = convert_rating(book.p['class'][1])
            price = book.find('p', class_='price_color').text[1:]
            in_stock = book.find('p', class_='instock availability').text.strip()
            image_url = book.div.a.img['src'].replace('../../', 'https://books.toscrape.com/')
            

            books.append({
                'title': title,
                'rating': rating,
                'price': price,
                'in_stock': in_stock,
                'image_url': image_url
            })
            total_books += 1
            if total_books >= 60:
                break

        current_page += 1

    return sort_books_by_rating(books)

# Fungsi untuk mengonversi teks rating menjadi angka bintang
def convert_rating(rating_text):
    rating_dict = {
        'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    rating_number = rating_dict.get(rating_text, 0)
    return f"{rating_number} bintang"

# Fungsi untuk mengurutkan daftar buku berdasarkan rating tertinggi
def sort_books_by_rating(books):
    return sorted(books, key=lambda x: int(x['rating'].split()[0]), reverse=True)

# Fungsi untuk menyimpan daftar buku ke dalam file CSV
def save_books_to_csv(books):
    with open('books.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Rating', 'Price', 'In Stock', 'Image URL'])
        
        for book in books:
            writer.writerow([book['title'], book['rating'], book['price'], book['in_stock'], book['image_url']])

# Variabel global untuk menyimpan daftar kategori buku yang sudah di-cache  
cached_categories = None
    
# Fungsi untuk mengambil daftar kategori buku
def fetch_categories():
    global cached_categories
    if cached_categories is not None:
        return cached_categories

    url = "https://books.toscrape.com/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        categories = []
        for link in soup.find('div', class_='side_categories').find_all('a')[1:]:
            category_name = link.text.strip()
            if 'Erotica' not in category_name:  
                category_url = url + link.get('href')
                categories.append((category_name, category_url))
        cached_categories = categories
        return categories
    else:
        return []

if __name__ == '__main__':
    books = scrape_books()
    save_books_to_csv(books)
    print("Books have been scraped and saved to CSV.")
