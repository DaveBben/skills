llama-server returns HTTP 500 "Failed to parse input at pos 0" when a model's output contains invalid UTF-8.

Models sometimes emit bytes that are not valid UTF-8. This is common with OCR and vision models (for example PaddleOCR-VL transcribing a receipt, where a `£` sign comes out as stray byte-fallback tokens). When that happens, `/v1/chat/completions` fails the whole, otherwise complete, generation with HTTP 500 and `Failed to parse input at pos 0: ...`. `--skip-chat-parsing` does not avoid it, because that path still runs the PEG parser. The legacy chat parser degraded to content-only in the same situation; the PEG path throws.

What we see: in `common/peg-parser.cpp`, `until` fails hard on invalid UTF-8, while `chars` stops gracefully at the bad byte. Fixing only `until` to stop early is not enough: the bad byte is left unconsumed, so an enclosing sequence that must reach the end of input (for example `p.content(p.rest()) + p.end()`) still fails.

Required behaviour:

- Parsing does not fail because of invalid UTF-8. Parsers that scan text (`until`, `rest` and the like) consume invalid bytes as part of the text they match, so a parse that would succeed on valid text succeeds.
- An AST node's `text` stays the raw input bytes. Each `common_peg_ast_node` gains `std::string sanitized_text() const`, which returns its text with invalid UTF-8 replaced by U+FFFD, following the Unicode Standard's "U+FFFD Substitution of Maximal Subparts" (chapter 3): each maximal subpart of an ill-formed sequence becomes one U+FFFD, and the bytes after it are decoded normally. For example `Hello\xFF\xFE` becomes `Hello` followed by two U+FFFD, and `\xC3(` becomes one U+FFFD followed by `(`.
- `common_peg_parse_result` gains `invalid_utf8`, the invalid runs the result consumed, in ascending order. Each entry is a `common_peg_invalid_utf8` with a byte offset `pos` and a length `len`. A run is recorded once, even when backtracking or a lookahead scans the same bytes more than once.
- The chat message the server returns carries the sanitized text in `content` and `reasoning_content`. Tool names and arguments are grammar-constrained to valid UTF-8 and do not need this.
- While streaming (partial input), an incomplete multi-byte sequence at the end of the input so far is not treated as invalid: it stays out of the output until the rest of it arrives. In a complete input, a truncated sequence at the end is invalid and is replaced.
