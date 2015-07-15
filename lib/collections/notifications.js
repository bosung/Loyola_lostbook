Notifications = new Meteor.Collection('notification');

Notifications.allow({
  update: function(userId, doc, fieldNames) {
    return ownsDocument(userId, doc) && fieldNames.length === 1 && fieldNames[0] === 'read';
  }
});

createNoticeNotification = function(notice) {
  if( notice.newFlag == true ){
	Notification.insert({
	  userId: notice.writer,
	  noticeId: notice._id,
	  read: false
	});
  }
};

