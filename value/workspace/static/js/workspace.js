$(function () {

  $(".js-tbl-instances tbody tr").click(function () {
    var id = $(this).attr("data-instance-id");
    location.href = "/workspace/" + id;
  });

});