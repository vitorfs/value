$.fn.loadchart = function (callback) {

  callback = callback || function () {};

  var url = $(this).attr("data-uri");
  var chart_type = $(".js-chart-type li.active a", this).attr("data-chart");
  if (chart_type) {
    url += "?chart=" + chart_type;
  }

  var container = $(this);
  var chart_container = $(this).closest(".panel").find(".panel-body");

  var display_loading = ! $(container).hasClass("loaded");
  display_loading=true;

  $.ajax({
    url: url,
    type: 'GET',
    dataType: 'json',
    cache: false,
    beforeSend: function () {
      if (display_loading) {
        $(chart_container).loading();
      }
    },
    success: function (data) {
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

  $(".btn-chart-expand").click(function () {

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

  $(".btn-chart-toggle").click(function () {

    var container = $(this).closest(".panel-heading");

    var target = $(container).attr("data-target");
    var id = $(container).attr("data-chart-id");

    if ($(target).is(":visible")) {
      $(".btn-chart-toggle .glyphicon", container).removeClass("glyphicon-minus").addClass("glyphicon-plus");
      $(".btn-chart-expand, .btn-chart-reload, .dropdown-toggle", container).prop("disabled", true);
      $(target).slideUp();
    }
    else {
      $(".btn-chart-toggle .glyphicon", container).addClass("glyphicon-minus").removeClass("glyphicon-plus");
      $(".btn-chart-expand, .btn-chart-reload, .dropdown-toggle", container).prop("disabled", false);
      $(target).slideDown(400, function () {
        if (!$(container).hasClass("loaded")) {
          $(container).loadchart();
        }
      });
    }

  });

  $(".btn-chart-reload").click(function () {
    var icon = $(".glyphicon", this);
    if (! $(icon).hasClass("fa-spin")) {
      $(icon).addClass("fa-spin");
      $(this).closest(".panel-heading").loadchart(function () {
        $(icon).removeClass("fa-spin");
      });
    }
  });

  $(".js-chart-type a").click(function () {
    if (!$(this).closest("li").hasClass("active")) {
      var ul = $(this).closest("ul");
      $("li", ul).removeClass("active");
      $(this).closest("li").addClass("active");
      $(this).closest(".panel-heading").loadchart();
    }
  });

});
