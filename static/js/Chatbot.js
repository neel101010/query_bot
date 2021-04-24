let form = document.querySelector(".question-and-answer-form");

$(".question-and-answer-form").submit(async function(e){
    e.preventDefault();
    let inputdata  = $("#questin-text-input").val();
    if(inputdata.length > 0){
        let chatsection = document.querySelector(".chat-body");
        var questionText = document.createElement('div');
        questionText.classList.add("chat-bubble");
        questionText.classList.add("me");
        var textNode = document.createTextNode(inputdata);
        questionText.appendChild(textNode);
        chatsection.appendChild(questionText);
        var newelm = document.createElement('div');
        let elmdata = `<div id="chat-loading-bubble" class="chat-bubble you">
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
            <circle cx="0" cy="44.1678" r="15" fill="#ffffff">
                <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate>
            </circle> <circle cx="45" cy="43.0965" r="15" fill="#ffffff">
            <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate>
        </circle> <circle cx="90" cy="52.0442" r="15" fill="#ffffff">
            <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate>
        </circle></svg>
    </div>`;
        newelm.innerHTML = elmdata;
        chatsection.appendChild(newelm);
        console.log(newelm);
        let allcourses = $(".course-section");
        let courseID = allcourses[0].getAttribute("data");
        let data = new FormData();
        data.append("question" , inputdata);
        let url = "/home/chat/" + courseID;
        const csrftoken = Cookies.get('csrftoken');
        fetch(url , { method : "POST",
          body : data,
          mode : "cors",
          cache : "no-cache",
          credentials : "same-origin",
          header : {
              "Content-type" : "application/json",
              "X-CSRFToken": csrftoken
          },
          redirect : "follow",
          refferrer : "no-referrer"
        }).then(response => response.json()).then(data => {
            let chatbubble = document.querySelector("#chat-loading-bubble");
            chatbubble.remove();
            let chatsection = document.querySelector(".chat-body");
            var newelm = document.createElement('div');
            newelm.classList.add("chat-bubble");
            newelm.classList.add("you");
            var textnode = document.createTextNode(data.answer);
            newelm.appendChild(textnode);
            chatsection.appendChild(newelm);
        }).catch(err => {
            console.log(err);
        });
        
    }else{
        let chatsection = document.querySelector(".chat-body");
        var newelm = document.createElement('div');
        newelm.classList.add("chat-bubble");
        newelm.classList.add("you");
        var textnode = document.createTextNode("Question length is zero. Please ask valid question.");
        newelm.appendChild(textnode);
        chatsection.appendChild(newelm);
    }
    
})



