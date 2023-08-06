# -*- coding: utf-8 -*-
"""
Render jinja data
"""
# Import local libs
import rend.exc

# Import third party libs
import jinja2
import jinja2.ext


async def render(hub, data):
    """
    Render the given data through Jinja2
    """
    env_args = {"extensions": [], "loader": jinja2.BaseLoader}

    if hasattr(jinja2.ext, "with_"):
        env_args["extensions"].append("jinja2.ext.with_")
    if hasattr(jinja2.ext, "do"):
        env_args["extensions"].append("jinja2.ext.do")
    if hasattr(jinja2.ext, "loopcontrols"):
        env_args["extensions"].append("jinja2.ext.loopcontrols")

    jinja_env = jinja2.Environment(
        undefined=jinja2.StrictUndefined, enable_async=True, **env_args
    )

    if isinstance(data, bytes):
        data = data.decode()

    try:
        template = jinja_env.from_string(data)
        ret = await template.render_async(hub=hub)
    except jinja2.exceptions.UndefinedError as exc:
        raise rend.exc.RenderException(f"Jinja variable {exc.message}")
    except jinja2.exceptions.TemplateSyntaxError as exc:
        raise rend.exc.RenderException(f"Jinja syntax error {exc.message}")
    return ret
