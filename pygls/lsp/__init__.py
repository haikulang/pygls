############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
from typing import Any, List, Union

from pygls.exceptions import MethodTypeNotRegisteredError
from pygls.lsp.methods import *
from pygls.lsp.types import *
from typeguard import check_type

__LSP_VERSION__ = "3.15"

# Holds lsp methods and their appropriate types. It is used for type-checking.
# {
#   'COMPLETION': (CompletionOptions, CompletionParams, Union[List[CompletionItem], CompletionList, None])
# }
# where:
#   - CompletionOptions is used when registering a method:
#   - CompletionParams are received from the client
#   - Union[List[CompletionItem], CompletionList, None] should be returned by the server (result field of ResponseMessage)
#
#       @json_server.feature(COMPLETION, CompletionOptions(trigger_characters=[',']))
#       def completions(params: CompletionParams = None) -> Union[List[CompletionItem], CompletionList, None]:
#           """Returns completion items."""

# TODO: support partial-results types
LSP_METHODS_MAP = {
    # General messages
    INITIALIZE: (None, InitializeParams, InitializeResult, ),
    INITIALIZED: (None, InitializedParams, None, ),
    SHUTDOWN: (None, None, None, ),
    EXIT: (None, None, None, ),
    # Window
    WINDOW_SHOW_MESSAGE: (None, None, ShowMessageParams, ),
    WINDOW_SHOW_MESSAGE_REQUEST: (None, None, ShowMessageRequestParams, ),
    WINDOW_LOG_MESSAGE: (None, None, LogMessageParams, ),
    WINDOW_WORK_DONE_PROGRESS_CREATE: (None, None, WorkDoneProgressCreateParams, ),
    WINDOW_WORK_DONE_PROGRESS_CANCEL: (None, None, WorkDoneProgressCancelParams, ),
    # Telemetry
    TELEMETRY_EVENT: (None, None, Any, ),
    # Client - (un)register capabilities
    CLIENT_REGISTER_CAPABILITY: (None, None, RegistrationParams, ),
    CLIENT_UNREGISTER_CAPABILITY: (None, None, UnregistrationParams, ),
    # Workspace
    WORKSPACE_FOLDERS: (None, Optional[List[WorkspaceFolder]], None, ),
    WORKSPACE_DID_CHANGE_WORKSPACE_FOLDERS: (None, DidChangeWorkspaceFoldersParams, None, ),
    WORKSPACE_DID_CHANGE_CONFIGURATION: (None, DidChangeConfigurationParams, None, ),
    WORKSPACE_CONFIGURATION: (None, List[Any], ConfigurationParams, ),
    WORKSPACE_DID_CHANGE_WATCHED_FILES: (None, DidChangeWatchedFilesParams, None, ),
    WORKSPACE_SYMBOL: (None, WorkspaceSymbolParams, Optional[List[SymbolInformation]], ),
    WORKSPACE_EXECUTE_COMMAND: (None, ExecuteCommandParams, Optional[Any], ),
    WORKSPACE_APPLY_EDIT: (None, ApplyWorkspaceEditResponse, ApplyWorkspaceEditParams, ),
    # Text Document Synchronization
    TEXT_DOCUMENT_DID_OPEN: (None, DidOpenTextDocumentParams, None, ),
    TEXT_DOCUMENT_DID_CHANGE: (None, DidChangeTextDocumentParams, None, ),
    TEXT_DOCUMENT_WILL_SAVE: (None, WillSaveTextDocumentParams, None, ),
    TEXT_DOCUMENT_WILL_SAVE_WAIT_UNTIL: (None, WillSaveTextDocumentParams, None, ),
    TEXT_DOCUMENT_DID_SAVE: (
        TextDocumentSaveRegistrationOptions,
        DidSaveTextDocumentParams,
        None,
    ),
    TEXT_DOCUMENT_DID_CLOSE: (None, DidCloseTextDocumentParams, None, ),
    # Diagnostics notification
    TEXT_DOCUMENT_PUBLISH_DIAGNOSTICS: (None, None, PublishDiagnosticsParams, ),
    # Language features
    COMPLETION: (
        CompletionOptions,
        CompletionParams,
        Union[List[CompletionItem], CompletionList, None],
    ),
    COMPLETION_ITEM_RESOLVE: (
        None,
        CompletionItem,
        CompletionItem,
    ),
    HOVER: (
        HoverOptions,
        HoverParams,
        Optional[Hover],
    ),
    SIGNATURE_HELP: (
        SignatureHelpOptions,
        SignatureHelpParams,
        Optional[SignatureHelp],
    ),
    DECLARATION: (
        DeclarationOptions,
        DeclarationParams,
        Union[Location, List[Location], List[LocationLink], None],
    ),
    DEFINITION: (
        DefinitionOptions,
        DefinitionParams,
        Union[Location, List[Location], List[LocationLink], None],
    ),
    TYPE_DEFINITION: (
        TypeDefinitionOptions,
        TypeDefinitionParams,
        Union[Location, List[Location], List[LocationLink], None],
    ),
    IMPLEMENTATION: (
        ImplementationOptions,
        ImplementationParams,
        Union[Location, List[Location], List[LocationLink], None],
    ),
    REFERENCES: (
        ReferenceOptions,
        ReferenceParams,
        Optional[List[Location]],
    ),
    DOCUMENT_HIGHLIGHT: (
        DocumentHighlightOptions,
        DocumentHighlightParams,
        Optional[List[DocumentHighlight]],
    ),
    DOCUMENT_SYMBOL: (
        DocumentSymbolOptions,
        DocumentSymbolParams,
        Union[List[DocumentSymbol], List[SymbolInformation], None],
    ),
    CODE_ACTION: (
        Union[CodeActionOptions, TextDocumentRegistrationOptions],
        CodeActionParams,
        Optional[List[Union[Command, CodeAction]]],
    ),
    CODE_LENS: (
        CodeLensOptions,
        CodeLensParams,
        Optional[List[CodeLens]],
    ),
    CODE_LENS_RESOLVE: (
        None,
        CodeLens,
        CodeLens,
    ),
    DOCUMENT_LINK: (
        DocumentLinkOptions,
        DocumentLinkParams,
        Optional[List[DocumentLink]],
    ),
    DOCUMENT_LINK_RESOLVE: (
        None,
        DocumentLink,
        DocumentLink,
    ),
    DOCUMENT_COLOR: (
        DocumentColorOptions,
        DocumentColorParams,
        List[ColorInformation],
    ),
    COLOR_PRESENTATION: (
        None,
        ColorPresentationParams,
        List[ColorPresentation],
    ),
    FORMATTING: (
        DocumentFormattingOptions,
        DocumentFormattingParams,
        Optional[List[TextEdit]],
    ),
    RANGE_FORMATTING: (
        DocumentRangeFormattingOptions,
        DocumentRangeFormattingParams,
        Optional[List[TextEdit]],
    ),
    ON_TYPE_FORMATTING: (
        DocumentOnTypeFormattingOptions,
        DocumentOnTypeFormattingParams,
        Optional[List[TextEdit]],
    ),
    RENAME: (
        RenameOptions,
        RenameParams,
        Optional[WorkspaceEdit],
    ),
    PREPARE_RENAME: (
        None,
        PrepareRenameParams,
        Union[Range, PrepareRename, None],
    ),
    FOLDING_RANGE: (
        FoldingRangeOptions,
        FoldingRangeParams,
        Optional[List[FoldingRange]],
    ),
    SELECTION_RANGE: (
        SelectionRangeOptions,
        SelectionRangeParams,
        Optional[List[SelectionRange]],
    ),
    DOCUMENT_SEMANTIC_TOKENS_FULL: (
        SemanticTokensOptions,
        SemanticTokensParams,
        Optional[Union[SemanticTokens, SemanticTokensPartialResult]],
    ),
    DOCUMENT_SEMANTIC_TOKENS_FULL_DELTA: (
        SemanticTokensOptions,
        SemanticTokensDeltaParams,
        Optional[Union[SemanticTokens, SemanticTokensDelta, SemanticTokensDeltaPartialResult]],
    ),
    DOCUMENT_SEMANTIC_TOKENS_RANGE: (
        SemanticTokensOptions,
        SemanticTokensRangeParams,
        Optional[Union[SemanticTokensDelta, SemanticTokensPartialResult]],
    ),
}


def get_method_registration_options_type(method_name, lsp_methods_map=LSP_METHODS_MAP):
    try:
        return lsp_methods_map[method_name][0]
    except KeyError:
        raise MethodTypeNotRegisteredError(method_name)


def get_method_params_type(method_name, lsp_methods_map=LSP_METHODS_MAP):
    try:
        return lsp_methods_map[method_name][1]
    except KeyError:
        raise MethodTypeNotRegisteredError(method_name)


def get_method_return_type(method_name, lsp_methods_map=LSP_METHODS_MAP):
    try:
        return lsp_methods_map[method_name][2]
    except KeyError:
        raise MethodTypeNotRegisteredError(method_name)


def _get_origin(t):
    try:
        return t.__origin__
    except AttributeError:
        return None


def _get_args(t):
    try:
        return t.__args__
    except AttributeError:
        return None


def is_instance(o, t):
    try:
        check_type('', o, t)
        return True
    except TypeError:
        return False
