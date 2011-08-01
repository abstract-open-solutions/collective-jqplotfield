from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget

class PlotWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "plot_macros",
        'rows'  : 5,
        'cols'  : 5,
        'plot_type': ['bar', 'pie', 'donut']
        })

    security = ClassSecurityInfo()
    
    def getTitle(self, field, instance):
        fieldName = field.getName()
        values = self.getValues(field, instance)
        return values['title']
        
    def getScripts(self, field, instance):
        """ return scripts """
        fieldName = field.getName()
        values = self.getValueForPlot(field, instance)
        
        seriesColor = '['
        seriesColor += '"#094467","#1D6F9F",'
        seriesColor += '"#2e5c77","#285B7A","#304a59","#50a0cf","#72accf","#7ca4bb","#A5C8DD",'
        seriesColor += '"#697F8C"'
        seriesColor += ']'
        
        if not (values['x'] and values['y']):
            return ''
        
        if values['type'] in ['pie', 'donut']:
            plot_type = values['type'] == 'pie' and 'PieRenderer' or 'DonutRenderer'
            return """
<script class="code" type="text/javascript">
    $(document).ready(function(){
        $.jqplot.config.enablePlugins = true;

        var %(fieldname)s_values = %(values)s;

        %(fieldname)s_pie = $.jqplot('%(fieldname)s_id', [%(fieldname)s_values], {
            captureRightClick: true,
            grid: {
                drawBorder: false, 
                drawGridlines: false,
                background: '#E5E6E7',
                shadow:false
            },
            axesDefaults: {

            },
            seriesDefaults:{
                renderer:$.jqplot.%(plot_type)s,
                rendererOptions: {
                    showDataLabels: true
                }
            },
            legend: {
                show: true,
                drawBorder: false,
                location: 'w'
            },
            highlighter: {
                show: false
            },
            seriesColors: %(colors)s
        });
    });
</script>""" % {
                'fieldname': fieldName,
                'plot_type': plot_type,
                'values': values['pie_value'],
                'colors': seriesColor
               }
        
        return """
<script class="code" type="text/javascript">
    $(document).ready(function(){
        $.jqplot.config.enablePlugins = true;

        var %(fieldname)s_value_y = %(value_y)s;
        var %(fieldname)s_ticks = %(value_x)s;
        var %(fieldname)s_label_x = "%(label_x)s";
        var %(fieldname)s_label_y = "%(label_y)s";
        
        %(fieldname)s_bar = $.jqplot('%(fieldname)s_id', [%(fieldname)s_value_y], {
            captureRightClick: true,
            grid: {
                drawBorder: true, 
                drawGridlines: true,
                background: '#E5E6E7',
                shadow:false
            },
            axesDefaults: {

            },
            seriesDefaults:{
                renderer:$.jqplot.BarRenderer,
                pointLabels: { show: true },
                yaxis:'yaxis', xaxis:'xaxis'
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: %(fieldname)s_ticks,
                    label: %(fieldname)s_label_x,
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    tickRenderer: $.jqplot.CanvasAxisTickRenderer,
                    tickOptions: {
                      enableFontSupport: true,
                      angle: -30,
                      mark: 'cross'
                    }
                },
                yaxis:{
                    borderWidth:1,
                    autoscale: true,
                    numberTicks:4,
                    label:%(fieldname)s_label_y,
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer
                }
            },
            legend: {
                show: false
            },
            seriesColors: %(colors)s,
            highlighter: { show: false }
        });
    });
</script>""" % {
            'fieldname': fieldName,
            'colors': seriesColor,
            'value_x': values['x'],
            'value_y': values['y'],
            'label_x': values['label_x'],
            'label_y': values['label_y'],
            }
        
    def getValueForPlot(self, field, instance):
        """ 
            if type==bar return x, y;
            if type==pie or type==donut return [(x1, y1), (x2,y2), ...(xn, yn)]
        """
        values = self.getValues(field, instance)
        if values['type'] in ['pie', 'donut']:
            y = [float(v) for v in values['y']]
            coppie = zip(values['x'], y)
            values['pie_value'] = [list(c) for c in coppie]
        
        return values
        
    def getValues(self, field, instance):
        values = field.get(instance)
        return values
        
    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """Basic impl for form processing in a widget"""
        value = TypesWidget.process_form(self, instance, field, form, empty_marker, emptyReturnsMarker)
        
        name_field_title = field.getName() + '-plot-title'
        name_field_type = field.getName() + '-type'
        name_field_x = field.getName() + '-x'
        name_field_y = field.getName() + '-y'
        name_field_label_x = field.getName() + '-label-x'
        name_field_label_y = field.getName() + '-label-y'
        
        title = form.get(name_field_title, empty_marker)
        value_type = form.get(name_field_type, empty_marker)
        value_x = form.get(name_field_x, empty_marker)
        value_y = form.get(name_field_y, empty_marker)
        label_x = form.get(name_field_label_x, empty_marker)
        label_y = form.get(name_field_label_y, empty_marker)
        
        return {'title': title, 'type': value_type, 'x': value_x, 'y': value_y, 'label_x': label_x, 'label_y': label_y}, {}
        
__all__ = ('PlotWidget')

registerWidget(PlotWidget,
               title='Plot Grid',
               description=('A spreadsheet like table'),
               used_for=('maire.contents.PlotField.PlotField',)
               )