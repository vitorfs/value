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

  $(".js-factors-selection a").click(function () {

    if ($(this).attr("data-selected") === "unselected") {
      $(this).attr("data-selected", "selected");
      $(this).css("font-weight", "bold");
      $(".glyphicon", this).removeClass("glyphicon-unchecked").addClass("glyphicon-check");
    }
    else {
      $(this).attr("data-selected", "unselected");
      $(this).css("font-weight", "normal");
      $(".glyphicon", this).removeClass("glyphicon-check").addClass("glyphicon-unchecked");
    }

    $(this).blur();

    return false;

  });

});
