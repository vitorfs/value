var loading = function () {
  if ($("body").hasClass("no-scroll")) {
    $("body").removeClass("no-scroll");
  }
  else {
    $("body").addClass("no-scroll");
  }
  $(".loading").toggle();
};

$(function () {

  // Active bootstrap popover plugin
  $("[data-toggle='popover']").popover();

});
