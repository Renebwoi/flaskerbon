<!-- This project is an api for a bookstore that allows the user to make orders, view books, view the status of the orders etc -->

# These are the available commands for the api

## for "/books" endpoint, GET and POST commands are available

GET returns all the registered books in the bookstore. each book has an author, title and automatically added id.

POST is for reistering in a new book. You have to give the author, language and title. Later we shall add it's summary and content.

## for "'/book/<int:id>'" endpoint, GET, PUT and DELETE commands are available

GET will return the details of the book with the matching id

PUT will update the details of the book with that id. You have to provide the new author, language and title

DELETE will delete the details of the book with matching id.

## for "/order" endpoint, GET and POST commands are available

GET will return all orders

POST will add a new order. It requires the username, book_id and an automatically generated order_id

## for "'/order/<int:id>'" endpoint, GET, PUT and DELETE commands are available

GET will get the order with the matching id

PUT will update that order details. It requires the username, book id and status(optional, defaults to ordered when not given)

DELETE will delete the order with matching id from the database

## for "/summary" endpoint, only POST command is available

POST will require the bookname and author and will use it generate a summary of the book and return that summary