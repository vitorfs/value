$(function () {

  $(".btn-toggle").click(function () {
    var container = $(this).closest(".panel-heading");
    var target = $(container).attr("data-target");
    if ($(target).is(":visible")) {
      $(target).slideUp();
    }
    else {
      $(target).slideDown(400, function () {
        if (!$(container).hasClass("loaded")) {
          // async load
        }
      });
    }
  });

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
    
  });

  $(".js-hide-all").click(function () {
    
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

    var panel = $(this).closest(".panel");

    var rows_count = $(panel).find(".table tbody > tr").length;
    var selected_rows_count = $(this).closest(".panel").find(".table tbody > tr.selected").length;
    var percent = (selected_rows_count / rows_count) * 100;
    percent = Math.round(percent, 1);
    var panel = $(this).closest(".panel");
    if (percent === 100) {
      $(panel).removeClass("panel-default").addClass("panel-success");
    }
    else {
      $(panel).removeClass("panel-success").addClass("panel-default");
    }

    var measure_value_percent = {};
    $(".table tbody tr.selected", panel).each(function () {
      var measure_value_id = $(".glyphicon-check", this).closest("td").attr("data-measure-value-id");
      if (measure_value_percent[measure_value_id] === undefined) {
        measure_value_percent[measure_value_id] = 0;
      }
      measure_value_percent[measure_value_id] += 1;
    });
    $(".measure-percent", panel).text("0");
    for (var key in measure_value_percent) {
      var percent = (measure_value_percent[key] / rows_count) * 100;
      percent = Math.round(percent, 1);
      $(".measure-percent[data-measure-id='" + key + "']", panel).text(percent);
    }

    var url = "/deliverables/" + $(this).attr("data-deliverable-id") + "/meetings/" + $(this).attr("data-meeting-id") + "/evaluate/save/";
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    var meeting_item_id = $(this).attr("data-meeting-item-id");
    var factor_id = $(this).attr("data-factor-id");
    var measure_id = $(this).attr("data-measure-id");
    var measure_value_id = $(this).attr("data-measure-value-id");

    $.ajax({
      url: url,
      data: {
        'csrfmiddlewaretoken': csrf,
        'meeting_item_id': meeting_item_id,
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
