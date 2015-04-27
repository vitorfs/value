$(function () {

  $(".evaluable").click(function () {
    var row = $(this).closest("tr");
    $(row).addClass("selected");
    $(".evaluable", row).each(function () {
      $(this).css("background-color", "transparent");
      $(".glyphicon", this).removeClass("glyphicon-check").addClass("glyphicon-unchecked");
    });

    var color = $(this).attr("data-color");
    $(this).css("background-color", color);
    $(".glyphicon", this).removeClass("glyphicon-unchecked").addClass("glyphicon-check");

    var rows_count = $(this).closest("tbody").find("tr").length;
    var selected_rows_count = $(this).closest("tbody").find("tr.selected").length;

    var percent = (selected_rows_count / rows_count) * 100;

    percent = Math.round(percent, 1);

    var panel = $(this).closest(".panel");

    if (percent === 100) {
      $(panel).removeClass("panel-default").addClass("panel-success");
    }

    $(".badge", panel).text(percent + "%");
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
