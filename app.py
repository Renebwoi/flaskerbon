from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

# books_list = [
#    { "id":0,
#     "author":"Chinua Achebe",
#     "language":"English",
#     "title":"Things Fall Apart",
#     },
#    {
#        "id":1,
#        "author":"Hans Christian Andersen",
#        "language": "Danish",
#        "title": "Fairy tales",
#    },
#    {
#        "id":2,
#        "author":"Jk Rowling",
#        "language": "English",
#        "title": "Harry Potter Sorcerer's stone",
#    },
#    {
#        "id":3,
#        "author":"Mary Anne",
#        "language": "Danish",
#        "title": "Little",
#    },
#    {
#        "id":4,
#        "author":"Jk Rowling",
#        "language": "English",
#        "title": "Harry Potter Prisoner of Azkaban",
#    },
#    {
#        "id":5,
#        "author":"Jk Rowling",
#        "language": "English",
#        "title": "Harry Potter Deathly Hallows 1",
#    },
#    {
#        "id":6,
#        "author":"Jk Rowling",
#        "language": "English",
#        "title": "Harry Potter Deathly Hallows 2",
#    }
# ]

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        # if len(books_list) > 0:
        #     return jsonify(books_list)
        # else:
        #     'Nothing Found', 404
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)                      
            
    if request.method == 'POST':
        new_author =request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        iD = books_list[-1]['id']+1
        
        # creating an object with these values and appending to the books_list
        new_obj = {
            'id': iD,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }
        books_list.append(new_obj)
        return jsonify(books_list), 201
    
@app.route('/book/<int:id>', methods=['GET','PUT','DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
            pass
    if request.method == 'PUT':
        for book in books_list:
            if book['id'] == id:
                book['author'] = request.form['author']
                book['language'] = request.form['language']
                book['title'] = request.form['title']
                updated_book = {
                    'id': id,
                    'author': book["author"],
                    'language': book["language"],
                    'title': book["title"]
                }
                return jsonify(updated_book)
    if request.method == 'DELETE':
        for index, book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(index)
                return jsonify(books_list)

def print_name(name):
    return 'Hi , {}'.format(name)

if __name__=='__main__':
    app.run(debug=True)