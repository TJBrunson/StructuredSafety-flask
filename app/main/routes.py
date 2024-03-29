from flask import render_template, flash, redirect, url_for, request, current_app
import app
from app import db
from app.main import bp
from app.models import User, Company
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from flask import send_from_directory
import os

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/contact')
def contactUs():
    return render_template('contact-us.html', title='Contact Us ')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    company = Company.query.filter_by(owner_id = user.id).first()
    return render_template('user.html', user=user, company=company)

@bp.route('/company/<company_name>')
def company(company_name):
    company = Company.query.filter_by(company_name=company_name).first_or_404()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('company.html', company=company, user=user)

@bp.route('company/<company_name>/add_document', methods=['GET', 'POST'])
def addDocuments(company_name):
    title = company_name + " - Add a Document"
    return render_template('add_document.html', title=title)

@bp.route('company/<company_name>/fetch_file/<sub_directory>/<file_name>')
@bp.route('company/<company_name>/fetch_file/<sub_directory>/<sub_directory2>/<file_name>')
def fetchFile(company_name, sub_directory, sub_directory2, file_name):
    print(sub_directory)
    print(sub_directory2)
    path = '/Users/tim/Documents/uploads/companies/' + company_name + '/' + sub_directory
    if sub_directory2 != 'None':
        path = path + '/' + sub_directory2
    print("PATH: " + path)
    return send_from_directory(path, file_name)

@bp.route('/demo')
def demo():
    path = "/Users/tim/Documents" + "/uploads/companies/Demo"
    return render_template('demo.html', files = make_files(path), title = "Demo")

@bp.route('frahler-electric-company-pvjaxudmry')
def frahler():
    path = "/Users/tim/Documents" + "/uploads/companies/Frahler_Electric_Company"
    return render_template('hard-coded-company.html', files = make_files(path), title = "Frahler_Electric_Company")

@bp.route('mccoy-electric-qr-code-uvhu9jk1ia')
def mccoy():
    path = "/Users/tim/Documents" + "/uploads/companies/McCoy_Electric"
    return render_template('hard-coded-company.html', files=make_files(path), title="McCoy_Electric")

def make_files(path):
    tree = dict(name=os.path.basename(path), children=[])
    lst = os.listdir(path)
    for name in lst:
        fn = os.path.join(path, name)
        if os.path.isdir(fn):
            tree['children'].append(make_files(fn))
        else:
            if name.find(".") != 0:
                tree['children'].append(dict(name=name))
    
    for dic in tree['children']:
        sorted(dic.items())
    return tree