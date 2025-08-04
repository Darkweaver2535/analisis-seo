from flask import Flask, render_template, request
from seo_analyzer import SEOAnalyzer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        analyzer = SEOAnalyzer()
        results = analyzer.analyze_seo(url)
        return render_template('results.html', results=results, url=url)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)