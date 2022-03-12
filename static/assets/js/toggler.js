$(document).ready(function () {
  $("#signup-box").hide();
});

$("#goto-signup").on("click", () => {
  $("#login-box").hide();
  $("#signup-box").show();
});

$("#goto-signin").on("click", () => {
  $("#login-box").show();
  $("#signup-box").hide();
});
