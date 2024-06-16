from flask import Flask, request, jsonify
from pymongo import MongoClient 
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

# def db_connection():
#     conn = None
#     try:
#         conn = sqlite3.connect('books.sqlite')
#     except sqlite3.error as e:
#         print(e)
#     return conn

# the database connection. it can return the connection to two collections:
# the books databas and orders databas
def db_connection(databas):
    client = MongoClient('mongodb://localhost:27017/') 
    db = client['bookstore'] 
    collection = db['books']
    collection2 = db['orders']
    # db_books_list = json.dumps(books_list)
    # collection.insert_many(books_list)
    # collection2.insert_one({
    #     'username': 'rene',
    #     'book_id': 3,
    #     'status':'completed',
    #     'order_id': 1
    #     })
    if databas == 'books':
        return collection
    elif databas == 'orders':
        return collection2



@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection('books')
    
    if request.method == 'GET':
        # got complex really quick
        # if the document in collection is not 0, get a cursor to iterate over the collection, store each book in doc_array and return 
        # doc array
        conn_count = int(conn.count_documents({}) )
        if conn_count > 0:
            cursor = conn.find({ })
            doc_array = []
            for books in cursor:
                doc_array.append(books)
            return f'{doc_array}'
        else:
            'Nothing Found', 404                    
            
    if request.method == 'POST':
        new_author =request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']
        # this print outputs the id of the last document. conn.find gets all doc in conn, 
        # .sort arranges them in descending order(from last to first),
        # .limit returns only one, .next because the shit returns a cursor😡...
        # 😑 then id to give me only the id. omit that part to get the entire document
        # print("here",conn.find({ }).sort({'id':-1}).limit(1).next()['id'])
        iD = conn.find({ }).sort({'id':-1}).limit(1).next()['id']+1
        
        # creating an object with these values and appending to the books_list(or the collection)
        new_obj = {
            'id': iD,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }
        
        # books_list.append(new_obj)
        conn.insert_one(new_obj)
        
        # just returning the collection. When i find a better way, i will change here 
            
        return f'{new_title} by {new_author} has been added with id {iD}', 201
        
        # return jsonify(books_list), 201
    
@app.route('/book/<int:id>', methods=['GET','PUT','DELETE'])
def single_book(id):
    conn = db_connection('books')
    if request.method == 'GET':
        selected_book = conn.find_one({'id':id})
        return f'{selected_book}'
        # # get all documents in collection, returns a cursor
        # cursor = conn.find({ })
        # # print("cursor is", cursor.next())
        # conn_count = int(conn.count_documents({}) ) #lenght of the collection
        # # loop over conn_count while pressing next on the cursor.
        # # when the cursor is same as given id, the doc value will be the doc at that id
        # # potential synchronicity issues in this, to be fixed later 
        # for book_num in range(conn_count):
        #     doc = cursor.next()
        #     if book_num == id:
        #         return f'{doc}'
        #     pass
    if request.method == 'PUT':
        selected_book = conn.find_one({'id':id})
        selected_book['author'] = request.form['author']
        selected_book['language'] = request.form['language']
        selected_book['title'] = request.form['title']
        return f"Book with name {selected_book['title']} and id {selected_book['id']} has been updated"
        
    if request.method == 'DELETE':
        selected_book = conn.find_one_and_delete({'id':id})
        return f"Book with name {selected_book['title']} and id {selected_book['id']} has been deleted"
        
            
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