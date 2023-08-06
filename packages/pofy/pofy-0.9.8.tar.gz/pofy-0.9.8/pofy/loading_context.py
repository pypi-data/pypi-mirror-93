"""Loading context class & utilities."""
from gettext import gettext as _
from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type

from yaml import MappingNode
from yaml import Node
from yaml import ScalarNode
from yaml import SequenceNode

from pofy.common import ErrorCode
from pofy.common import SchemaResolver
from pofy.common import default_schema_resolver
from pofy.common import get_exception_type
from pofy.interfaces import IBaseField
from pofy.interfaces import ILoadingContext
from pofy.tag_handlers.tag_handler import TagHandler

ErrorHandler = Optional[Callable[[Node, ErrorCode, str], Any]]
NodeStack = List[Tuple[Node, Optional[str]]]


class LoadingContext(ILoadingContext):
    """Context aggregating resolve & error reporting functions."""

    def __init__(
        self,
        error_handler: ErrorHandler,
        tag_handlers: Iterable[TagHandler],
        flags: Optional[Set[str]] = None,
        schema_resolver: Optional[SchemaResolver] = None
    ):
        """Initialize context."""
        self._error_handler = error_handler
        self._tag_handlers = list(tag_handlers)
        self._node_stack: NodeStack = []
        self._flags = flags if flags is not None else set()
        if schema_resolver is not None:
            self._schema_resolver = schema_resolver
        else:
            self._schema_resolver = default_schema_resolver

    def load(
        self,
        field: IBaseField,
        node: Node,
        location: Optional[str] = None
    ) -> Any:
        """Push a node in the context.

        This is solely used to know which node is currently loaded when calling
        error function, to avoid having to pass around node objects.

        Args:
            field: Field describing this node.
            node: Currently loaded node.
            location: The path from which this node was loaded. Every node
                       pushed subsequently will be considered having the
                       same path, except until another child path is pushed.

        """
        if len(self._node_stack) > 0:
            assert self._node_stack[-1][0] != node

        self._node_stack.append((node, location))

        try:
            tag_handler = self._get_tag_handler(node)
            if tag_handler is not None:
                result = tag_handler.load(self, field)
            else:
                result = field.load(self)
        finally:
            self._node_stack.pop()

        return result

    def is_defined(self, flag: str) -> bool:
        return flag in self._flags

    def get_schema_resolver(self) -> SchemaResolver:
        return self._schema_resolver

    def current_node(self) -> Node:
        """Return the currently loaded node."""
        nodes = self._node_stack
        assert len(nodes) > 0
        return nodes[-1][0]

    def current_location(self) -> Optional[str]:
        """Return the location of the document owning the current node.

        If no path can be found, returs None.
        """
        for __, location in reversed(self._node_stack):
            if location is not None:
                return location

        return None

    def expect_scalar(self, message: Optional[str] = None) -> bool:
        """Return false and raise an error if the current node isn't scalar."""
        if message is None:
            message = _('Expected a scalar value.')
        return self._expect_node(
            ScalarNode,
            message
        )

    def expect_sequence(self) -> bool:
        """Return false and raise if the current node isn't a sequence."""
        return self._expect_node(
            SequenceNode,
            _('Expected a sequence value.')
        )

    def expect_mapping(self) -> bool:
        """Return false and raise if the current node isn't a mapping."""
        return self._expect_node(
            MappingNode,
            _('Expected a mapping value.')
        )

    def error(
        self,
        code: ErrorCode,
        message_format: str,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Register an error in the current loading context.

        If errors occured in the scope of a context, an error will be raised
        at the end of the object loading.

        Args:
            code: Code of the error.
            message_format: The error message format.
            *args, **kwargs: Arguments used to format message.

        """
        assert len(self._node_stack) > 0
        node, __ = self._node_stack[-1]
        message = message_format.format(*args, **kwargs)
        if self._error_handler is not None:
            self._error_handler(node, code, message)
        else:
            exception_type = get_exception_type(code)
            raise exception_type(node, message)

    def _expect_node(
        self,
        node_type: Type[Node],
        error_format: str,
        *args: Any,
        **kwargs: Any
    ) -> bool:
        current_node = self.current_node()
        if not isinstance(current_node, node_type):
            self.error(
                ErrorCode.UNEXPECTED_NODE_TYPE,
                error_format,
                *args,
                **kwargs
            )
            return False

        return True

    def _get_tag_handler(self, node: Node) -> Optional[TagHandler]:
        tag = node.tag
        if not tag.startswith('!'):
            return None

        found_handler = None
        for handler in self._tag_handlers:
            if not handler.match(node):
                continue

            if found_handler is not None:
                self.error(
                    ErrorCode.MULTIPLE_MATCHING_HANDLERS,
                    _('Got multiple matching handlers for tag {}'), tag
                )
                continue

            found_handler = handler

        return found_handler
