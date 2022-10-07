// TODO:
// Zoeken in item titles
// Inklapbare fieldsets
var dashy = (function () {
    function createItem(item) {
        var link = document.createElement('a');
        link.className = 'dashy-link';
        link.href = item.url;
        link.innerHTML = '<span class="dashy-icon"><i class="fa fa-' + item.icon + '"></i></span><span class="dashy-title">' + item.title + '</span>';
        link.style.color = item.color;
        return link;
    }

    function getDashy(items, menu) {
        var inner = document.createElement('div');
        var className = 'dashy-container';
        if (menu) className += ' dashy-menu';
        inner.className = className;
        for (var i = 0, l = items.length; i < l; i++) {
            var fieldset = items[i];
            for (var j = 0, k = fieldset.children.length; j < k; j++) {
                var item = fieldset.children[j];
                inner.appendChild(createItem(item));
            }
        }
        return inner;
    }

    return function (options) {
        var el = document.getElementById(options.appendTo);
        var inner = getDashy(options.items, options.menu);
        el.appendChild(inner);
    }
}());
