from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json

app = Flask(__name__, static_url_path='/static')
def is_flask():
    return request.url_root.startswith('http')  # Detect if we're in Flask

@app.context_processor
def inject_env_info():
    # Return a dictionary with environment info
    return {
        'is_flask': is_flask()  # This tells the template whether it's running under Flask or as a file
    }
# Path to store reviews (you could also use a database in a real app)
reviews_file = "reviews.json"

@app.route('/images/<filename>')
def images(filename):
    return send_from_directory('images', filename)


@app.route('/index.html')
def home():
    reviews = []
    if os.path.exists(reviews_file):
        with open(reviews_file, 'r') as file:
            reviews = json.load(file)
    return render_template('index.html', reviews=reviews)

@app.route('/')
def index():
    reviews = []
    if os.path.exists(reviews_file):
        with open(reviews_file, 'r') as file:
            reviews = json.load(file)
    return render_template('index.html', reviews=reviews)



#review submission
@app.route('/submit-review', methods=['POST'])
def submit_review():
    data = request.get_json()
    
    name = data['name']
    rating = data['rating']
    review = data['review']
    

    review_data = {
        'name': name,
        'rating': rating,
        'review': review,
    }
    
    # Append the new review to the reviews list in the JSON file
    reviews = []
    if os.path.exists(reviews_file):
        with open(reviews_file, 'r') as file:
            reviews = json.load(file)
    
    reviews.append(review_data)
    
    # Save the updated list of reviews back to the JSON file
    with open(reviews_file, 'w') as file:
        json.dump(reviews, file, indent=4)
    
    return jsonify({'status': 'success'})
@app.route('/events.html')
def events():
    return render_template('events.html')

@app.route('/menu.html')
def menu():
    return render_template('menu.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/location.html')
def location():
    return render_template('location.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/events.html#event1')
def event1():
    return render_template('events.html#event1')
@app.route('/events.html#event2')
def event2():
    return render_template('events.html#event2')

if __name__ == "__main__":
    #Make sure reviews file exists & create an empty list if not
    if not os.path.exists(reviews_file):
        with open(reviews_file, 'w') as file:
            json.dump(file, indent=4)  # create empty list for reviews
    
    app.run(debug=True)

