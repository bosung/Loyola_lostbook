Notices = new Meteor.Collection('notices');

Notices.allow({
  insert: function(userId, doc) {
    return !! userId;
  }
});
