console.log("Hello from app.js");

$(document).ready(function(){
    $('.profileTitleBtn').on("click", function(){
        let title = $(this).attr('title');
        $('.profileTitle').replaceWith("<h1 class='profileTitle'>"+title+"</h1>");
    });
    $(".like").click( function(){
        $(this).toggleClass("heart");

    });
});


function sendtoServer2(path, method, entry, ids) 
{
    
    return fetch(`${window.origin}`+path, {
        method: method,
        credentials: "include",
        body: entry,
        cache: "no-cache"
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
      })
      .catch(function (error) {
          console.log("Fetch error: " + error);
      });
}

function getMessagesFromServer(entry){
    fetch(`${window.origin}/messages/getMessage`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
        }
        response.json().then(function (data) {
            console.log(data);
            // Clear chat
            document.getElementById('toUsername').innerHTML = $(".conversation.active").find(".title-text").text();
            $("#chat-message-list div").remove();

            // Load messages
            for (const [key, value] of Object.entries(data.messages)) {
                let temp = `<div class="message-row ${value.sender}">
                                <div class="message-content">
                                    <img src="${value.img }"/>
                                    <div class="message-text">${value.message }</div>
                                    <div class="message-time"> ${value.date}</div>
                                </div>  
                            </div>`;
                ($("#chat-message-list").append(temp));
            }

        });
    })
    .catch(function (error) {
        console.log("Fetch error: " + error);
    });
}


function sendtoServer(path, method, entry, ids) 
{
    
    fetch(`${window.origin}`+path, {
        method: method,
        credentials: "include",
        body: entry,
        cache: "no-cache"
    })
    .then(function (response) {
        if (response.status !== 200) {
            console.log(`Looks like there was a problem. Status code: ${response.status}`);
            return;
        }
        response.json().then(function (data) {
            console.log(data);

            if(data.error){
                alert(data.error);
                return;
            }else{
                let id;                
                for(id of ids){
                    $(id).fadeOut(1000).html(data.value).fadeIn(1000);
                }  
            } 
        });
  
    })
      .catch(function (error) {
          console.log("Fetch error: " + error);
      });
}


