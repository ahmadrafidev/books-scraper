# Books Scraper Project

This project demonstrates the implementation of a Book Scraper web application using Flask and BeautifulSoup to scrape, filter, and display book data from a fictional website.

## Project Structure

- `app.py`: Contains the main Flask application setup, routes, and business logic.
- `templates/`: Holds the HTML templates for rendering the search form and displaying search results.

## Technologies Used

- **Flask**: A lightweight WSGI (Web Server Gateway Interface) web application framework used to build the web server.
- **BeautifulSoup**: A library for parsing HTML and XML documents, used extensively in this project for web scraping.
- **Python**: The primary programming language for the project.
- **Requests**: A Python HTTP library used to make requests to the target website for web scraping.
- **CSV**: Python's built-in library for handling CSV file operations.

## Getting Started

### Prerequisites

- Python 3.x: Ensure you have Python installed, as it's required to run the Flask application and perform web scraping.
- pip: Python's package installer, needed to install dependencies.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ahmadrafidev/books-scraper.git
   
2. Navigate to the project directory:
    ```bash
    cd books-scraper

3. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`

1. Install the required Python packages:
   ```bash
   pip install Flask requests beautifulsoup4

2. Run the Flask application:
   ```bash
   flask run

The above steps will set up the environment and start the Flask server, making the application accessible from a web browser at the default address http://127.0.0.1:5000/.

Have fun!