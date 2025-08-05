

// 삭제할 기존 이미지 id를 저장
let deletedImageIds = [];

function removeExistingImage(imageId) {
    deletedImageIds.push(imageId);
    document.querySelector(`[data-image-id="${imageId}"]`).remove();
    document.getElementById('delete-images').value = deletedImageIds.join(',');
}

// 새로 추가할 이미지 관리
let selectedFiles = [];

document.getElementById('image').addEventListener('change', function(event) {
    const newFiles = Array.from(event.target.files);
    selectedFiles = selectedFiles.concat(newFiles);
    renderPreviews();
});

function renderPreviews() {
    const previewContainer = document.getElementById('image-preview-container');
    
    // 기존 삭제 요청이 된 이미지 제외하고 기존 이미지 표시
    const existingWrappers = document.querySelectorAll('[data-image-id]');
    existingWrappers.forEach(wrapper => {
        previewContainer.appendChild(wrapper);
    });

    // 추가 업로드할 이미지 표시
    selectedFiles.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const wrapper = document.createElement('div');
            wrapper.className = 'post-edit-image-wrapper';

            const img = document.createElement('img');
            img.src = e.target.result;
            img.className = "post-edit-image rounded";

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'X';
            deleteBtn.className = 'btn btn-danger btn-sm position-absolute top-0 end-0 image-remove-btn';
            deleteBtn.addEventListener('click', () => {
                selectedFiles.splice(index, 1);
                renderPreviews();
            });

            wrapper.appendChild(img);
            wrapper.appendChild(deleteBtn);
            previewContainer.appendChild(wrapper);
        };
        reader.readAsDataURL(file);
    });
}

// submit
document.getElementById('post-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', document.querySelector('[name="csrfmiddlewaretoken"]').value);
    formData.append('category', document.getElementById('category').value);
    formData.append('title', document.getElementById('title').value);
    formData.append('content', document.getElementById('content').value);
    formData.append('delete_images', document.getElementById('delete-images').value);

    selectedFiles.forEach(file => {
        formData.append('images', file);
    });

    fetch(window.location.href, {
        method: "POST",
        body: formData,
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            alert("업로드 실패");
        }
    })
    .catch(error => {
        console.error(error);
        alert("에러가 발생했습니다.");
    });
});
