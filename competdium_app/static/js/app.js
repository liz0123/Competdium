console.log("Hello from app.js");

$(document).ready(function(){
    $('.updateProfile').on("click", function(){

        let member_id = $(this).attr('member_id');

        let email = $('#profileEmailInput'+member_id).val()
        let bio = $('#profileBioInput'+member_id).val()

        req = $.ajac({
            url: "/myprofile",
            type:"POST",
            data:{email:email, bio:bio, id:member_id}
        });

        

    });

});
