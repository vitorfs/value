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

    var url = "/workspace/" + $(this).attr("data-instance-id") + "/evaluate/save/";
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    var factor_id = $(this).attr("data-factor-id");
    var measure_id = $(this).attr("data-measure-id");
    var measure_value_id = $(this).attr("data-measure-value-id");

    $.ajax({
      url: url,
      data: {
        'csrfmiddlewaretoken': csrf,
        'factor_id': factor_id,
        'measure_id': measure_id,
        'measure_value_id': measure_value_id
      },
      type: 'post',
      success: function (data) {

      }
    });

  });

});
