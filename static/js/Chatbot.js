let form = document.querySelector(".question-and-answer-form");
let chatsection = ""; 
const csrftoken = Cookies.get('csrftoken');
let inputquestiontext = "";
$(".question-and-answer-form").submit(async function(e){
    try { 
        e.preventDefault();

        // Make api call for text classification
        //   if yes
        //     GP2 chatbot call
        //   else 
        //     Make call for FAQ question match
        //     Make call for Question generation Albert model 

        chatsection = document.querySelector(".chat-body");
        let inputdata  = $("#questin-text-input").val();
        inputquestiontext = inputdata;
        $("#questin-text-input").val("");
        if(inputdata.length > 0){
            // Putting question on chatnot
            
            var questionText = document.createElement('div');
            questionText.classList.add("chat-bubble");
            questionText.classList.add("me");
            var textNode = document.createTextNode(inputdata);
            questionText.appendChild(textNode);
            chatsection.appendChild(questionText);
            // ===================

            var newelm = document.createElement('div');
            // Loading animation ==
            let elmdata = `<div id="chat-loading-bubble" class="chat-bubble you">
                <span class="processing-text">Processing your question</span> 
                <svg class="svg-chat-section" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                    <circle cx="0" cy="44.1678" r="15" fill="#ffffff">
                        <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate>
                    </circle> <circle cx="45" cy="43.0965" r="15" fill="#ffffff">
                    <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate>
                    </circle> <circle cx="90" cy="52.0442" r="15" fill="#ffffff">
                        <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate>
                    </circle>
                </svg>
            </div>`;
            
            // Loading response from chatbot
            newelm.innerHTML = elmdata;
            chatsection.appendChild(newelm);
            console.log(newelm);
            // ===== 
            let allcourses = $(".course-section");
            let courseID = allcourses[0].getAttribute("data");
            let videoID = 0;

            let data = new FormData();
            data.append("question" , inputdata);
            let url = "/home/chat/classifytext/" +  courseID  + "/"+ videoID;
            const csrftoken = Cookies.get('csrftoken');
            // First API call 
            // console.log(typeof(courseID))
            let textclassifierresponse = await fetch(url , { 
                method : "POST",
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
            });
            
            
            // Setting chatbot response === 
            let textclassifierdata = await textclassifierresponse.json();
            console.log(textclassifierdata);
            


            if(textclassifierdata.value === 0){
                // Chatbot with general conversation
                let gpt2url =  "/home/chat/gpt2chatbot/" + courseID + "/" + videoID;
                let gpt2response = await fetch(gpt2url , { method : "POST",
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
                });
                // Setting chatbot response === 
                let chatbubble = document.querySelector("#chat-loading-bubble");
                chatbubble.remove();
                let gpt2responsedata = await gpt2response.json();
                console.log(gpt2responsedata);
                var newelm = document.createElement('div');
                newelm.classList.add("chat-bubble");
                newelm.classList.add("you");
                var textnode = document.createTextNode(gpt2responsedata.answer);
                newelm.appendChild(textnode);
                chatsection.appendChild(newelm);    
            }else{
                let chatbubble = document.querySelector("#chat-loading-bubble");
                chatbubble.remove();
                // Checking similar question in FAQ forum
                var newelm = document.createElement('div');
                // Loading animation ==
                let elmdata = `<div id="chat-loading-bubble" class="chat-bubble you">
                    <span class="processing-text">Checking similar question in FAQ</span> 
                    <svg class="svg-chat-section" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                        <circle cx="0" cy="44.1678" r="15" fill="#ffffff">
                            <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate>
                        </circle> <circle cx="45" cy="43.0965" r="15" fill="#ffffff">
                        <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate>
                        </circle> <circle cx="90" cy="52.0442" r="15" fill="#ffffff">
                            <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate>
                        </circle>
                    </svg>
                </div>`;
                newelm.innerHTML = elmdata;
                chatsection.appendChild(newelm);
                // API reques for similar match
                let similarquestionurl =  "/home/chat/similarmatch/" + courseID + "/" + videoID;
                let similarquestionresponse = await fetch(similarquestionurl , { method : "POST",
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
                });
                

                let chatbubble2 = document.querySelector("#chat-loading-bubble");
                chatbubble2.remove();
                // Setting chatbot response === 
                let similarquestiondata = await similarquestionresponse.json();
               
                if(similarquestiondata.ismatched){
                    var newelm = document.createElement('div');
                    // Loading animation ==
                    let elmdata = `<div id="chat-faq-section" class="chat-bubble you">
                        <span class="processing-text">Found match in FAQ.<span> 
                        <i id="right-id" class="fas fa-check-circle"></i>
                    </div>`;
                    newelm.innerHTML = elmdata;
                    chatsection.appendChild(newelm);
                    var newelm = document.createElement('div');
                    newelm.classList.add("chat-bubble");
                    newelm.classList.add("you");
                    let newelmdata = `<p style="color : white;"><span style="font-weight : 600;">Question: </span>${similarquestiondata.matchedquestion} </p>
                    <p style="color : white;"><span style="font-weight : 600;">Answer: </span>${similarquestiondata.matchedanswer} </p>
                    `;
                    newelm.innerHTML = newelmdata;
                    chatsection.appendChild(newelm);

                    // Ask for user that it that useful or not
                    let isuserfuldiv =  await isuserfulbuttons();
                    let nobuttonselection = document.querySelector("#useful-no-button");
                    nobuttonselection.addEventListener("click" , function(){
                        isuserfuldiv.remove();
                        questionandanswers();
                    });

                    let yesbuttonselection = document.querySelector("#useful-yes-button");
                    yesbuttonselection.addEventListener("click" , function(){
                        isuserfuldiv.remove();
                    });

                }else{

                    var newelm = document.createElement('div');
                    // Loading animation ==
                    let elmdata = `<div id="chat-faq-section" class="chat-bubble you">
                        <span class="processing-text">No similar question exist in FAQ.<span> 
                        <i id="wrong-id" style="color :red;" class="fas fa-times-circle"></i>
                    </div>`;
                    newelm.innerHTML = elmdata;
                    chatsection.appendChild(newelm);
                }

                // If not then Send for question generation model   
                if(!similarquestiondata.ismatched){
                      // IF the answer does not exist then generate the asnwer 
                      questionandanswers();
                      
                }
            }
        }else{
            let chatsection = document.querySelector(".chat-body");
            var newelm = document.createElement('div');
            newelm.classList.add("chat-bubble");
            newelm.classList.add("you");
            var textnode = document.createTextNode("Question length is zero. Please ask valid question.");
            newelm.appendChild(textnode);
            chatsection.appendChild(newelm);
        }

    }catch(err){
        console.log(err.message);
    }
})



async function questionandanswers(){
    var newelm = document.createElement('div');
    // Loading animation ==
    let elmdata = `<div id="chat-loading-bubble" class="chat-bubble you">
        <span class="processing-text">Generating Answer. please wait it can take long time</span> 
        <svg class="svg-chat-section" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
            <circle cx="0" cy="44.1678" r="15" fill="#ffffff">
                <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate>
            </circle> <circle cx="45" cy="43.0965" r="15" fill="#ffffff">
            <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate>
            </circle> <circle cx="90" cy="52.0442" r="15" fill="#ffffff">
                <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate>
            </circle>
        </svg>
    </div>`;
    newelm.innerHTML = elmdata;
    chatsection.appendChild(newelm);
    let courseID = 1;
    let videoID = 0;
    let data = new FormData();
    data.append("question" , inputquestiontext);
    
    let QuestionAndAnswerURL =  "/home/chat/generateanswer/" + courseID  + "/"+ videoID;
    let QuestionAndAnswerRes = await fetch(QuestionAndAnswerURL , { method : "POST",
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
    });
    let chatbubble = document.querySelector("#chat-loading-bubble");
    chatbubble.remove();
    let QuestionAndAnswerdata = await QuestionAndAnswerRes.json();

    var newelm = document.createElement('div');
    newelm.classList.add("chat-bubble");
    newelm.classList.add("you");
    var textnode = document.createTextNode(QuestionAndAnswerdata.answer);
    
    newelm.appendChild(textnode);
    chatsection.appendChild(newelm);  

    let isuserfuldiv = await isuserfulbuttons();

    let yesbuttonselection = document.querySelector("#useful-yes-button");
    yesbuttonselection.addEventListener("click" , function(){
        isuserfuldiv.remove();
    });
    let nobuttonselection = document.querySelector("#useful-no-button");
    nobuttonselection.addEventListener("click" , async function(){
        isuserfuldiv.remove();
        var newelm = document.createElement('div');
        // Loading animation ==
        let elmdata = `<div id="chat-loading-bubble" class="chat-bubble you">
            <span class="processing-text">Posting question in Q&A Forum</span> 
            <svg class="svg-chat-section" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="margin: auto;display: block;shape-rendering: auto;width: 43px;height: 20px;" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid">
                <circle cx="0" cy="44.1678" r="15" fill="#ffffff">
                    <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.6s"></animate>
                </circle> <circle cx="45" cy="43.0965" r="15" fill="#ffffff">
                <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.39999999999999997s"></animate>
                </circle> <circle cx="90" cy="52.0442" r="15" fill="#ffffff">
                    <animate attributeName="cy" calcMode="spline" keySplines="0 0.5 0.5 1;0.5 0 1 0.5;0.5 0.5 0.5 0.5" repeatCount="indefinite" values="57.5;42.5;57.5;57.5" keyTimes="0;0.3;0.6;1" dur="1s" begin="-0.19999999999999998s"></animate>
                </circle>
            </svg>
        </div>`;
        newelm.innerHTML = elmdata;
        chatsection.appendChild(newelm);
        
        console.log("Called posting question section");
        let QuestionPostedURL =  `/home/questions/questionpost/${courseID}/1`;
        let Questionposteddata = await fetch(QuestionPostedURL , { method : "POST",
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
        });
        let chatbubble = document.querySelector("#chat-loading-bubble");
        chatbubble.remove();
        let postquestionjson = await Questionposteddata.json();
        console.log(postquestionjson);
        var newelm = document.createElement('div');
        newelm.classList.add("chat-bubble");
        newelm.classList.add("you");
        var textnode = document.createTextNode("Thank you. Question is posted in Q&A forum");
        newelm.appendChild(textnode);
        chatsection.appendChild(newelm);
    });
}



function isuserfulbuttons(){
    var newelm = document.createElement('div');
    newelm.classList.add("chat-bubble");
    newelm.classList.add("you");
    let textnodedata = `
        <p style="color : white; font-weight : 600; margin-bottom : 5px">Is the answer is useful ? </p>
        <button id="useful-yes-button" type="button" class="btn btn-sm btn-success mr-1"> Yes </button>
        <button id="useful-no-button" type="button" class="btn btn-sm btn-danger"> No </button>
     `;
     newelm.innerHTML = textnodedata;
     chatsection.appendChild(newelm);
     return newelm;
}