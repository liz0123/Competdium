
$(document).ready(function(){
    $('#uploadProfileImage').submit(function(event){
        event.preventDefault();
        let path = "/myprofile/setting/updateProfileImg";
        let formData = new FormData(document.querySelector('#uploadProfileImage'));
        
        sendForm(path, formData)
        .then(data=>{
            $('#profileAvatar').attr('src', '../static/img/profiles/'+data.img+"?"+new Date().getTime());
            console.log(data.update);
        })
        .catch(error=>{
            console.log(error); 
        });
    
    });
    $('#uploadProfileBio').submit(function(event){
        event.preventDefault();
        let path = "/myprofile/setting/updateBio";
        let formData = new FormData(document.querySelector('#uploadProfileBio'));
  
        sendForm(path, formData)
        .then(data=>{
          console.log(data.update);
          $("#profileSettingsCurrBio").html(data.value);
          $("#profileBio").html(data.value); 
          $('#profileSettingsNewBio').val('');      
  
        })
        .catch(error=>{
          console.log(error); 
        });
  
      });

    //
    $('.search_select select').selectpicker();
    $('.selectpicker').selectpicker();
    // Pusher for comments
	var pusher = new Pusher('c7fa9a824f00223cea96', {
        cluster: 'us2'
    });
	var channel = pusher.subscribe('comment-channel');

	channel.bind("new-comment", function(data){
		comment_template = `<div class="comment">
								<img id ="comment_img" src='../static/img/profiles/${data.img}?${new Date().getTime()}' class="rounded-circle" style="height: 40px;" alt="..."></img>
								<div id="comment_username">${data.username}</div>
								<div id="comment_date">${data.date}</div>
								<div id="comment_content">${data.comment}</div>
								<a href="#">Reply</a>
							</div>`;
		($('#comment-list'+data.post_id).prepend(comment_template));
	});
    //
    $('#image').on("change", function(event){
        $("#display").removeAttr("src").attr("src",URL.createObjectURL(event.target.files[0]) );
        $("#display").show();
        $(".btn-remove").show();
    });
    $('.pill').on("click", function(){
        let title = $(this).attr('title');
        $('.profileTitle').replaceWith("<h1 class='profileTitle'>"+title+"</h1>");
    }); 
});

function save(item){
    event.preventDefault();
    let type = $(item).attr("saveType");
    let id  = $(item).attr('item_id');
    let path = "";
    $(item).toggleClass('active');
    if(type =='like'){
        path = "/feed/likePost/";
        $("i",item).toggleClass("bi-hand-thumbs-up-fill  bi-hand-thumbs-up ");
    }
    else if(type =='save'){
        path = "/feed/savePost";
        $("i",item).toggleClass("bi-bookmark-fill bi-bookmark");
        //$(item).children('span').toggle('Saved')
    }
    else if(type == 'heart'){
        path = "/searchPets/likedPet";
    }

    sendData(path, {'id':id})
        .then(result => {
            if(result.likes >= 0){
                $(item).children("span").text(result.likes);
            }
            console.log('Success:', result);
        })
        .catch(error => {
            console.log('Error:', error);
        });
}

function sendForm(path, data){
    return fetch(`${window.origin}`+path, {
        method: "POST",
        credentials: "include",
        body: data,
        cache: "no-cache"
    }).then(response => response.json())
}

function sendData(path, entry){
    return fetch(`${window.origin}`+path, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
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


