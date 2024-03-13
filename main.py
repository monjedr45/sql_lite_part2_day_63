from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table, Float, Numeric, insert, VARCHAR, update, text, delete
from sqlalchemy.engine import result
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker



app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
class CafeForm(FlaskForm):
    book_name = StringField('book name', validators=[DataRequired()])
    book_author = StringField('book author', validators=[DataRequired()])
    rating = StringField('rating', validators=[DataRequired()])
    change_rating = StringField('change rating', validators=[DataRequired()])
    submit = SubmitField('submit')
    change = SubmitField('change')

database_url = 'sqlite:///new-books-collection.db'
engine = create_engine(database_url, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()
books = Table(
    'books', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique=True),
    Column('author', String),
    Column('rating', Float),
)
metadata.create_all(engine)
conn = engine.connect()

@app.route('/')
def home():
    all_books = []
    sql = text('SELECT * FROM books') 
    result = conn.execute(sql).fetchall()
    for record in result: 
        all_books.append(record)

    print(all_books)
    return render_template('index.html', books = all_books)

@app.route("/add", methods=['GET', 'POST'])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        Book_name = form.book_name.data
        Author_name = form.book_author.data
        Rating = form.rating.data
        print(Book_name, Author_name, Rating)

        try:
            insert_statement = books.insert().values(name=Book_name, author=Author_name, rating=Rating)
            conn.execute(insert_statement)
            session.commit()
            print("Data inserted successfully!")
        except Exception as e:
            print(f"Error: {e}")

    return render_template('add.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = CafeForm()
    if form.is_submitted() and form.validate_on_submit():
        try:
            sql_update = text('UPDATE books SET rating=:rating WHERE id=:id')
            conn.execute(sql_update, {'rating': form.change_rating.data, 'id': id})
            conn.commit()
            print("Rating updated successfully!")
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")

    return render_template('edit.html', form=form, id=id)

if __name__ == "__main__":
    app.run(debug=True)