"""
Renderer for Python.
"""
from abc import abstractmethod
from typing import Any, List, Optional

from bitproto._ast import (
    Alias,
    Array,
    Bool,
    BoundDefinition,
    Constant,
    Enum,
    Int,
    Integer,
    Message,
    MessageField,
    SingleType,
)
from bitproto.renderer.block import (
    Block,
    BlockAheadNotice,
    BlockBindAlias,
    BlockBindConstant,
    BlockBindEnum,
    BlockBindEnumField,
    BlockBindMessage,
    BlockBindMessageField,
    BlockBindProto,
    BlockBoundDefinitionDispatcher,
    BlockComposition,
    BlockWrapper,
)
from bitproto.renderer.impls.py.formatter import PyFormatter as F
from bitproto.renderer.renderer import Renderer
from bitproto.utils import cached_property, override


class BlockProtoDocstring(BlockBindProto[F]):
    @override(Block)
    def render(self) -> None:
        self.push_definition_docstring()


class BlockGeneralImports(Block[F]):
    @override(Block)
    def render(self) -> None:
        self.push("import json")
        self.push("from dataclasses import dataclass, field")
        self.push("from typing import ClassVar, Dict, List")
        self.push_empty_line()
        self.push("from bitprotolib import bp")


class BlockImportChildProto(BlockBindProto[F]):
    @override(Block)
    def render(self) -> None:
        statement = self.formatter.format_import_statement(self.d, as_name=self.name)
        self.push(statement)


class BlockImportChildProtoList(BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block]:
        return [
            BlockImportChildProto(proto, name=name)
            for name, proto in self.bound.protos(recursive=False)
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n"


class BlockImportList(BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block]:
        return [
            BlockGeneralImports(),
            BlockImportChildProtoList(),
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n\n"


class BlockAliasMethodProcessor(BlockBindAlias[F]):
    @override(Block)
    def render(self) -> None:
        processor_name = self.formatter.format_processor_name_alias(self.d)
        to = self.formatter.format_processor(self.d.type)
        self.push(f"def {processor_name}() -> bp.Processor:")
        self.push(f"return bp.AliasProcessor({to})", indent=4)


class BlockAliasMethodDefaultFactory(BlockBindAlias[F]):
    @override(Block)
    def render(self) -> None:
        factory_name = self.formatter.formart_default_factory_alias(self.d)
        alias_type = self.formatter.format_alias_type(self.d)
        default_value = self.formatter.format_default_value(self.d.type)
        self.push(f"def {factory_name}() -> {alias_type}:")
        self.push(f"return {default_value}", indent=4)


class BlockAliasDef(BlockBindAlias[F]):
    @override(Block)
    def render(self) -> None:
        self.push_definition_comments()
        self.push(f"{self.alias_name} = {self.aliased_type}")
        self.push_typing_hint_inline_comment()


class BlockAlias(BlockBindAlias[F], BlockComposition):
    @override(BlockComposition)
    def blocks(self) -> List[Block]:
        return [
            BlockAliasDef(self.d),
            BlockAliasMethodProcessor(self.d),
            BlockAliasMethodDefaultFactory(self.d),
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n\n"


class BlockConstant(BlockBindConstant[F]):
    @override(Block)
    def render(self) -> None:
        self.push_definition_comments()
        self.push(
            f"{self.constant_name}: {self.constant_value_type} = {self.constant_value}"
        )


class BlockEnumField(BlockBindEnumField[F]):
    @override(Block)
    def render(self) -> None:
        self.push_definition_comments()
        self.push(
            f"{self.enum_field_name}: {self.enum_field_type} = {self.enum_field_value}"
        )


class BlockEnumFieldList(BlockBindEnum[F], BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block]:
        return [BlockEnumField(field) for field in self.d.fields()]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n"


class BlockEnumFieldListWrapper(BlockBindEnum[F], BlockWrapper[F]):
    @override(BlockWrapper)
    def wraps(self) -> Block:
        return BlockEnumFieldList(self.d)

    @override(BlockWrapper)
    def before(self) -> None:
        self.render_enum_type()

    def render_enum_type(self) -> None:
        self.push_definition_comments()
        self.push(f"{self.enum_name} = int")
        self.push_typing_hint_inline_comment()


class BlockEnumValueToNameMapItem(BlockBindEnumField[F]):
    @override(Block)
    def render(self) -> None:
        self.push(f'{self.enum_field_value}: "{self.enum_field_name}",')


class BlockEnumValueToNameMapItemList(BlockBindEnum[F], BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block]:
        return [
            BlockEnumValueToNameMapItem(field, indent=4) for field in self.d.fields()
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n"


class BlockEnumValueToNameMap(BlockBindEnum[F], BlockWrapper[F]):
    @override(BlockWrapper)
    def wraps(self) -> Block:
        return BlockEnumValueToNameMapItemList(self.d)

    @override(BlockWrapper)
    def before(self) -> None:
        map_name = self.formatter.format_enum_value_to_name_map_name(self.d)
        self.push(f"{map_name}: Dict[{self.enum_name}, str] = {{")

    @override(BlockWrapper)
    def after(self) -> None:
        self.push("}")


class BlockEnumMethodProcessor(BlockBindEnum[F]):
    @override(Block)
    def render(self) -> None:
        processor_name = self.formatter.format_processor_name_enum(self.d)
        ut = self.formatter.format_processor_uint(self.d.type)
        self.push(f"def {processor_name}() -> bp.Processor:")
        self.push(f"return bp.EnumProcessor({ut})", indent=4)


class BlockEnum(BlockBindEnum[F], BlockComposition[F]):
    @override(BlockComposition[F])
    def blocks(self) -> List[Block]:
        return [
            BlockEnumFieldListWrapper(self.d),
            BlockEnumValueToNameMap(self.d),
            BlockEnumMethodProcessor(self.d),
        ]


class BlockMessageField(BlockBindMessageField[F]):
    @cached_property
    def message_field_default_value(self) -> str:
        return self.formatter.format_field_default_value(self.d.type)

    @override(Block)
    def render(self) -> None:
        self.push_definition_comments()
        self.push(
            f"{self.message_field_name}: {self.message_field_type} = {self.message_field_default_value}"
        )
        self.push_typing_hint_inline_comment()


class BlockMessageBase(BlockBindMessage[F]):
    @override(BlockBindMessage)
    @cached_property
    def message_size_constant_name(self) -> str:
        return "BYTES_LENGTH"


class BlockMessageSize(BlockMessageBase):
    @override(Block)
    def render(self) -> None:
        self.push_comment(f"Number of bytes to serialize class {self.message_name}")
        self.push(
            f"{self.message_size_constant_name}: ClassVar[int] = {self.message_nbytes}"
        )


class BlockMessageFieldList(BlockMessageBase, BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block]:
        return [
            BlockMessageField(field, indent=self.indent)
            for field in self.d.sorted_fields()
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n"


class BlockMessageClassDefs(BlockMessageBase, BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block]:
        return [
            BlockMessageSize(self.d, indent=self.indent),
            BlockMessageFieldList(self.d, indent=self.indent),
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n\n"


class BlockMessageClass(BlockMessageBase, BlockWrapper[F]):
    @override(BlockWrapper)
    def wraps(self) -> Block[F]:
        return BlockMessageClassDefs(self.d, indent=4)

    @override(BlockWrapper)
    def before(self) -> None:
        self.push("@dataclass")
        self.push(f"class {self.message_name}(bp.MessageBase):")
        self.push_definition_docstring(indent=4)


class BlockMessageMethodProcessorFieldItem(BlockBindMessageField[F]):
    @override(Block)
    def render(self) -> None:
        type_processor = self.formatter.format_processor(self.d.type)
        field_number = self.formatter.format_int_value(self.d.number)
        self.push(f"bp.MessageFieldProcessor({field_number}, {type_processor}),")


class BlockMessageMethodProcessorFieldList(BlockMessageBase, BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block[F]]:
        return [
            BlockMessageMethodProcessorFieldItem(d, indent=self.indent)
            for d in self.d.sorted_fields()
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n"


class BlockMessageMethodProcessor(BlockMessageBase, BlockWrapper[F]):
    @override(BlockWrapper)
    def wraps(self) -> Block[F]:
        return BlockMessageMethodProcessorFieldList(self.d, indent=self.indent + 8)

    @override(BlockWrapper)
    def before(self) -> None:
        self.push("def bp_processor(self) -> bp.Processor:")
        self.push("field_processors: List[bp.Processor] = [", indent=self.indent + 4)

    @override(BlockWrapper)
    def after(self) -> None:
        extensible = self.formatter.format_bool_value(self.d.extensible)
        nbits = self.formatter.format_int_value(self.d.nbits())

        if self.d.nfields() == 0:
            self.push_string("]", separator="")
        else:
            self.push("]", indent=self.indent + 4)
        self.push(
            f"return bp.MessageProcessor({extensible}, {nbits}, field_processors)",
            indent=self.indent + 4,
        )


class BlockMessageMethodGetSetByteItemBase(BlockBindMessageField[F]):
    def __init__(
        self,
        *args: Any,
        **kwds: Any,
    ) -> None:
        super().__init__(*args, **kwds)
        self.array_depth: int = 0

    def format_data_ref(self) -> str:
        array_indexing = "".join(f"[di.i({i})]" for i in range(self.array_depth))
        return f"self.{self.message_field_name}" + array_indexing

    def render_case(self) -> None:
        field_number = self.formatter.format_int_value(self.d.number)
        self.push(f"if di.field_number == {field_number}:")

    @abstractmethod
    def render_single(self, single: SingleType) -> None:
        raise NotImplementedError

    def render_array(self, array: Array) -> None:
        try:
            self.array_depth += 1
            if isinstance(array.element_type, SingleType):
                return self.render_single(array.element_type)
            if isinstance(array.element_type, Alias):
                return self.render_alias(array.element_type)
        finally:
            self.array_depth -= 1

    def render_alias(self, alias: Alias) -> None:
        if isinstance(alias.type, SingleType):
            return self.render_single(alias.type)
        if isinstance(alias.type, Array):
            return self.render_array(alias.type)

    @override(Block)
    def render(self) -> None:
        if isinstance(self.d.type, SingleType):
            return self.render_single(self.d.type)
        if isinstance(self.d.type, Array):
            return self.render_array(self.d.type)
        if isinstance(self.d.type, Alias):
            return self.render_alias(self.d.type)


class BlockMessageMethodSetByteItem(BlockMessageMethodGetSetByteItemBase):
    @override(BlockMessageMethodGetSetByteItemBase)
    def render_single(self, single: SingleType) -> None:
        left = self.format_data_ref()
        assign = "|="
        type_name = self.formatter.format_type(single)
        shift = "<< lshift"
        caster = ""

        if isinstance(single, Bool):
            assign = "="
            type_name = "bool"
            shift = ""
        if isinstance(single, Int):
            # Cast to signed-int if overflows
            # Python dosen't have a type for int8, int16..
            caster = "bp.int{}".format(self.formatter.get_nbits_of_integer(single))

        right = value = f"{type_name}(b)"

        if shift:
            right = f"({value} {shift})"

        self.render_case()

        if caster:
            self.push(f"{left} {assign} {caster}({right})", indent=self.indent + 4)
        else:
            self.push(f"{left} {assign} {right}", indent=self.indent + 4)


class BlockMessageMethodSetByteItemDefault(Block[F]):
    @override(Block)
    def render(self) -> None:
        self.push(f"return")


class BlockMessageMethodSetByteItemList(BlockMessageBase, BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block[F]]:
        b: List[Block[F]] = [
            BlockMessageMethodSetByteItem(field, indent=self.indent)
            for field in self.d.sorted_fields()
        ]
        b.append(BlockMessageMethodSetByteItemDefault(indent=self.indent))
        return b

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n"


class BlockMessageMethodSetByte(BlockBindMessage[F], BlockWrapper[F]):
    @override(BlockWrapper)
    def wraps(self) -> Block[F]:
        return BlockMessageMethodSetByteItemList(self.d, indent=self.indent + 4)

    @override(BlockWrapper)
    def before(self) -> None:
        self.push(
            f"def bp_set_byte(self, di: bp.DataIndexer, lshift: int, b: bp.byte) -> None:"
        )


class BlockMessageMethodGetByteItem(BlockMessageMethodGetSetByteItemBase):
    @override(BlockMessageMethodGetSetByteItemBase)
    def render_single(self, single: SingleType) -> None:
        shift = ">> rshift"
        value = data = self.format_data_ref()

        if isinstance(single, Bool):
            value = f"int({data})"

        self.render_case()
        self.push(f"return ({value} {shift}) & 255", indent=self.indent + 4)


class BlockMessageMethodGetByteItemDefault(Block[F]):
    @override(Block)
    def render(self) -> None:
        self.push(f"return bp.byte(0)  # Won't reached")


class BlockMessageMethodGetByteItemList(BlockMessageBase, BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block[F]]:
        b: List[Block[F]] = [
            BlockMessageMethodGetByteItem(field, indent=self.indent)
            for field in self.d.sorted_fields()
        ]
        b.append(BlockMessageMethodGetByteItemDefault(indent=self.indent))
        return b

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n"


class BlockMessageMethodGetByte(BlockMessageBase, BlockWrapper[F]):
    @override(BlockWrapper)
    def wraps(self) -> Block[F]:
        return BlockMessageMethodGetByteItemList(self.d, indent=self.indent + 4)

    @override(BlockWrapper)
    def before(self) -> None:
        self.push(f"def bp_get_byte(self, di: bp.DataIndexer, rshift: int) -> bp.byte:")


class BlockMessageMethodGetAccessorItem(BlockBindMessageField[F]):
    def __init__(
        self,
        *args: Any,
        **kwds: Any,
    ) -> None:
        super().__init__(*args, **kwds)
        self.array_depth: int = 0

    def format_data_ref(self) -> str:
        array_indexing = "".join(f"[di.i({i})]" for i in range(self.array_depth))
        return f"self.{self.message_field_name}" + array_indexing

    def render_case(self) -> None:
        field_number = self.formatter.format_int_value(self.d.number)
        self.push(f"if di.field_number == {field_number}:")

    def render_array(self, array: Array) -> None:
        try:
            self.array_depth += 1
            if isinstance(array.element_type, Message):
                return self.render_message(array.element_type)
            if isinstance(array.element_type, Alias):
                return self.render_alias(array.element_type)
        finally:
            self.array_depth -= 1

    def render_alias(self, alias: Alias) -> None:
        if isinstance(alias.type, Array):
            return self.render_array(alias.type)

    def render_message(self, message: Message) -> None:
        self.render_case()
        data = self.format_data_ref()
        self.push(f"return {data}", indent=self.indent + 4)

    @override(Block)
    def render(self) -> None:
        if isinstance(self.d.type, Message):
            return self.render_message(self.d.type)
        if isinstance(self.d.type, Array):
            return self.render_array(self.d.type)
        if isinstance(self.d.type, Alias):
            return self.render_alias(self.d.type)


class BlockMessageMethodGetAccessorItemDefault(Block[F]):
    @override(Block)
    def render(self) -> None:
        self.push(f"return bp.NilAccessor() # Won't reached")


class BlockMessageMethodGetAccessorList(BlockBindMessage[F], BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block[F]]:
        b: List[Block[F]] = [
            BlockMessageMethodGetAccessorItem(field, indent=self.indent)
            for field in self.d.sorted_fields()
        ]
        b.append(BlockMessageMethodGetAccessorItemDefault(indent=self.indent))
        return b

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n"


class BlockMessageMethodGetAccessor(BlockMessageBase, BlockWrapper[F]):
    @override(BlockWrapper)
    def wraps(self) -> Block[F]:
        return BlockMessageMethodGetAccessorList(self.d, indent=self.indent + 4)

    @override(BlockWrapper)
    def before(self) -> None:
        self.push(f"def bp_get_accessor(self, di: bp.DataIndexer) -> bp.Accessor:")


class BlockMessageMethodEncode(BlockMessageBase):
    @override(Block)
    def render(self) -> None:
        self.push(f"def encode(self) -> bytearray:")
        self.push_docstring("Encode this object to bytearray.", indent=self.indent + 4)
        self.push(f"s = bytearray(self.BYTES_LENGTH)", indent=self.indent + 4)
        self.push(f"ctx = bp.ProcessContext(True, s)", indent=self.indent + 4)
        self.push(
            f"self.bp_processor().process(ctx, bp.NIL_DATA_INDEXER, self)",
            indent=self.indent + 4,
        )
        self.push(f"return ctx.s", indent=self.indent + 4)


class BlockMessageMethodDecode(BlockMessageBase):
    @override(Block)
    def render(self) -> None:
        self.push(f"def decode(self, s: bytearray) -> None:")
        self.push_docstring(
            "Decode given bytearray s to this object.",
            ":param s: A bytearray with length at least `BYTES_LENGTH`.",
            indent=self.indent + 4,
        )
        self.push(
            f"assert len(s) >= self.BYTES_LENGTH, bp.NotEnoughBytes()",
            indent=self.indent + 4,
        )
        self.push(f"ctx = bp.ProcessContext(False, s)", indent=self.indent + 4)
        self.push(
            f"self.bp_processor().process(ctx, bp.NIL_DATA_INDEXER, self)",
            indent=self.indent + 4,
        )


class BlockMessage(BlockMessageBase, BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block[F]]:
        return [
            BlockMessageClass(self.d),
            BlockMessageMethodProcessor(self.d, indent=4),
            BlockMessageMethodSetByte(self.d, indent=4),
            BlockMessageMethodGetByte(self.d, indent=4),
            BlockMessageMethodGetAccessor(self.d, indent=4),
            BlockMessageMethodEncode(self.d, indent=4),
            BlockMessageMethodDecode(self.d, indent=4),
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n\n"


class BlockBoundDefinitionList(BlockBoundDefinitionDispatcher):
    @override(BlockBoundDefinitionDispatcher)
    def dispatch(self, d: BoundDefinition) -> Optional[Block[F]]:
        if isinstance(d, Alias):
            return BlockAlias(d)
        if isinstance(d, Constant):
            return BlockConstant(d)
        if isinstance(d, Enum):
            return BlockEnum(d)
        if isinstance(d, Message):
            return BlockMessage(d)
        return None

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n\n\n"


class BlockList(BlockComposition[F]):
    @override(BlockComposition)
    def blocks(self) -> List[Block[F]]:
        return [
            BlockAheadNotice(),
            BlockProtoDocstring(self.bound),
            BlockImportList(),
            BlockBoundDefinitionList(),
        ]

    @override(BlockComposition)
    def separator(self) -> str:
        return "\n\n\n"


class RendererPy(Renderer[F]):
    """Renderer for Python language."""

    @override(Renderer)
    def language_name(self) -> str:
        return "py"

    @override(Renderer)
    def file_extension(self) -> str:
        return ".py"

    @override(Renderer)
    def formatter(self) -> F:
        return F()

    @override(Renderer)
    def block(self) -> Block[F]:
        return BlockList()
