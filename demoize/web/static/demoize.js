var demoize = {};

demoize.scrollToCenterOnLine = function(line) {
    var lineEl = $('#line-' + line);
    var h = $(window).height();
    var elH = lineEl.height();
    var elOff = lineEl.offset();
    $(window).scrollTop(elOff.top + (elH / 2) - (h / 2));
};
