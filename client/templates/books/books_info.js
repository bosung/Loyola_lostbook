Template.bookInfo.helpers({
  domain: function() {
    var a = document.createElement('a');
	a.href = this.addr;
	return a.hostname;
  }
});

