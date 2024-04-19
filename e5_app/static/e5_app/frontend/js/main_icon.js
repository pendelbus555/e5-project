$(document).ready(function () {
  $(".navbar-brand").hover(
    function () {
      $("#custom_icon_2").removeClass("custom_icon_2_out").addClass("custom_icon_2_in");
      $("#custom_icon_1").removeClass("custom_icon_1_out").addClass("custom_icon_1_in");
    },
    function () {
      $("#custom_icon_2").removeClass("custom_icon_2_in").addClass("custom_icon_2_out");
      $("#custom_icon_1").removeClass("custom_icon_1_in").addClass("custom_icon_1_out");
    }
  );
});
