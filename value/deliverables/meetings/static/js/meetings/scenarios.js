$(function () {

  $(".charts .panel-heading:eq(0)").loadchart();

  $("#modal-add-scenario").on("shown.bs.modal", function () {
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
      },
      complete: function () {
        $("#modal-add-scenario .modal-body").loading();
      }
    });
  });
  $("#modal-add-scenario").on("hidden.bs.modal", function () {
    $("#modal-add-scenario .modal-body").html("");
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

  $("#modal-scenario-builder").on("shown.bs.modal", function () {
    var url = $("#btn-scenario-builder").attr("data-remote-url");
    var category = $("#btn-scenario-builder").attr("data-scenario-builder");
    $.ajax({
      url: url,
      type: 'get',
      data: {
        'category': category
      },
      dataType: 'json',
      cache: false,
      beforeSend: function () {
        $("#modal-scenario-builder .modal-body").loading();
      },
      success: function (data) {
        $("#modal-scenario-builder .modal-body").html(data.form);
      },
      complete: function () {
        $("#modal-scenario-builder .modal-body").loading();
      }
    });
  });
  $("#modal-scenario-builder").on("hidden.bs.modal", function () {
    $("#modal-scenario-builder .modal-body").html("");
  });

  $("#form-scenario-builder").submit(function () {
    var form = $(this);
    $.ajax({
      url: $(form).attr("action"),
      type: $(form).attr("method"),
      data: $(form).serialize(),
      beforeSend: function () {

      },
      success: function (data) {
        if (data.is_valid) {
          $("#scenarios").load(" #scenarios > *", function () {
            $(".charts .panel-heading:eq(0)").loadchart();
          });
          $("#modal-scenario-builder").modal("hide");
        }
        else {
          $("#modal-scenario-builder .modal-body").html(data.form);
        }
      }
    });
    return false;
  });
      
});
