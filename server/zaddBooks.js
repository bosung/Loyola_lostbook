console.log("Hello World\n");

var fs = Meteor.npmRequire('fs');
var data = {};

fs.readFile('../lib/collection/updateBooks.json', 'utf-8', function(err, content){
	data = content;
});

for ( var i in data ) {
	if( data[i].status == "last" ) 
		break;
	if(data[i].status == "대출가능") { 
		data[i].checked=false; 
	} else { 
		data[i].checked = true; checkedBookNum++; 
	} 
	
	Books.update(data[i],{$set:{"status":data[i].status}},{upsert:true}); 
}
