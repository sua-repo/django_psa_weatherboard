document.getElementById('commentImage').addEventListener('change', function(event) {
    var preview = document.getElementById('preview');
    var file = event.target.files[0];

    if (file) {
        var reader = new FileReader();

        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        };

        reader.readAsDataURL(file);
    } else {
        preview.src = "#";
        preview.style.display = 'none';
    }
});