from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.main import bp
from app.models import User, Company
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    company = Company.query.filter_by(owner_id = user.id).first()
    return render_template('user.html', user=user, company=company)

@bp.route('/demo')
def demo():
    return render_template('demo.html', title="Demo")

@bp.route('/company/<company_name>')
def company(company_name):
    company = Company.query.filter_by(company_name=company_name).first_or_404()
    user = User.query.filter_by(username=current_user.username).first_or_404()
    return render_template('company.html', company=company, user=user)

@bp.route('company/<company_name>/add_document', methods=['GET', 'POST'])
def addDocuments(company_name):
    title = company_name + " - Add a Document"
    return render_template('add_document.html', title=title)