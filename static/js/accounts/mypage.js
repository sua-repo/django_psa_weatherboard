const filterSelect = document.getElementById('filterSelect');
const postList = document.getElementById('post-list');
const commentList = document.getElementById('comment-list');
const likeList = document.getElementById('like-list');
const scrapList = document.getElementById('scrap-list');

function updateActivityList() {
    const selected = filterSelect.value;
    postList.style.display = (selected === 'all' || selected === 'posts') ? 'block' : 'none';
    commentList.style.display = (selected === 'all' || selected === 'comments') ? 'block' : 'none';
    likeList.style.display = (selected === 'all' || selected === 'likes') ? 'block' : 'none';
    scrapList.style.display = (selected === 'all' || selected === 'scraps') ? 'block' : 'none';
}

// 셀렉트 박스 값이 변경될 때
filterSelect.addEventListener('change', function() {
    const selected = filterSelect.value;
    // 페이지를 새로 요청 (filter값 추가)
    window.location.href = "?filter=" + selected;
});

// 페이지 로드 시, 현재 선택된 필터 옵션을 셋팅
window.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const currentFilter = urlParams.get('filter') || 'all';
    filterSelect.value = currentFilter;
});
