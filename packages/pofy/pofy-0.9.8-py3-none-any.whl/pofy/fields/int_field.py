"""Integer field class & utilities."""
from gettext import gettext as _
from typing import Any
from typing import Optional
from typing import cast

from pofy.common import ErrorCode
from pofy.common import UNDEFINED
from pofy.fields.base_field import ScalarField
from pofy.fields.base_field import ValidateCallback
from pofy.interfaces import ILoadingContext


class IntField(ScalarField):
    """Integer YAML object field."""

    def __init__(
        self,
        base: int = 0,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        required: bool = False,
        validate: Optional[ValidateCallback] = None,
    ):
        """Initialize int field.

        Args:
            base: Base in which this field is encoded. By default, base is 0,
                  meaning that python will distinguish automatically decimal,
                  octal, and hexadecimal notations from the string.
            minimum: Minimum value for the field. If the value is out of bound,
                     a VALIDATION_ERROR will be raised.
            maximum: Maximum value for the field. If the value is out of bound,
                     a VALIDATION_ERROR will be raised.
            required: See BaseField constructor.
            validate: See BaseField constructor.

        """
        super().__init__(required=required, validate=validate)
        self._base = base
        self._minimum = minimum
        self._maximum = maximum

    def _convert(self, context: ILoadingContext) -> Any:
        node = context.current_node()
        value = node.value
        result: Optional[int] = None

        try:
            result = int(value, self._base)
        except ValueError:
            context.error(
                ErrorCode.VALUE_ERROR,
                _('Can\'t convert "{}" to an integer'), value
            )
            return UNDEFINED

        return cast(Optional[int], ScalarField._check_in_bounds(
            context,
            result,
            self._minimum,
            self._maximum
        ))
