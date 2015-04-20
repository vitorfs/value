$(function () {

  $(".js-add-value").click(function () {

    var template = [
      "<tr>",
      "<td>",
      "<input type='hidden' name='measurevalue_set-#-id' id='id_measurevalue_set-#-id'>",
      "<input type='hidden' name='measurevalue_set-#-measure' id='id_measurevalue_set-#-measure'>",
      "<input type='text' maxlength='255' name='measurevalue_set-#-description' id='id_measurevalue_set-#-description' value='' class='form-control'>",
      "</td>",
      "<td>",
      "<input type='number' name='measurevalue_set-#-weight' id='id_measurevalue_set-#-weight' value='' class='form-control'>",
      "</td>",
      "<td>",
      "<a href='#' class='js-remove-value'>",
      "<span class='glyphicon glyphicon-remove-sign'></span>",
      "</a>",
      "</td>",
      "</tr>"
    ];

    var count = parseInt($("#id_measurevalue_set-TOTAL_FORMS").val());
    var html = template.join("\n").replace(/#/g, count);
    $("table tbody").append(html);
    count = count + 1;
    $("#id_measurevalue_set-TOTAL_FORMS").val(count);

    return false;
  });


  $("table tbody").on("click", ".js-remove-value", function () {
    $(this).closest("tr").remove();

    return false;
  });

});