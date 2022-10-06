from zope.component import adapter
from zope.interface import implementer, implementer_only
from zope.schema.interfaces import IField

from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import ITextAreaWidget

from z3c.form.browser.textarea import TextAreaWidget
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import DISPLAY_MODE

from collective.geo.mapwidget.browser import widget
from collective.geo.mapwidget.browser.shapewidget import  ShapeMapWidget


class MapWidget(widget.MapWidget):
    js = None

    def __init__(self, view, request, context):
        self.view = view
        self.request = request
        self.context = context
        #self.mapid = "%s-map" % self.view.name.replace('.', '-')

    @property
    def mapid(self):
        return "%s-map" % self.view.name.replace('.', '-')

    def coords(self):
        return self.view.value


class MapDisplayWidget(MapWidget):
    _layers = ['shapedisplay']


class IFormMapWidget(ITextAreaWidget):
    """Interface for z3c.form map widget"""
    pass

@implementer_only(IFormMapWidget)
class FormMapWidget(TextAreaWidget):

    def update(self):
        super(FormMapWidget, self).update()

    @property
    def cgmap(self):
        # import pdb; pdb.set_trace()
        if self.mode == DISPLAY_MODE:
            # return ShapeMapWidget(self, self.request, self.context)
            return MapDisplayWidget(self, self.request, self.context)
        return MapWidget(self, self.request, self.context)


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def MapFieldWidget(field, request):
    """IFieldWidget factory for FormMapWidget."""
    return FieldWidget(field, FormMapWidget(request))
