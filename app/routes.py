from flask import Blueprint, render_template, request, flash
from .painpoints import get_company_pain_points

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/get_pain_points', methods=['POST'])
def get_pain_points():
    company_name = request.form['company_name']
    pain_points = get_company_pain_points(company_name)
    
    if not pain_points:
        pain_points = [
            f"No specific pain points found for {company_name}.",
            "This could be due to scraping limitations or no negative sentiment detected."
        ]
    
    return render_template('results.html', 
                         company_name=company_name, 
                         pain_points=pain_points)
