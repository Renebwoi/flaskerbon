from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)

books_list = [
   { "id":0,
    "author":"Chinua Achebe",
    "language":"English",
    "title":"Things Fall Apart",
    },
   {
       "id":1,
       "author":"Hans Christian Andersen",
       "language": "Danish",
       "title": "Fairy tales",
   },
   {
       "id":2,
       "author":"Jk Rowling",
       "language": "English",
       "title": "Harry Potter Sorcerer's stone",
   },
   {
       "id":3,
       "author":"Mary Anne",
       "language": "Danish",
       "title": "Little",
   },
   {
       "id":4,
       "author":"Jk Rowling",
       "language": "English",
       "title": "Harry Potter Prisoner of Azkaban",
   },
   {
       "id":5,
       "author":"Jk Rowling",
       "language": "English",
       "title": "Harry Potter Deathly Hallows 1",
   },
   {
       "id":6,
       "author":"Jk Rowling",
       "language": "English",
       "title": "Harry Potter Deathly Hallows 2",
   }
]
# statuses - pending (ordered order_fail) processing (delivered deliver_fail) completed
orders_list = [{
    'username': 'rene',
    'book_id': 3,
    'status':'completed',
    'order_id': 1
    }
]

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
        if len(books_list) > 0:
            return jsonify(books_list)
        else:
            'Nothing Found', 404
        # cursor = conn.execute("SELECT * FROM book")
        # books = [
        #     dict(id=row[0], author=row[1], language=row[2], title=row[3])
        #     for row in cursor.fetchall()
        # ]
        # if books is not None:
        #     return jsonify(books)                      
            
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
            
# to place an order
@app.route('/order', methods=['POST','GET','PUT','DELETE'])
def orders():
    if request.method == 'POST':
        # for post, if the id is in the filtered array of book list ids, add the order details
        # to the orders_list array and return. else, the book is not in the library.
        id=int(request.form['book_id'])
        id_array = []
        for book in books_list:
            id_array.append(book['id'])
            
        if id in id_array:
            username = request.form['username']
            book_id =int(request.form['book_id'])
            order = {
                'username': username,
                'book_id': book_id,
                'status': 'ordered',
                'order_id': orders_list[-1]['order_id']+1
            }
            
            orders_list.append(order)
            return jsonify(orders_list)
        else:
            return "Book is not in our library"

    if request.method == 'GET':
        # if get, then assign an array. list of orders will be filtered by the username only if book_id parameter is 0(no book specified).
        # else it is also filtered by the book id and returned.
        order_display = []
        for orders in orders_list:
            if orders['username'] == request.form['username']:
                if int(request.form['book_id']) == 0:
                    order_display.append(orders)
                elif int(request.form['book_id']) == orders['book_id']:
                    order_display.append(orders['status'])
        return jsonify(order_display)






def print_name(name):
    return 'Hi , {}'.format(name)

if __name__=='__main__':
    app.run(debug=True)