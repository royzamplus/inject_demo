#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from flaskext.mysql import MySQL    # pip install Flask-Mysql
from flask.ext.bootstrap import Bootstrap

mysql = MySQL()
app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123456'
app.config['MYSQL_DATABASE_DB'] = 'inject_demo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'hard to guess string'

mysql.init_app(app)


class BookForm(Form):
    title = StringField('Book title')
    arthor = StringField('Arthor')
    publisher = StringField('Publisher')
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html', name='haha')


@app.route('/books', methods=['GET'])
def view_books():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, title, arthur, publisher FROM book WHERE 1=1")
    booklist = cursor.fetchall()
    return jsonify({'books':booklist})


@app.route('/books/<book_id>', methods=['GET'])
def view_book(book_id):
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT id, title, arthur, publisher FROM book WHERE id=" + book_id + " ORDER BY id DESC")
    book = cursor.fetchall()
    return render_template('book.html', book=book)
    # return jsonify({'book':book})


@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if request.method == 'POST':
        title = form.title.data
        arthor = form.arthor.data
        publisher = form.publisher.data
        sql = "INSERT INTO book(title, arthur, publisher) VALUES ('" + title + "','" + arthor + "','" + publisher + "')"
        print sql
        cursor = mysql.get_db().cursor()
        cursor.execute(sql)
        return redirect(url_for('view_books'))
    return render_template('add_book.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)