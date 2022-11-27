
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, IntegerField, DateField, RadioField, \
    BooleanField, PasswordField
from wtforms.validators import InputRequired, EqualTo, Length
from .extensions import mongo

states = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AS', 'American Samoa'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('GU', 'Guam'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('MP', 'Northern Mariana Islands'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VI', 'Virgin Islands'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')]

cctype = ["Cast", "Crew"]

search_select = ['Production', 'Person', 'Genre', 'Company']
sort_select = ['Production', 'Company', 'Date']


def show_type():
    items = []
    documents = mongo.db.Prod_Type.find({'Active': True}, {'Name': 1})
    for document in documents:
        items.append(document['Name'])
    return items


def person():
    item = [x['Name'] for x in mongo.db.People.find({'Active': True}, {'Name': 1, '_id': 0})]
    item.insert(0, 'Select Person')
    return item


def company():
    item = [(coms['_id'], coms['Name']) for coms in mongo.db.Company.find({'Active': True})]
    return item


def com_type():
    item = [x['Name'] for x in mongo.db.Com_Type.find({'Active': True}, {'Name': 1, '_id': 0})]
    item.insert(0, 'Select Type')
    return item


class ProductionForm(FlaskForm):
    production = StringField("Production", validators=[InputRequired()])
    company = SelectField("Company", validators=[InputRequired()], choices=[])
    shows = IntegerField("Number of Shows", validators=[InputRequired()])
    s_type = SelectMultipleField("Show Type", validators=[InputRequired()])
    show_open = DateField("Show Open", validators=[InputRequired()])
    submit = SubmitField("Submit")


class CastCrew(FlaskForm):
    person = SelectField("Person", validators=[InputRequired()])
    type = SelectField("Type", validators=[InputRequired()], choices=cctype)
    role = StringField("Role", validators=[InputRequired()])
    submit = SubmitField("Submit", validators=[InputRequired()])


class SearchForm(FlaskForm):
    criteria = StringField("Criteria")
    search_field = RadioField("Field to Search", choices=search_select, default='Production')
    search_type = RadioField('Sort by', choices=sort_select, default='Production')
    date_start = DateField("Start Date")
    date_end = DateField("End Date")
    submit = SubmitField("Submit")


class UtilityForm(FlaskForm):
    name = StringField("Name")
    active = BooleanField("Active")
    submit = SubmitField("Submit")


class CompanyForm(FlaskForm):
    company = StringField("Company", validators=[InputRequired()])
    city = StringField("City", validators=[InputRequired()])
    state = SelectField("State", validators=[InputRequired()], choices=states, default="LA")
    c_type = SelectField("Type", validators=[InputRequired()])
    active = BooleanField("Active", default=True)
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ChangePassword(FlaskForm):
    password = PasswordField("Password", [InputRequired(), EqualTo('password2', message='Passwords must match'),
                                          Length(min=6, message='Must be at least 6 characters long')])
    password2 = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Submit")