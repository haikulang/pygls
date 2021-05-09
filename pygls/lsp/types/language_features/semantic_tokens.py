import enum
from typing import Optional, Union
from pygls.lsp.types import (TextDocumentIdentifier)
from pygls.lsp.types.basic_structures import (Model, NumType, PartialResultParams, Range,
                                              TextDocumentRegistrationOptions, WorkDoneProgressParams,
                                              StaticRegistrationOptions, WorkDoneProgressOptions)


class SemanticTokenTypes(str, enum.Enum):
    """
    Represents a generic type. Acts as a fallback for types which
    can't be mapped to a specific type like class or enum.
    """
    Namespace = 'namespace'
    Type = 'type'
    Class = 'class'
    Enum = 'enum'
    Interface = 'interface'
    Struct = 'struct'
    TypeParameter = 'typeParameter'
    Parameter = 'parameter'
    Variable = 'variable'
    Property = 'property'
    EnumMember = 'enumMember'
    Event = 'event'
    Function = 'function'
    Method = 'method'
    Macro = 'macro'
    Keyword = 'keyword'
    Modifier = 'modifier'
    Comment = 'comment'
    String = 'string'
    Number = 'number'
    Regexp = 'regexp'
    Operator = 'operator'


class SemanticTokenModifiers(str, enum.Enum):
    Declaration = 'declaration'
    Definition = 'definition'
    Readonly = 'readonly'
    Static = 'static'
    Deprecated = 'deprecated'
    Abstract = 'abstract'
    Async = 'async'
    Modification = 'modification'
    Documentation = 'documentation'
    DefaultLibrary = 'defaultLibrary'


class SemanticTokensLegend(Model):
    tokenTypes: list[str]
    tokenModifiers: list[str]


class SemanticTokenRequestsFull(Model):
    delta: Optional[bool] = False


class SemanticTokenRequests(Model):
    range: Optional[bool] = False
    full: Optional[Union[bool, SemanticTokenRequestsFull]] = False


class SemanticTokensClientCapabilities(Model):
    dynamicRegistration: Optional[bool] = False
    requests: SemanticTokenRequests = None
    tokenTypes: list[str]
    tokenModifiers: list[str]
    formats: list[str]
    overlappingTokenSupport: bool = False
    multilineTokenSupport: bool = False


class SemanticTokensOptions(WorkDoneProgressOptions):
    legend: SemanticTokensLegend = None
    range: Optional[bool]
    full: Optional[Union[dict[str, bool], bool]] = False


class SemanticTokensRegistrationOptions(TextDocumentRegistrationOptions, SemanticTokensOptions,
                                        StaticRegistrationOptions):
    ...


class SemanticTokensParams(WorkDoneProgressParams, PartialResultParams):
    textDocument: TextDocumentIdentifier


class SemanticTokens(Model):
    result_id: Optional[str] = None
    data: list[int]


class SemanticTokensPartialResult(Model):
    data: list[int]


class SemanticTokensDeltaParams(WorkDoneProgressParams, PartialResultParams):
    textDocument: TextDocumentIdentifier = None
    previousResultId: str = None


class SemanticTokensEdit(Model):
    start: int = None
    deleteCount: int = None
    data: Optional[list[int]] = None


class SemanticTokensDelta(Model):
    resultId: Optional[str] = None
    edits: list[SemanticTokensEdit]


class SemanticTokensDeltaPartialResult(Model):
    edits: list[SemanticTokensEdit]


class SemanticTokensRangeParams(WorkDoneProgressParams, PartialResultParams):
    textDocument: TextDocumentIdentifier = None
    range: Range = None


class SemanticTokensWorkspaceClientCapabilities(Model):
    refreshSupport: Optional[bool] = False
