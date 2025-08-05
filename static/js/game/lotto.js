// 로또 번호 랜덤으로 6개 만들어주는 함수 
function getLottoNum() {
    const lottoSet = new Set()  // 중복 막기 위해 Set 사용

    while (lottoSet.size < 6) {
        const num = Math.floor(Math.random() * 45) + 1  // 1 ~ 45사이 숫자
        lottoSet.add(num)   
    }
    return Array.from(lottoSet)
}

// 번호 별 색상
function getColor(num) {
    let color = ""
    if (num <= 10) {
        color = 'gold'
    } 
    else if (num <= 20) {
        color = 'blue'
    } 
    else if (num <= 30) {
        color = 'red'
    } 
    else if (num <= 40) {
        color = 'gray'
    }
    else {
        color = 'green'
    }
    return color
}

// 로또 번호 화면에 출력하는 함수
function drawLottoNumbers() {
    const container = document.getElementById("lottoArea");  // 번호가 들어갈 div
    const balls = container.querySelectorAll("div");  // lottoArea 안에 있는 6개의 div들

    const numbers = getLottoNum();  // 랜덤한 숫자 6개 뽑기

    numbers.forEach((num, index) => {
        balls[index].textContent = num;  // 텍스트 설정
        balls[index].style.backgroundColor = getColor(num);  // 배경색 설정
    });
}

// 페이지가 처음 열릴 때 한 번 그려줌
document.addEventListener("DOMContentLoaded", () => {
    drawLottoNumbers();

    // 클릭 시 새 번호로 교체
    const lottoArea = document.getElementById("lottoArea");
    lottoArea.addEventListener("click", drawLottoNumbers);
});
