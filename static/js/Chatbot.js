let form = document.querySelector(".question-and-answer-form");

$(".question-and-answer-form").submit(function(e){
    e.preventDefault();
    let inputdata = $("#questin-text-input").val();
    if(inputdata.length > 0){
        let allcourses = $(".course-section");
        let courseID = allcourses[0].getAttribute("data");

        $(this).get('/home', { courseid:courseID, question: inputdata }, function(response){ 
            console.log(response);
        });
    }else{
        let chatsection = document.querySelector(".chat-body");
        var newelm = document.createElement('div');
        newelm.classList.add("chat-bubble");
        newelm.classList.add("you");
        newelm.value = "Question length is zero. Please ask valid question.";
        console.log(newelm);
        chatsection.appendChild(newelm);

    }
    
})



