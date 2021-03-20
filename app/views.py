"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
from app.forms import PropertyForm
from app.models import Property, db
from app import app
from flask import render_template, request, redirect, url_for, flash


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/property', methods=['GET', 'POST'])
def add_property():
    form = PropertyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                title = form.title.data
                bedroom_count = int(form.bathroom_count.data)
                bathroom_count = int(form.bathroom_count.data)
                location = form.location.data
                price = float(form.price.data)
                type = form.type.data
                description = form.description.data
                photo = form.photo.data
                photo_path = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'],photo_path))
                prop = Property(title, bedroom_count, bathroom_count,
                            location, price, type, description, photo_path)
                db.session.add(prop)
                db.session.commit()
                flash('Property saved successfully','success')
                return redirect(url_for('show_properties'))
            except Exception as e:
                print(e)
                flash('Something went wrong','danger')
        else:
            flash_errors(form)
    
    return render_template('add_property.html',form=form)


@app.route('/properties')
def show_properties():
    props = Property.query.all()
    return render_template('properties.html',properties=props)


@app.route("/property/<propertyid>")
def view_property(propertyid):
    prop = Property.query.get(propertyid)
    return render_template('property_details.html', prop=prop)

@app.route("/images/<filename>")
def get_image(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir,app.config['UPLOAD_FOLDER']),filename)

###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')


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
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
