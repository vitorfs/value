$(function () {

  $(".charts .panel-heading:eq(0)").loadchart();

  $("#modal-add-scenario").on("show.bs.modal", function () {
    $.ajax({
      url: $("#form-add-scenario").attr("action"),
      dataType: 'json',
      beforeSend: function () {
        $("#modal-add-scenario .modal-body").loading();
      },
      success: function (data) {
        var DESCENDING = 1;
        var VALUE_RANKING_COLUMN = 3; 

        $("#modal-add-scenario .modal-body").html(data.form);
        $("#table-decision-items").tablesorter({ 
          headers: { 0: { sorter: false } },
          sortList: [[VALUE_RANKING_COLUMN, DESCENDING]]
        });
        initializeCheckAll();
      }
    });
  });

  $("#form-add-scenario").submit(function () {
    $.ajax({
      url: $("#form-add-scenario").attr("action"),
      data: $("#form-add-scenario").serialize(),
      type: $("#form-add-scenario").attr("method"),
      dataType: 'json',
      beforeSend: function () {
        
      },
      success: function (data) {
        if (data.is_valid) {
          $("#scenarios").load(" #scenarios > *", function () {
            $(".charts .panel-heading:eq(0)").loadchart();
          });
          $("#modal-add-scenario").modal("hide");
        }
        else {
          $("#modal-add-scenario .modal-body").html(data.form);
          $("#table-decision-items").tablesorter({ headers: { 0: { sorter: false }}});
          initializeCheckAll();
        }
      }
    });
    return false;
  });
      
});
