from fastapi import FastAPI,HTTPException,Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book(BaseModel):
    id:int
    title: str
    author: str
    price : float = Field(gt=0)
    in_stock : bool

books =[
    {"id":1,"title":"Harry Potter","author":"J K Rowling","price":400,"in_stock":True},
    {"id":2,"title":"Sherlock Holmes","author":"Arthur Conan Doyle","price":700,"in_stock":False},
    {"id":3,"title":"The Alchemist","author":"Paulo Coelho", "price":600,"in_stock":True}
]

@app.get("/books")
def get_all_books():
    return {"books": books}

@app.get("/books/count")
def get_books_count():
    return {"total_books": len(books)}

@app.get("/books/available")
def get_available_books():
    available_books = [b for b in books if b["in_stock"]]
    return {"available_books": available_books}

@app.get("/books/search")
def search_books(
        author: Optional[str] = Query(None),
        max_price: Optional[float] = Query(None)
):
    filtered_books = books
    if author is not None:
        filtered_books = [b for b in filtered_books if author.lower() in b["author"].lower()]
    if max_price is not None:
        filtered_books = [b for b in filtered_books if b["price"] <= max_price]
    return {"results": filtered_books}

@app.get("/books/{book_id}")
def get_book(book_id:int):
    for b in books:
        if b["id"] == book_id:
            return b
    raise HTTPException(status_code=404, detail="book not found")

@app.post(path="/books",status_code=201)
def add_book(book: Book):
    for b in books:
        if b["id"] == book.id:
            return{"message":"book already exists"}
    books.append(book.dict())
    return {"message":"Book added successfully","book":book}



@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book : Book):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            books[i] = updated_book.dict()
            return {"message":"Book updated","book":updated_book}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, b in enumerate(books):
        if b["id"] == book_id:
            del books[i]
            return {"message": "Book deleted successfully", "book":b}
    raise HTTPException(status_code=404, detail="Book not found")


