document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('uploadResult');
        if (data.error) {
            resultDiv.innerHTML = '<p style="color: red;">' + data.error + '</p>';
        } else {
            resultDiv.innerHTML = '<p style="color: green;">' + data.message + '</p>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
