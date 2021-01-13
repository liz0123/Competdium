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
            }else if(data.img){


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


