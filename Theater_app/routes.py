
from flask import render_template, request, redirect, url_for, flash, session, Blueprint
from .model import *
from Theater_app import mongo
from .forms import ProductionForm, CastCrew, person, show_type, company, com_type, SearchForm, UtilityForm, CompanyForm
from .search import db_find_results

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def welcome():
    form = SearchForm()
    if request.method == 'POST':
        if form.criteria.data == '':
            form.criteria.data = None
        session['field'] = form.search_field.data
        session['sort'] = form.search_type.data
        session['criteria'] = form.criteria.data
        session['start_date'] = form.date_start.data
        session['end_date'] = form.date_end.data
        return redirect(url_for('main.search_results'))

    else:
        return render_template("index.html", form=form)


@main.route("/search_results/")
def search_results():
    results = db_find_results(mongo.db.Productions, session['field'], session['criteria'], session['sort'],
                              session['start_date'], session['end_date'])
    return render_template("search_results.html", results=results)


@main.route("/productiondetail/<pid>")
def production_detail(pid):
    op = db_open_record(mongo.db.Productions, pid)
    return render_template("production_detail.html", output=op, pid=pid)


@main.route("/add_production/", methods=['GET', 'POST'])
def add_production():
    form = ProductionForm()
    form.s_type.choices = show_type()
    form.company.choices = company()
    if request.method == "GET":
        return render_template("edit_production.html", form=form, type='Add')
    else:
        pid = db_add_record(mongo.db.Productions, form)
        flash("Production has been added!")
        return redirect(url_for('main.production_detail', pid=pid))


@main.route("/edit_production/<pid>", methods=['GET', 'POST'])
def edit_production(pid):
    form = ProductionForm()
    form.s_type.choices = show_type()
    form.company.choices = company()
    if request.method == "POST":
        db_edit_record(mongo.db.Productions, form=form, pid=pid)
        flash("Production has been edited!")
        return redirect(url_for('main.production_detail', pid=pid))

    else:
        op = db_open_record(mongo.db.Productions, pid)
        form.production.data = op['Production']
        form.company.data = op['Company']['Name']
        form.shows.data = op['Number of Shows']
        form.show_open.data = op['Show Open']
        form.s_type.data = op['Production Type']
        return render_template("edit_production.html", form=form, type='Edit')


@main.route("/add_cast_crew/<pid>", methods=['GET', 'POST'])
def add_cast_crew(pid):
    form = CastCrew()
    form.person.choices = person()
    if request.method == "POST":
        db_add_cc(mongo.db.Productions, form=form, pid=pid)
        flash("Cast and Crew has been added!")
        return redirect(url_for('main.production_detail', pid=pid))
    else:
        return render_template('add_cc.html', form=form, pid=pid)


@main.route("/remove_cast_crew/<pid>")
def remove_cast_crew(pid):
    op = db_open_record(mongo.db.Productions, pid)
    return render_template('cc_list.html', output=op, pid=pid)


@main.route("/remove_cc/<pid>/<Person>/<Role>")
def remove_cc(pid, Person, Role):
    db_remove_cc(mongo.db.Productions, Role, Person, pid)
    return redirect(url_for('main.remove_cast_crew', pid=pid))


@main.route("/utility/<name>")
def pull_list(name):
    match name:
        case 'People':
            output = db_pull_list(mongo.db.People)
            return render_template("utility_list.html", results=output, lname='People')
        case 'Company':
            output = db_pull_list(mongo.db.Company)
            return render_template("company_list.html", results=output, lname='Company')
        case 'Company Type':
            output = db_pull_list(mongo.db.Com_Type)
            return render_template("utility_list.html", results=output, lname='Company Type')
        case 'Show Type':
            output = db_pull_list(mongo.db.Prod_Type)
            return render_template("utility_list.html", results=output, lname='Show Type')


@main.route("/utility_update/<pid>,<lname>,<type>",  methods=['GET', 'POST'])
def utility_update(pid, lname, type):
    form = UtilityForm ()
    db1 =None
    match lname:
        case 'People':
            db1 = mongo.db.People
        case 'Company':
            db1 = mongo.db.Company
        case 'Company Type':
            db1 = mongo.db.Com_Type
        case 'Show Type':
            db1 = mongo.db.Prod_Type

    match type:
        case 'edit':
            if request.method == "POST":
                db_edit_utility_list(db1, form, pid)
                print(lname)
                return redirect(url_for('main.pull_list', name=lname))
            else:
                op = db_open_record(db1, pid)
                form.name.data = op['Name']
                form.active.data =op['Active']
                return render_template("edit_utility.html", form=form, type='Edit' ,lname=lname)

        case 'add':
            if request.method == "GET":
                return render_template("edit_utility.html", form=form, type='Add', lname=lname)
            else:
                pid = db_add_utility_list(db1, form)
                flash("Production has been added!")
                return redirect(url_for('main.pull_list', name=lname))


@main.route("/company_update/<pid>,<type>",  methods=['GET', 'POST'])
def company_update(pid, type):
    form = CompanyForm ()
    form.c_type.choices = com_type()
    match type:
        case 'edit':
            if request.method == "POST":
                db_edit_company_list(mongo.db.Company, form, pid)
                return redirect(url_for('main.pull_list', name='Company'))
            else:
                op = db_open_record(mongo.db.Company, pid)
                form.company.data = op['Name']
                form.active.data = op['Active']
                form.state.data = op['State']
                form.city.data = op['City']
                form.c_type.data = op['Type']
                print(form.c_type.data)
                return render_template("edit_company.html", form=form, type='Edit')

        case 'add':
            if request.method == "GET":
                return render_template("edit_company.html", form=form, type='Add')
            else:
                pid = db_add_company_list(mongo.db.Company, form)
                flash("Company has been added!")
                return redirect(url_for('main.company_list'))