# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TopAppBar(Component):
    """A TopAppBar component.
An app bar at the top of the screen.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): Content on the right of the app bar.
- id (string; optional): The ID used to identify this component in Dash callbacks.
- n_menu_clicks (number; default 0): Clicks made on the menu button.
- title (string; optional): A title displayed at the top of the dashboard."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, n_menu_clicks=Component.UNDEFINED, title=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'n_menu_clicks', 'title']
        self._type = 'TopAppBar'
        self._namespace = 'materialdashboard'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'n_menu_clicks', 'title']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TopAppBar, self).__init__(children=children, **args)
