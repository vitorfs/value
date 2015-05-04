$(function () {

  $(".panel-collapsable .panel-heading").click(function () {

    
    var target = $(this).attr("data-target");
    var id = $(this).attr("data-chart-id");

    if ($(target).is(":visible")) {
      $(target).slideUp(400, function () {

      });
    }
    else {

      $(".panel-body", target).loading();

      $(target).slideDown(400, function () {
        $("#chart-container-" + id).highcharts(options[id]);
        
      });
    }

  });

});