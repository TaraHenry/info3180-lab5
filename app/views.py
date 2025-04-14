"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
import os
from app import app, db
from flask import render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from .models import Movie
from .forms import MovieForm
from datetime import datetime
from flask_wtf.csrf import generate_csrf


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['GET','POST'])
def movies():
    # Instantiate form class
    form = MovieForm()
    # Validate file upload on submit
    if request.method == 'POST':
        if form.validate_on_submit():
            # Get form data and save poster to uploads folder
            title = form.title.data
            description = form.description.data
            poster = form.poster.data

            # Secure filename and save file
            filename = secure_filename(poster.filename)
            poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Create new movie entry
            new_movie = Movie(
                title = title,
                description = description,
                poster = filename
            )

            # Add and commit to database
            db.session.add(new_movie)
            db.session.commit()

            # Return success response
            return jsonify({
                'success': True,
                'message': 'Movie Successfully added',
                'movie': {
                    'title': title,
                    'description': description,
                    'poster': filename
                }
            }), 201
        # If validation fails, return the error
        errors = form_errors(form)
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    elif(request.method == 'GET'):
        movies = Movie.query.all()
        movies_list = []

        for movie in movies:
            movies_list.append({
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'poster':  f'/api/v1/posters/{movie.poster}'
            })
        return jsonify({
            'movies': movies_list
        })
    
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/posters/<filename>', methods=['GET'])
def get_poster(filename):
    # View function to return a specific image from the upload folder
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Content-Type"] = "application/json"
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)