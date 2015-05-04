$.fn.loadchart = function () {

  var instance_id = $(this).attr("data-instance-id");
  var item_id = $(this).attr("data-item-id");

  var container = $(this);
  var chart_container = $(this).closest(".panel").find(".panel-body");

  $.ajax({
    url: '/workspace/' + instance_id + '/analyze/features/' + item_id + '/',
    type: 'GET',
    dataType: 'json',
    beforeSend: function () {
      $(chart_container).loading();
    },
    success: function (data) {
      $(chart_container).highcharts(data);
      $(container).addClass("loaded");
    },
    complete: function () {
      $(chart_container).loading();
    }
  });
};

$(function () {

  $(".panel-collapsable .panel-heading").click(function () {

    var target = $(this).attr("data-target");
    var id = $(this).attr("data-chart-id");

    if (!$(this).hasClass("loaded")) {
      $(this).loadchart();
    }

    if ($(target).is(":visible")) {
      $(target).slideUp(400, function () {

      });
    }
    else {
      $(target).slideDown(400, function () {
        
      });
    }

  });


  $("[data-toggle='dropdown']").click(function (e) {
    $(this).dropdown("toggle");
    e.stopImmediatePropagation();
  });

  $(".btn-chart-reload").click(function (e) {
    $(this).closest(".panel-heading").loadchart();
    e.stopPropagation();
  });

});
