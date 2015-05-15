$(function () {

  $(".js-tbl-deliverables tbody tr").click(function () {
    var id = $(this).attr("data-deliverable-id");
    location.href = "/deliverables/" + id;
  });

});
