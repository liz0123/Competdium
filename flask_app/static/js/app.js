console.log("Hello from app.js");

$(document).ready(function(){
    $('.profileTitleBtn').on("click", function(){
        let title = $(this).attr('title');
        $('.profileTitle').replaceWith("<h1 class='profileTitle'>"+title+"</h1>");
    });
    $('.like').on('click', function() {
        // add active class to clicked element
        if( $(this).hasClass("active") ){
            $(this).removeClass("active");
            // remove pet from db
            $.post("/searchPets/removeLikedPet",{ "pet_id":$(this).attr("pet_id") });
        }
        else{
            $(this).addClass("active");
            // add like pet in db
            $.post("/searchPets/likedPet",{ "pet_id":$(this).attr("pet_id") });
        }
    });
});
function sendForm(path, data){
    return fetch(`${window.origin}`+path, {
        method: "POST",
        credentials: "include",
        body: data,
        cache: "no-cache"
    })
    .then(response => response.json())
}
function sendData(path, entry){
    return fetch(`${window.origin}`+path, {
        method: "POST",
        credentials: "include",
        headers: { 'Content-Type': 'application/json', },
        body: JSON.stringify(entry),
        cache: "no-cache"
    }).then(response => response.json())
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
                alert(data.update);
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


