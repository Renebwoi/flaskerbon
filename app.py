from flask import Flask, request, jsonify
from pymongo import MongoClient 
import json
import sqlite3
from dotenv import load_dotenv
import os

import google.generativeai as genai

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
    load_dotenv()
    database_url = os.getenv('DATABASE_URI')
    client = MongoClient(database_url) 
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
    conn = db_connection('orders')
    if request.method == 'POST':
        order_iD = conn.find({ }).sort({'order_id':-1}).limit(1).next()['order_id']+1
        username = request.form['username']
        book_id =int(request.form['book_id'])
        order = {
            'username': username,
            'book_id': book_id,
            'status': 'ordered',
            'order_id': order_iD
        }
        conn.insert_one(order)
        return f"{username} has ordered the book with id {book_id}"
       

    if request.method == 'GET':
        conn_count = int(conn.count_documents({}) )
        if conn_count > 0:
            cursor = conn.find({ })
            doc_array = []
            for books in cursor:
                doc_array.append(cursor.next())
            return f'{doc_array}'
        else:
            return 'Nothing Found', 404  
        
# function to generate book summary. Later iterations will be to support file upload for better summary
# and pay for OpenAI api so i can use that instead. For now the post request can simply ask for a 
# summary of the book.
@app.route('/summary', methods=['POST'])
def summary():
    if request.method == 'POST':
            
        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # Create the model
        # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }


        model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
        # safety_settings = Adjust safety settings
        )

        chat_session = model.start_chat(
        history=[
        ]
        )

        book_name = request.form["bookname"]
        author = request.form['author']
        response = chat_session.send_message(f"In one paragraph only, summarize the book {book_name} by {author}. Don't spoil the books story entirely. Just return a bit of the story along with some engaging sentences on it's theme")

        return response.text       





def print_name(name):
    return 'Hi , {}'.format(name)

if __name__=='__main__':
    app.run(debug=True)