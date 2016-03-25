$(function () {

  $(".color-selector").colorselector();

  var manage_value_order = function () {
    $("#table-measure-values").updateFormsetIndex();
    $("#table-measure-values tbody tr").each(function () {
      $("td:eq(0) input", this).val($(this).index());
    });

    $(".js-order-increase, .js-order-decrease").show();

    $("#table-measure-values tbody tr:first-child .js-order-increase").hide();
    $("#table-measure-values tbody tr:last-child .js-order-decrease").hide();
  };

  manage_value_order();

  $(".js-add-value").click(function () {

    var template = [
      "<tr>",
      "<td class='text-center' style='vertical-align: middle'>",
      "<a href='#' class='js-order-increase' style='display: block;'><span class='glyphicon glyphicon-triangle-top'></span></a>",
      "<a href='#' class='js-order-decrease' style='display: block;'><span class='glyphicon glyphicon-triangle-bottom'></span></a>",
      "<input type='hidden' name='measurevalue_set-{value}-order' id='id_measurevalue_set-{value}-order'>",
      "</td>",
      "<td style='vertical-align: middle'>",
      "<input type='hidden' name='measurevalue_set-{value}-id' id='id_measurevalue_set-{value}-id'>",
      "<input type='hidden' name='measurevalue_set-{value}-measure' id='id_measurevalue_set-{value}-measure'>",
      "<input type='text' maxlength='255' name='measurevalue_set-{value}-description' id='id_measurevalue_set-{value}-description' value='' class='form-control'>",
      "</td>",
      "<td class='text-center' style='vertical-align: middle'>",
      "<select id='id_measurevalue_set-{value}-color' name='measurevalue_set-{value}-color' class='color-selector' style='display: none;'>",
      "<option data-color='#5CB85C' value='#5CB85C'>#5CB85C</option>",
      "<option data-color='#BAE8BA' value='#BAE8BA'>#BAE8BA</option>",
      "<option data-color='#8AD38A' value='#8AD38A'>#8AD38A</option>",
      "<option data-color='#369836' value='#369836'>#369836</option>",
      "<option data-color='#1B7C1B' value='#1B7C1B'>#1B7C1B</option>",
      "<option data-color='#F0AD4E' value='#F0AD4E'>#F0AD4E</option>",
      "<option data-color='#FFD8A0' value='#FFD8A0'>#FFD8A0</option>",
      "<option data-color='#FFC675' value='#FFC675'>#FFC675</option>",
      "<option data-color='#DE9226' value='#DE9226'>#DE9226</option>",
      "<option data-color='#AD6D11' value='#AD6D11'>#AD6D11</option>",
      "<option data-color='#D9534F' value='#D9534F'>#D9534F</option>",
      "<option data-color='#FFADAB' value='#FFADAB'>#FFADAB</option>",
      "<option data-color='#FC827F' value='#FC827F'>#FC827F</option>",
      "<option data-color='#BE2F2B' value='#BE2F2B'>#BE2F2B</option>",
      "<option data-color='#961512' value='#961512'>#961512</option>",
      "<option data-color='#5BC1DE' value='#5BC1DE'>#5BC1DE</option>",
      "<option data-color='#BAEAF8' value='#BAEAF8'>#BAEAF8</option>",
      "<option data-color='#85D5EC' value='#85D5EC'>#85D5EC</option>",
      "<option data-color='#39ACCD' value='#39ACCD'>#39ACCD</option>",
      "<option data-color='#1993B6' value='#1993B6'>#1993B6</option>",
      "<option data-color='#337BB7' value='#337BB7' selected>#337BB7</option>",
      "<option data-color='#7EB1DC' value='#7EB1DC'>#7EB1DC</option>",
      "<option data-color='#5393C8' value='#5393C8'>#5393C8</option>",
      "<option data-color='#1265AB' value='#1265AB'>#1265AB</option>",
      "<option data-color='#094B83' value='#094B83'>#094B83</option>",
      "<option data-color='#222222' value='#222222'>#222222</option>",
      "<option data-color='#929191' value='#929191'>#929191</option>",
      "<option data-color='#5E5E5E' value='#5E5E5E'>#5E5E5E</option>",
      "<option data-color='#000000' value='#000000'>#000000</option>",
      "<option data-color='#030202' value='#030202'>#030202</option>",
      "</select>",
      "</td>",
      "<td class='text-center' style='vertical-align: middle'>",
      "<a href='#' class='js-remove-value'>",
      "<span class='glyphicon glyphicon-remove-sign'></span>",
      "</a>",
      "</td>",
      "</tr>"
    ];

    var html = template.join("\n");
    $("#table-measure-values tbody").append(html);
    $("#table-measure-values tbody tr:last td .color-selector").colorselector();
    manage_value_order();
    return false;
  });

  $("#table-measure-values tbody").on("click", ".js-remove-value", function () {
    $(this).closest("tr").remove();
    manage_value_order();
    return false;
  });

  $("#table-measure-values tbody").on("click", ".js-order-increase", function () {
    var i = $(this).closest("tr").index();
    if (i > 0) {
      var sibling = $("#table-measure-values tbody tr:eq(" + (i - 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).before(row);
    }
    manage_value_order();
    return false;
  });

  $("#table-measure-values tbody").on("click", ".js-order-decrease", function () {
    var container = $(this).closest("tbody");
    var rows = $("tr", container).length - 1;
    var i = $(this).closest("tr").index();
    if (i < rows) {
      var sibling = $("#table-measure-values tbody tr:eq(" + (i + 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).after(row);
    }
    manage_value_order();
    return false;
  });

});
