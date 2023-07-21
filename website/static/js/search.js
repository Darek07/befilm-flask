function performSearch() {
    var searchQuery = document.getElementById('searchInput').value.toLowerCase();
    var records = document.getElementsByClassName('note');

    for (var i = 0; i < records.length; i++) {
        var record = records[i];
        var recordText = record.innerText.toLowerCase();

        if (recordText.includes(searchQuery)) {
            record.style.display = 'block';  // Show matching record
        } else {
            record.style.display = 'none';   // Hide non-matching record
        }
    }
}