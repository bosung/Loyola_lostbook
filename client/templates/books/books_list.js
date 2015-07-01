// This is template helper.
// in books_list.html, we declared helper named "books" in block helper.
// This helper returns all Books objects. -- by. bosung

Template.bookList.helpers({
  books: function() {
    return Books.find();
  }
});
