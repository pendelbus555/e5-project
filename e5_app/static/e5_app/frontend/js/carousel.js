$(window).on("load", function () {
  $("#carouselExampleCaptions, #carouselExampleCaptions1").each(function () {
    var $carousel = $(this);
    $carousel.find(".carousel-item img").css("max-height", $carousel.css("height"));
  });
});
