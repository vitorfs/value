$(function () {

  // Definition of a startsWith string function
  if (typeof String.prototype.startsWith != "function") {
    String.prototype.startsWith = function (str){
      return this.slice(0, str.length) == str;
    };
  }

  // Add class to the header menu based on the current URL
  var pathname = window.location.pathname;
  $("header a").each(function () {
    var href = $(this).attr("href");
    if (pathname.startsWith(href)) {
      $(this).closest("li").addClass("active");
    }
  });

  // Active bootstrap popover plugin
  $("[data-toggle='popover']").popover();

});