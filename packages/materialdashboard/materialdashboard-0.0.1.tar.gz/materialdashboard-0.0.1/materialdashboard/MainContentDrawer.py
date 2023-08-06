# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MainContentDrawer(Component):
    """A MainContentDrawer component.
A component adding a drawer and nesting the main page content.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The main content for the page.
- id (string; optional): The ID of the component.
- open (boolean; default True): Whether the drawer is open.
- pages (dict; optional): The list of pages, as dictionary elements:
{"value": "pageId", "label": "Displayed title"}. pages has the following type: list of dicts containing keys 'value', 'label'.
Those keys have the following types:
  - value (string; required)
  - label (string; required)
- persistence (boolean | string | number; optional): Used to allow user interactions in this component to be persisted when
the component - or the page - is refreshed. If `persisted` is truthy and
hasn't changed from its previous value, a `value` that the user has
changed while using the app will keep that change, as long as
the new `value` also matches what was given originally.
Used in conjunction with `persistence_type`.
- persisted_props (list of a value equal to: 'value's; default ['value']): Properties whose user interactions will persist after refreshing the
component or the page. Since only `value` is allowed this prop can
normally be ignored.
- persistence_type (a value equal to: 'local', 'session', 'memory', 'location'; default 'local'): Where persisted user changes will be stored:
memory: only kept in memory, reset on page refresh.
local: window.localStorage, data is kept after the browser quit.
session: window.sessionStorage, data is cleared once the browser quit.
location: window.location, data appears in the URL and can be shared with others.
- value (string; optional): The ID of the currently selected page."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, open=Component.UNDEFINED, pages=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, value=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'open', 'pages', 'persistence', 'persisted_props', 'persistence_type', 'value']
        self._type = 'MainContentDrawer'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'open', 'pages', 'persistence', 'persisted_props', 'persistence_type', 'value']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(MainContentDrawer, self).__init__(children=children, **args)
