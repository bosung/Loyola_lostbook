Meteor.publish('books', function() {
  return Books.find();
});

Meteor.publish('notices', function() {
  return Notices.find();
});
