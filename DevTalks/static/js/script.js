function displayLikeBadge(id) {
    // console.log("displayLikeBadge");
    var badge = document.getElementById('badge-que-'+id);
    var dislike = document.getElementById('dislike-'+id);
    badge.classList.remove('bg-danger');
    badge.classList.remove('toggle-badge-text');
    badge.innerHTML = "Like";
    badge.classList.add('hover-animation');
    dislike.classList.remove('fill-color-dislike');
    dislike.classList.add('fill-color-like');
    badge.classList.remove('sr-only');
}

function removeLikeBadge(id) {
    // console.log("removeLikeBadge");
    var badge = document.getElementById('badge-que-'+id);
    var dislike = document.getElementById('dislike-'+id);
    badge.classList.remove('hover-animation');
    dislike.classList.remove('fill-color-like');
    dislike.classList.add('fill-color-dislike');
    badge.classList.add('sr-only')
}

function displayDislikeBadge(id) {
    // console.log("displayDislikeBadge");
    var badge = document.getElementById('badge-que-'+id);
    var like = document.getElementById('like-'+id);
    badge.classList.remove('bg-danger');
    badge.classList.remove('toggle-badge-text');
    badge.innerHTML = "Dislike";
    badge.classList.add('hover-animation');
    like.classList.remove('fill-color-like');
    like.classList.add('fill-color-dislike');
    badge.classList.remove('sr-only');
}

function removeDislikeBadge(id) {
    // console.log("removeDislikeBadge");
    var badge = document.getElementById('badge-que-'+id);
    var like = document.getElementById('like-'+id);
    like.classList.remove('fill-color-dislike');
    like.classList.add('fill-color-like');
    badge.classList.remove('hover-animation');
    badge.classList.add('sr-only')
}

function displayUpvoteBadge(id) {
    // console.log(id);
    var badge = document.getElementById('badge-ans-'+id);
    var noUpvote = document.getElementById('no-upvote-'+id);
    badge.classList.remove('bg-danger');
    badge.classList.remove('toggle-badge-text');
    badge.innerHTML = "Upvote";
    badge.classList.add('hover-animation');
    noUpvote.classList.remove('fill-color-no-upvote');
    noUpvote.classList.add('fill-color-upvote');
    badge.classList.remove('sr-only');
}

function removeUpvoteBadge(id) {
    // console.log(id);
    var badge = document.getElementById('badge-ans-'+id);
    var noUpvote = document.getElementById('no-upvote-'+id);
    badge.classList.remove('hover-animation');
    noUpvote.classList.remove('fill-color-upvote');
    noUpvote.classList.add('fill-color-no-upvote');
    badge.classList.add('sr-only')
}

function displayNoUpvoteBadge(id) {
    // console.log(id);
    var badge = document.getElementById('badge-ans-'+id);
    var upvote = document.getElementById('upvote-'+id);
    badge.classList.remove('bg-danger');
    badge.classList.remove('toggle-badge-text');
    badge.innerHTML = "Downvote";
    badge.classList.add('hover-animation');
    upvote.classList.remove('fill-color-upvote');
    upvote.classList.add('fill-color-no-upvote');
    badge.classList.remove('sr-only');
}

function removeNoUpvoteBadge(id) {
    // console.log(id);
    var badge = document.getElementById('badge-ans-'+id);
    var upvote = document.getElementById('upvote-'+id);
    badge.classList.remove('hover-animation');
    upvote.classList.remove('fill-color-no-upvote');
    upvote.classList.add('fill-color-upvote');
    badge.classList.add('sr-only')
}

function displayVerifyBadge(id) {
    // console.log(id);
    var badge = document.getElementById('badge-verify-'+id);
    var noUpvote = document.getElementById('no-verify-'+id);
    badge.classList.remove('bg-danger');
    badge.classList.remove('toggle-badge-text');
    badge.innerHTML = "Verify";
    badge.classList.add('hover-animation');
    noUpvote.classList.remove('bi-patch-check');
    noUpvote.classList.add('bi-patch-check-fill');
    badge.classList.remove('sr-only');
}

function removeVerifyBadge(id) {
    // console.log(id);
    var badge = document.getElementById('badge-verify-'+id);
    var noUpvote = document.getElementById('no-verify-'+id);
    badge.classList.remove('hover-animation');
    noUpvote.classList.remove('bi-patch-check-fill');
    noUpvote.classList.add('bi-patch-check');
    badge.classList.add('sr-only')
}

function displayNoVerifyBadge(id) {
    // console.log(id);
    var badge = document.getElementById('badge-verify-'+id);
    var upvote = document.getElementById('verify-'+id);
    badge.classList.remove('bg-danger');
    badge.classList.remove('toggle-badge-text');
    badge.innerHTML = "Cancel";
    badge.classList.add('hover-animation');
    upvote.classList.remove('bi-patch-check-fill');
    upvote.classList.add('bi-patch-check');
    badge.classList.remove('sr-only');
}

function removeNoVerifyBadge(id) {
    // console.log(id);
    var badge = document.getElementById('badge-verify-'+id);
    var upvote = document.getElementById('verify-'+id);
    badge.classList.remove('hover-animation');
    upvote.classList.remove('bi-patch-check');
    upvote.classList.add('bi-patch-check-fill');
    badge.classList.add('sr-only')
}



$(function () {
    "use strict";

    $(".btn-toggle-like").click(function () {
        // console.log("Clicked");
        var children = $(this).children();
        // console.log(children);
        const id = children[1].id.split("badge-que-")[1];
        var button = document.getElementById("btn-toggle-like-"+id);
        
        $.ajax({
            url: "/question/like/" + id + "/",
            method: "POST",
            success: function (json) {  
                console.log(json);
                // var success = json["Success"];
                if(json["Success"] == 1) {
                    // console.log("Liked");
                    children[0].id = "like-" + id;
                    children[1].id = "badge-que-" + id;
                    // console.log(children);
                    // $("#"+id).removeClass("toggle-badge-text");
                    // $("#"+id).html("Like");
                    $("#like-"+id).removeClass("dislike");
                    $("#like-"+id).addClass("like");
                    $("#badge-que-"+id).removeClass("badge-like");
                    $("#badge-que-"+id).addClass("badge-dislike");
                    $("#badge-que-"+id).addClass("toggle-badge-text");
                    $("#badge-que-"+id).html("Liked");

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
                    children[1].id = "badge-que-" + id;
                    // console.log(children);
                    // $("#"+id).removeClass("toggle-badge-text");
                    // $("#"+id).html("Dislike");
                    $("#dislike-"+id).removeClass("like");
                    $("#dislike-"+id).addClass("dislike");
                    $("#badge-que-"+id).removeClass("badge-dislike");
                    $("#badge-que-"+id).addClass("badge-like");
                    $("#badge-que-"+id).addClass("toggle-badge-text");
                    $("#badge-que-"+id).html("Disliked");

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
                    $("#badge-que-"+id).addClass("bg-danger");
                    $("#badge-que-"+id).html("Error");
                }
            },
        });
    });



    $(".btn-toggle-upvote").click(function () {
        // console.log("Clicked");
        var children = $(this).children();
        // console.log(children);
        const id = children[1].id.split("badge-ans-")[1];
        var button = document.getElementById("btn-toggle-upvote-"+id);
        
        $.ajax({
            url: "/question/answer/upvote/" + id + "/",
            method: "POST",
            success: function (json) {  
                console.log(json);
                // var success = json["Success"];
                if(json["Success"] == 1) {
                    // console.log("Liked");
                    children[0].id = "upvote-" + id;
                    children[1].id = "badge-ans-"+id;
                    // console.log(children);
                    // $("#"+id).removeClass("toggle-badge-text");
                    // $("#"+id).html("Upvote");
                    $("#upvote-"+id).removeClass("no-upvote");
                    $("#upvote-"+id).addClass("upvote");
                    $("#badge-ans-"+id).removeClass("badge-upvote");
                    $("#badge-ans-"+id).addClass("badge-no-upvote");
                    $("#badge-ans-"+id).addClass("toggle-badge-text");
                    $("#badge-ans-"+id).html("Upvoted");

                    let count = parseInt($("#upvote-count-"+id).html());
                    $("#upvote-count-"+id).html(count+1);

                    // console.log(button.onmouseover);
                    button.onmouseover = function() { displayNoUpvoteBadge(id); }
                    button.onmouseleave = function() { removeNoUpvoteBadge(id); }
                    // console.log(button.onmouseover);

                    $(this).removeClass("btn-no-upvote");
                    $(this).addClass("btn-upvote");
                    // console.log(button);
                }
                else if(json["Success"] == 2) {
                    // console.log("Disliked");
                    children[0].id = "no-upvote-" + id;
                    children[1].id = "badge-ans-" + id;
                    // console.log(children);
                    // $("#"+id).removeClass("toggle-badge-text");
                    // $("#"+id).html("Dislike");
                    $("#no-upvote-"+id).removeClass("upvote");
                    $("#no-upvote-"+id).addClass("no-upvote");
                    $("#badge-ans-"+id).removeClass("badge-no-upvote");
                    $("#badge-ans-"+id).addClass("badge-upvote");
                    $("#badge-ans-"+id).addClass("toggle-badge-text");
                    $("#badge-ans-"+id).html("Downvoted");

                    let count = parseInt($("#upvote-count-"+id).html());
                    $("#upvote-count-"+id).html(count-1);

                    // console.log(button.onmouseover);
                    button.onmouseover = function() { displayUpvoteBadge(id); }
                    button.onmouseleave = function() { removeUpvoteBadge(id); }
                    // console.log(button.onmouseover);

                    $(this).removeClass("btn-upvote");
                    $(this).addClass("btn-no-upvote");
                    // console.log(button);
                }
                else {
                    // console.log("Failed");
                    $("#badge-ans-"+id).addClass("bg-danger");
                    $("#badge-ans-"+id).html("Error");
                }
            },
        });
    });



    $(".btn-toggle-verify").click(function () {
        // console.log("Clicked");
        var children = $(this).children();
        // console.log(children);
        const id = children[1].id.split("badge-verify-")[1];
        var button = document.getElementById("btn-toggle-verify-"+id);
        
        $.ajax({
            url: "/question/answer/verify/" + id + "/",
            method: "POST",
            success: function (json) {  
                console.log(json);
                // var success = json["Success"];
                if(json["Success"] == 1) {
                    // console.log("Liked");
                    children[0].id = "verify-" + id;
                    children[1].id = "badge-verify-"+id;
                    // console.log(children);
                    // $("#"+id).removeClass("toggle-badge-text");
                    // $("#"+id).html("Upvote");
                    $("#verify-"+id).removeClass("no-verify");
                    $("#verify-"+id).addClass("verify");
                    $("#badge-verify-"+id).removeClass("badge-verify");
                    $("#badge-verify-"+id).addClass("badge-no-verify");
                    $("#badge-verify-"+id).addClass("toggle-badge-text");
                    $("#badge-verify-"+id).html("Verified");

                    // let count = parseInt($("#upvote-count-"+id).html());
                    // $("#upvote-count-"+id).html(count+1);

                    // console.log(button.onmouseover);
                    button.onmouseover = function() { displayNoVerifyBadge(id); }
                    button.onmouseleave = function() { removeNoVerifyBadge(id); }
                    // console.log(button.onmouseover);

                    $(this).removeClass("btn-no-verify");
                    $(this).addClass("btn-verify");
                    // console.log(button);
                }
                else if(json["Success"] == 2) {
                    // console.log("Disliked");
                    children[0].id = "no-verify-" + id;
                    children[1].id = "badge-verify-" + id;
                    // console.log(children);
                    // $("#"+id).removeClass("toggle-badge-text");
                    // $("#"+id).html("Dislike");
                    $("#no-verify-"+id).removeClass("verify");
                    $("#no-verify-"+id).addClass("no-verify");
                    $("#badge-verify-"+id).removeClass("badge-no-verify");
                    $("#badge-verify-"+id).addClass("badge-verify");
                    $("#badge-verify-"+id).addClass("toggle-badge-text");
                    $("#badge-verify-"+id).html("Cancelled");

                    // let count = parseInt($("#upvote-count-"+id).html());
                    // $("#upvote-count-"+id).html(count-1);

                    // console.log(button.onmouseover);
                    button.onmouseover = function() { displayVerifyBadge(id); }
                    button.onmouseleave = function() { removeVerifyBadge(id); }
                    // console.log(button.onmouseover);

                    $(this).removeClass("btn-verify");
                    $(this).addClass("btn-no-verify");
                    // console.log(button);
                }
                else {
                    // console.log("Failed");
                    $("#badge-verify-"+id).addClass("bg-danger");
                    $("#badge-verify-"+id).html("Error");
                }
            },
        });
    });

});