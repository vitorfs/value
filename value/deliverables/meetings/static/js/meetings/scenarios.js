$(function () {

  /* Add scenario functions */

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
        $("#add-table-decision-items").tablesorter({ 
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
      success: function (data) {
        if (data.is_valid) {
          $.get("", function (data) {
            $("#scenarios").replaceWith($("#scenarios", data));
            $("#scenarios-menu").replaceWith($("#scenarios-menu", data));
            $(".charts [data-preload='True']").each(function () {
              $(".panel-heading", this).loadchart();
            });
          }, "html");
          $("#modal-add-scenario").modal("hide");
        }
        else {
          $("#modal-add-scenario .modal-body").html(data.form);
          $("#add-table-decision-items").tablesorter({ headers: { 0: { sorter: false }}});
          initializeCheckAll();
        }
      }
    });
    return false;
  });

  /* Edit scenario functions */

  $(document).on("click", ".btn-chart-edit", function () {
    var url = $(this).attr("data-remote-url");
    $("#form-edit-scenario").attr("action", url);
  });

  $("#modal-edit-scenario").on("shown.bs.modal", function () {
    $.ajax({
      url: $("#form-edit-scenario").attr("action"),
      dataType: 'json',
      beforeSend: function () {
        $("#modal-edit-scenario .modal-body").loading();
      },
      success: function (data) {
        var DESCENDING = 1;
        var VALUE_RANKING_COLUMN = 3;

        $("#modal-edit-scenario .modal-body").html(data.form);
        $("#edit-table-decision-items").tablesorter({ 
          headers: { 0: { sorter: false } },
          sortList: [[VALUE_RANKING_COLUMN, DESCENDING]]
        });
        initializeCheckAll();
      },
      complete: function () {
        $("#modal-edit-scenario .modal-body").loading();
      }
    });
  });
  $("#modal-edit-scenario").on("hidden.bs.modal", function () {
    $("#modal-edit-scenario .modal-body").html("");
  });

  $("#form-edit-scenario").submit(function () {
    $.ajax({
      url: $("#form-edit-scenario").attr("action"),
      data: $("#form-edit-scenario").serialize(),
      type: $("#form-edit-scenario").attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.is_valid) {
          $.get("", function (data) {
            $("#scenarios").replaceWith($("#scenarios", data));
            $("#scenarios-menu").replaceWith($("#scenarios-menu", data));
            $(".charts [data-preload='True']").each(function () {
              $(".panel-heading", this).loadchart();
            });
          }, "html");
          $("#modal-edit-scenario").modal("hide");
        }
        else {
          $("#modal-edit-scenario .modal-body").html(data.form);
          $("#edit-table-decision-items").tablesorter({ headers: { 0: { sorter: false }}});
          initializeCheckAll();
        }
      }
    });
    return false;
  });

  /* Scenario builder functions */

  $("#modal-scenario-builder").on("shown.bs.modal", function () {
    var url = $(".js-scenario-builder").attr("data-remote-url");
    $.ajax({
      url: url,
      type: 'get',
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
          $.get("", function (data) {
            $("#scenarios").replaceWith($("#scenarios", data));
            $("#scenarios-menu").replaceWith($("#scenarios-menu", data));
            $("#scenarios .panel-heading:eq(0)").loadchart();
          }, "html");
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
