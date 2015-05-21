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

});
