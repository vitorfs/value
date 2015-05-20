$(function () {

  $("#order_by").sortable({
    group: "order",
    animation: 150,
    store: {
      get: function (sortable) {
        var order = localStorage.getItem(sortable.options.group);
        return order ? order.split('|') : [];
      },
      set: function (sortable) {
        var order = sortable.toArray();
        localStorage.setItem(sortable.options.group, order.join('|'));
      }
    },
    onAdd: function (evt){ console.log('onAdd.foo:', [evt.item, evt.from]); },
    onUpdate: function (evt){ console.log('onUpdate.foo:', [evt.item, evt.from]); },
    onRemove: function (evt){ console.log('onRemove.foo:', [evt.item, evt.from]); },
    onStart:function(evt){ console.log('onStart.foo:', [evt.item, evt.from]);},
    onSort:function(evt){ console.log('onStart.foo:', [evt.item, evt.from]);},
    onEnd: function(evt){ console.log('onEnd.foo:', [evt.item, evt.from]);}
  });


  $("#columns").sortable({
    group: "order",
    animation: 150,
    onAdd: function (evt){ console.log('onAdd.bar:', evt.item); },
    onUpdate: function (evt){ console.log('onUpdate.bar:', evt.item); },
    onRemove: function (evt){ console.log('onRemove.bar:', evt.item); },
    onStart:function(evt){ console.log('onStart.foo:', evt.item);},
    onEnd: function(evt){ console.log('onEnd.foo:', evt.item);}
  });
});
