$(function () {

  $(".js-factor-description").popover();
  
  var factorsCount = $(".panel-group-evaluation .panel:eq(0) .table-evaluate tbody tr").length;
  $(".panel-group-evaluation .panel .table-evaluate tbody").each(function () {
    if ($("tr.selected", this).length === factorsCount) {
      $(this).closest(".panel").attr("class", "panel panel-success");
    }
  });

  $(".panel-group-evaluation").on("click", ".js-save-rationale", function () {
    var container = $(this).closest(".popover");
    var btn = $(this);

    var url = $("#save-rationale-url").val();
    var csrf = $("[name='csrfmiddlewaretoken']").val();
    var meeting_item_id = $(this).closest("table").attr("data-meeting-item-id");
    var factor_id = $(this).closest("tr").attr("data-factor-id");
    var measure_id = $(this).closest("tr").attr("data-measure-id");
    var rationale = $(".evaluation-rationale", container).val();

    rationale = rationale.trim();

    $.ajax({
      url: url,
      type: 'post',
      cache: false,
      data: {
        'csrfmiddlewaretoken': csrf,
        'meeting_item_id': meeting_item_id,
        'factor_id': factor_id,
        'measure_id': measure_id,
        'text': rationale
      },
      beforeSend: function (jqXHR, settings) {
        $(btn).prop("disabled", true);
        $(btn).text("Saving…");
      },
      success: function (data, textStatus, jqXHR) {
        toastr.success("Rationale saved successfully!");
        $(container).siblings(".js-rationale").attr("data-rationale", rationale);
        if (rationale.length > 0) {
          $(container).siblings(".js-rationale").removeClass("no-comment");
        }
        else {
          $(container).siblings(".js-rationale").addClass("no-comment"); 
        }
        $(container).popover("hide");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        toastr.error(jqXHR.responseText);
      },
      complete: function (jqXHR, textStatus) {
        $(btn).prop("disabled", false);
        $(btn).text("Save");
      }
    });

  });

  $(".js-rationale").popover({
    html: true,
    content: function () {
      var rationale = $(this).attr("data-rationale");
      var id = uuid();
      var template = $('#rationale-template').html();
      var rendered = Mustache.render(template, { 
        'rationale': rationale,
        'id': id
      });
      return rendered;
    }
  });

  $(".js-rationale").on("shown.bs.popover", function () {
    var popover = $(this).siblings(".popover");
    if ($("textarea", popover).text().length === 0 && !$("textarea", popover).prop("readonly")) {
      $("textarea", popover).focus();
    }
  });

  $(".btn-toggle").click(function () {
    var container = $(this).closest(".panel-heading");
    var target = $(container).attr("data-target");
    if ($(target).is(":visible")) {
      $(target).slideUp();
    }
    else {
      $(target).slideDown(400, function () {
        if (!$(container).hasClass("loaded")) {
          // :TODO async load
        }
      });
    }
  });

  $(".js-grid-filters a").click(function () {

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
    $(".panel-group-evaluation .panel").each(function () {
      var container = $(".panel-heading", this);
      var target = $(container).attr("data-target");
      if (!$(target).is(":visible")) {
        $(target).slideDown();
      }
    });    
  });

  $(".js-hide-all").click(function () {
    $(".panel-group-evaluation .panel").each(function () {
      var container = $(".panel-heading", this);
      var target = $(container).attr("data-target");
      if ($(target).is(":visible")) {
        $(target).slideUp();
      }
    });
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
    $(".measure-percent", panel).closest(".progress-bar").css("width", "0%");
    for (var key in measure_value_percent) {
      var percent = (measure_value_percent[key] / rows_count) * 100;
      var display_percent = percent.toFixed(2);
      $(".measure-percent[data-measure-id='" + key + "']", panel).text(display_percent);
      $(".measure-percent[data-measure-id='" + key + "']", panel).closest(".progress-bar").css("width", percent + "%");
    }

    var url = $(this).closest("form").attr("action");
    var csrf = getCSRF();

    var meeting_item_id = $(this).closest("table").attr("data-meeting-item-id");

    var factor_id = $(this).closest("tr").attr("data-factor-id");
    var measure_id = $(this).closest("tr").attr("data-measure-id");
    
    var measure_value_id = do_evaluate ? $(this).attr("data-measure-value-id") : "";

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
        if (data.meeting_closed) {
          location.reload();
        }
        else {
          $("#meeting-progress").replaceWith(data.html);
        }
      }
    });

  });

});
