# SEO Evaluator Flask

This project is a web application built using Flask that allows users to evaluate the SEO aspects of a given webpage. The application provides a user-friendly interface for inputting a URL and receiving an evaluation based on various SEO criteria.

## Features

- Input form for URL submission
- Evaluation of multiple SEO aspects
- Display of results with percentages and explanations
- Adherence to SEO best practices and guidelines

## Project Structure

```
seo-evaluator-flask
├── app.py                # Main entry point of the Flask application
├── templates             # HTML templates for the application
│   ├── base.html        # Base template with common structure
│   ├── index.html       # Form for URL input
│   └── results.html     # Results display for SEO evaluation
├── static               # Static files (CSS and JS)
│   ├── css
│   │   └── style.css    # Styles for the application
│   └── js
│       └── main.js      # JavaScript functionality
├── seo_analyzer.py      # Logic for analyzing SEO aspects
├── requirements.txt      # Project dependencies
└── README.md            # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/seo-evaluator-flask.git
   cd seo-evaluator-flask
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Enter the URL you want to evaluate in the provided form and submit.

4. Review the results displayed on the results page, which includes checks for various SEO aspects, their percentages, and explanations based on SEO guidelines.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.# analisis-seo
