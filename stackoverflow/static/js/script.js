function displayLikeBadge(id) {
    // console.log("displayLikeBadge");
    var badge = document.getElementById(id);
    var dislike = document.getElementById('dislike-'+id);
    badge.classList.remove('toggle-badge-text');
    badge.innerHTML = "Like";
    badge.classList.add('hover-animation');
    dislike.classList.remove('fill-color-dislike');
    dislike.classList.add('fill-color-like');
    badge.classList.remove('sr-only');
}

function removeLikeBadge(id) {
    // console.log("removeLikeBadge");
    var badge = document.getElementById(id);
    var dislike = document.getElementById('dislike-'+id);
    badge.classList.remove('hover-animation');
    dislike.classList.remove('fill-color-like');
    dislike.classList.add('fill-color-dislike');
    badge.classList.add('sr-only')
}

function displayDislikeBadge(id) {
    // console.log("displayDislikeBadge");
    var badge = document.getElementById(id);
    var like = document.getElementById('like-'+id);
    badge.classList.remove('toggle-badge-text');
    badge.innerHTML = "Dislike";
    badge.classList.add('hover-animation');
    like.classList.remove('fill-color-like');
    like.classList.add('fill-color-dislike');
    badge.classList.remove('sr-only');
}

function removeDislikeBadge(id) {
    // console.log("removeDislikeBadge");
    var badge = document.getElementById(id);
    var like = document.getElementById('like-'+id);
    like.classList.remove('fill-color-dislike');
    like.classList.add('fill-color-like');
    badge.classList.remove('hover-animation');
    badge.classList.add('sr-only')
}

$(function () {
    "use strict";

    $(".btn-toggle-like").click(function () {
        // console.log("Clicked");
        var children = $(this).children();
        // console.log(children);
        const id = children[1].id;
        var button = document.getElementById("btn-toggle-like-"+id);
        
        $.ajax({
            url: "/question/like/" + id + "/",
            method: "POST",
            success: function (json) {  
                // console.log(json);
                // var success = json["Success"];
                if(json["Success"] == 1) {
                    // console.log("Liked");
                    children[0].id = "like-" + id;
                    children[1].id = id;
                    // console.log(children);
                    // $("#"+id).removeClass("toggle-badge-text");
                    // $("#"+id).html("Like");
                    $("#like-"+id).removeClass("dislike");
                    $("#like-"+id).addClass("like");
                    $("#"+id).removeClass("badge-like");
                    $("#"+id).addClass("badge-dislike");
                    $("#"+id).addClass("toggle-badge-text");
                    $("#"+id).html("Liked");

                    let count = parseInt($("#like-count-"+id).html());
                    $("#like-count-"+id).html(count+1);

                    // console.log(button.onmouseover);
                    button.onmouseover = function() { displayDislikeBadge(id); }
                    button.onmouseleave = function() { removeDislikeBadge(id); }
                    // console.log(button.onmouseover);

                    $(this).removeClass("btn-dislike");
                    $(this).addClass("btn-like");
                    // console.log(button);
                }
                else if(json["Success"] == 2) {
                    // console.log("Disliked");
                    children[0].id = "dislike-" + id;
                    children[1].id = id;
                    // console.log(children);
                    // $("#"+id).removeClass("toggle-badge-text");
                    // $("#"+id).html("Dislike");
                    $("#dislike-"+id).removeClass("like");
                    $("#dislike-"+id).addClass("dislike");
                    $("#"+id).removeClass("badge-dislike");
                    $("#"+id).addClass("badge-like");
                    $("#"+id).addClass("toggle-badge-text");
                    $("#"+id).html("Disliked");

                    let count = parseInt($("#like-count-"+id).html());
                    $("#like-count-"+id).html(count-1);

                    // console.log(button.onmouseover);
                    button.onmouseover = function() { displayLikeBadge(id); }
                    button.onmouseleave = function() { removeLikeBadge(id); }
                    // console.log(button.onmouseover);

                    $(this).removeClass("btn-like");
                    $(this).addClass("btn-dislike");
                    // console.log(button);
                }
                else {
                    // console.log("Failed");
                }
            },
        });
    });



    // $(".btn-dislike").click(function () {
    //     // console.log("Clicked");
    //     var children = $(this).children();
    //     // console.log(children);
    //     const id = children[1].id;
    //     var button = document.getElementById("btn-"+id);
        
    //     $.ajax({
    //         url: "/question/like/" + id + "/",
    //         method: "POST",
    //         success: function (json) {                
    //             if(json["Success"] == 1) {
                    
    //             }
    //             else if(json["Success"] == 2) {
    //                 console.log("Failed");
    //             }
    //         },
    //     });
    // });
});