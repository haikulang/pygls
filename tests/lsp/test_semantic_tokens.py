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
import unittest
from typing import List, Optional, Union

from pygls.lsp.methods import DOCUMENT_SEMANTIC_TOKENS_FULL
from pygls.lsp.types import (SemanticTokensOptions, SemanticTokensLegend, SemanticTokensParams, SemanticTokens,
                             SemanticTokensPartialResult, TextDocumentIdentifier)
from pygls.server import LanguageServer

from ..conftest import CALL_TIMEOUT, ClientServer


class TestSemanticTokens(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client_server = ClientServer()
        cls.client, cls.server = cls.client_server

        @cls.server.feature(
            DOCUMENT_SEMANTIC_TOKENS_FULL,
            SemanticTokensOptions(
                work_done_progress=False,
                legend=SemanticTokensLegend(
                    token_types=['property', 'type', 'class'],
                    token_modifiers=['private', 'static']),
                range=False,
                full={"delta": False}
            ),
        )
        def f(params: SemanticTokensParams) -> Optional[Union[SemanticTokens, SemanticTokensPartialResult]]:
            if params.text_document.uri == 'file://return.list':
                return SemanticTokens(result_id='class', data=[2, 5, 3, 0, 3, 0, 5, 4, 1, 0, 3, 2, 7, 2, 0])
            else:
                return None

        cls.client_server.start()

    @classmethod
    def tearDownClass(cls):
        cls.client_server.stop()

    def test_capabilities(self):
        capabilities = self.server.server_capabilities

        assert capabilities.semantic_token_provider

    def test_tokens_list(self):
        response = self.client.lsp.send_request(
            DOCUMENT_SEMANTIC_TOKENS_FULL,
            SemanticTokensParams(
                text_document=TextDocumentIdentifier(uri='file://return.list')
            ),
        ).result(timeout=CALL_TIMEOUT)

        assert response


if __name__ == '__main__':
    unittest.main()

