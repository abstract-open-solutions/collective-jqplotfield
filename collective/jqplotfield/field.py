import logging
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Field import ObjectField
from Products.Archetypes.Field import encode
from Products.Archetypes.Field import decode
from Products.Archetypes.Field import registerField
from widget import PlotWidget
from interfaces import IPlotField
from zope.interface import implements

# # Our logger object
logger = logging.getLogger('PlotField')
logger.debug("PlotField loading")

class PlotField(ObjectField):
    """ For creating plot objects
    """
    implements(IPlotField)

    _properties = ObjectField._properties.copy()
    _properties.update({
        'type' : 'plot',
        'mode' : 'rw',
        # inital data of the field in form sequence of dicts
        'default' : {},
        'widget' : PlotWidget,
        })

    security = ClassSecurityInfo()


    def __init__(self, name=None, **kwargs):
        """ Create PlotField instance
        """

        # call super constructor
        ObjectField.__init__(self, name, **kwargs)

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """
        The passed in object should be a records object, or a sequence of dictionaries
        """
        __traceback_info__ = value, type(value)
        if value == {}:
            value = {}
            
        if isinstance(value, dict):
            title = value.get('title', '')
            value_type = value.get('type','')
            values_x = value.get('x',[])
            values_y = value.get('y',[])
            label_x = value.get('label_x','')
            label_y = value.get('label_y','')
            
            if title:
                title = decode(title.strip(), instance, **kwargs)
            if value_type:
                value_type = decode(value_type.strip(), instance, **kwargs)
            if label_x:
                label_x = decode(label_x.strip(), instance, **kwargs)
            if label_y:
                label_y = decode(label_y.strip(), instance, **kwargs)
                
            if values_x:
                values_x = [decode(v.strip(), instance, **kwargs)
                            for v in values_x if v and v.strip()]
            
            if values_y:
                values_y = [decode(v.strip(), instance, **kwargs)
                            for v in values_y if v and v.strip()]
            
            value = {'title': title, 'type': value_type, 'x': values_x, 'y': values_y, 'label_x': label_x, 'label_y': label_y}

        ObjectField.set(self, instance, value, **kwargs)

    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        values = ObjectField.get(self, instance, **kwargs) or {}
        
        title = ''
        value_type = ''
        data_x = []
        data_y = []
        label_x = ''
        label_y = ''
        
        if values:
            title = encode(values.get('title', ''), instance, **kwargs)
            value_type = encode(values.get('type', ''), instance, **kwargs)
            label_x = encode(values.get('label_x', ''), instance, **kwargs)
            label_y = encode(values.get('label_y', ''), instance, **kwargs)
            values_x = values.get('x', [])
            values_y = values.get('y', [])
            data_x = [encode(v, instance, **kwargs) for v in values_x]
            data_y = [encode(v, instance, **kwargs) for v in values_y]
        
        return {'title': title, 
                'type': value_type,
                'x': data_x,
                'y': data_y, 
                'label_x': label_x, 
                'label_y': label_y,}

    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
        return self.get(instance, **kwargs)

    security.declarePublic('get_size')
    def get_size(self, instance):
        """Get size of the stored data used for get_size in BaseObject
        """
        size=0
        for line in self.get(instance):
            size+=len(str(line))
        return size

registerField(PlotField,
              title='PlotField',
              description=('Used for storing tabular string data'))
