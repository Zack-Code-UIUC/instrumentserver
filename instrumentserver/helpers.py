import inspect
from typing import Dict, Any, List, Union
import html

from qcodes import Instrument, Parameter

from .serialize import toParamDict


def nestedAttributeFromString(root: Any, loc: str) -> Any:
    """return a sub-object. Example::

        >>> nestedAttributeFromString(parent_object, 'foo.bar.spam.bacon')

    returns the object than can be found at parent_object.foo.bar.spam.bacon.
    """
    mods = loc.split('.')
    obj = root
    for m in mods:
        obj = getattr(obj, m)
    return obj


def getInstrumentParameters(ins: Instrument) -> Dict[str, Dict[str, str]]:
    """return the parameters of an instrument.

    :param ins: instrument instance
    :returns: a param dict with entries `unit`, `vals`, for each
        instrument parameter.
    """
    paramDict = toParamDict([ins], includeMeta=['unit', 'vals'])
    for k, v in paramDict.items():
        paramDict[k].pop('value', None)
    return paramDict


def getInstrumentMethods(ins: Instrument) -> Dict[str, Dict[str, Union[str, List[str]]]]:
    """return the methods of an instrument.

    :param ins: instrument instance
    :returns: a dictionary, with keys being the names of methods that are not private
        and not inherited from qcodes.Instrument. Each entry is a dictionary containing:
        - 'parameters': List of string representations of the parameters
        - 'doc': Docstring of the method
        - 'return': string representation of the return type.
    """
    funcs = {}
    for attr_name in dir(ins):
        if attr_name[0] != '_' and attr_name not in dir(Instrument):
            obj = getattr(ins, attr_name)
            if callable(obj) and not isinstance(obj, Parameter):
                funcs[attr_name] = dict()

    for fname in funcs.keys():
        fun = getattr(ins, fname)
        signature = inspect.signature(fun)
        funcs[fname]['parameters'] = [str(signature.parameters[a]) for a in
                                      signature.parameters]
        funcs[fname]['doc'] = str(fun.__doc__)
        funcs[fname]['return'] = str(signature.return_annotation)

    return funcs


def toHtml(obj: Union[Parameter, Instrument]):
    if isinstance(obj, Parameter):
        return parameterToHtml(obj, headerLevel=1)
    else:
        return instrumentToHtml(obj)


def parameterToHtml(param: Parameter, headerLevel=None):
    ret = ""
    if headerLevel is not None:
        ret = f"<h{headerLevel}>{param.name}</h{headerLevel}>"

    ret += f"""
<ul>
    <li><b>Type:</b> {html.escape(str(type(param)))}
    <li><b>Unit:</b> {param.unit}
    <li><b>Validator:</b> {html.escape(str(param.vals))}
    <li><b>Doc:</b> {html.escape(param.__doc__)}
</ul>
    """
    return ret


def instrumentToHtml(ins: Instrument):
    ret = f"""
<h1>{ins.name}</h1>
<ul>
    <li><b>Type:</b> {html.escape(str(type(ins)))}
    <li><b>Doc:</b> {html.escape(str(ins.__doc__))}
</ul>
"""

    ret += """<h2>Parameters:</h2>
<ul>
    """
    for pn in sorted(ins.parameters):
        p = ins.parameters[pn]
        ret += f"<li>{parameterToHtml(p, 2)}</li>"
    ret += "</ul>"

    ret += """<h2>Methods:</h2>
<ul>
"""
    for meth, desc in getInstrumentMethods(ins).items():
        ret += f"""
<li>
    <h3>{meth}</h3>
    <ul>
        <li><b>Call parameters:</b> {html.escape(str(desc['parameters']))}</li>
        <li><b>Return type:</b> {html.escape(str(desc['return']))}</li>
        <li><b>Doc:</b> {html.escape(str(desc['doc']))}</li>
    </ul>
</li>
"""
    ret += "</ul>"

    return ret