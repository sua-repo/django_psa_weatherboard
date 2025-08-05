
document.addEventListener("DOMContentLoaded", function() {
    const btnScissor = document.getElementById("btn-scissor")
    const btnRock = document.getElementById("btn-rock")
    const btnPaper = document.getElementById("btn-paper")

    const userImg = document.getElementById("user-img")
    const comImg = document.getElementById("com-img")
    const comChoiceBtn = document.getElementById("com-choice")
    const judgeText = document.getElementById("judge-text")

    const rspList = ["가위", "바위", "보"]
    const rspImgMap = {
        "가위" : "{% static 'game/rsp/scissor.jpg' %}", 
        "바위" : "{% static 'game/rsp/rock.jpg' %}", 
        "보" : "{% static 'game/rsp/paper.jpg' %}"
    }

    
    let win = 0
    let draw = 0
    let lose = 0

    let result = ""

    // 결과 판정
    function judgeResult(user, com) {
        if (user === com) {
            draw++
            result = "비겼습니다."
        }

        else if ((user === "가위" && com === "보") || (user === "바위" && com === "가위") || (user === "보" && com === "바위")) {
            win++
            result = "당신이 이겼습니다."
        }

        else {
            lose++
            result = "컴퓨터가 이겼습니다."
        }

        return result
    }

    function updateRecord() {
        document.getElementById("record").textContent = `${win}승 ${draw}무 ${lose}패`
    }

    function run(userChoice) {
        // 사용자 이미지 변경
        userImg.src = rspImgMap[userChoice]

        // 컴퓨터 랜덤 선택
        const comChoice = rspList[Math.floor(Math.random() * 3)]
        comImg.src = rspImgMap[comChoice]
        comChoiceBtn.textContent = comChoice

        // 심판 결과
        judgeText.textContent = judgeResult(userChoice, comChoice)
        updateRecord()
        
        console.log(userChoice, comChoice)
    }

    // 버튼 이벤트 등록 
    btnScissor.addEventListener("click", () => run("가위"))
    btnRock.addEventListener("click", () => run("바위"))
    btnPaper.addEventListener("click", () => run("보"))
})
