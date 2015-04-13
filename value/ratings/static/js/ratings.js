$(function () {

  $(".js-add-value").click(function () {

    var template = [
      "<tr>",
      "<td>",
      "<input type='hidden' name='ratingvalue_set-#-id' id='id_ratingvalue_set-#-id'>",
      "<input type='hidden' name='ratingvalue_set-#-rating' id='id_ratingvalue_set-#-rating'>",
      "<input type='text' maxlength='255' name='ratingvalue_set-#-description' id='id_ratingvalue_set-#-description' value='' class='form-control'>",
      "</td>",
      "<td>",
      "<input type='number' name='ratingvalue_set-#-weight' id='id_ratingvalue_set-#-weight' value='' class='form-control'>",
      "</td>",
      "<td>",
      "<a href='#' class='js-remove-value'>",
      "<span class='glyphicon glyphicon-remove-sign'></span>",
      "</a>",
      "</td>",
      "</tr>"
    ];

    var count = parseInt($("#id_ratingvalue_set-TOTAL_FORMS").val()) + 1;
    var html = template.join("\n").replace(/#/g, count);
    $("#id_ratingvalue_set-TOTAL_FORMS").val(count);
    $("table tbody").append(html);

    return false;
  });


  $("table tbody").on("click", ".js-remove-value", function () {
    $(this).closest("tr").remove();

    //var count = $("table tbody tr").length;
    //$("#id_ratingvalue_set-TOTAL_FORMS").val(count);

    return false;
  });

});