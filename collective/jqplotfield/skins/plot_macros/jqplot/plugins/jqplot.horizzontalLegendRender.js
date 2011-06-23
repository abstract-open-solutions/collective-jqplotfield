(function($) {

    // Class: $.jqplot.horizontalLegendRenderer
    // Renders the table legends horizontally.

    if ($.jqplot == undefined) { return }

    $.jqplot.horizontalLegendRenderer = function() { };
    $.jqplot.horizontalLegendRenderer.prototype.init = function(options) {
        $.extend(true, this, options);
    };

    // The draw function should return the HTML <table> element with the chart legends.
    $.jqplot.horizontalLegendRenderer.prototype.draw = function(options) {
        var series = this._series;
        // The legends table contains a single row, with one td per series.
        // each td element contains two divs - the series color and series label.
        this._elem = $('<table class="jqplot-table-legend"><tr></tr></table>');
        for ( var i = 0; i < series.length; i++ ) {
            var s = series[i];
            var td = $('<td>'
                     + '    <div style="float:left">' // This div contains the color swatch
                     + '        <div class="jqplot-table-legend-swatch" style="width:10px; height: 10px; border: 1px solid black; margin: 2px 2px 0 2px;"/>'
                     + '    </div>'
                     + '    <div style="float: right"></div>' // This div contains the series label
                     + '</td>');
            td.find('div:eq(0) div').css('background-color', s.color);
            td.children('div:eq(1)').append(s.label);
            this._elem.append(td);
        }
        return this._elem;
    }

    // The pack function positions the legends table.
    $.jqplot.horizontalLegendRenderer.prototype.pack = function(offsets) {
        this._elem.css('left', offsets.left + this.xoffset);
        this._elem.css('top', offsets.top + this.yoffset);
    }


})(jQuery);
