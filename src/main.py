from Extracter import Scraper
from flask import Flask, render_template, request


app = Flask(__name__)
scraper = Scraper()

@app.route('/')
def home():
    return render_template('template.html')  # Ensure this template exists

@app.route('/search')
def search():
    search_param = request.args.get('q')
    scraper.set_query(search_param)
    result_html = scraper.scrape()  # Get HTML string directly from scrape()
    return result_html

    

@app.route('/about')
def about():
    return 'About'


if __name__ == '__main__': 
    app.run(debug=True, port=5000)
scraper.close()
