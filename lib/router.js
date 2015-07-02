Router.configure({
	// set basic layout for every route
	layoutTemplate: 'layout',
	loadingTemplate: 'loading',
	waitOn: function() { return Meteor.subscribe('books'); }
});

Router.route('/', {name: 'bookList'});

