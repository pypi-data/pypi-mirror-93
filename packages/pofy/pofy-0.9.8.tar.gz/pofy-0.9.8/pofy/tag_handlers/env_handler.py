"""Handler loading environment variables."""
from gettext import gettext as _
from os import environ
from typing import Any

from yaml import ScalarNode

from pofy.common import UNDEFINED
from pofy.interfaces import IBaseField
from pofy.interfaces import ILoadingContext
from pofy.tag_handlers.tag_handler import TagHandler


class EnvHandler(TagHandler):
    """Tag loading YAML values from environment variables.

    Will replace the loaded node by the value of the environment variable.
    """

    tag_pattern = '^env$'

    def load(self, context: ILoadingContext, field: IBaseField) \
            -> Any:
        if not context.expect_scalar(
            _('!env must be set on a string node containing the variable name.')
        ):
            return UNDEFINED

        node = context.current_node()
        var_name = node.value

        if var_name not in environ:
            return UNDEFINED

        fake_node = ScalarNode(
            '',
            environ[var_name],
            node.start_mark,
            node.end_mark
        )

        return context.load(field, fake_node)
