function previewImage() {
    const fileInput = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const maxWidth = 500;
    const maxHeight = 300;

    // Check if a file is selected
    if (fileInput.files && fileInput.files[0]) {
      const reader = new FileReader();
      const file = fileInput.files[0];

      // Set up the FileReader onload event
      reader.onload = function(e) {
            const img = new Image();
            img.onload = function() {
                let width = img.width;
                let height = img.height;

                // Check image dimensions
                if (width > maxWidth || height > maxHeight) {
                    // Resize the image
                    if (width > maxWidth) {
                        height *= maxWidth / width;
                        width = maxWidth;
                    }

                    if (height > maxHeight) {
                        width *= maxHeight / height;
                        height = maxHeight;
                    }
                }

                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = width;
                canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);
                const resizedDataUrl = canvas.toDataURL(file.type);

                imagePreview.src = resizedDataUrl;
                imagePreview.style.display = 'block';
            };
            console.log("resizing");
            img.src = e.target.result;
      };

      // Read the selected file as a URL
      reader.readAsDataURL(fileInput.files[0]);
    }
}

const fileInput = document.getElementById('imageUpload');
fileInput.addEventListener('change', previewImage);
