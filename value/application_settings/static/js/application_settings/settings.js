$(function () {

  $("#order-by").sortable({
    group: "order",
    store: {
      get: function (sortable) {
        var order = localStorage.getItem(sortable.options.group);
        return order ? order.split('|') : [];
      },
      set: function (sortable) {
        var order = sortable.toArray();
        localStorage.setItem(sortable.options.group, order.join('|'));
      }
    }
  });


  $("#columns").sortable({
    group: "order",
    animation: 150
  });


  $("#column-display-order").sortable({
    draggable: ".sortable"
  });

  $("#plain-text-column-order").sortable({
    draggable: ".sortable"
  });

  $("#id_orientation").change(function () {
    $("#id_orientation option").each(function () {
      var cssclass = $(this).val();
      $(cssclass).hide();
    });
    var cssclass = $(this).val();
    $(cssclass).show();
  });

});
