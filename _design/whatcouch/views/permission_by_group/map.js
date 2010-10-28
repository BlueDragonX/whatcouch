function(doc) {
	if (doc.doc_type == 'Group') {
		for (var i = 0; i < doc.permissions.length; i++) {
			emit(doc.name, doc.permissions[i]);
		}
	}
}
