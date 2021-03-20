from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.fields.core import SelectField
from wtforms.fields.simple import TextAreaField, TextField
from wtforms.validators import InputRequired, Regexp


class PropertyForm(FlaskForm):
    title = TextField(validators=[InputRequired()])
    description = TextAreaField(validators=[InputRequired()])
    bedroom_count = TextField("No. of Rooms", validators=[InputRequired(), Regexp("^\d+$",message="The number of bedrooms must be an integer")])
    bathroom_count = TextField("No. of Bathrooms", validators=[InputRequired(),Regexp("^\d+$",message="The number of bathrooms must be an integer")])
    price = TextField(validators=[InputRequired(), Regexp("^\d+\.*\d*$",message="The price must be a number")])
    type=SelectField(label="Property Type",choices=[('HOUSE','House'),('APARTMENT','Apartment')],validators=[InputRequired()])
    location = TextField(validators=[InputRequired()])
    photo = FileField(validators=[FileRequired(),FileAllowed(['jpg','png'],"Only images in jpg and png format are accepted")])

