from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget

class PlotWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "plot_macros",
        'rows'  : 5,
        'cols'  : 5,
        'plot_type': ['bar', 'pie']
        })

    security = ClassSecurityInfo()
    
    def getScripts(self, field, instance):
        """ return scripts """
        fieldName = field.getName()
        values = self.getValueForPlot(field, instance)
        
        if not (values['x'] and values['y']):
            return ''
        
        if values['type'] == 'pie':
            return """
<script class="code" type="text/javascript">
    $(document).ready(function(){
        $.jqplot.config.enablePlugins = true;

        var %(fieldname)s_values = %(values)s;

        %(fieldname)s_pie = $.jqplot('%(fieldname)s_id', [%(fieldname)s_values], {
            captureRightClick: true,
            seriesDefaults:{
                renderer:$.jqplot.PieRenderer,
                shadow: false,
                rendererOptions:{
                    startAngle: 90,
                    sliceMargin: 4,
                    highlightMouseDown: true,
                    showDataLabels: true
                }
            },
            legend: {
                    show:true,
                    location: 'nw',
                    renderer: $.jqplot.horizontalLegendRenderer,
                    yoffset: 5,
                    xoffset: 5
            }
        });
    });
</script>""" % {
                'fieldname': fieldName,
                'values': values['pie_value'],
               }
        
        return """
<script class="code" type="text/javascript">
    $(document).ready(function(){
        $.jqplot.config.enablePlugins = true;

        var %(fieldname)s_value_y = %(value_y)s;
        var %(fieldname)s_ticks = %(value_x)s;
        var %(fieldname)s_label_x = '%(label_x)s';
        var %(fieldname)s_label_y = '%(label_y)s';
        
        %(fieldname)s_bar = $.jqplot('%(fieldname)s_id', [%(fieldname)s_value_y], {
            seriesDefaults:{
                renderer:$.jqplot.BarRenderer,
                pointLabels: { show: true },
                yaxis:'yaxis', xaxis:'xaxis'
            },
            axes: {
                xaxis: {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                    tickOptions:{
                        showGridline: true
                    },
                    ticks: %(fieldname)s_ticks,
                    label: %(fieldname)s_label_x
                },
                yaxis:{
                    borderWidth:1,
                    autoscale: true,
                    numberTicks:4,
                    label:%(fieldname)s_label_y,
                    labelRenderer: $.jqplot.CanvasAxisLabelRenderer,
                }
            },
            highlighter: { show: false }
        });
    });
</script>""" % {
            'fieldname': fieldName,
            'value_x': values['x'],
            'value_y': values['y'],
            'label_x': values['label_x'],
            'label_y': values['label_y'],
            }
        
    def getValueForPlot(self, field, instance):
        """ 
            if type==bar return x, y;
            if type==pie return [(x1, y1), (x2,y2), ...(xn, yn)]
        """
        values = field.get(instance)
        if values['type'] == 'pie':
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
        
        name_field_type = field.getName() + '-type'
        name_field_x = field.getName() + '-x'
        name_field_y = field.getName() + '-y'
        name_field_label_x = field.getName() + '-label-x'
        name_field_label_y = field.getName() + '-label-y'
        
        value_type = form.get(name_field_type, empty_marker)
        value_x = form.get(name_field_x, empty_marker)
        value_y = form.get(name_field_y, empty_marker)
        label_x = form.get(name_field_label_x, empty_marker)
        label_y = form.get(name_field_label_y, empty_marker)
        
        return {'type': value_type, 'x': value_x, 'y': value_y, 'label_x': label_x, 'label_y': label_y}, {}
        
__all__ = ('PlotWidget')

registerWidget(PlotWidget,
               title='Plot Grid',
               description=('A spreadsheet like table'),
               used_for=('maire.contents.PlotField.PlotField',)
               )