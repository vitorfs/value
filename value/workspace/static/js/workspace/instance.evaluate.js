$(function () {

  $(".js-grid-filters a").click(function () {

    $(".panel-group .panel-collapsable").togglePanel(false);

    $(".js-grid-filters .glyphicon").removeClass("glyphicon-check").addClass("glyphicon-unchecked");

    var action = $(this).attr("data-action");

    if (action === "all") {
      $(".panel-group .panel").show();
    }

    else if (action === "todo") {
      $(".panel-group .panel").hide();
      $(".panel-group .panel-default").show();
    }

    else if (action === "finished") {
      $(".panel-group .panel").hide();
      $(".panel-group .panel-success").show();
    }

    $(".glyphicon", this).removeClass("glyphicon-unchecked").addClass("glyphicon-check");

  });

  $(".js-show-all").click(function () {
    $(".panel-group .panel-collapsable").togglePanel(true);
  });

  $(".js-hide-all").click(function () {
    $(".panel-group .panel-collapsable").togglePanel(false);
  });

  var content_type = "table";

  if ($(".panel-group .panel-body").length > 0) {
    content_type = ".panel-body";
  }
  

  $.fn.togglePanel = function (is_collapsed) {

    if (is_collapsed === undefined) {
      is_collapsed = $(this).hasClass("panel-collapsed");
    }

    var container = $(content_type, this);

    if (is_collapsed) {
      $(container).show();
      $(this).removeClass("panel-collapsed");
    }
    else {
      $(container).hide();
      $(this).addClass("panel-collapsed");
    }
  };

  $(".panel-collapsable .panel-heading").click(function () {
    $(this).closest(".panel-collapsable").togglePanel();
  });

  $(".evaluable").click(function () {

    var do_evaluate = true

    if ($(".glyphicon", this).hasClass("glyphicon-check")) {
      do_evaluate = false;
    }

    var row = $(this).closest("tr");
    $(row).removeClass("selected");
    $(".evaluable", row).each(function () {
      $(this).css("background-color", "transparent");
      $(".glyphicon", this).removeClass("glyphicon-check").addClass("glyphicon-unchecked");
    });

    if (do_evaluate) {
      $(row).addClass("selected");
      var color = $(this).attr("data-color");
      $(this).css("background-color", color);
      $(".glyphicon", this).removeClass("glyphicon-unchecked").addClass("glyphicon-check");
    }

    var rows_count = $(this).closest(".panel").find("tbody > tr").length;
    var selected_rows_count = $(this).closest(".panel").find("tbody > tr.selected").length;

    var percent = (selected_rows_count / rows_count) * 100;

    percent = Math.round(percent, 1);

    var panel = $(this).closest(".panel");

    if (percent === 100) {
      $(panel).removeClass("panel-default").addClass("panel-success");
    }
    else {
      $(panel).removeClass("panel-success").addClass("panel-default");
    }

    $(".badge", panel).text(percent + "%");

    var url = "/workspace/" + $(this).attr("data-instance-id") + "/evaluate/save/";
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    var item_id = $(this).attr("data-item-id");
    var factor_id = $(this).attr("data-factor-id");
    var measure_id = $(this).attr("data-measure-id");
    var measure_value_id = $(this).attr("data-measure-value-id");

    $.ajax({
      url: url,
      data: {
        'csrfmiddlewaretoken': csrf,
        'item_id': item_id,
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
