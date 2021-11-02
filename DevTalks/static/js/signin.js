$(function () {
    "use strict";    

    $(".form-control").on("input", function () {
        var $field = $(this).closest(".form-group");
        if (this.value) {
            $field.addClass("field--not-empty");
        } else {
            $field.removeClass("field--not-empty");
        }
    });

    $("#username").change(function (e) {
        e.preventDefault();
        let value = $("#username").val().trim();
        $.ajax({
            url: "/user/check_username/" + value + "/",
            method: "POST",
            success: function (json) {
                var regEx = /^[0-9a-zA-Z]+$/;
                if(json["exists"]) {
                    $("#errorUsername").html("Username already taken");
                }
                else if(value.length > 20) {
                    $("#errorUsername").html("Username must be under 20 charcters!!");
                }
                else if(!value.match(regEx)) {
                    $("#errorUsername").html("Username must be Alpha-Numeric!!");
                }
                else {
                    $("#errorUsername").html("");
                }
            },
        });
    });

    $("#email").change(function (e) {
        e.preventDefault();
        let value = $("#email").val().trim();
        $.ajax({
            url: "/user/check_email/" + value + "/",
            method: "POST",
            success: function (json) {
                if(json["exists"]) {
                    $("#errorEmail").html("Email already taken");
                }
                else {
                    $("#errorEmail").html("");
                }
                    
            },
        });
    });

    $("#retypepassword").change(function (e) {
        e.preventDefault();
        let password = $("#password").val().trim();
        let retypepassword = $("#retypepassword").val().trim();
        //console.log(password)
        //console.log(retypepassword)
        if(password != retypepassword)  {
            $("#errorPassword").html("Password not match");
        }
        else {
            $("#errorPassword").html("");
        }
            
    });
});