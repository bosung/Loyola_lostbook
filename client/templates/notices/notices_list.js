Template.noticeList.helpers({
	notices: function() {
		return Notices.find();
	},
	newNotice: function() {
		return Session.equals('addNotice',true);
	}
});

Session.set('addNotice', false);

Template.noticeList.events({
	'click #btnNewNotice': function(){
		Session.set('addNotice', true);

		Meteor.flush();
		//(t.find("#add-notice")).focus();
		//(t.find("#add-notice")).select();
	},
	'submit form': function(e) {
		e.preventDefault();
		
		var d = new Date();
		var date = d.toDateString();
		var con = $(e.target).find('[name=add-notice]').val();
		if( con ){
			Notices.insert({"date":date ,"writer":Meteor.user().username, "contents":con});
			Session.set('addNotice',false);
		}
	},
	'click #btnCancel': function(){
		Session.set('addNotice',false);
	}
});
