$(function () {

  $(".evaluable").click(function () {

    var row = $(this).closest("tr");
    $(".evaluable", row).each(function () {
      $(this).css("background-color", "transparent");
      $(".glyphicon", this).removeClass("glyphicon-check").addClass("glyphicon-unchecked");
    });

    var color = $(this).attr("data-color");
    $(this).css("background-color", color);
    $(".glyphicon", this).removeClass("glyphicon-unchecked").addClass("glyphicon-check");
  });

});
