$(function () {

  if (typeof String.prototype.startsWith != "function") {
    String.prototype.startsWith = function (str){
      return this.slice(0, str.length) == str;
    };
  }

  var pathname = window.location.pathname;
  
  $("header a").each(function () {
    var href = $(this).attr("href");
    if (pathname.startsWith(href)) {
      $(this).closest("li").addClass("active");
    }
  });

});