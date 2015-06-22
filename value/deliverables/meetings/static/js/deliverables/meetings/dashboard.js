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

  $(".js-select-stakeholder").click(function (e) {
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

  $(".btn-chart-download").click(function () {
    var panel = $(this).closest(".panel");
    var chart = $(".panel-body", panel).highcharts(), svg = chart.getSVG();
    $("#id_svg").val(svg);
    $("#chart-download").submit();
  });

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
      $(".btn-chart-expand, .btn-chart-modal, .btn-chart-reload, .btn-chart-download, .dropdown-toggle", container).prop("disabled", true);
      $(target).slideUp();
    }
    else {
      $(".btn-chart-toggle .glyphicon", container).addClass("glyphicon-minus").removeClass("glyphicon-plus");
      $(".btn-chart-expand, .btn-chart-modal, .btn-chart-reload, .btn-chart-download, .dropdown-toggle", container).prop("disabled", false);
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

  $(".btn-chart-modal").click(function () {

    var form = $(this).closest("form");

    var url = $(form).attr("action");
    var data = $(form).serialize();
    url += "?" + data;
    var name = uuid();
    var win = window.open(url, name, 'height=500,width=800,resizable=yes,scrollbars=yes');

    /*var container = $(this).closest(".panel");
    var title = $(".panel-title", container).text();
    var chart = $(".panel-body", container).highcharts();


    var id = uuid();
    var template = $("#modal-template-chart").html();
    var rendered = Mustache.render(template, { 
      'id': id,
      'title': 'Test'
    });

    $("body").prepend(rendered);

    var detachedChartCssSelector = "#" + id + " .panel-body";
    var detachedChartContainer = $(detachedChartCssSelector);

    //var chartId = uuid();
    //$("body").prepend("<div id='" + chartId + "' class='chart-window'></div>");

    $(detachedChartContainer).highcharts(chart.options);
    //var windowChart = $(detachedChartContainer).highcharts();

    interact("#" + id)
      .draggable({
        inertia: true,
        onmove: function (event) {
          var target = event.target,
              x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
              y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

          target.style.webkitTransform =
          target.style.transform =
            'translate(' + x + 'px, ' + y + 'px)';

          target.setAttribute('data-x', x);
          target.setAttribute('data-y', y);
        }
      }).resizable({
        edges: { left: true, right: true, bottom: true, top: true }
      }).on('resizemove', function (event) {
        var target = event.target,
            x = (parseFloat(target.getAttribute('data-x')) || 0),
            y = (parseFloat(target.getAttribute('data-y')) || 0);

        target.style.width  = event.rect.width + 'px';
        target.style.height = event.rect.height + 'px';

        x += event.deltaRect.left;
        y += event.deltaRect.top;

        target.style.webkitTransform = target.style.transform =
            'translate(' + x + 'px,' + y + 'px)';

        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);

        //windowChart.reflow();

    });*/
  });
});
