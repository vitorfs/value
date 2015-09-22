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

$(function () {

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
    return false;
  });

  $(document).on("click", ".btn-chart-download", function () {
    var panel = $(this).closest(".panel");
    var chart = $(".panel-body", panel).highcharts(), svg = chart.getSVG();
    $("#id_svg").val(svg);
    $("#chart-download").submit();
  });

  $(document).on("click", ".btn-chart-expand", function () {

    var container = $(this).closest(".panel");
    var title = $(".panel-title", container).text();

    $("#expand-chart .modal-title").text(title);
    $("#expand-chart .modal-body").html("<div id='modal-chart-container' style='min-height: 500px'></div>")

    var chart = $(".panel-body", container).highcharts();
    

    $("#expand-chart").modal();

    $("#expand-chart").on("shown.bs.modal", function () {
      $("#modal-chart-container").highcharts(chart.options);
    })

  });

  $(document).on("click", ".btn-chart-toggle", function () {

    var container = $(this).closest(".panel-heading");

    var target = $(container).attr("data-target");
    var id = $(container).attr("data-chart-id");

    if ($(target).is(":visible")) {
      $(".btn-chart-toggle .glyphicon", container).removeClass("glyphicon-minus").addClass("glyphicon-plus");
      $(".btn-chart-expand, .btn-chart-modal, .btn-chart-reload, .btn-chart-download, .btn-chart-delete, .btn-chart-edit, .dropdown-toggle", container).prop("disabled", true);
      $(target).slideUp();
    }
    else {
      $(".btn-chart-toggle .glyphicon", container).addClass("glyphicon-minus").removeClass("glyphicon-plus");
      $(".btn-chart-expand, .btn-chart-modal, .btn-chart-reload, .btn-chart-download, .btn-chart-delete, .btn-chart-edit, .dropdown-toggle", container).prop("disabled", false);
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

  $(document).on("click", ".select-all-stakeholders", function (e) {
    e.stopPropagation();
    var container = $(this).closest(".js-stakeholders");
    var group_name = $(this).closest("li").attr("data-target-group-name");
    $("[data-group-name='" + group_name + "']", container).each(function () {
      var stakeholder = $(this);
      if (!$("[name='stakeholder']", this).is(":checked")) {
        $(stakeholder).click();
      }
    });
  });

  $(document).on("click", ".select-none-stakeholders", function (e) {
    e.stopPropagation();
    var container = $(this).closest(".js-stakeholders");
    var group_name = $(this).closest("li").attr("data-target-group-name");
    $("[data-group-name='" + group_name + "']", container).each(function () {
      var stakeholder = $(this);
      if ($("[name='stakeholder']", this).is(":checked")) {
        $(stakeholder).click();
      }
    });
  });

  $(document).on("click", ".btn-chart-delete", function () {
    var container = $(this).closest("form");
    var scenario_id = $(container).attr("data-chart-id");
    var name = $(".panel-title", container).text();

    $("#delete-scenario").val(scenario_id);
    $(".scenario-name").text(name);
    $("#modal-delete-scenario").modal("show");
  });

});
