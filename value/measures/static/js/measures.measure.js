$(function () {

  $(".color-selector").colorselector();

  var manage_value_order = function () {
    $("table tbody tr").each(function () {
      $("td:eq(0) input", this).val($(this).index());
    });
  };

  manage_value_order();

  $(".js-add-value").click(function () {

    var template = [
      "<tr>",
      "<td class='text-center' style='vertical-align: middle'>",
      "<a href='#' class='js-order-increase'><span class='glyphicon glyphicon-triangle-top'></span></a>",
      "<a href='#' class='js-order-decrease'><span class='glyphicon glyphicon-triangle-bottom'></span></a>",
      "<input type='hidden' name='measurevalue_set-{value}-order' id='id_measurevalue_set-{value}-order'>",
      "</td>",
      "<td style='vertical-align: middle'>",
      "<input type='hidden' name='measurevalue_set-{value}-id' id='id_measurevalue_set-{value}-id'>",
      "<input type='hidden' name='measurevalue_set-{value}-measure' id='id_measurevalue_set-{value}-measure'>",
      "<input type='text' maxlength='255' name='measurevalue_set-{value}-description' id='id_measurevalue_set-{value}-description' value='' class='form-control'>",
      "</td>",
      "<td class='text-center' style='vertical-align: middle'>",
      "<select id='id_measurevalue_set-{value}-color' name='measurevalue_set-{value}-color' class='color-selector' style='display: none;'>",
      "<option data-color='#A0522D' value='#A0522D'>sienna</option>",
      "<option data-color='#CD5C5C' value='#CD5C5C'>indianred</option>",
      "<option data-color='#FF4500' value='#FF4500'>orangered</option>",
      "<option data-color='#008B8B' value='#008B8B'>darkcyan</option>",
      "<option data-color='#B8860B' value='#B8860B'>darkgoldenrod</option>",
      "<option selected='selected' data-color='#32CD32' value='#32CD32'>limegreen</option>",
      "<option data-color='#FFD700' value='#FFD700'>gold</option>",
      "<option data-color='#48D1CC' value='#48D1CC'>mediumturquoise</option>",
      "<option data-color='#87CEEB' value='#87CEEB'>skyblue</option>",
      "<option data-color='#FF69B4' value='#FF69B4'>hotpink</option>",
      "<option data-color='#CD5C5C' value='#CD5C5C'>indianred</option>",
      "<option data-color='#87CEFA' value='#87CEFA'>lightskyblue</option>",
      "<option data-color='#6495ED' value='#6495ED'>cornflowerblue</option>",
      "<option data-color='#DC143C' value='#DC143C'>crimson</option>",
      "<option data-color='#FF8C00' value='#FF8C00'>darkorange</option>",
      "<option data-color='#C71585' value='#C71585'>mediumvioletred</option>",
      "<option data-color='#000000' value='#000000'>black</option>",
      "</select>",
      "</td>",
      "<td class='text-center' style='vertical-align: middle'>",
      "<a href='#' class='js-remove-value'>",
      "<span class='glyphicon glyphicon-remove-sign'></span>",
      "</a>",
      "</td>",
      "</tr>"
    ];

    var count = parseInt($("#id_measurevalue_set-TOTAL_FORMS").val());
    var html = template.join("\n").replace(/{value}/g, count);
    $("table tbody").append(html);
    $("#id_measurevalue_set-" + count + "-color").colorselector();
    count = count + 1;
    $("#id_measurevalue_set-TOTAL_FORMS").val(count);
    manage_value_order();
    return false;
  });

  $("table tbody").on("click", ".js-remove-value", function () {
    $(this).closest("tr").remove();
    manage_value_order();
    return false;
  });

  $("table tbody").on("click", ".js-order-increase", function () {
    var i = $(this).closest("tr").index();
    if (i > 0) {
      var sibling = $("table tbody tr:eq(" + (i - 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).before(row);
    }
    manage_value_order();
    return false;
  });

  $("table tbody").on("click", ".js-order-decrease", function () {
    var container = $(this).closest("tbody");
    var rows = $("tr", container).length - 1;
    var i = $(this).closest("tr").index();
    if (i < rows) {
      var sibling = $("table tbody tr:eq(" + (i + 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).after(row);      
    }
    manage_value_order();
    return false;
  });

});