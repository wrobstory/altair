"""
Altair HTML renderer. Uses native vega-lite/vega rendering
"""

import os
import json
import numpy


def render(spec, width=None, height=None):
    """
    Render vega specification to html.

    Uses native vega-lite parser/Vega renderer. Useful for
    rendering visualizations in notebooks.

    Parameters
    ----------
    spec : altair.api.Viz object
        Represents the visualization spec to be rendered to html

    width : int, optional, default=None
        Width in pixels.

    height : int, optional, default=None
        Height in pixels.

    Returns
    -------
    html : str
    """

    from jinja2 import Template, Environment, PackageLoader, escape

    env = Environment(loader=PackageLoader('altair', 'templates'))

    if width is not None:
        spec.vlconfig.width = width
    else:
        width = spec.vlconfig.width
    if height is not None:
        spec.vlconfig.height = height
    else:
        height = spec.vlconfig.height

    template = env.get_template('template.html')
    d = spec.to_dict()

    class NumpyConvert(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, numpy.generic):
                return numpy.asscalar(obj)
            return json.JSONEncoder.default(self, obj)

    spec = escape(json.dumps(d, cls=NumpyConvert))
    fields = {'spec': spec, 'width': width, 'height': height}
    html = template.render(**fields)
    return html

def save(spec, fname, overwrite=False, width=None, height=None):
    """
    Save an html-rendering of a vega specification to a file.

    Parameters
    ----------
    spec : altair.api.Viz object
        Represents the visualization spec to be rendered to html

    fname : str
        Name of file to write to

    overwrite : boolean, optional, default=False
        Whether to overwrite an existing file.
        If false, will raise an error if file already exists.

    width : int, optional, default=None
        Width in pixels.

    height : int, optional, default=None
        Height in pixels.
    """

    if not os.path.splitext(fname)[-1] == '.html':
        fname += '.html'

    exists = os.path.exists(fname)

    if exists is True:
        if overwrite is False:
            raise ValueError("File '%s' exists and overwrite is False" % fname)
        else:
            os.remove(fname)

    blob = render(spec, width, height)

    with open(fname, 'w') as f:
        f.write(blob)
