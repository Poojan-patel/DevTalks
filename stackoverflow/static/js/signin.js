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
      url: "/users/check_username/" + value + "/",
      method: "POST",
      success: function (json) {
        console.log(json["exists"]);
      },
    });
  });

  $("#email").change(function (e) {
    e.preventDefault();
    let value = $("#email").val().trim();
    $.ajax({
      url: "/users/check_email/" + value + "/",
      method: "POST",
      success: function (json) {
        console.log(json["exists"]);
      },
    });
  });
});
