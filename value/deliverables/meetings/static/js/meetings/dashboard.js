$.fn.loadchart = function (callback) {

  callback = callback || function () {};

  var form = $(this).closest("form");
  
  var container = $(this);
  var chart_container = $(this).closest(".panel").find(".panel-body");

  var display_loading = ! $(container).hasClass("loaded");
  display_loading = true;

  $.ajax({
    url: $(form).attr("action"),
    data: $(form).serialize(),
    type: 'GET',
    dataType: 'json',
    cache: false,
    beforeSend: function () {
      if (display_loading) {
        $(chart_container).loading();
      }
    },
    success: function (data) {
      data["exporting"] = { enabled: false };
      $(chart_container).highcharts(data);
      $(container).addClass("loaded");
    },
    complete: function () {
      if (display_loading) {
        $(chart_container).loading();
      }
      callback();
    }
  });
};

$.fn.loadpopupchart = function (options, removeExtra) {
  removeExtra = removeExtra || function () {};

  $(".chart-options .btn-chart-info").remove();
  $(".chart-options .btn-chart-rationale").remove();
  $(".chart-options .btn-chart-toggle").remove();
  $(".chart-options .btn-chart-expand").remove();
  $(".chart-options .btn-chart-modal").remove();
  
  removeExtra();

  // Remove "a" element from panel title to avoid hover effect
  // and chart toggle action, preserving the text only. 
  $(".panel-title").text($(".panel-title").text());

  $(this).highcharts(options);
};

$.fn.selectAllStakeholders = function () {
  var container = $(this).closest(".js-stakeholders");
  var group_name = $(this).closest("li").attr("data-target-group-name");
  $("[data-group-name='" + group_name + "']", container).each(function () {
    var stakeholder = $(this);
    if (!$("[name='stakeholder']", this).is(":checked")) {
      $(stakeholder).click();
    }
  });
};

$.fn.selectNoneStakeholders = function () {
  var container = $(this).closest(".js-stakeholders");
  var group_name = $(this).closest("li").attr("data-target-group-name");
  $("[data-group-name='" + group_name + "']", container).each(function () {
    var stakeholder = $(this);
    if ($("[name='stakeholder']", this).is(":checked")) {
      $(stakeholder).click();
    }
  });
};

$(function () {

  $(document).on("click", ".js-select-all-stakeholders", function (e) {
    e.preventDefault();
    var icon = $(".glyphicon", this);
    var unselectAllStakeholders = $(icon).hasClass("glyphicon-check");
    if (unselectAllStakeholders) {
      $(this).selectNoneStakeholders();
      $(icon).removeClass().addClass("glyphicon glyphicon-unchecked");
    }
    else {
      $(this).selectAllStakeholders();
      $(icon).removeClass().addClass("glyphicon glyphicon-check");
    }
    return false;
  });

  $(document).on("click", ".js-select-stakeholder", function (e) {
    e.preventDefault();
    var checkbox = $("input[type='checkbox'][name='stakeholder']", this);
    var icon = $(".glyphicon", this);
    $(icon).removeClass();
    var stakeholderIsSelected = $(checkbox).is(":checked");
    if (stakeholderIsSelected) {
      $(checkbox).prop("checked", false);
      $(icon).addClass("glyphicon glyphicon-unchecked");
    }
    else {
      $(checkbox).prop("checked", true);
      $(icon).addClass("glyphicon glyphicon-check");
    }

    var groupName = $(this).attr("data-group-name");
    var allStakeholdersInGroupAreChecked = true;
    $(".js-stakeholders a[data-group-name='" + groupName + "']").each(function () {
      var checkbox = $("input[type='checkbox'][name='stakeholder']", this);
      if (!$(checkbox).is(":checked")) {
        allStakeholdersInGroupAreChecked = false;
        return;
      }
    });

    var groupIcon = $("[data-target-group-name='" + groupName + "'] .glyphicon");
    if (allStakeholdersInGroupAreChecked) {
      $(groupIcon).removeClass().addClass("glyphicon glyphicon-check");
    }
    else {
      $(groupIcon).removeClass().addClass("glyphicon glyphicon-unchecked");
    }

    return false;
  });

  $(document).on("click", ".btn-chart-expand", function () {

    var container = $(this).closest(".panel");
    var title = $(".panel-title", container).text();

    $("#expand-chart .modal-title").text(title);
    $("#expand-chart .modal-body").html("<div id='modal-chart-container' style='min-height: 500px'></div>")

    var chart = $(".panel-body", container).highcharts();

    $("#expand-chart").modal();
    setTimeout(function () {
      $("#modal-chart-container").highcharts(chart.options);
    }, 250);
    

  });

  $(document).on("click", ".btn-chart-toggle", function () {

    var container = $(this).closest(".panel-heading");
    var target = $(container).attr("data-target");

    if ($(target).is(":visible")) {
      $(".btn-chart-toggle .glyphicon", container).removeClass("glyphicon-resize-small").addClass("glyphicon-resize-full");
      $(".btn-chart-expand, .btn-chart-modal, .btn-chart-reload, .dropdown-toggle", container).prop("disabled", true);
      $(target).slideUp();
    }
    else {
      $(".btn-chart-toggle .glyphicon", container).addClass("glyphicon-resize-small").removeClass("glyphicon-resize-full");
      $(".btn-chart-expand, .btn-chart-modal, .btn-chart-reload, .dropdown-toggle", container).prop("disabled", false);
      $(target).slideDown(400, function () {
        if (!$(container).hasClass("loaded")) {
          $(container).loadchart();
        }
      });
    }

  });

  $(document).on("click", ".btn-chart-reload", function () {
    var icon = $(".glyphicon", this);
    if (! $(icon).hasClass("fa-spin")) {
      $(icon).addClass("fa-spin");
      $(this).closest(".panel-heading").loadchart(function () {
        $(icon).removeClass("fa-spin");
      });
    }
  });

  $(document).on("click", ".js-chart-type a", function () {
    var item = $(this).closest("li");
    if (!$(item).hasClass("active")) {
      var ul = $(this).closest("ul");
      $("li", ul).removeClass("active");
      $("input[type='radio']", ul).prop("checked", false);
      $(item).addClass("active");
      $("input[type='radio']", item).prop("checked", true);
      $(this).closest(".panel-heading").loadchart();
    }
  });

  $(document).on("click", ".btn-chart-modal", function () {
    var form = $(this).closest("form");
    var url = $(form).attr("action");
    var data = $(form).serialize();
    url += "?" + data;
    url += "&popup=1";
    var name = uuid();
    var win = window.open(url, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
  });

  $(document).on("click", ".btn-chart-delete", function () {
    var container = $(this).closest(".panel");
    var scenario_id = $(container).attr("data-chart-id");
    var name = $(this).attr("data-chart-name");

    $("#delete-scenario").val(scenario_id);
    $(".scenario-name").text(name);
    $("#modal-delete-scenario").modal("show");
  });

  $(document).on("click", ".btn-chart-info", function () {
    $(this).tooltip("hide");
    var url = $(this).attr("data-remote-url");
    var type = $(this).closest("form").attr("data-type");
    var modal;
    
    if (type === "scenario") {
      modal = $("#modal-scenario-details");
    }
    else {
      modal = $("#modal-decision-item-details");
    }

    $.ajax({
      url: url,
      cache: false,
      beforeSend: function () {
        $(modal).modal("show");
        $(".modal-body", modal).html("");
      },
      success: function (data) {
        var DESCENDING = 1;
        var VALUE_RANKING_COLUMN = 2;
        $(".modal-body", modal).html(data);
        if (type === "scenario") {
          $("table", modal).tablesorter({
            sortList: [[VALUE_RANKING_COLUMN, DESCENDING]]
          });
        }
      }
    });

  });

  $(document).on("click", ".btn-chart-rationale", function () {
    $("#modal-rationale").modal("show");
    var panel = $(this).closest(".panel");
    var title = $(".panel-title", panel).text();
    title = "Discussion: ".concat(title);
    var url = $(this).attr("data-remote-url");
    $.ajax({
      url: url,
      type: 'get',
      cache: false,
      dataType: 'html',
      beforeSend: function () {
        $("#modal-rationale .modal-title").text(title);
      },
      success: function (data) {
        $("#modal-rationale .modal-body").html(data);
      }
    });
  });

});
