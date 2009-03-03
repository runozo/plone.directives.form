import zope.interface
import zope.interface.interface
import zope.interface.interfaces

import zope.component

import martian
import martian.error

import grokcore.component

import grokcore.view
import grokcore.view.util

import plone.directives.form.schema

import z3c.form.interfaces
import z3c.form.form
import z3c.form.button
import plone.autoform.formbase

import zope.i18nmessageid

import zope.publisher.interfaces.browser
import zope.publisher.publish

import Products.statusmessages.interfaces
import Products.Five.browser.metaconfigure

import plone.z3cform.layout

_ = zope.i18nmessageid.MessageFactory(u'plone.directives.form')

def default_view_name(factory, module=None, **data):
    return factory.__name__.lower()

# Base classes

class GrokkedForm(object):
    """Marker base class for all grokked forms. Do not use directly.
    """
    martian.baseclass()
    
# Page forms

class Form(GrokkedForm, z3c.form.form.Form):
    """A basic form.
    """
    martian.baseclass()

class SchemaForm(plone.autoform.formbase.AutoExtensibleForm, Form):
    """A basic extensible form
    """
    martian.baseclass()
    
    schema = None # Must be set by subclass

# Add forms

class AddForm(GrokkedForm, z3c.form.form.AddForm):
    """A standard add form.
    """
    martian.baseclass()
    
    immediate_view = None
    
    def __init__(self, context, request):
        super(AddForm, self).__init__(context, request)
        self.request['disable_border'] = True
    
    def nextURL(self):
        if self.immediate_view is not None:
            return self.immediate_view
        else:
            return self.context.absolute_url()
    
    # Buttons
    
    @z3c.form.button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            Products.statusmessages.interfaces.IStatusMessage(self.request) \
                .addStatusMessage(_(u"Changes saved"), "info")
    
    @z3c.form.button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        Products.statusmessages.interfaces.IStatusMessage(self.request) \
            .addStatusMessage(_(u"Add New Item operation cancelled"), "info")
        self.request.response.redirect(self.nextURL()) 

    def updateActions(self):
        super(AddForm, self).updateActions()
        self.actions["save"].addClass("context")
        self.actions["cancel"].addClass("standalone")

class SchemaAddForm(plone.autoform.formbase.AutoExtensibleForm, AddForm):
    """An extensible add form.
    """
    martian.baseclass()
    
    schema = None # Must be set by subclass

# Edit forms

class EditForm(GrokkedForm, z3c.form.form.EditForm):
    """A standard edit form
    """
    martian.baseclass()
    
    @z3c.form.button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        Products.statusmessages.interfaces.IStatusMessage(self.request) \
            .addStatusMessage(_(u"Changes saved"), "info")
        self.request.response.redirect(self.context.absolute_url())
    
    @z3c.form.button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        Products.statusmessages.interfaces.IStatusMessage(self.request) \
            .addStatusMessage(_(u"Edit cancelled"), "info")
        self.request.response.redirect(self.context.absolute_url()) 
    
    def updateActions(self):
        super(EditForm, self).updateActions()
        self.actions["save"].addClass("context")
        self.actions["cancel"].addClass("standalone")

class SchemaEditForm(plone.autoform.formbase.AutoExtensibleForm, EditForm):
    """An extensible edit form
    """
    martian.baseclass()
    
    schema = None # Must be set by subclass

# Grokkers

class FormGrokker(martian.ClassGrokker):
    martian.component(GrokkedForm)
    
    martian.directive(grokcore.component.context)
    martian.directive(grokcore.view.layer, default=zope.publisher.interfaces.browser.IDefaultBrowserLayer)
    martian.directive(grokcore.component.name, get_default=default_view_name)
    martian.directive(grokcore.security.require, name='permission', default=None)
    
    default_permissions = {
        EditForm          : 'cmf.ModifyPortalContent',
        SchemaEditForm    : 'cmf.ModifyPortalContent',
        AddForm           : 'cmf.AddPortalContent',
        SchemaAddForm     : 'cmf.AddPortalContent',
    }
    
    permission_fallback = 'zope.Public'

    def execute(self, form, config, context, layer, name, permission, **kw):
        
        if permission is None:
            permission = self.default_permissions.get(form.__class__, self.permission_fallback)

        if issubclass(form, plone.autoform.formbase.AutoExtensibleForm):
            if getattr(form, 'schema', None) is None:
                
                if issubclass(form, (EditForm, Form)):
                    form.schema = context
                else:
                    raise martian.error.GrokImportError(
                        u"The schema form %s must have a 'schema' attribute "
                          "defining a schema interface for the form. If you want "
                          "to set up your fields manually, use a non-schema form "
                          "base class instead." % (form.__name__))
        
        factory = plone.z3cform.layout.wrap_form(form)
        form.__view_name__ = factory.__view_name__ = name
        form.__name__ = factory.__name__ = name
        
        Products.Five.browser.metaconfigure.page(
                config,
                name=name,
                permission=permission,
                for_=context,
                layer=layer,
                class_=factory
            )

        return True
    
__all__ = ('Form', 'SchemaForm', 'AddForm', 'SchemaAddForm', 
            'EditForm', 'SchemaEditForm', 'DisplayForm', 'SchemaDisplayForm')