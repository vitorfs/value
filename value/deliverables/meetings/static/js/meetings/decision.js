$(function () {
  $("#table-final-decision").tablesorter();

  $("[name='final-decision']").change(function () {
    if ($(this).is(":checked")) {
      $(this).siblings(".decision-text").text("Yes");
    }
    else {
      $(this).siblings(".decision-text").text("No");
    }
  });
});
