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
	'click #btnSubmit': function(e,t){
		var con = String(e.target.value || "");
		if( con ){
			Notices.insert({"contents":con});
			Session.set('addNotice',false);
		}
	},
	'click #btnCancel': function(){
		Session.set('addNotice',false);
	}
});
