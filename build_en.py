"""
TextKit 영어 버전 자동 생성 스크립트
실행: python build_en.py
결과: en/ 폴더에 영어 버전 HTML 파일 생성
"""

import os, re, shutil, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))
EN_DIR = os.path.join(BASE, 'en')
os.makedirs(EN_DIR, exist_ok=True)

SITE_URL = 'https://textkit.wooahouse.com'
SITE_NAME = 'WooaText'

# ── 1. 페이지별 메타 번역 ──────────────────────────────────────────────────────
PAGE_META = {
    'index.html': {
        'title': 'Free Online Text Tools — Character Counter, Converter, Formatter & More | WooaText',
        'desc':  'Free browser-based text tools: character counter, text diff, case converter, URL encoder, Base64, JSON formatter, hash generator, markdown editor, regex tester, CSV↔JSON and more. No sign-up needed.',
        'kw':    'character counter, text tools, case converter, URL encoder, Base64, JSON formatter, hash generator, markdown editor, regex tester, CSV to JSON, text diff, free online tools',
        'og_title': 'Free Online Text Tools | WooaText',
        'og_desc':  '15+ free text tools in your browser: character counter, converter, formatter, markdown editor, regex tester, and more.',
        'h1': 'All Text Tasks, Free, in One Place',
        'app_name': 'WooaText',
    },
    'char-counter.html': {
        'title': 'Character Counter Online Free — Word, Line & Sentence Count | WooaText',
        'desc':  'Count characters, words, lines, sentences, and paragraphs in real time. Includes/excludes spaces toggle. Essential for blog posts, SNS, and manuscript length. 100% free online character counter.',
        'kw':    'character counter, word counter, letter count, character count online, count words free, text counter, string length, WooaText',
        'og_title': 'Character Counter Free Online | WooaText',
        'og_desc':  'Count characters, words, lines, sentences, and paragraphs in real time. Free, no sign-up required.',
        'app_name': 'Character Counter',
        'faq': [
            ('Are spaces counted in the character count?',
             'Yes — both "with spaces" and "without spaces" counts are shown at the same time.'),
            ('Is counting done in real time?',
             'Yes. The count updates instantly as you type or paste text.'),
            ('Can it accurately count Korean characters?',
             'Yes. Hangul, English, numbers, and special characters are all counted accurately.'),
        ],
        'h1': 'Character Counter — Free Online',
        'tool_desc': 'Enter text to count characters, words, lines, sentences, and paragraphs in real time.',
        'breadcrumb': 'Character Counter',
    },
    'text-diff.html': {
        'title': 'Text Diff Checker Online Free — Compare Two Texts | WooaText',
        'desc':  'Compare two texts and highlight differences in color. Find added, removed, or changed content instantly. Free online text diff tool, no upload needed.',
        'kw':    'text diff, compare text online, text comparison, find differences, diff checker free, text diff tool, WooaText',
        'og_title': 'Text Diff Checker Free Online | WooaText',
        'og_desc':  'Compare two texts and highlight differences instantly. Free, no sign-up needed.',
        'app_name': 'Text Diff Checker',
        'faq': [
            ('How does the diff comparison work?',
             'The tool highlights added text in green and removed text in red, making differences easy to spot.'),
            ('Can I compare large texts?',
             'Yes. All processing is done in your browser, so there is no file size limit.'),
            ('Is my text sent to a server?',
             'No. All comparison happens locally in your browser. Your text never leaves your device.'),
        ],
        'h1': 'Text Diff Checker — Free Online',
        'tool_desc': 'Paste two texts to compare them and highlight differences with color.',
        'breadcrumb': 'Text Diff',
    },
    'case-converter.html': {
        'title': 'Case Converter Online Free — UPPER, lower, Title, camelCase, snake_case | WooaText',
        'desc':  'Convert text case online for free: UPPERCASE, lowercase, Title Case, camelCase, PascalCase, snake_case, kebab-case, and more. Instant, no sign-up needed.',
        'kw':    'case converter, uppercase lowercase, camelCase, snake_case, title case, text case change, online case converter, WooaText',
        'og_title': 'Case Converter Free Online | WooaText',
        'og_desc':  'Convert text to UPPER, lower, Title, camelCase, snake_case and more. Free, instant, no sign-up.',
        'app_name': 'Case Converter',
        'faq': [
            ('What case formats are supported?',
             'UPPERCASE, lowercase, Title Case, camelCase, PascalCase, snake_case, and kebab-case are all supported.'),
            ('Can I convert Korean text?',
             'Korean characters are not affected by case conversion. Only English letters are changed.'),
            ('Is the conversion done in real time?',
             'Yes. The output updates instantly as you type.'),
        ],
        'h1': 'Case Converter — Free Online',
        'tool_desc': 'Convert text to any case format: UPPERCASE, lowercase, Title Case, camelCase, snake_case, and more.',
        'breadcrumb': 'Case Converter',
    },
    'url-encoder.html': {
        'title': 'URL Encoder / Decoder Online Free | WooaText',
        'desc':  'Encode or decode URL strings online for free. Instantly percent-encode special characters for URLs, or decode percent-encoded strings. No sign-up needed.',
        'kw':    'URL encoder, URL decoder, percent encoding, URL encode online free, URL decode, encodeURIComponent, WooaText',
        'og_title': 'URL Encoder / Decoder Free Online | WooaText',
        'og_desc':  'Encode or decode URL strings in one click. Free, instant, browser-based.',
        'app_name': 'URL Encoder / Decoder',
        'faq': [
            ('What is URL encoding?',
             'URL encoding (percent-encoding) converts special characters into a format that can be transmitted over the Internet safely.'),
            ('When do I need URL encoding?',
             'When you include special characters like spaces, Korean, or symbols in URLs or query parameters.'),
            ('What is the difference between encodeURI and encodeURIComponent?',
             'encodeURI encodes a full URL while encodeURIComponent encodes a single URL component like a query value.'),
        ],
        'h1': 'URL Encoder / Decoder — Free Online',
        'tool_desc': 'Encode special characters for use in URLs, or decode percent-encoded strings back to readable text.',
        'breadcrumb': 'URL Encoder',
    },
    'base64.html': {
        'title': 'Base64 Encoder / Decoder Online Free | WooaText',
        'desc':  'Encode text to Base64 or decode Base64 strings back to plain text online for free. Supports Unicode and multi-language input. No sign-up needed.',
        'kw':    'Base64 encoder, Base64 decoder, Base64 online, encode Base64 free, decode Base64, base64 converter, WooaText',
        'og_title': 'Base64 Encoder / Decoder Free Online | WooaText',
        'og_desc':  'Encode text to Base64 or decode Base64 back to text. Free, instant, browser-based.',
        'app_name': 'Base64 Encoder / Decoder',
        'faq': [
            ('What is Base64?',
             'Base64 is an encoding scheme that represents binary data as ASCII characters, commonly used in data transfer and storage.'),
            ('Can I encode Korean (non-ASCII) text?',
             'Yes. The tool uses UTF-8 encoding, so Korean and other non-ASCII characters are fully supported.'),
            ('Is Base64 the same as encryption?',
             'No. Base64 is encoding, not encryption. Anyone can decode a Base64 string without a key.'),
        ],
        'h1': 'Base64 Encoder / Decoder — Free Online',
        'tool_desc': 'Encode text to Base64 or decode a Base64 string back to readable text instantly.',
        'breadcrumb': 'Base64',
    },
    'html-entity.html': {
        'title': 'HTML Entity Converter Online Free — Encode & Decode Special Characters | WooaText',
        'desc':  'Convert special characters to HTML entities (&amp;, &lt;, &gt;, &quot;) and back online for free. Instant, no sign-up needed.',
        'kw':    'HTML entity converter, HTML encode, HTML decode, special characters HTML, &amp; &lt; &gt;, HTML entity free, WooaText',
        'og_title': 'HTML Entity Converter Free Online | WooaText',
        'og_desc':  'Encode special characters to HTML entities or decode HTML entities back to text. Free, instant.',
        'app_name': 'HTML Entity Converter',
        'faq': [
            ('What are HTML entities?',
             'HTML entities are special codes that represent reserved characters in HTML, such as &amp; for & and &lt; for <.'),
            ('When do I need HTML entities?',
             'Use them when you want to display HTML special characters (like < or >) as text in a webpage without them being interpreted as HTML.'),
            ('Which characters are converted?',
             'Common characters like &, <, >, ", \' and other special symbols are converted to their HTML entity equivalents.'),
        ],
        'h1': 'HTML Entity Converter — Free Online',
        'tool_desc': 'Convert special characters to HTML entities or decode HTML entities back to readable text.',
        'breadcrumb': 'HTML Entity',
    },
    'line-tools.html': {
        'title': 'Line Sort & Remove Duplicates Online Free | WooaText',
        'desc':  'Sort lines alphabetically, remove duplicate lines, delete blank lines, reverse, or shuffle text lines online for free. Instant, no sign-up needed.',
        'kw':    'sort lines, remove duplicate lines, delete blank lines, reverse lines, shuffle lines, line sorter online free, WooaText',
        'og_title': 'Line Sort & Remove Duplicates Free Online | WooaText',
        'og_desc':  'Sort, deduplicate, reverse, or shuffle text lines online. Free, instant, browser-based.',
        'app_name': 'Line Tools',
        'faq': [
            ('Can I sort Korean or non-English text?',
             'Yes. Lines are sorted using Unicode character order, which works correctly for Korean and other languages.'),
            ('How does the duplicate removal work?',
             'All lines that appear more than once are reduced to a single occurrence. Comparison is case-sensitive by default.'),
            ('Is there a limit on the number of lines?',
             'No. All processing is done in your browser, so there is no practical limit.'),
        ],
        'h1': 'Line Sort & Duplicate Remover — Free Online',
        'tool_desc': 'Sort lines alphabetically, remove duplicates, delete blank lines, reverse, or shuffle — choose your operation below.',
        'breadcrumb': 'Line Tools',
    },
    'whitespace.html': {
        'title': 'Whitespace Remover Online Free — Trim, Clean & Normalize Spaces | WooaText',
        'desc':  'Remove leading/trailing spaces, collapse multiple spaces, convert tabs to spaces, or strip all whitespace from text online for free. Instant, no sign-up.',
        'kw':    'whitespace remover, trim spaces, remove extra spaces, collapse spaces, tabs to spaces, text cleaner online free, WooaText',
        'og_title': 'Whitespace Remover Free Online | WooaText',
        'og_desc':  'Trim, normalize, or strip whitespace from text. Free, instant, browser-based.',
        'app_name': 'Whitespace Remover',
        'faq': [
            ('What types of whitespace can be removed?',
             'Leading/trailing spaces, consecutive spaces, tabs, and newlines can each be cleaned separately or all at once.'),
            ('Will the tool remove newlines?',
             'Only if you choose the "remove all whitespace" option. Other modes preserve line breaks.'),
            ('Is there a character limit?',
             'No. All processing is done in your browser with no server upload.'),
        ],
        'h1': 'Whitespace Remover — Free Online',
        'tool_desc': 'Remove leading/trailing spaces, collapse multiple spaces, convert tabs, or strip all whitespace from your text.',
        'breadcrumb': 'Whitespace',
    },
    'lorem-ipsum.html': {
        'title': 'Lorem Ipsum Generator Online Free — Placeholder Text | WooaText',
        'desc':  'Generate Lorem Ipsum placeholder text online for free. Choose number of paragraphs, sentences, or words. Includes a Korean placeholder text option.',
        'kw':    'Lorem Ipsum generator, placeholder text, dummy text online free, Lorem Ipsum free, random text generator, WooaText',
        'og_title': 'Lorem Ipsum Generator Free Online | WooaText',
        'og_desc':  'Generate Lorem Ipsum placeholder text instantly. Choose paragraphs, sentences, or words. Free, no sign-up.',
        'app_name': 'Lorem Ipsum Generator',
        'faq': [
            ('What is Lorem Ipsum?',
             'Lorem Ipsum is standard placeholder text used in design and publishing to fill space before real content is ready.'),
            ('Can I specify the amount of text?',
             'Yes. You can set the number of paragraphs, sentences, or words to generate.'),
            ('Is there a Korean Lorem Ipsum option?',
             'Yes. The tool provides a Korean placeholder text mode in addition to the classic Latin Lorem Ipsum.'),
        ],
        'h1': 'Lorem Ipsum Generator — Free Online',
        'tool_desc': 'Generate Lorem Ipsum placeholder text. Set paragraphs, sentences, or words, and copy instantly.',
        'breadcrumb': 'Lorem Ipsum',
    },
    'password-generator.html': {
        'title': 'Password Generator Online Free — Strong Random Passwords | WooaText',
        'desc':  'Generate strong, random passwords online for free. Set length and choose character types: uppercase, lowercase, numbers, symbols. 100% browser-based, never saved.',
        'kw':    'password generator, strong password, random password free, secure password creator, password maker online, WooaText',
        'og_title': 'Password Generator Free Online | WooaText',
        'og_desc':  'Generate strong random passwords. Set length and character options. Free, browser-based, never stored.',
        'app_name': 'Password Generator',
        'faq': [
            ('Are generated passwords stored anywhere?',
             'No. Passwords are generated locally in your browser and never sent to any server.'),
            ('What character types can I include?',
             'Uppercase letters, lowercase letters, numbers, and special symbols can each be toggled on or off.'),
            ('How long can the password be?',
             'You can set any length you need. Longer passwords are always more secure.'),
        ],
        'h1': 'Password Generator — Free Online',
        'tool_desc': 'Generate a strong, random password. Set length and choose which character types to include.',
        'breadcrumb': 'Password Generator',
    },
    'json-formatter.html': {
        'title': 'JSON Formatter & Validator Online Free — Pretty Print & Minify | WooaText',
        'desc':  'Format and validate JSON online for free. Pretty-print with indentation, minify/compress, or validate JSON syntax errors. Instant, browser-based, no sign-up.',
        'kw':    'JSON formatter, JSON validator, pretty print JSON, JSON beautifier, JSON minifier, format JSON online free, WooaText',
        'og_title': 'JSON Formatter & Validator Free Online | WooaText',
        'og_desc':  'Format, validate, and minify JSON online. Free, instant, browser-based.',
        'app_name': 'JSON Formatter',
        'faq': [
            ('Can the tool detect JSON errors?',
             'Yes. If your JSON is invalid, the tool shows an error message pointing out where the issue is.'),
            ('What is the difference between format and minify?',
             'Formatting adds indentation and line breaks for readability. Minifying removes all whitespace to reduce file size.'),
            ('Is there a size limit for JSON input?',
             'No. All processing is done in your browser, so there is no server-side size limit.'),
        ],
        'h1': 'JSON Formatter & Validator — Free Online',
        'tool_desc': 'Paste your JSON to format it with proper indentation, minify it, or check for syntax errors.',
        'breadcrumb': 'JSON Formatter',
    },
    'hash-generator.html': {
        'title': 'Hash Generator Online Free — MD5, SHA-1, SHA-256, SHA-512 | WooaText',
        'desc':  'Generate MD5, SHA-1, SHA-256, and SHA-512 hashes from text online for free. Instant, browser-based, no upload needed.',
        'kw':    'hash generator, MD5 generator, SHA-256 online, SHA-512, text hash free, hash calculator, checksum online, WooaText',
        'og_title': 'Hash Generator Free Online — MD5, SHA-256, SHA-512 | WooaText',
        'og_desc':  'Generate MD5, SHA-1, SHA-256, SHA-512 hashes instantly. Free, browser-based, no upload.',
        'app_name': 'Hash Generator',
        'faq': [
            ('What is a hash?',
             'A hash is a fixed-length string produced by a hash function from any input. Even a tiny change in input produces a completely different hash.'),
            ('Which hash algorithms are supported?',
             'MD5, SHA-1, SHA-256, and SHA-512 are all supported.'),
            ('Can I use this to store passwords securely?',
             'MD5 and SHA-1 are not recommended for passwords. Use bcrypt or SHA-256/512 with a salt for secure password hashing.'),
        ],
        'h1': 'Hash Generator — Free Online',
        'tool_desc': 'Enter text to instantly generate MD5, SHA-1, SHA-256, and SHA-512 hash values.',
        'breadcrumb': 'Hash Generator',
    },
    'markdown-editor.html': {
        'title': 'Markdown Editor Online Free — Live Preview | WooaText',
        'desc':  'Write and preview Markdown online for free. Real-time HTML preview with syntax highlighting. Export to HTML. No sign-up, no upload.',
        'kw':    'markdown editor online, markdown preview, live markdown, markdown to HTML, markdown free, online markdown editor, WooaText',
        'og_title': 'Markdown Editor Free Online — Live Preview | WooaText',
        'og_desc':  'Write Markdown with live HTML preview. Free, browser-based, no sign-up.',
        'app_name': 'Markdown Editor',
        'faq': [
            ('Is the preview updated in real time?',
             'Yes. The HTML preview updates instantly as you type Markdown.'),
            ('Which Markdown syntax is supported?',
             'Standard Markdown including headings, lists, links, images, code blocks, tables, and bold/italic text.'),
            ('Can I export the result?',
             'Yes. You can copy the rendered HTML or download the Markdown file.'),
        ],
        'h1': 'Markdown Editor — Live Preview',
        'tool_desc': 'Write Markdown on the left and see the live HTML preview on the right. Copy or download anytime.',
        'breadcrumb': 'Markdown Editor',
    },
    'regex-tester.html': {
        'title': 'Regex Tester Online Free — Regular Expression Matcher | WooaText',
        'desc':  'Test regular expressions online for free. Enter a pattern and see all matches highlighted in real time. Supports flags: global, case-insensitive, multiline. No sign-up.',
        'kw':    'regex tester, regular expression tester, regex online free, regex match, regex checker, test regex, javascript regex, WooaText',
        'og_title': 'Regex Tester Free Online | WooaText',
        'og_desc':  'Test regex patterns with live match highlighting. Free, instant, browser-based.',
        'app_name': 'Regex Tester',
        'faq': [
            ('Which regex flavor is used?',
             'JavaScript RegExp is used, which is compatible with most modern programming languages.'),
            ('What flags are supported?',
             'Global (g), case-insensitive (i), and multiline (m) flags are all supported.'),
            ('Are match groups shown?',
             'Yes. Capture groups are displayed alongside each match result.'),
        ],
        'h1': 'Regex Tester — Free Online',
        'tool_desc': 'Enter a regular expression pattern and test it against your text with live match highlighting.',
        'breadcrumb': 'Regex Tester',
    },
    'csv-json.html': {
        'title': 'CSV to JSON Converter Online Free — JSON to CSV | WooaText',
        'desc':  'Convert CSV to JSON or JSON to CSV online for free. Paste data, choose direction, and copy the result instantly. Browser-based, no upload needed.',
        'kw':    'CSV to JSON, JSON to CSV, convert CSV JSON online free, CSV JSON converter, data format converter, WooaText',
        'og_title': 'CSV ↔ JSON Converter Free Online | WooaText',
        'og_desc':  'Convert between CSV and JSON formats instantly. Free, browser-based, no sign-up.',
        'app_name': 'CSV ↔ JSON Converter',
        'faq': [
            ('Does CSV to JSON use the first row as headers?',
             'Yes. The first row of the CSV is used as the JSON field names (keys).'),
            ('Can I convert nested JSON to CSV?',
             'Nested JSON objects are flattened. Complex nested structures may not convert perfectly to CSV.'),
            ('Is there a row or size limit?',
             'No. All processing is done locally in your browser.'),
        ],
        'h1': 'CSV ↔ JSON Converter — Free Online',
        'tool_desc': 'Paste CSV to convert to JSON, or paste JSON to convert to CSV. Instant, browser-based.',
        'breadcrumb': 'CSV ↔ JSON',
    },
    'html-css-editor.html': {
        'title': 'Online HTML/CSS/JS Editor — Live Preview & URL Share | WooaText',
        'desc':  'Write HTML, CSS, and JavaScript with a live preview in your browser. Free online editor with URL sharing support. No sign-up, no installation.',
        'kw':    'HTML CSS JS editor, online code editor, live preview, HTML editor online free, code playground, web editor, WooaText',
        'og_title': 'HTML/CSS/JS Editor Free Online — Live Preview | WooaText',
        'og_desc':  'Code HTML, CSS, and JS with an instant live preview. Share via URL. Free, no sign-up.',
        'app_name': 'HTML/CSS/JS Editor',
        'faq': [
            ('Is there a live preview?',
             'Yes. The preview panel updates in real time as you type code.'),
            ('Can I share my code?',
             'Yes. Use the URL sharing feature to generate a link that others can open to see your code and preview.'),
            ('Does it support JavaScript?',
             'Yes. HTML, CSS, and JavaScript are all fully supported in the editor.'),
        ],
        'h1': 'HTML / CSS / JS Editor — Live Preview',
        'tool_desc': 'Write HTML, CSS, and JavaScript and see the live result instantly. Share your code with a URL.',
        'breadcrumb': 'HTML/CSS/JS Editor',
    },
    'jwt-decoder.html': {
        'title': 'JWT Decoder Online Free — Parse & Inspect JWT Tokens | WooaText',
        'desc':  'Decode and inspect JWT (JSON Web Tokens) online for free. View header, payload, and expiry without sending tokens to any server. 100% browser-based.',
        'kw':    'JWT decoder, JSON Web Token decoder, JWT parser, decode JWT online free, JWT inspect, token debugger, WooaText',
        'og_title': 'JWT Decoder Free Online | WooaText',
        'og_desc':  'Decode JWT tokens in your browser. View header, payload, and expiry. Free, 100% private.',
        'app_name': 'JWT Decoder',
        'faq': [
            ('Is the JWT sent to a server?',
             'No. All decoding happens locally in your browser. Your token is never sent to any server.'),
            ('Does the tool verify the JWT signature?',
             'This tool decodes (parses) the JWT without signature verification. For full verification, use a server-side library.'),
            ('Can I check the expiry time?',
             'Yes. The tool shows the "exp" claim as a human-readable date and tells you if the token is expired.'),
        ],
        'h1': 'JWT Decoder — Free Online',
        'tool_desc': 'Paste a JWT token to decode its header and payload. Check expiry date. No server upload — 100% private.',
        'breadcrumb': 'JWT Decoder',
    },
    'unicode-converter.html': {
        'title': 'Unicode Converter Online Free — Text to \\uXXXX, &#XXXX; & U+XXXX | WooaText',
        'desc':  'Convert text to Unicode escape sequences (\\uXXXX), HTML numeric references (&#XXXX;), and code points (U+XXXX) online for free. Reverse conversion included.',
        'kw':    'unicode converter, text to unicode, unicode escape, \\uXXXX, &#XXXX; converter, unicode code point, WooaText',
        'og_title': 'Unicode Converter Free Online | WooaText',
        'og_desc':  'Convert text to Unicode escape sequences, HTML numeric references, and code points. Free, instant.',
        'app_name': 'Unicode Converter',
        'faq': [
            ('What is a Unicode escape sequence?',
             'A Unicode escape sequence represents a character as \\uXXXX where XXXX is the hex code point.'),
            ('What formats does the tool support?',
             'JavaScript/JSON \\uXXXX, HTML &#XXXX; (decimal), HTML &#xXXXX; (hex), and U+XXXX code points.'),
            ('Can I convert back from Unicode to text?',
             'Yes. The tool supports both encoding (text → unicode) and decoding (unicode → text).'),
        ],
        'h1': 'Unicode Converter — Free Online',
        'tool_desc': 'Convert text to Unicode escape sequences (\\uXXXX), HTML numeric entities (&#XXXX;), or U+XXXX code points, and back.',
        'breadcrumb': 'Unicode Converter',
    },
    'text-replacer.html': {
        'title': 'Text Find & Replace Online Free — Regex Mode & Multi-Rule | WooaText',
        'desc':  'Find and replace text online for free. Supports regex mode and multiple replacement rules at once. Instant, browser-based, no sign-up needed.',
        'kw':    'text find replace, text replacer online free, find and replace regex, bulk text replace, string replace tool, WooaText',
        'og_title': 'Text Find & Replace Free Online | WooaText',
        'og_desc':  'Find and replace text with regex support and multi-rule mode. Free, instant, browser-based.',
        'app_name': 'Text Replacer',
        'faq': [
            ('Does it support regular expressions?',
             'Yes. Enable regex mode to use regular expression patterns for both find and replace fields.'),
            ('Can I apply multiple rules at once?',
             'Yes. Add as many find/replace pairs as you need and apply them all in one click.'),
            ('Is the replacement case-sensitive?',
             'Yes by default. You can toggle case-insensitive mode if needed.'),
        ],
        'h1': 'Text Find & Replace — Free Online',
        'tool_desc': 'Find and replace text with regex mode and multiple replacement rules. Results update instantly.',
        'breadcrumb': 'Text Replacer',
    },
    'xml-formatter.html': {
        'title': 'XML Formatter & Validator Online Free — Pretty Print & Minify | WooaText',
        'desc':  'Format, validate, and minify XML online for free. Pretty-print with indentation, check for syntax errors, or compress XML. Instant, browser-based.',
        'kw':    'XML formatter, XML validator, pretty print XML, XML beautifier, XML minifier, format XML online free, WooaText',
        'og_title': 'XML Formatter & Validator Free Online | WooaText',
        'og_desc':  'Format, validate, and minify XML instantly. Free, browser-based, no sign-up.',
        'app_name': 'XML Formatter',
        'faq': [
            ('Can it detect XML errors?',
             'Yes. Invalid XML is flagged with an error message explaining the issue.'),
            ('What is the difference between format and minify?',
             'Formatting adds indentation for readability. Minifying removes all unnecessary whitespace to reduce file size.'),
            ('Is there a size limit for XML input?',
             'No. All processing is done locally in your browser.'),
        ],
        'h1': 'XML Formatter & Validator — Free Online',
        'tool_desc': 'Paste XML to format it with proper indentation, check for syntax errors, or compress it to a single line.',
        'breadcrumb': 'XML Formatter',
    },
    'timestamp-converter.html': {
        'title': 'Unix Timestamp Converter Online Free — Timestamp to Date & Back | WooaText',
        'desc':  'Convert Unix timestamps to human-readable dates and vice versa online for free. Live current timestamp display. Supports seconds and milliseconds.',
        'kw':    'unix timestamp converter, timestamp to date, date to timestamp, epoch converter online free, current unix time, WooaText',
        'og_title': 'Unix Timestamp Converter Free Online | WooaText',
        'og_desc':  'Convert Unix timestamps to dates and back. Real-time current timestamp. Free, instant.',
        'app_name': 'Timestamp Converter',
        'faq': [
            ('What is a Unix timestamp?',
             'A Unix timestamp is the number of seconds (or milliseconds) elapsed since January 1, 1970, 00:00:00 UTC.'),
            ('Does it support milliseconds?',
             'Yes. Both second-precision and millisecond-precision timestamps are supported.'),
            ('Is the current timestamp shown in real time?',
             'Yes. The current Unix timestamp is displayed and updated every second.'),
        ],
        'h1': 'Unix Timestamp Converter — Free Online',
        'tool_desc': 'Convert a Unix timestamp to a human-readable date, or convert a date to a Unix timestamp. Real-time current timestamp shown.',
        'breadcrumb': 'Timestamp Converter',
    },
    'number-base.html': {
        'title': 'Number Base Converter Online Free — Binary, Octal, Decimal, Hex | WooaText',
        'desc':  'Convert numbers between binary (base 2), octal (base 8), decimal (base 10), and hexadecimal (base 16) online for free. Real-time conversion.',
        'kw':    'number base converter, binary to decimal, hex to decimal, octal converter, base conversion online free, binary hex converter, WooaText',
        'og_title': 'Number Base Converter Free Online | WooaText',
        'og_desc':  'Convert between binary, octal, decimal, and hex in real time. Free, instant, browser-based.',
        'app_name': 'Number Base Converter',
        'faq': [
            ('Which bases are supported?',
             'Binary (base 2), octal (base 8), decimal (base 10), and hexadecimal (base 16).'),
            ('Is conversion done in real time?',
             'Yes. All four representations update instantly as you type in any field.'),
            ('Can I convert negative numbers?',
             'The tool currently supports non-negative integers for base conversion.'),
        ],
        'h1': 'Number Base Converter — Free Online',
        'tool_desc': 'Enter a number in any base and see the binary, octal, decimal, and hexadecimal equivalents in real time.',
        'breadcrumb': 'Number Base',
    },
    'text-stats.html': {
        'title': 'Text Statistics Online Free — Word Frequency & Readability | WooaText',
        'desc':  'Analyze text statistics online for free: top 20 word frequency, sentence count, paragraph count, readability score, and more. Instant, browser-based.',
        'kw':    'text statistics, word frequency, text analysis online free, readability score, word count statistics, text analyzer, WooaText',
        'og_title': 'Text Statistics Free Online | WooaText',
        'og_desc':  'Analyze word frequency, readability, and text structure. Free, instant, browser-based.',
        'app_name': 'Text Statistics',
        'faq': [
            ('What statistics are shown?',
             'Word frequency (top 20), character count, word count, sentence count, paragraph count, and estimated reading time.'),
            ('Is word frequency case-sensitive?',
             'No. Words are compared in lowercase so "The" and "the" are counted as the same word.'),
            ('Is my text uploaded anywhere?',
             'No. All analysis is done locally in your browser. Your text never leaves your device.'),
        ],
        'h1': 'Text Statistics — Free Online',
        'tool_desc': 'Paste text to analyze word frequency, sentence count, paragraph count, and readability in real time.',
        'breadcrumb': 'Text Statistics',
    },
    'slug-generator.html': {
        'title': 'Slug Generator Online Free — URL Friendly Slug from Text | WooaText',
        'desc':  'Generate URL-friendly slugs from text online for free. Convert spaces and special characters to hyphens. Korean romanization option included.',
        'kw':    'slug generator, URL slug, text to slug, SEO slug, create slug online free, URL friendly string, WooaText',
        'og_title': 'Slug Generator Free Online | WooaText',
        'og_desc':  'Generate URL-friendly slugs from text. Korean romanization option. Free, instant.',
        'app_name': 'Slug Generator',
        'faq': [
            ('What is a URL slug?',
             'A slug is a URL-friendly version of a string, using only lowercase letters, numbers, and hyphens — no spaces or special characters.'),
            ('Does it support Korean text?',
             'Yes. Korean characters can be romanized (transliterated) and converted into a valid slug.'),
            ('Can I customize the separator?',
             'Yes. You can choose a hyphen (-) or underscore (_) as the separator.'),
        ],
        'h1': 'Slug Generator — Free Online',
        'tool_desc': 'Convert any text into a URL-friendly slug. Supports Korean romanization and custom separators.',
        'breadcrumb': 'Slug Generator',
    },
    'line-numbering.html': {
        'title': 'Line Numbering Tool Online Free — Add Numbers to Lines | WooaText',
        'desc':  'Add line numbers, bullets, or custom symbols to each line of text online for free. Customize prefix format and starting number. Instant, browser-based.',
        'kw':    'line numbering, add line numbers, numbered list, line number tool online free, prefix lines, WooaText',
        'og_title': 'Line Numbering Tool Free Online | WooaText',
        'og_desc':  'Add numbers, bullets, or custom prefixes to each text line. Free, instant, browser-based.',
        'app_name': 'Line Numbering',
        'faq': [
            ('Can I choose the starting number?',
             'Yes. Set the starting number for the line sequence.'),
            ('What prefix styles are available?',
             'Numbers (1. 2. 3.), bullets (• or -), or a custom symbol you define.'),
            ('Is there a line limit?',
             'No. All processing is done locally in your browser.'),
        ],
        'h1': 'Line Numbering Tool — Free Online',
        'tool_desc': 'Add line numbers, bullets, or custom prefixes to every line of your text. Set starting number and format.',
        'breadcrumb': 'Line Numbering',
    },
    'yaml-json.html': {
        'title': 'YAML to JSON Converter Online Free — JSON to YAML | WooaText',
        'desc':  'Convert YAML to JSON or JSON to YAML online for free. Auto-detect mode available. Instant, browser-based, no sign-up needed.',
        'kw':    'YAML to JSON, JSON to YAML, YAML JSON converter online free, YAML parser, JSON to YAML converter, WooaText',
        'og_title': 'YAML ↔ JSON Converter Free Online | WooaText',
        'og_desc':  'Convert between YAML and JSON formats instantly. Auto-detect mode. Free, browser-based.',
        'app_name': 'YAML ↔ JSON Converter',
        'faq': [
            ('What is the difference between YAML and JSON?',
             'YAML is a human-readable data format that avoids quotes and brackets. JSON is more strict and widely used in APIs.'),
            ('Does auto-detect mode work?',
             'Yes. The tool automatically detects whether your input is YAML or JSON and converts to the other format.'),
            ('Are YAML anchors and aliases supported?',
             'Basic anchors and aliases are supported. Highly complex YAML features may not be fully handled.'),
        ],
        'h1': 'YAML ↔ JSON Converter — Free Online',
        'tool_desc': 'Convert YAML to JSON or JSON to YAML. Auto-detect mode converts in the right direction automatically.',
        'breadcrumb': 'YAML ↔ JSON',
    },
    'html-markdown.html': {
        'title': 'HTML to Markdown Converter Online Free | WooaText',
        'desc':  'Convert HTML to Markdown online for free. Paste HTML and get clean Markdown output instantly. Browser-based, no sign-up needed.',
        'kw':    'HTML to Markdown, convert HTML to MD, HTML markdown converter online free, html2markdown, WooaText',
        'og_title': 'HTML to Markdown Converter Free Online | WooaText',
        'og_desc':  'Convert HTML to Markdown instantly. Free, browser-based, no sign-up.',
        'app_name': 'HTML to Markdown',
        'faq': [
            ('Which HTML elements are converted?',
             'Headings, paragraphs, links, images, bold, italic, lists, tables, and code blocks are all converted.'),
            ('What happens to unsupported HTML?',
             'Unsupported or complex HTML may be left as raw HTML in the Markdown output.'),
            ('Can I convert Markdown back to HTML?',
             'For Markdown → HTML, use the Markdown Editor tool on WooaText.'),
        ],
        'h1': 'HTML to Markdown — Free Online',
        'tool_desc': 'Paste HTML and convert it to clean Markdown syntax instantly.',
        'breadcrumb': 'HTML → Markdown',
    },
    'morse-code.html': {
        'title': 'Morse Code Translator Online Free — Text to Morse & Back | WooaText',
        'desc':  'Translate text to Morse code or decode Morse code back to text online for free. Supports audio playback. Instant, browser-based, no sign-up.',
        'kw':    'morse code translator, text to morse code, morse code decoder, morse code online free, morse code generator, WooaText',
        'og_title': 'Morse Code Translator Free Online | WooaText',
        'og_desc':  'Translate text to Morse code or decode Morse back to text. Audio playback included. Free, instant.',
        'app_name': 'Morse Code Translator',
        'faq': [
            ('Does it support audio playback?',
             'Yes. The tool can play the Morse code as audio beeps so you can hear the signal.'),
            ('Which characters are supported?',
             'Letters A-Z, digits 0-9, and common punctuation marks are all supported in Morse code.'),
            ('Can I decode Morse code back to text?',
             'Yes. Enter dots and dashes and the tool will decode them back to readable text.'),
        ],
        'h1': 'Morse Code Translator — Free Online',
        'tool_desc': 'Convert text to Morse code or decode Morse code to text. Audio playback available.',
        'breadcrumb': 'Morse Code',
    },
}

# ── 2. 공통 한국어→영어 치환 ──────────────────────────────────────────────────
COMMON = [
    # ── 내비게이션 ──
    ('>글자수 세기<', '>Char Counter<'),
    ('>대소문자 변환<', '>Case Converter<'),
    ('>JSON 포맷터<', '>JSON Formatter<'),
    ('>비밀번호 생성<', '>Password Gen<'),
    ('>해시 생성<', '>Hash Generator<'),
    ('>소개<', '>About<'),

    # ── 히어로 (index.html) ──
    ('<h1>모든 텍스트 작업 무료로, 한 곳에서</h1>',
     '<h1>All Text Tasks, Free, in One Place</h1>'),
    ('<strong style="color:#FEF3C7;">15가지 도구</strong>',
     '<strong style="color:#FEF3C7;">15+ tools</strong>'),
    ('글자수 세기·변환·포맷·마크다운·정규식까지',
     'Character counter, converter, formatter, markdown, regex and more —'),
    ('회원가입 없이, 텍스트는 브라우저 밖으로 나가지 않아요',
     'No sign-up needed. Text never leaves your browser.'),
    ('>📌 홈 화면에 추가<', '>📌 Add to Home Screen<'),
    # hero-related
    ('<span>JSON·코드 작업엔 VS Code도 →</span>',
     '<span>For JSON & code tasks, try VS Code →</span>'),
    ('>WooaVS에서 확장 보기 →<', '>Browse Extensions on WooaVS →<'),

    # ── 카테고리 (index.html) ──
    ('<span class="category-title">분석</span>', '<span class="category-title">Analysis</span>'),
    ('<p class="category-desc">텍스트를 분석하고 차이점을 비교하는 도구</p>',
     '<p class="category-desc">Tools to analyze text and compare differences</p>'),
    ('<span class="category-title">변환</span>', '<span class="category-title">Convert</span>'),
    ('<p class="category-desc">텍스트 형식·인코딩·케이스 변환 도구</p>',
     '<p class="category-desc">Tools for text format, encoding, and case conversion</p>'),
    ('<span class="category-title">정리</span>', '<span class="category-title">Clean</span>'),
    ('<p class="category-desc">텍스트를 깔끔하게 정리하는 도구</p>',
     '<p class="category-desc">Tools to clean and organize your text</p>'),
    ('<span class="category-title">생성</span>', '<span class="category-title">Generate</span>'),
    ('<p class="category-desc">텍스트·비밀번호·JSON을 생성하는 도구</p>',
     '<p class="category-desc">Tools to generate text, passwords, and data</p>'),
    ('<span class="category-title">해시·암호화</span>', '<span class="category-title">Hash & Crypto</span>'),
    ('<p class="category-desc">텍스트의 해시값을 생성하는 도구</p>',
     '<p class="category-desc">Generate hash values from text</p>'),
    ('<span class="category-title">코드 & 개발</span>', '<span class="category-title">Code & Dev</span>'),
    ('<p class="category-desc">마크다운 편집, 정규식 테스트, 데이터 변환 도구</p>',
     '<p class="category-desc">Markdown editor, regex tester, and data conversion tools</p>'),

    # ── 툴카드 이름 (index.html) ──
    ('<div class="tool-name">글자수 세기</div>', '<div class="tool-name">Char Counter</div>'),
    ('<div class="tool-name">텍스트 비교</div>', '<div class="tool-name">Text Diff</div>'),
    ('<div class="tool-name">텍스트 통계</div>', '<div class="tool-name">Text Stats</div>'),
    ('<div class="tool-name">대소문자 변환</div>', '<div class="tool-name">Case Converter</div>'),
    ('<div class="tool-name">URL 인코딩</div>', '<div class="tool-name">URL Encoder</div>'),
    ('<div class="tool-name">Base64 변환</div>', '<div class="tool-name">Base64</div>'),
    ('<div class="tool-name">HTML 엔티티</div>', '<div class="tool-name">HTML Entity</div>'),
    ('<div class="tool-name">유니코드 변환기</div>', '<div class="tool-name">Unicode Converter</div>'),
    ('<div class="tool-name">타임스탬프 변환기</div>', '<div class="tool-name">Timestamp</div>'),
    ('<div class="tool-name">이진수/진법 변환기</div>', '<div class="tool-name">Number Base</div>'),
    ('<div class="tool-name">줄 정렬·중복 제거</div>', '<div class="tool-name">Line Tools</div>'),
    ('<div class="tool-name">공백 제거·정리</div>', '<div class="tool-name">Whitespace</div>'),
    ('<div class="tool-name">텍스트 치환기</div>', '<div class="tool-name">Text Replacer</div>'),
    ('<div class="tool-name">번호 매기기</div>', '<div class="tool-name">Line Numbering</div>'),
    ('<div class="tool-name">슬러그 생성기</div>', '<div class="tool-name">Slug Generator</div>'),
    ('<div class="tool-name">Lorem Ipsum 생성</div>', '<div class="tool-name">Lorem Ipsum</div>'),
    ('<div class="tool-name">비밀번호 생성기</div>', '<div class="tool-name">Password Generator</div>'),
    ('<div class="tool-name">JSON 포맷터</div>', '<div class="tool-name">JSON Formatter</div>'),
    ('<div class="tool-name">해시 생성기</div>', '<div class="tool-name">Hash Generator</div>'),
    ('<div class="tool-name">마크다운 에디터</div>', '<div class="tool-name">Markdown Editor</div>'),
    ('<div class="tool-name">정규식 테스터</div>', '<div class="tool-name">Regex Tester</div>'),
    ('<div class="tool-name">CSV ↔ JSON 변환</div>', '<div class="tool-name">CSV ↔ JSON</div>'),
    ('<div class="tool-name">HTML/CSS/JS 에디터</div>', '<div class="tool-name">HTML/CSS/JS Editor</div>'),
    ('<div class="tool-name">JWT 디코더</div>', '<div class="tool-name">JWT Decoder</div>'),
    ('<div class="tool-name">XML 포맷터</div>', '<div class="tool-name">XML Formatter</div>'),
    ('<div class="tool-name">YAML ↔ JSON 변환</div>', '<div class="tool-name">YAML ↔ JSON</div>'),
    ('<div class="tool-name">HTML → 마크다운</div>', '<div class="tool-name">HTML → Markdown</div>'),
    ('<div class="tool-name">모스 부호</div>', '<div class="tool-name">Morse Code</div>'),

    # ── 툴카드 설명 (index.html) ──
    ('<div class="tool-desc">글자·단어·줄·문장·단락 수 실시간 카운트</div>',
     '<div class="tool-desc">Real-time count of chars, words, lines, sentences</div>'),
    ('<div class="tool-desc">두 텍스트의 차이점을 색으로 하이라이트</div>',
     '<div class="tool-desc">Highlight differences between two texts</div>'),
    ('<div class="tool-desc">단어 빈도 Top20·문장·단락 실시간 분석</div>',
     '<div class="tool-desc">Word frequency Top20, sentence & paragraph analysis</div>'),
    ('<div class="tool-desc">UPPER·lower·Title·camelCase·snake_case 등</div>',
     '<div class="tool-desc">UPPER, lower, Title, camelCase, snake_case and more</div>'),
    ('<div class="tool-desc">URL 인코딩·디코딩 변환</div>',
     '<div class="tool-desc">URL encode and decode conversion</div>'),
    ('<div class="tool-desc">Base64 인코딩·디코딩</div>',
     '<div class="tool-desc">Base64 encode and decode</div>'),
    ('<div class="tool-desc">HTML 특수문자 ↔ 엔티티 변환</div>',
     '<div class="tool-desc">Special characters ↔ HTML entity conversion</div>'),
    ('<div class="tool-desc">텍스트 ↔ \\uXXXX · &#XXXX; · U+XXXX 변환</div>',
     '<div class="tool-desc">Text ↔ \\uXXXX · &#XXXX; · U+XXXX conversion</div>'),
    ('<div class="tool-desc">Unix timestamp ↔ 날짜시간, 현재시각 실시간 표시</div>',
     '<div class="tool-desc">Unix timestamp ↔ date/time, live current timestamp</div>'),
    ('<div class="tool-desc">2·8·10·16진수 실시간 상호 변환</div>',
     '<div class="tool-desc">Binary, octal, decimal, hex real-time conversion</div>'),
    ('<div class="tool-desc">정렬·중복제거·빈줄제거·섞기</div>',
     '<div class="tool-desc">Sort, deduplicate, remove blanks, shuffle</div>'),
    ('<div class="tool-desc">앞뒤·연속·탭→스페이스 공백 처리</div>',
     '<div class="tool-desc">Trim, collapse, tab→space whitespace processing</div>'),
    ('<div class="tool-desc">찾기·바꾸기, 정규식 모드, 다중 규칙 적용</div>',
     '<div class="tool-desc">Find & replace, regex mode, multi-rule support</div>'),
    ('<div class="tool-desc">줄마다 번호·불릿·커스텀 기호 자동 추가</div>',
     '<div class="tool-desc">Add numbers, bullets, or custom prefix per line</div>'),
    ('<div class="tool-desc">텍스트 → URL slug, 한글 음역 옵션</div>',
     '<div class="tool-desc">Text → URL slug, Korean romanization option</div>'),
    ('<div class="tool-desc">단락·문장·단어 수 지정, 한국어 버전 포함</div>',
     '<div class="tool-desc">Set paragraphs, sentences, or words. Korean version included</div>'),
    ('<div class="tool-desc">길이·문자 조합 옵션으로 안전한 비밀번호 생성</div>',
     '<div class="tool-desc">Generate secure passwords with length and character options</div>'),
    ('<div class="tool-desc">JSON 정렬·압축·유효성 검사</div>',
     '<div class="tool-desc">Format, minify, and validate JSON</div>'),
    ('<div class="tool-desc">MD5·SHA-1·SHA-256·SHA-512 해시 생성</div>',
     '<div class="tool-desc">Generate MD5, SHA-1, SHA-256, SHA-512 hashes</div>'),
    ('<div class="tool-desc">실시간 마크다운 편집 및 HTML 미리보기</div>',
     '<div class="tool-desc">Real-time Markdown editing with HTML preview</div>'),
    ('<div class="tool-desc">Regex 패턴 실시간 테스트 및 매칭 확인</div>',
     '<div class="tool-desc">Real-time regex pattern testing and match highlighting</div>'),
    ('<div class="tool-desc">CSV와 JSON 형식 상호 변환</div>',
     '<div class="tool-desc">Convert between CSV and JSON formats</div>'),
    ('<div class="tool-desc">코드 작성 후 실시간 미리보기, URL 공유 지원</div>',
     '<div class="tool-desc">Live preview as you code, with URL sharing</div>'),
    ('<div class="tool-desc">JWT 토큰 파싱·만료일 확인, 서버 전송 없음</div>',
     '<div class="tool-desc">Parse JWT tokens, check expiry, 100% private</div>'),
    ('<div class="tool-desc">XML 들여쓰기 정렬·검증·압축</div>',
     '<div class="tool-desc">Format, validate, and minify XML</div>'),
    ('<div class="tool-desc">YAML·JSON 상호 변환, 자동 변환 모드</div>',
     '<div class="tool-desc">YAML ↔ JSON conversion with auto-detect mode</div>'),

    # ── free badge / new badge ──
    ('<span class="free-badge">무료</span>', '<span class="free-badge">Free</span>'),
    ('<span class="new-badge">NEW</span>', '<span class="new-badge">NEW</span>'),

    # ── 툴 페이지 공통 UI ──
    ('<div class="text-panel-title">텍스트 입력</div>', '<div class="text-panel-title">Text Input</div>'),
    ('<div class="text-panel-title">분석 결과</div>', '<div class="text-panel-title">Results</div>'),
    ('<div class="text-panel-title">상세 정보</div>', '<div class="text-panel-title">Details</div>'),
    ('<div class="text-panel-title">결과</div>', '<div class="text-panel-title">Result</div>'),
    ('<div class="text-panel-title">출력</div>', '<div class="text-panel-title">Output</div>'),
    ('<div class="text-panel-title">입력</div>', '<div class="text-panel-title">Input</div>'),
    # stat labels (char-counter)
    ('<div class="stat-label">전체 글자수</div>', '<div class="stat-label">Total Chars</div>'),
    ('<div class="stat-label">공백 제외 글자수</div>', '<div class="stat-label">Chars (no spaces)</div>'),
    ('<div class="stat-label">단어수</div>', '<div class="stat-label">Words</div>'),
    ('<div class="stat-label">문장수</div>', '<div class="stat-label">Sentences</div>'),
    ('<div class="stat-label">줄수</div>', '<div class="stat-label">Lines</div>'),
    ('<div class="stat-label">단락수</div>', '<div class="stat-label">Paragraphs</div>'),
    ('<div class="stat-label">한글 글자수</div>', '<div class="stat-label">Korean Chars</div>'),
    ('<div class="stat-label">영문 글자수</div>', '<div class="stat-label">English Chars</div>'),
    ('<div class="stat-label">숫자 개수</div>', '<div class="stat-label">Numbers</div>'),
    ('<div class="stat-label">공백 개수</div>', '<div class="stat-label">Spaces</div>'),
    ('<div class="stat-label">바이트 (UTF-8)</div>', '<div class="stat-label">Bytes (UTF-8)</div>'),
    ('<div class="stat-label">읽기 시간 (분)</div>', '<div class="stat-label">Reading Time (min)</div>'),
    # checkbox
    ('공백 포함 카운트', 'Include spaces'),
    # buttons
    ('>지우기<', '>Clear<'),
    ('>복사<', '>Copy<'),
    ('>변환<', '>Convert<'),
    ('>생성<', '>Generate<'),
    ('>포맷<', '>Format<'),
    ('>압축<', '>Minify<'),
    ('>실행<', '>Run<'),
    # breadcrumb
    ('<a href="index.html">WooaText</a>', '<a href="../index.html">WooaText</a>'),
    # cross-link tips (common patterns)
    ('💡 텍스트를 비교하고 싶다면?', '💡 Want to compare text?'),
    ('<a href="text-diff.html">텍스트 비교 도구 →</a>', '<a href="../text-diff.html">Text Diff Tool →</a>'),
    ('💡 글자수도 세고 싶다면?', '💡 Need to count characters?'),
    ('<a href="char-counter.html">글자수 세기 →</a>', '<a href="../char-counter.html">Character Counter →</a>'),
    ('💡 JSON을 포맷팅하고 싶다면?', '💡 Want to format JSON?'),
    ('<a href="json-formatter.html">JSON 포맷터 →</a>', '<a href="../json-formatter.html">JSON Formatter →</a>'),
    # FAQ section
    ('<h2 style="font-size:1.4rem;margin-bottom:1.5rem;">자주 묻는 질문</h2>',
     '<h2 style="font-size:1.4rem;margin-bottom:1.5rem;">Frequently Asked Questions</h2>'),
    # footer
    ('© 2026 WooaText. 모든 권리 보유.', '© 2026 WooaText. All rights reserved.'),
    ('>개인정보처리방침<', '>Privacy Policy<'),
    ('>소개<', '>About<'),
    ('>홈<', '>Home<'),
    ('<p class="coupang-notice">이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>', ''),

    # ── our-sites-bar active link ──
    ('href="https://textkit.wooahouse.com/" target="_blank" rel="noopener" class="active"',
     'href="https://textkit.wooahouse.com/en/" target="_blank" rel="noopener" class="active"'),

    # ── 상대 경로 수정 (en/ 서브디렉토리) ──
    ('href="/manifest.json"', 'href="../manifest.json"'),
    ('href="manifest.json"', 'href="../manifest.json"'),
    ('href="css/style.css"', 'href="../css/style.css"'),
    ('src="js/pwa-install.js"', 'src="../js/pwa-install.js"'),
    ('href="about.html"', 'href="../about.html"'),
    ('href="privacy.html"', 'href="../privacy.html"'),
    ('href="index.html"', 'href="../index.html"'),

    # ── index.html ld+json ListItem names ──
    ('"name":"글자수 세기"', '"name":"Character Counter"'),
    ('"name":"텍스트 비교"', '"name":"Text Diff"'),
    ('"name":"대소문자 변환"', '"name":"Case Converter"'),
    ('"name":"URL 인코딩/디코딩"', '"name":"URL Encoder/Decoder"'),
    ('"name":"Base64 인코딩/디코딩"', '"name":"Base64 Encoder/Decoder"'),
    ('"name":"HTML 엔티티 변환"', '"name":"HTML Entity Converter"'),
    ('"name":"줄 정렬/중복 제거"', '"name":"Line Sort & Deduplicate"'),
    ('"name":"공백 제거/정리"', '"name":"Whitespace Remover"'),
    ('"name":"Lorem Ipsum 생성기"', '"name":"Lorem Ipsum Generator"'),
    ('"name":"비밀번호 생성기"', '"name":"Password Generator"'),
    ('"name":"JSON 포맷터"', '"name":"JSON Formatter"'),
    ('"name":"해시 생성기"', '"name":"Hash Generator"'),
    ('"name":"마크다운 에디터"', '"name":"Markdown Editor"'),
    ('"name":"정규식 테스터"', '"name":"Regex Tester"'),
    ('"name":"CSV JSON 변환"', '"name":"CSV JSON Converter"'),
    ('"name":"HTML CSS JS 에디터"', '"name":"HTML CSS JS Editor"'),
    ('"name":"JWT 디코더"', '"name":"JWT Decoder"'),
    ('"name":"유니코드 변환기"', '"name":"Unicode Converter"'),
    ('"name":"텍스트 치환기"', '"name":"Text Replacer"'),
    ('"name":"XML 포맷터"', '"name":"XML Formatter"'),
    ('"name":"타임스탬프 변환기"', '"name":"Timestamp Converter"'),
    ('"name":"이진수/진법 변환기"', '"name":"Number Base Converter"'),
    ('"name":"텍스트 통계"', '"name":"Text Statistics"'),
    ('"name":"슬러그 생성기"', '"name":"Slug Generator"'),
    ('"name":"번호 매기기"', '"name":"Line Numbering"'),
    ('"name":"YAML JSON 변환"', '"name":"YAML JSON Converter"'),

    # ── index.html features section ──
    ('<div class="feature-title">100% 안전</div>', '<div class="feature-title">100% Safe</div>'),
    ('<div class="feature-desc">텍스트가 서버로 전송되지 않습니다. 모든 처리가 브라우저 안에서 이루어집니다.</div>',
     '<div class="feature-desc">Text never leaves your browser. All processing happens locally.</div>'),
    ('<div class="feature-title">즉시 처리</div>', '<div class="feature-title">Instant Results</div>'),
    ('<div class="feature-desc">실시간으로 결과를 확인하세요. 인터넷 속도와 무관합니다.</div>',
     '<div class="feature-desc">See results in real time. No internet speed dependency.</div>'),
    ('<div class="feature-title">완전 무료</div>', '<div class="feature-title">Completely Free</div>'),
    ('<div class="feature-desc">회원가입 없이 모든 기능을 무제한 무료로 사용할 수 있습니다.</div>',
     '<div class="feature-desc">Use all features unlimited, no sign-up required.</div>'),
    ('<div class="feature-title">모든 기기</div>', '<div class="feature-title">All Devices</div>'),
    ('<div class="feature-desc">PC, 태블릿, 스마트폰 어디서나 사용 가능한 반응형 디자인.</div>',
     '<div class="feature-desc">Responsive design works on PC, tablet, and smartphone.</div>'),

    # ── index.html footer ──
    ('<p>무료 온라인 텍스트 도구 모음. 글자수 세기부터 해시 생성까지 모든 텍스트 작업을 안전하게.</p>',
     '<p>Free online text tools. From character counting to hash generation — safely in your browser.</p>'),
    ('<h4>분석</h4>', '<h4>Analysis</h4>'),
    ('<a href="text-diff.html">텍스트 비교</a>', '<a href="text-diff.html">Text Diff</a>'),
    ('<a href="url-encoder.html">URL 인코딩</a>', '<a href="url-encoder.html">URL Encoder</a>'),
    ('<a href="base64.html">Base64 변환</a>', '<a href="base64.html">Base64</a>'),
    ('<a href="html-entity.html">HTML 엔티티</a>', '<a href="html-entity.html">HTML Entity</a>'),
    ('<h4>정리·생성</h4>', '<h4>Clean & Generate</h4>'),
    ('<a href="line-tools.html">줄 정렬·중복 제거</a>', '<a href="line-tools.html">Line Tools</a>'),
    ('<a href="whitespace.html">공백 제거·정리</a>', '<a href="whitespace.html">Whitespace</a>'),
    ('<a href="lorem-ipsum.html">Lorem Ipsum 생성</a>', '<a href="lorem-ipsum.html">Lorem Ipsum</a>'),
    ('<a href="password-generator.html">비밀번호 생성기</a>', '<a href="password-generator.html">Password Generator</a>'),
    ('<a href="hash-generator.html">해시 생성기</a>', '<a href="hash-generator.html">Hash Generator</a>'),
    ('<h4>변환 (신규)</h4>', '<h4>Convert (New)</h4>'),
    ('<a href="unicode-converter.html">유니코드 변환기</a>', '<a href="unicode-converter.html">Unicode Converter</a>'),
    ('<a href="timestamp-converter.html">타임스탬프 변환기</a>', '<a href="timestamp-converter.html">Timestamp Converter</a>'),
    ('<a href="number-base.html">이진수/진법 변환기</a>', '<a href="number-base.html">Number Base</a>'),
    ('<a href="slug-generator.html">슬러그 생성기</a>', '<a href="slug-generator.html">Slug Generator</a>'),
    ('<h4>코드 & 개발</h4>', '<h4>Code & Dev</h4>'),
    ('<a href="html-css-editor.html">HTML/CSS/JS 에디터</a>', '<a href="html-css-editor.html">HTML/CSS/JS Editor</a>'),
    ('<a href="jwt-decoder.html">JWT 디코더</a>', '<a href="jwt-decoder.html">JWT Decoder</a>'),
    ('<a href="xml-formatter.html">XML 포맷터</a>', '<a href="xml-formatter.html">XML Formatter</a>'),
    ('<a href="yaml-json.html">YAML ↔ JSON 변환</a>', '<a href="yaml-json.html">YAML ↔ JSON</a>'),
    ('<a href="markdown-editor.html">마크다운 에디터</a>', '<a href="markdown-editor.html">Markdown Editor</a>'),
    ('<a href="regex-tester.html">정규식 테스터</a>', '<a href="regex-tester.html">Regex Tester</a>'),
    ('<a href="csv-json.html">CSV ↔ JSON 변환</a>', '<a href="csv-json.html">CSV ↔ JSON</a>'),
    ('<h4>정리 (신규)</h4>', '<h4>Clean (New)</h4>'),
    ('<a href="text-replacer.html">텍스트 치환기</a>', '<a href="text-replacer.html">Text Replacer</a>'),
    ('<a href="line-numbering.html">번호 매기기</a>', '<a href="line-numbering.html">Line Numbering</a>'),
    ('<a href="text-stats.html">텍스트 통계</a>', '<a href="text-stats.html">Text Statistics</a>'),
    ('<h4>정보</h4>', '<h4>Info</h4>'),
    ('<a href="../about.html">서비스 소개</a>', '<a href="../about.html">About</a>'),
    ('<h4>WooaHouse 서비스</h4>', '<h4>WooaHouse Services</h4>'),

    # ── index.html: tool cards missing from COMMON ──
    ('<div class="tool-name">HTML ↔ 마크다운 변환</div>', '<div class="tool-name">HTML → Markdown</div>'),
    ('<div class="tool-name">모스부호 변환</div>', '<div class="tool-name">Morse Code</div>'),
    ('<div class="tool-desc">HTML을 마크다운으로, 마크다운을 HTML로 상호 변환</div>',
     '<div class="tool-desc">Convert HTML to Markdown and Markdown to HTML</div>'),
    ('<div class="tool-desc">텍스트 ↔ 모스부호 변환, 신호음 재생 지원</div>',
     '<div class="tool-desc">Text ↔ Morse code, audio playback supported</div>'),

    # ── Breadcrumb spans (source pages use plain <span> without id) ──
    ('<span>글자수 세기</span>', '<span>Character Counter</span>'),
    ('<span>텍스트 비교</span>', '<span>Text Diff</span>'),
    ('<span>텍스트 통계</span>', '<span>Text Statistics</span>'),
    ('<span>대소문자 변환</span>', '<span>Case Converter</span>'),
    ('<span>URL 인코딩/디코딩</span>', '<span>URL Encoder/Decoder</span>'),
    ('<span>Base64 변환</span>', '<span>Base64</span>'),
    ('<span>HTML 엔티티 변환</span>', '<span>HTML Entity Converter</span>'),
    ('<span>줄 정렬·중복 제거</span>', '<span>Line Tools</span>'),
    ('<span>공백 제거·정리</span>', '<span>Whitespace</span>'),
    ('<span>Lorem Ipsum 생성기</span>', '<span>Lorem Ipsum Generator</span>'),
    ('<span>비밀번호 생성기</span>', '<span>Password Generator</span>'),
    ('<span>JSON 포맷터</span>', '<span>JSON Formatter</span>'),
    ('<span>해시 생성기</span>', '<span>Hash Generator</span>'),
    ('<span>마크다운 에디터</span>', '<span>Markdown Editor</span>'),
    ('<span>정규식 테스터</span>', '<span>Regex Tester</span>'),
    ('<span>CSV ↔ JSON 변환</span>', '<span>CSV ↔ JSON Converter</span>'),
    ('<span>HTML/CSS/JS 에디터</span>', '<span>HTML/CSS/JS Editor</span>'),
    ('<span>JWT 디코더</span>', '<span>JWT Decoder</span>'),
    ('<span>유니코드 변환기</span>', '<span>Unicode Converter</span>'),
    ('<span>텍스트 치환기</span>', '<span>Text Replacer</span>'),
    ('<span>XML 포맷터</span>', '<span>XML Formatter</span>'),
    ('<span>타임스탬프 변환기</span>', '<span>Timestamp Converter</span>'),
    ('<span>이진수/진법 변환기</span>', '<span>Number Base Converter</span>'),
    ('<span>슬러그 생성기</span>', '<span>Slug Generator</span>'),
    ('<span>번호 매기기</span>', '<span>Line Numbering</span>'),
    ('<span>YAML ↔ JSON 변환</span>', '<span>YAML ↔ JSON Converter</span>'),
    ('<span>HTML ↔ 마크다운 변환</span>', '<span>HTML → Markdown Converter</span>'),
    ('<span>모스부호 변환</span>', '<span>Morse Code Translator</span>'),

    # ── Tool page <p> descriptions (used when id="toolDesc" not present) ──
    ('<p>텍스트를 입력하면 글자수·단어수·줄수·문장수·단락수를 실시간으로 세어 드립니다</p>',
     '<p>Enter text to count characters, words, lines, sentences, and paragraphs in real time.</p>'),
    ('<p>두 텍스트를 입력하고 비교 버튼을 누르면 차이점을 색으로 표시합니다</p>',
     '<p>Enter two texts and click Compare to highlight differences with color.</p>'),
    ('<p>텍스트를 입력하면 글자수·단어수·문장수·단락수·단어 빈도 Top20을 실시간으로 분석합니다</p>',
     '<p>Paste text to analyze word frequency, sentence count, paragraph count, and readability in real time.</p>'),
    ('<p>텍스트를 다양한 케이스 형식으로 변환합니다</p>',
     '<p>Convert text to any case format: UPPERCASE, lowercase, Title Case, camelCase, snake_case, and more.</p>'),
    ('<p>텍스트를 URL 형식으로 인코딩하거나 URL을 디코딩합니다</p>',
     '<p>Encode special characters for use in URLs, or decode percent-encoded strings back to readable text.</p>'),
    ('<p>텍스트를 Base64로 인코딩하거나 Base64를 원래 텍스트로 디코딩합니다</p>',
     '<p>Encode text to Base64 or decode a Base64 string back to readable text instantly.</p>'),
    ('<p>HTML 특수문자를 엔티티로 인코딩하거나 엔티티를 원래 문자로 디코딩합니다</p>',
     '<p>Convert special characters to HTML entities or decode HTML entities back to readable text.</p>'),
    ('<p>텍스트 줄을 정렬하고 중복·빈 줄을 제거하거나 순서를 변경합니다</p>',
     '<p>Sort lines alphabetically, remove duplicates, delete blank lines, reverse, or shuffle — choose your operation below.</p>'),
    ('<p>텍스트의 공백을 다양한 방식으로 제거하고 정리합니다</p>',
     '<p>Remove leading/trailing spaces, collapse multiple spaces, convert tabs, or strip all whitespace from your text.</p>'),
    ('<p>디자인·개발에 사용할 더미 텍스트를 원하는 형태로 생성합니다</p>',
     '<p>Generate Lorem Ipsum placeholder text. Set paragraphs, sentences, or words, and copy instantly.</p>'),
    ('<p>길이와 문자 조합을 설정해 안전한 랜덤 비밀번호를 생성합니다</p>',
     '<p>Generate a strong, random password. Set length and choose which character types to include.</p>'),
    ('<p>JSON을 보기 좋게 정렬하거나 압축하고 유효성을 검사합니다</p>',
     '<p>Paste your JSON to format it with proper indentation, minify it, or check for syntax errors.</p>'),
    ('<p>텍스트의 SHA-256, SHA-1, SHA-512 해시값을 브라우저에서 안전하게 생성합니다</p>',
     '<p>Enter text to instantly generate MD5, SHA-1, SHA-256, and SHA-512 hash values.</p>'),
    ('<p>마크다운을 실시간으로 HTML로 변환하며 미리보기합니다</p>',
     '<p>Write Markdown on the left and see the live HTML preview on the right. Copy or download anytime.</p>'),
    ('<p>정규식 패턴을 실시간으로 테스트하고 매칭 결과를 확인합니다</p>',
     '<p>Enter a regular expression pattern and test it against your text with live match highlighting.</p>'),
    ('<p>CSV를 JSON으로, JSON을 CSV로 무료 변환합니다</p>',
     '<p>Paste CSV to convert to JSON, or paste JSON to convert to CSV. Instant, browser-based.</p>'),
    ('<p>JWT 토큰을 붙여넣으면 Header, Payload, Signature를 즉시 파싱합니다. 만료일시 및 남은 시간 표시. 100% 브라우저 처리.</p>',
     '<p>Paste a JWT token to decode its header and payload. Check expiry date. No server upload — 100% private.</p>'),
    ('<p>텍스트를 Unicode escape(\\uXXXX), HTML 엔티티(&#XXXX;), 코드포인트(U+XXXX)로 변환하거나 반대로 복원합니다</p>',
     '<p>Convert text to Unicode escape sequences (\\uXXXX), HTML numeric entities (&#XXXX;), or U+XXXX code points, and back.</p>'),
    ('<p>단어·문장을 한번에 치환합니다. 정규식 모드와 대소문자 무시 옵션을 규칙별로 설정하고, 여러 규칙을 순서대로 일괄 적용할 수 있습니다.</p>',
     '<p>Find and replace text with regex mode and multiple replacement rules. Results update instantly.</p>'),
    ('<p>XML을 보기 좋게 들여쓰기 정렬하거나 압축하고 유효성을 검사합니다</p>',
     '<p>Paste XML to format it with proper indentation, check for syntax errors, or compress it to a single line.</p>'),
    ('<p>Unix timestamp를 날짜시간으로, 날짜시간을 timestamp로 변환합니다. 초/밀리초 자동 감지, 현재 시각 실시간 표시.</p>',
     '<p>Convert a Unix timestamp to a human-readable date, or convert a date to a Unix timestamp. Real-time current timestamp shown.</p>'),
    ('<p>어느 칸에 값을 입력하거나 수정해도 나머지 진법이 즉시 자동 변환됩니다. 16진수는 대소문자 모두 입력 가능하며 결과는 대문자로 표시됩니다.</p>',
     '<p>Enter a number in any base and see the binary, octal, decimal, and hexadecimal equivalents in real time.</p>'),
    ('<p>텍스트를 URL에 사용할 수 있는 슬러그로 변환합니다. 한글 음역, 구분자·대소문자 옵션을 지원합니다.</p>',
     '<p>Convert any text into a URL-friendly slug. Supports Korean romanization and custom separators.</p>'),
    ('<p>텍스트 각 줄에 번호나 글머리 기호를 자동으로 추가합니다. 다양한 형식과 시작 번호를 자유롭게 설정하세요.</p>',
     '<p>Add line numbers, bullets, or custom prefixes to every line of your text. Set starting number and format.</p>'),
    ('<p>YAML을 JSON으로, JSON을 YAML로 즉시 변환합니다. 유효성 검사와 실시간 변환을 지원합니다.</p>',
     '<p>Convert YAML to JSON or JSON to YAML. Auto-detect mode converts in the right direction automatically.</p>'),
    ('<p>HTML을 마크다운으로, 마크다운을 HTML로 상호 변환합니다</p>',
     '<p>Paste HTML and convert it to clean Markdown syntax instantly.</p>'),
    ('<p>텍스트를 모스부호로, 모스부호를 텍스트로 변환하고 실제 신호음으로 재생합니다</p>',
     '<p>Convert text to Morse code or decode Morse code to text. Audio playback available.</p>'),

    # ── Common UI: panel titles ──
    ('<div class="text-panel-title">입력 텍스트</div>', '<div class="text-panel-title">Input Text</div>'),
    ('<div class="text-panel-title">원본 텍스트</div>', '<div class="text-panel-title">Original Text</div>'),
    ('<div class="text-panel-title">비교 텍스트</div>', '<div class="text-panel-title">Compare Text</div>'),
    ('<div class="text-panel-title">JSON 입력</div>', '<div class="text-panel-title">JSON Input</div>'),
    ('<div class="text-panel-title">정규식 패턴</div>', '<div class="text-panel-title">Regex Pattern</div>'),
    ('<div class="text-panel-title">빠른 패턴 모음</div>', '<div class="text-panel-title">Quick Patterns</div>'),
    ('<div class="text-panel-title">테스트 문자열</div>', '<div class="text-panel-title">Test String</div>'),
    ('<div class="text-panel-title">치환 (Replace)</div>', '<div class="text-panel-title">Replace</div>'),
    ('<div class="text-panel-title">JWT 토큰 입력</div>', '<div class="text-panel-title">JWT Token Input</div>'),
    ('<div class="text-panel-title">기본 통계</div>', '<div class="text-panel-title">Basic Statistics</div>'),
    ('<div class="text-panel-title">단어 빈도 Top 20</div>', '<div class="text-panel-title">Word Frequency Top 20</div>'),
    ('<div class="text-panel-title">XML 입력</div>', '<div class="text-panel-title">XML Input</div>'),
    ('<div class="text-panel-title">입력 텍스트 <span style="font-size:0.8rem;font-weight:400;color:var(--text-light);">(최대 50자)</span></div>',
     '<div class="text-panel-title">Input Text <span style="font-size:0.8rem;font-weight:400;color:var(--text-light);">(max 50 chars)</span></div>'),
    ('<div class="text-panel-title">문자별 상세 정보 <span style="font-size:0.8rem;font-weight:400;color:var(--text-light);">(최대 50자)</span></div>',
     '<div class="text-panel-title">Per-character Details <span style="font-size:0.8rem;font-weight:400;color:var(--text-light);">(max 50 chars)</span></div>'),

    # ── stat-label variants ──
    ('<div class="stat-label">총 글자수</div>', '<div class="stat-label">Total Chars</div>'),
    ('<div class="stat-label">공백 제외 글자</div>', '<div class="stat-label">Chars (no spaces)</div>'),
    ('<div class="stat-label">단어 수</div>', '<div class="stat-label">Words</div>'),
    ('<div class="stat-label">문장 수</div>', '<div class="stat-label">Sentences</div>'),
    ('<div class="stat-label">단락 수</div>', '<div class="stat-label">Paragraphs</div>'),
    ('<div class="stat-label">줄 수</div>', '<div class="stat-label">Lines</div>'),
    ('<div class="stat-label">평균 단어 길이</div>', '<div class="stat-label">Avg Word Length</div>'),
    ('<div class="stat-label">가장 긴 단어</div>', '<div class="stat-label">Longest Word</div>'),

    # ── line-tools buttons ──
    ('>🔼 오름차순 정렬<', '>🔼 Sort A→Z<'),
    ('>🔽 내림차순 정렬<', '>🔽 Sort Z→A<'),
    ('>🔲 중복 줄 제거<', '>🔲 Remove Duplicates<'),
    ('>⬜ 빈 줄 제거<', '>⬜ Remove Blank Lines<'),
    ('>🔃 줄 순서 뒤집기<', '>🔃 Reverse Lines<'),
    ('>🔀 줄 섞기<', '>🔀 Shuffle Lines<'),
    ('<span class="line-stat-item">입력 줄 수: <strong id="inputLineCount">0</strong></span>',
     '<span class="line-stat-item">Input lines: <strong id="inputLineCount">0</strong></span>'),
    ('<span class="line-stat-item">결과 줄 수: <strong id="outputLineCount">0</strong></span>',
     '<span class="line-stat-item">Result lines: <strong id="outputLineCount">0</strong></span>'),
    ('💡 공백도 정리하고 싶다면? <a href="whitespace.html">공백 제거·정리 →</a>',
     '💡 Need to clean whitespace too? <a href="whitespace.html">Whitespace Remover →</a>'),

    # ── whitespace buttons ──
    ('>✂️ 각 줄 앞뒤 공백 제거<', '>✂️ Trim Each Line<'),
    ('>📏 연속 공백 하나로<', '>📏 Collapse Spaces<'),
    ('>🚫 모든 공백 제거<', '>🚫 Remove All Whitespace<'),
    ('>⇥→□ 탭→스페이스 변환<', '>⇥→□ Tabs→Spaces<'),
    ('>🔪 전체 앞뒤 공백 제거<', '>🔪 Trim All<'),
    ('💡 빈 줄도 제거하고 싶다면? <a href="line-tools.html">줄 정렬·중복 제거 →</a>',
     '💡 Need to remove blank lines too? <a href="line-tools.html">Line Tools →</a>'),

    # ── lorem-ipsum UI ──
    ('<label for="loremType">유형</label>', '<label for="loremType">Type</label>'),
    ('<option value="paragraphs">단락 (Paragraphs)</option>', '<option value="paragraphs">Paragraphs</option>'),
    ('<option value="sentences">문장 (Sentences)</option>', '<option value="sentences">Sentences</option>'),
    ('<option value="words">단어 (Words)</option>', '<option value="words">Words</option>'),
    ('<label for="loremCount">개수</label>', '<label for="loremCount">Count</label>'),
    ('<label for="loremLang">언어</label>', '<label for="loremLang">Language</label>'),
    ('<option value="korean">한국어</option>', '<option value="korean">Korean</option>'),
    ('>✨ 생성하기<', '>✨ Generate<'),
    ('<div class="text-panel-title" style="margin-bottom:0;" id="outputLabel">결과</div>',
     '<div class="text-panel-title" style="margin-bottom:0;" id="outputLabel">Result</div>'),
    ('>📋 복사<', '>📋 Copy<'),
    ('placeholder="생성하기 버튼을 클릭하면 텍스트가 생성됩니다..."',
     'placeholder="Click Generate to create placeholder text..."'),
    ('✅ 클립보드에 복사되었습니다!', '✅ Copied to clipboard!'),
    ('💡 비밀번호 생성이 필요하신가요? <a href="password-generator.html">비밀번호 생성기 →</a>',
     '💡 Need a password generator? <a href="password-generator.html">Password Generator →</a>'),

    # ── password-generator UI ──
    ('<label for="pwLength">길이</label>', '<label for="pwLength">Length</label>'),
    ('<label for="optUpper">대문자 (A-Z)</label>', '<label for="optUpper">Uppercase (A-Z)</label>'),
    ('<label for="optLower">소문자 (a-z)</label>', '<label for="optLower">Lowercase (a-z)</label>'),
    ('<label for="optDigit">숫자 (0-9)</label>', '<label for="optDigit">Numbers (0-9)</label>'),
    ('<label for="optSpecial">특수문자 (!@#$%^&amp;*)</label>', '<label for="optSpecial">Special chars (!@#$%^&amp;*)</label>'),
    ('<label for="optNoAmbiguous">헷갈리는 문자 제외 (0,O,l,1,I)</label>',
     '<label for="optNoAmbiguous">Exclude ambiguous chars (0,O,l,1,I)</label>'),
    ('>🔑 비밀번호 생성<', '>🔑 Generate Password<'),
    ('placeholder="비밀번호가 여기 표시됩니다"', 'placeholder="Password will appear here"'),
    ('>🔄 다시 생성<', '>🔄 Regenerate<'),
    ('💡 생성된 비밀번호의 해시가 필요하신가요? <a href="hash-generator.html">해시 생성기 →</a>',
     '💡 Need to hash your password? <a href="hash-generator.html">Hash Generator →</a>'),

    # ── hash-generator UI ──
    ('<div style="font-size:0.88rem; font-weight:600; color:var(--text-light); margin-bottom:10px;">해시 알고리즘 선택</div>',
     '<div style="font-size:0.88rem; font-weight:600; color:var(--text-light); margin-bottom:10px;">Select hash algorithm</div>'),
    ('>#️⃣ 해시 생성<', '>#️⃣ Generate Hash<'),
    ('placeholder="해시를 생성할 텍스트를 입력하세요...&#10;예: 안녕하세요 / Hello World / pa$$w0rd"',
     'placeholder="Enter text to generate hash...&#10;e.g.: Hello World / pa$$w0rd"'),
    ('💡 비밀번호 생성이 필요하신가요? <a href="password-generator.html">비밀번호 생성기 →</a>',
     '💡 Need a password generator? <a href="password-generator.html">Password Generator →</a>'),

    # ── base64 UI ──
    ('>🔒 Base64 인코딩<', '>🔒 Encode to Base64<'),
    ('>🔓 Base64 디코딩<', '>🔓 Decode from Base64<'),
    ('placeholder="인코딩하거나 디코딩할 텍스트를 입력하세요...&#10;예: 안녕하세요 / 6rCV64S26riwIOyasOyepQ=="',
     'placeholder="Enter text to encode or Base64 to decode..."'),
    ('placeholder="변환 버튼을 클릭하면 결과가 표시됩니다..."',
     'placeholder="Click a button to see the result..."'),
    ('💡 URL 인코딩이 필요하신가요? <a href="url-encoder.html">URL 인코딩/디코딩 →</a>',
     '💡 Need URL encoding? <a href="url-encoder.html">URL Encoder →</a>'),

    # ── url-encoder UI ──
    ('>🔒 인코딩 (Encode)<', '>🔒 Encode<'),
    ('>🔓 디코딩 (Decode)<', '>🔓 Decode<'),
    ('placeholder="인코딩하거나 디코딩할 텍스트를 입력하세요...&#10;예: 안녕하세요 / https://example.com/검색?q=텍스트"',
     'placeholder="Enter text to encode or URL to decode..."'),
    ('💡 Base64 인코딩이 필요하신가요? <a href="base64.html">Base64 변환 →</a>',
     '💡 Need Base64 encoding? <a href="base64.html">Base64 →</a>'),

    # ── html-entity UI ──
    ('>🔒 엔티티 인코딩<', '>🔒 Encode to HTML Entity<'),
    ('>🔓 엔티티 디코딩<', '>🔓 Decode from HTML Entity<'),
    ('placeholder="변환할 텍스트를 입력하세요...&#10;예: &lt;div class=&quot;hello&quot;&gt;안녕 &amp; 반가워&lt;/div&gt;"',
     'placeholder="Enter text to encode or HTML entities to decode..."'),
    ('<h3 style="font-size:0.95rem; font-weight:700; margin-bottom:12px;">변환 대상 문자</h3>',
     '<h3 style="font-size:0.95rem; font-weight:700; margin-bottom:12px;">Characters converted</h3>'),
    ('💡 JSON 형식 처리가 필요하신가요? <a href="../json-formatter.html">JSON Formatter →</a>',
     '💡 Need JSON formatting? <a href="../json-formatter.html">JSON Formatter →</a>'),

    # ── json-formatter UI ──
    ('<div class="text-panel-title">JSON 입력</div>', '<div class="text-panel-title">JSON Input</div>'),
    ('>✨ 예쁘게 정렬<', '>✨ Format<'),
    ('>📦 압축 (Minify)<', '>📦 Minify<'),
    ('>✅ 유효성 검사<', '>✅ Validate<'),
    ('placeholder=\'JSON을 붙여넣거나 입력하세요...&#10;예: {"name":"WooaText","tools":12,"free":true}\'',
     'placeholder=\'Paste or enter JSON here...&#10;e.g.: {"name":"WooaText","tools":12,"free":true}\''),
    ('💡 HTML 엔티티 변환이 필요하신가요? <a href="html-entity.html">HTML 엔티티 변환 →</a>',
     '💡 Need HTML entity conversion? <a href="html-entity.html">HTML Entity →</a>'),

    # ── case-converter UI ──
    ('placeholder="변환할 텍스트를 입력하세요...&#10;예: Hello World, foo bar baz"',
     'placeholder="Enter text to convert...&#10;e.g.: Hello World, foo bar baz"'),
    ('<div class="text-panel-title">입력 텍스트</div>', '<div class="text-panel-title">Input Text</div>'),
    ('💡 JSON 키를 snake_case로 바꾸고 싶다면? <a href="../json-formatter.html">JSON Formatter →</a>',
     '💡 Want to convert JSON keys to snake_case? <a href="../json-formatter.html">JSON Formatter →</a>'),

    # ── char-counter UI ──
    ('placeholder="여기에 텍스트를 입력하거나 붙여넣기 하세요..."',
     'placeholder="Type or paste text here..."'),

    # ── text-diff UI ──
    ('<div class="text-panel-title">원본 텍스트</div>', '<div class="text-panel-title">Original Text</div>'),
    ('<div class="text-panel-title">비교 텍스트</div>', '<div class="text-panel-title">Compare Text</div>'),
    ('placeholder="원본 텍스트를 입력하세요..."', 'placeholder="Enter original text..."'),
    ('placeholder="비교할 텍스트를 입력하세요..."', 'placeholder="Enter text to compare..."'),
    ('>🔍 비교하기<', '>🔍 Compare<'),
    ('대소문자 무시', 'Ignore case'),
    ('공백 무시', 'Ignore whitespace'),
    ('<div class="text-panel-title">비교 결과</div>', '<div class="text-panel-title">Comparison Result</div>'),
    ('<span><span class="legend-add"></span> 추가됨</span>', '<span><span class="legend-add"></span> Added</span>'),
    ('<span><span class="legend-remove"></span> 삭제됨</span>', '<span><span class="legend-remove"></span> Removed</span>'),
    ('💡 글자수를 확인하고 싶다면? <a href="../char-counter.html">Character Counter →</a>',
     '💡 Want to count characters? <a href="../char-counter.html">Character Counter →</a>'),

    # ── text-stats UI ──
    ('placeholder="여기에 분석할 텍스트를 입력하거나 붙여넣기 하세요..."',
     'placeholder="Type or paste text to analyze here..."'),
    ('⏱️ 예상 읽기 시간: <span id="readTime">—</span>',
     '⏱️ Estimated reading time: <span id="readTime">—</span>'),
    ('<div class="freq-empty">텍스트를 입력하면 단어 빈도를 분석합니다.</div>',
     '<div class="freq-empty">Enter text to analyze word frequency.</div>'),
    ('불용어 제외 (a, the, 이, 그 등)', 'Exclude stop words (a, the, etc.)'),

    # ── slug-generator UI ──
    ('<div class="text-panel-title">입력 텍스트</div>', '<div class="text-panel-title">Input Text</div>'),
    ('<div class="slug-option-label">구분자</div>', '<div class="slug-option-label">Separator</div>'),
    ('<label for="sepHyphen">하이픈 <code>-</code> (기본)</label>',
     '<label for="sepHyphen">Hyphen <code>-</code> (default)</label>'),
    ('<label for="sepUnderscore">언더스코어 <code>_</code></label>',
     '<label for="sepUnderscore">Underscore <code>_</code></label>'),
    ('<label for="sepDot">점 <code>.</code></label>',
     '<label for="sepDot">Dot <code>.</code></label>'),
    ('<div class="slug-option-label">대소문자</div>', '<div class="slug-option-label">Case</div>'),
    ('<label for="caseLower">소문자 (기본)</label>', '<label for="caseLower">Lowercase (default)</label>'),
    ('<label for="caseUpper">대문자</label>', '<label for="caseUpper">Uppercase</label>'),
    ('<label for="caseOriginal">원문 유지</label>', '<label for="caseOriginal">Keep original</label>'),
    ('<div class="slug-option-label">한글 처리</div>', '<div class="slug-option-label">Korean handling</div>'),
    ('<label for="hangulRoman">음역 (romanization)</label>', '<label for="hangulRoman">Romanize</label>'),
    ('<label for="hangulKeep">한글 그대로</label>', '<label for="hangulKeep">Keep Korean</label>'),
    ('<label for="hangulRemove">제거</label>', '<label for="hangulRemove">Remove</label>'),
    ('<div class="slug-option-label">추가 옵션</div>', '<div class="slug-option-label">Extra options</div>'),
    ('<label for="removeNumbers">숫자 제거</label>', '<label for="removeNumbers">Remove numbers</label>'),
    ('<div class="slug-result-label">생성된 슬러그</div>', '<div class="slug-result-label">Generated slug</div>'),
    ('<div class="slug-result-value empty" id="slugResult">텍스트를 입력하면 슬러그가 실시간으로 생성됩니다.</div>',
     '<div class="slug-result-value empty" id="slugResult">Enter text to generate a slug in real time.</div>'),
    ('<div class="slug-result-label" style="margin-top:16px;">URL 미리보기</div>',
     '<div class="slug-result-label" style="margin-top:16px;">URL Preview</div>'),
    ('💡 URL 인코딩이 필요하신가요? <a href="url-encoder.html">URL 인코딩 도구 →</a>',
     '💡 Need URL encoding? <a href="url-encoder.html">URL Encoder →</a>'),

    # ── line-numbering UI ──
    ('<div class="text-panel-title">원본 텍스트</div>', '<div class="text-panel-title">Input Text</div>'),
    ('<div class="options-panel-title">형식 선택</div>', '<div class="options-panel-title">Format</div>'),
    ('<button class="format-btn active" data-format="1.">1. 숫자점</button>',
     '<button class="format-btn active" data-format="1.">1. Number+dot</button>'),
    ('<button class="format-btn" data-format="1)">1) 숫자괄호</button>',
     '<button class="format-btn" data-format="1)">1) Number+paren</button>'),
    ('<button class="format-btn" data-format="(1)">(1) 괄호숫자</button>',
     '<button class="format-btn" data-format="(1)">(1) Paren+number</button>'),
    ('<button class="format-btn" data-format="①">① 원문자</button>',
     '<button class="format-btn" data-format="①">① Circled</button>'),
    ('<button class="format-btn" data-format="-">- 하이픈</button>',
     '<button class="format-btn" data-format="-">- Hyphen</button>'),
    ('<button class="format-btn" data-format="•">• 불릿</button>',
     '<button class="format-btn" data-format="•">• Bullet</button>'),
    ('<button class="format-btn" data-format="▸">▸ 화살표</button>',
     '<button class="format-btn" data-format="▸">▸ Arrow</button>'),
    ('<button class="format-btn" data-format="★">★ 별</button>',
     '<button class="format-btn" data-format="★">★ Star</button>'),
    ('<button class="format-btn" data-format="custom">✏️ 커스텀</button>',
     '<button class="format-btn" data-format="custom">✏️ Custom</button>'),
    ("placeholder='커스텀 접두사 입력 (예: >>, Step, ※)' maxlength=\"20\"",
     "placeholder='Enter custom prefix (e.g. >>, Step, ※)' maxlength=\"20\""),
    ('<label>시작 번호 (숫자 형식에만 적용)</label>', '<label>Start number (for numeric formats only)</label>'),
    ('<label>구분자 (번호와 텍스트 사이)</label>', '<label>Separator (between number and text)</label>'),
    ('<option value=" ">공백</option>', '<option value=" ">Space</option>'),
    ('<option value="	">탭</option>', '<option value="	">Tab</option>'),
    ('<option value="">없음</option>', '<option value="">None</option>'),
    ('<label>빈 줄 처리</label>', '<label>Empty line handling</label>'),
    ('<option value="include">번호 포함</option>', '<option value="include">Include number</option>'),
    ('<option value="skip">번호 건너뜀</option>', '<option value="skip">Skip number</option>'),
    ('<option value="remove">빈 줄 제거</option>', '<option value="remove">Remove line</option>'),
    ('<label>정렬 패딩</label>', '<label>Alignment padding</label>'),
    ('자리수 맞추기 (01. 02. … 10.)', 'Pad digits (01. 02. … 10.)'),
    ('placeholder="번호를 매길 텍스트를 입력하세요...&#10;예:&#10;사과&#10;바나나&#10;포도&#10;딸기"',
     'placeholder="Enter text to number...&#10;e.g.:&#10;Apple&#10;Banana&#10;Grape&#10;Strawberry"'),
    ('placeholder="변환 버튼을 클릭하면 결과가 표시됩니다..."',
     'placeholder="Click Convert to see the result..."'),
    ('💡 줄 정렬이나 중복 제거도 필요하다면? <a href="line-tools.html">줄 정렬·중복 제거 →</a>',
     '💡 Need to sort or deduplicate lines? <a href="line-tools.html">Line Tools →</a>'),

    # ── timestamp-converter UI ──
    ('<div style="font-size:0.85rem;opacity:0.9;margin-bottom:6px;">현재 Unix Timestamp (초)</div>',
     '<div style="font-size:0.85rem;opacity:0.9;margin-bottom:6px;">Current Unix Timestamp (seconds)</div>'),
    ('>이 값 사용<', '>Use this value<'),
    ('<div class="result-section-title">🔢 Timestamp → 날짜시간</div>',
     '<div class="result-section-title">🔢 Timestamp → Date/Time</div>'),
    ('<div style="margin-bottom:10px;font-size:0.85rem;color:var(--text-light);">10자리(초) 또는 13자리(밀리초)를 입력하면 자동 감지합니다.</div>',
     '<div style="margin-bottom:10px;font-size:0.85rem;color:var(--text-light);">Enter 10-digit (seconds) or 13-digit (milliseconds) — auto-detected.</div>'),
    ('placeholder="예: 1715230800 (초) 또는 1715230800000 (밀리초)"',
     'placeholder="e.g.: 1715230800 (sec) or 1715230800000 (ms)"'),
    ('<div class="result-card-label">로컬 시간</div>', '<div class="result-card-label">Local Time</div>'),
    ('<div class="result-card-label">상대 시간</div>', '<div class="result-card-label">Relative Time</div>'),
    ('<div class="result-card-label">감지된 단위</div>', '<div class="result-card-label">Detected unit</div>'),
    ('<div class="result-section-title">📅 날짜시간 → Timestamp</div>',
     '<div class="result-section-title">📅 Date/Time → Timestamp</div>'),
    ('<div style="margin-bottom:10px;font-size:0.85rem;color:var(--text-light);">현재 기기의 로컬 시간대 기준으로 변환합니다.</div>',
     '<div style="margin-bottom:10px;font-size:0.85rem;color:var(--text-light);">Converts based on your device\'s local timezone.</div>'),
    ('<div class="result-card-label">초 (seconds)</div>', '<div class="result-card-label">Seconds</div>'),
    ('<div class="result-card-label">밀리초 (milliseconds)</div>', '<div class="result-card-label">Milliseconds</div>'),
    ('💡 해시값이 필요하신가요? <a href="hash-generator.html">해시 생성기 →</a>',
     '💡 Need a hash value? <a href="hash-generator.html">Hash Generator →</a>'),

    # ── number-base UI ──
    ('<div class="base-label">2진수 (Binary)</div>', '<div class="base-label">Binary (Base 2)</div>'),
    ('<div class="base-label">8진수 (Octal)</div>', '<div class="base-label">Octal (Base 8)</div>'),
    ('<div class="base-label">10진수 (Decimal)</div>', '<div class="base-label">Decimal (Base 10)</div>'),
    ('<div class="base-label">16진수 (Hexadecimal)</div>', '<div class="base-label">Hexadecimal (Base 16)</div>'),
    ('<div class="section-title">자주 쓰는 값</div>', '<div class="section-title">Common values</div>'),
    ('<th>비트 수 (Bit Length)</th>', '<th>Bit Length</th>'),
    ('<th>부호 있는 32비트 정수 (Int32)</th>', '<th>Signed 32-bit Int (Int32)</th>'),
    ('<th>IEEE 754 단정밀도 (Float32)</th>', '<th>IEEE 754 Float32</th>'),
    ('<th>IEEE 754 배정밀도 (Float64)</th>', '<th>IEEE 754 Float64</th>'),
    ('💡 텍스트 해시가 필요하신가요? <a href="hash-generator.html">해시 생성기 →</a>',
     '💡 Need a text hash? <a href="hash-generator.html">Hash Generator →</a>'),

    # ── unicode-converter UI ──
    ('placeholder="변환할 텍스트를 입력하세요...&#10;예: 안녕하세요 / Hello 🌍 / 안녕"',
     'placeholder="Enter text to convert...&#10;e.g.: Hello 🌍 / World"'),
    ('>→ 코드포인트<', '>→ Code Points<'),
    ('>← 텍스트로 복원<', '>← Restore to Text<'),
    ('<th>문자</th>', '<th>Char</th>'),
    ('<th>코드포인트</th>', '<th>Code Point</th>'),
    ('💡 HTML 엔티티 변환도 필요하신가요? <a href="html-entity.html">HTML 엔티티 변환기 →</a>',
     '💡 Need HTML entity conversion too? <a href="html-entity.html">HTML Entity →</a>'),

    # ── regex-tester UI ──
    ('placeholder="정규식 패턴을 입력하세요"', 'placeholder="Enter regex pattern"'),
    ('<label><input type="checkbox" id="flagG" checked onchange="updateFlags()"> <code>g</code> 전역</label>',
     '<label><input type="checkbox" id="flagG" checked onchange="updateFlags()"> <code>g</code> global</label>'),
    ('<label><input type="checkbox" id="flagI" onchange="updateFlags()"> <code>i</code> 대소문자 무시</label>',
     '<label><input type="checkbox" id="flagI" onchange="updateFlags()"> <code>i</code> case-insensitive</label>'),
    ('<label><input type="checkbox" id="flagM" onchange="updateFlags()"> <code>m</code> 멀티라인</label>',
     '<label><input type="checkbox" id="flagM" onchange="updateFlags()"> <code>m</code> multiline</label>'),
    ('<button onclick="setPattern(\'[a-zA-Z0-9._%+\\\\-]+@[a-zA-Z0-9.\\\\-]+\\\\.[a-zA-Z]{2,}\')">이메일</button>',
     '<button onclick="setPattern(\'[a-zA-Z0-9._%+\\\\-]+@[a-zA-Z0-9.\\\\-]+\\\\.[a-zA-Z]{2,}\')">Email</button>'),
    ('<button onclick="setPattern(\'01[0-9]-?\\\\d{3,4}-?\\\\d{4}\')">전화번호</button>',
     '<button onclick="setPattern(\'01[0-9]-?\\\\d{3,4}-?\\\\d{4}\')">Phone</button>'),
    ('<button onclick="setPattern(\'[가-힣]+\')">한글만</button>',
     '<button onclick="setPattern(\'[가-힣]+\')">Korean only</button>'),
    ('<button onclick="setPattern(\'\\\\d+\')">숫자만</button>',
     '<button onclick="setPattern(\'\\\\d+\')">Numbers only</button>'),
    ('<button onclick="setPattern(\'\\\\d{4}-\\\\d{2}-\\\\d{2}\')">날짜</button>',
     '<button onclick="setPattern(\'\\\\d{4}-\\\\d{2}-\\\\d{2}\')">Date</button>'),
    ('<button onclick="setPattern(\'\\\\s+\')">공백</button>',
     '<button onclick="setPattern(\'\\\\s+\')">Whitespace</button>'),
    ('<button onclick="setPattern(\'<[^>]+>\')">HTML 태그</button>',
     '<button onclick="setPattern(\'<[^>]+>\')">HTML tag</button>'),
    ('placeholder="테스트할 문자열을 입력하세요...&#10;예: test@email.com 010-1234-5678 https://example.com"',
     'placeholder="Enter test string...&#10;e.g.: test@email.com 010-1234-5678 https://example.com"'),
    ('<span class="match-badge" id="matchCount">0개 매칭</span>',
     '<span class="match-badge" id="matchCount">0 matches</span>'),
    ('<div style="color:var(--text-light); font-size:0.88rem;">패턴과 테스트 문자열을 입력하면 매칭 결과가 표시됩니다.</div>',
     '<div style="color:var(--text-light); font-size:0.88rem;">Enter a pattern and test string to see matches.</div>'),
    ('input type="text" id="replacePattern" placeholder="치환 패턴 (예: $1-$2)"',
     'input type="text" id="replacePattern" placeholder="Replace pattern (e.g. $1-$2)"'),
    ('💡 URL 인코딩/디코딩이 필요하신가요? <a href="url-encoder.html">URL 인코딩 도구 →</a>',
     '💡 Need URL encoding/decoding? <a href="url-encoder.html">URL Encoder →</a>'),

    # ── jwt-decoder UI ──
    ('>🔍 디코딩<', '>🔍 Decode<'),
    ('알고리즘 &amp; 토큰 타입', 'Algorithm &amp; Token Type'),
    ('클레임 데이터', 'Claims Data'),
    ('서명 (Base64URL)', 'Signature (Base64URL)'),
    ('<p style="margin:8px 0 0; font-size:0.8rem; color:#9ca3af;">⚠️ 서명 검증은 지원하지 않습니다. 검증은 서버에서 비밀키로 확인하세요.</p>',
     '<p style="margin:8px 0 0; font-size:0.8rem; color:#9ca3af;">⚠️ Signature verification is not supported. Use a server-side library with your secret key.</p>'),
    ('💡 JSON 데이터를 보기 좋게 정렬하고 싶으신가요? <a href="../json-formatter.html">JSON Formatter →</a>',
     '💡 Want to format JSON data? <a href="../json-formatter.html">JSON Formatter →</a>'),

    # ── xml-formatter UI ──
    ('<label for="indentSelect">들여쓰기:</label>', '<label for="indentSelect">Indent:</label>'),
    ('<option value="2spaces">공백 2칸</option>', '<option value="2spaces">2 spaces</option>'),
    ('<option value="4spaces" selected>공백 4칸</option>', '<option value="4spaces" selected>4 spaces</option>'),
    ('<option value="tab">탭(Tab)</option>', '<option value="tab">Tab</option>'),
    ('placeholder=\'XML을 붙여넣거나 입력하세요...&#10;예: &lt;?xml version="1.0"?&gt;&lt;root&gt;&lt;item id="1"&gt;Hello&lt;/item&gt;&lt;/root&gt;\'',
     'placeholder=\'Paste or enter XML here...&#10;e.g.: &lt;?xml version="1.0"?&gt;&lt;root&gt;&lt;item id="1"&gt;Hello&lt;/item&gt;&lt;/root&gt;\''),
    ('>✨ 예쁘게 정렬<', '>✨ Format<'),
    ('>📦 압축<', '>📦 Minify<'),
    ('>✅ 유효성 검사<', '>✅ Validate<'),
    ('💡 JSON 데이터 정렬이 필요하신가요? <a href="../json-formatter.html">JSON Formatter →</a>',
     '💡 Need to format JSON? <a href="../json-formatter.html">JSON Formatter →</a>'),

    # ── yaml-json UI ──
    ('↔ 양방향 자동 변환', '↔ Auto-detect & Convert'),
    ('>📋 예시 불러오기<', '>📋 Load Example<'),
    ('>🗑️ 전체 지우기<', '>🗑️ Clear All<'),
    ('placeholder="YAML을 입력하세요..." oninput="onYamlInput()"',
     'placeholder="Enter YAML here..." oninput="onYamlInput()"'),
    ('>→ JSON 변환<', '>→ Convert to JSON<'),
    ('placeholder="JSON을 입력하세요..." oninput="onJsonInput()"',
     'placeholder="Enter JSON here..." oninput="onJsonInput()"'),
    ('>→ YAML 변환<', '>→ Convert to YAML<'),

    # ── html-markdown UI ──
    ('<div id="loadingMsg" style="text-align:center;padding:20px;color:var(--text-light);">라이브러리 로딩 중...</div>',
     '<div id="loadingMsg" style="text-align:center;padding:20px;color:var(--text-light);">Loading library...</div>'),
    ('>HTML → 마크다운<', '>HTML → Markdown<'),
    ('>마크다운 → HTML<', '>Markdown → HTML<'),
    ('>🗑️ 초기화<', '>🗑️ Clear<'),
    ('<span class="convert-panel-title">입력</span>', '<span class="convert-panel-title">Input</span>'),
    ('<span class="convert-panel-title">결과</span>', '<span class="convert-panel-title">Result</span>'),
    ('<span class="panel-label label-md" id="outputLabel">마크다운</span>',
     '<span class="panel-label label-md" id="outputLabel">Markdown</span>'),
    ('placeholder="여기에 HTML 또는 마크다운을 입력하세요...',
     'placeholder="Enter HTML or Markdown here...'),
    ('placeholder="변환 버튼을 클릭하면 여기에 결과가 표시됩니다..."',
     'placeholder="Click a button to see the result here..."'),
    ('<p style="font-size:0.8rem;color:var(--text-light);text-align:center;margin:8px 0 0;">💡 HTML→마크다운: Turndown.js 사용 | 마크다운→HTML: marked.js 사용 | 모든 변환은 브라우저 내에서 처리됩니다</p>',
     '<p style="font-size:0.8rem;color:var(--text-light);text-align:center;margin:8px 0 0;">💡 HTML→Markdown: Turndown.js | Markdown→HTML: marked.js | All processing in browser</p>'),
    ('💡 마크다운 실시간 편집이 필요하다면 <a href="markdown-editor.html">마크다운 에디터</a>를 이용하세요.',
     '💡 Need live Markdown editing? Try <a href="markdown-editor.html">Markdown Editor</a>.'),

    # ── markdown-editor UI ──
    ('<button class="active" onclick="showTab(\'editor\')">편집</button>',
     '<button class="active" onclick="showTab(\'editor\')">Edit</button>'),
    ('<button onclick="showTab(\'preview\')">미리보기</button>',
     '<button onclick="showTab(\'preview\')">Preview</button>'),
    ('placeholder="마크다운을 입력하세요..." spellcheck="false"',
     'placeholder="Enter Markdown here..." spellcheck="false"'),
    ('<div class="md-preview-label">미리보기</div>', '<div class="md-preview-label">Preview</div>'),
    ('<span>글자 <strong id="statChars">0</strong></span>', '<span>Chars <strong id="statChars">0</strong></span>'),
    ('<span>단어 <strong id="statWords">0</strong></span>', '<span>Words <strong id="statWords">0</strong></span>'),
    ('<span>줄 <strong id="statLines">0</strong></span>', '<span>Lines <strong id="statLines">0</strong></span>'),
    ('>📂 MD 파일 불러오기<', '>📂 Load MD File<'),
    ('>💾 MD 저장<', '>💾 Save MD<'),
    ('>📋 HTML 복사<', '>📋 Copy HTML<'),
    ('>⬇️ HTML 다운로드<', '>⬇️ Download HTML<'),
    ('클립보드에 복사되었습니다!', 'Copied to clipboard!'),
    ('💡 코드 작업에 유용한 VS Code 확장이 필요하신가요? <a href="https://vskit.wooahouse.com/" target="_blank" rel="noopener">Browse Extensions on WooaVS →</a>',
     '💡 Need useful VS Code extensions? <a href="https://vskit.wooahouse.com/" target="_blank" rel="noopener">Browse Extensions on WooaVS →</a>'),

    # ── morse-code UI ──
    ('<div class="panel-title">변환 도구</div>', '<div class="panel-title">Conversion Tool</div>'),
    ('>📡 텍스트 → 모스부호<', '>📡 Text → Morse<'),
    ('>✏️ 모스부호 → 텍스트<', '>✏️ Morse → Text<'),
    ('>🗑️ 초기화<', '>🗑️ Clear<'),
    ('<span class="morse-panel-title">텍스트</span>', '<span class="morse-panel-title">Text</span>'),
    ('<span class="morse-panel-title">모스부호 ( · 단음, — 장음, / 글자, // 단어)</span>',
     '<span class="morse-panel-title">Morse ( · dit, — dah, / letter, // word)</span>'),
    ('<div style="font-size:0.88rem;font-weight:700;margin-bottom:10px;color:var(--text);">🎵 신호음 재생</div>',
     '<div style="font-size:0.88rem;font-weight:700;margin-bottom:10px;color:var(--text);">🎵 Audio Playback</div>'),
    ('<label style="white-space:nowrap;">재생 속도</label>', '<label style="white-space:nowrap;">Speed</label>'),
    ('<label style="white-space:nowrap;margin-left:12px;">주파수</label>',
     '<label style="white-space:nowrap;margin-left:12px;">Frequency</label>'),
    ('>▶ 재생<', '>▶ Play<'),
    ('>⏹ 정지<', '>⏹ Stop<'),
    ('<div class="panel-title">모스부호 표</div>', '<div class="panel-title">Morse Code Table</div>'),
    ('<div style="font-size:0.82rem;color:var(--text-light);margin-bottom:10px;">· = 단음(dit) &nbsp; — = 장음(dah)</div>',
     '<div style="font-size:0.82rem;color:var(--text-light);margin-bottom:10px;">· = short (dit) &nbsp; — = long (dah)</div>'),
    ('<div style="font-size:0.88rem;font-weight:700;margin-bottom:6px;color:var(--text);">알파벳</div>',
     '<div style="font-size:0.88rem;font-weight:700;margin-bottom:6px;color:var(--text);">Alphabet</div>'),
    ('<div style="font-size:0.88rem;font-weight:700;margin:16px 0 6px;color:var(--text);">숫자</div>',
     '<div style="font-size:0.88rem;font-weight:700;margin:16px 0 6px;color:var(--text);">Numbers</div>'),
    ('<div style="font-size:0.88rem;font-weight:700;margin:16px 0 6px;color:var(--text);">특수문자</div>',
     '<div style="font-size:0.88rem;font-weight:700;margin:16px 0 6px;color:var(--text);">Special chars</div>'),
    ('💡 문자 인코딩 변환이 필요하다면 <a href="unicode-converter.html">유니코드 변환기</a>도 이용해보세요.',
     '💡 Need character encoding conversion? Try <a href="unicode-converter.html">Unicode Converter</a>.'),

    # ── csv-json UI ──
    ('<label><input type="checkbox" id="csvHeader" checked> 첫 행을 헤더로 사용</label>',
     '<label><input type="checkbox" id="csvHeader" checked> Use first row as header</label>'),
    ('<label><input type="checkbox" id="csvNullEmpty"> 빈 값을 null로 처리</label>',
     '<label><input type="checkbox" id="csvNullEmpty"> Treat empty values as null</label>'),
    ('<h3>CSV 입력</h3>', '<h3>CSV Input</h3>'),
    ('<h3>JSON 결과</h3>', '<h3>JSON Result</h3>'),
    ('<h3>JSON 입력</h3>', '<h3>JSON Input</h3>'),
    ('<h3>CSV 결과</h3>', '<h3>CSV Result</h3>'),
    ('>📂 CSV 파일 업로드<', '>📂 Upload CSV<'),
    ('>📂 JSON 파일 업로드<', '>📂 Upload JSON<'),
    ('>⬇️ JSON 다운로드<', '>⬇️ Download JSON<'),
    ('>⬇️ CSV 다운로드<', '>⬇️ Download CSV<'),
    ('>🔄 CSV → JSON 변환<', '>🔄 Convert CSV → JSON<'),
    ('>🔄 JSON → CSV 변환<', '>🔄 Convert JSON → CSV<'),
    ('<div id="copyAlert" class="alert alert-success">클립보드에 복사되었습니다!</div>',
     '<div id="copyAlert" class="alert alert-success">Copied to clipboard!</div>'),
    ('💡 JSON 포맷팅이 필요하신가요? <a href="../json-formatter.html">JSON Formatter →</a>',
     '💡 Need JSON formatting? <a href="../json-formatter.html">JSON Formatter →</a>'),

    # ── text-replacer UI ──
    ('<label for="sourceText" class="form-label">원본 텍스트</label>',
     '<label for="sourceText" class="form-label">Source Text</label>'),
    ('placeholder="치환할 텍스트를 입력하거나 붙여넣으세요..."',
     'placeholder="Enter or paste text to process..."'),
    ('<div class="rules-section-title">치환 규칙</div>', '<div class="rules-section-title">Replacement Rules</div>'),
    ('<span style="flex:1;font-size:0.78rem;color:var(--text-light);font-weight:600;">찾기</span>',
     '<span style="flex:1;font-size:0.78rem;color:var(--text-light);font-weight:600;">Find</span>'),
    ('<span style="flex:1;font-size:0.78rem;color:var(--text-light);font-weight:600;">바꾸기</span>',
     '<span style="flex:1;font-size:0.78rem;color:var(--text-light);font-weight:600;">Replace</span>'),
    ('<span style="width:36px;font-size:0.78rem;color:var(--text-light);font-weight:600;text-align:center;">정규식</span>',
     '<span style="width:36px;font-size:0.78rem;color:var(--text-light);font-weight:600;text-align:center;">Regex</span>'),
    ('<button class="btn-add-rule" id="addRuleBtn">＋ 규칙 추가</button>',
     '<button class="btn-add-rule" id="addRuleBtn">＋ Add rule</button>'),
    ('<span class="rule-hint">규칙은 위에서 아래 순서로 적용됩니다.</span>',
     '<span class="rule-hint">Rules are applied top to bottom.</span>'),
    ('>▶ 치환 실행<', '>▶ Apply Rules<'),
    ('<span class="result-label">결과</span>', '<span class="result-label">Result</span>'),
    ('placeholder="치환 결과가 여기에 표시됩니다..."', 'placeholder="Result will appear here..."'),
    ('<span>🔄 치환 횟수: </span>', '<span>🔄 Replacements: </span>'),

    # ── html-css-editor UI ──
    ('<a href="char-counter.html">글자수</a>', '<a href="char-counter.html">Chars</a>'),
    ('<a href="markdown-editor.html">마크다운</a>', '<a href="markdown-editor.html">Markdown</a>'),
    ('<a href="regex-tester.html">정규식</a>', '<a href="regex-tester.html">Regex</a>'),
    ('<span class="toolbar-title">🖥️ HTML/CSS/JS 에디터</span>',
     '<span class="toolbar-title">🖥️ HTML/CSS/JS Editor</span>'),
    ('>▶ 실행<', '>▶ Run<'),
    ('<option value="">템플릿 선택…</option>', '<option value="">Choose template…</option>'),
    ('<option value="blank">빈 페이지</option>', '<option value="blank">Blank page</option>'),
    ('<option value="flexbox">Flexbox 예제</option>', '<option value="flexbox">Flexbox example</option>'),
    ('<option value="grid">CSS Grid 예제</option>', '<option value="grid">CSS Grid example</option>'),
    ('<option value="animation">CSS 애니메이션</option>', '<option value="animation">CSS animation</option>'),
    ('<option value="card">카드 컴포넌트</option>', '<option value="card">Card component</option>'),
    ('<option value="button">버튼 스타일</option>', '<option value="button">Button styles</option>'),
    ('<option value="darkmode">다크모드 토글</option>', '<option value="darkmode">Dark mode toggle</option>'),
    ('>↔ 수직 레이아웃<', '>↔ Vertical layout<'),
    ('>🔗 URL 공유<', '>🔗 Share URL<'),
    ('>⛶ 미리보기 전체화면<', '>⛶ Fullscreen preview<'),
    ('>🗑 초기화<', '>🗑 Clear<'),
    ('> 자동 실행', '> Auto-run'),
    ('<span>📺 미리보기</span>', '<span>📺 Preview</span>'),
    ('<span id="previewStatus" style="color:#22c55e;">● 준비</span>',
     '<span id="previewStatus" style="color:#22c55e;">● Ready</span>'),
    # html-css-editor footer
    ('<p>HTML·CSS·JS 온라인 에디터. 코드를 작성하고 실시간으로 미리보기. URL로 공유 가능.</p>',
     '<p>Online HTML/CSS/JS editor. Write code with live preview. Share via URL.</p>'),
    ('<h4>코드 & 개발</h4>', '<h4>Code & Dev</h4>'),
    ('<a href="html-css-editor.html">HTML/CSS/JS 에디터</a>', '<a href="html-css-editor.html">HTML/CSS/JS Editor</a>'),
    ('<a href="markdown-editor.html">마크다운 에디터</a>', '<a href="markdown-editor.html">Markdown Editor</a>'),
    ('<a href="regex-tester.html">정규식 테스터</a>', '<a href="regex-tester.html">Regex Tester</a>'),
    ('<a href="csv-json.html">CSV ↔ JSON 변환</a>', '<a href="csv-json.html">CSV ↔ JSON</a>'),
    ('<h4>텍스트 도구</h4>', '<h4>Text Tools</h4>'),
    ('<a href="text-diff.html">텍스트 비교</a>', '<a href="text-diff.html">Text Diff</a>'),
    ('<a href="hash-generator.html">해시 생성기</a>', '<a href="hash-generator.html">Hash Generator</a>'),
    ('<h4>관련 서비스</h4>', '<h4>Related Services</h4>'),
    ('<a href="https://colorkit.wooahouse.com/css-variables.html" target="_blank" rel="noopener">CSS 변수 생성기 →</a>',
     '<a href="https://colorkit.wooahouse.com/css-variables.html" target="_blank" rel="noopener">CSS Variables →</a>'),
    ('<h4>정보</h4>', '<h4>Info</h4>'),
    ('<a href="../about.html">서비스 소개</a>', '<a href="../about.html">About</a>'),

    # ── about.html og: tags ──
    ('<meta property="og:title" content="서비스 소개 | WooaText">',
     '<meta property="og:title" content="About WooaText | Free Online Text Tools">'),
    ('<meta property="og:description" content="글자수 세기·변환·포맷·암호화까지 12가지 텍스트 도구 무료 제공. 회원가입 없이 브라우저에서 바로 사용.">',
     '<meta property="og:description" content="WooaText is a free collection of browser-based text tools. No sign-up required.">'),
    ('<meta property="og:url" content="https://textkit.wooahouse.com/about.html">',
     '<meta property="og:url" content="https://textkit.wooahouse.com/en/about.html">'),

    # ── about.html body content ──
    ('<h1>서비스 소개</h1>', '<h1>About WooaText</h1>'),
    ('<p class="subtitle">WooaText에 대해 알아보세요</p>',
     '<p class="subtitle">Learn about WooaText</p>'),
    ('<h2>✏️ WooaText이란?</h2>', '<h2>✏️ What is WooaText?</h2>'),
    ('<p>WooaText(WooaText)은 개발자, 작가, 학생, 직장인 모두를 위한 무료 온라인 텍스트 도구 모음 서비스입니다.</p>',
     '<p>WooaText is a free online text tools collection for developers, writers, students, and professionals.</p>'),
    ('<p>글자수 세기, 대소문자 변환, URL 인코딩, Base64, JSON 포맷터, 해시 생성 등 12가지 도구를 한 곳에서 편리하게 사용할 수 있습니다. 모든 처리는 브라우저 안에서 이루어지며 텍스트가 서버로 전송되지 않습니다.</p>',
     '<p>Character counter, case converter, URL encoder, Base64, JSON formatter, hash generator, and more — all in one place. All processing happens in your browser; text never leaves your device.</p>'),
    ('<h2>✅ 서비스 특징</h2>', '<h2>✅ Features</h2>'),
    ('<li>회원가입, 로그인 없이 즉시 사용 가능</li>', '<li>No sign-up or login required — use instantly</li>'),
    ('<li>텍스트가 서버로 전송되지 않는 100% 브라우저 처리</li>',
     '<li>100% browser-based — text never sent to any server</li>'),
    ('<li>분석·변환·정리·생성·해시 5개 카테고리 12가지 도구</li>',
     '<li>12+ tools across 5 categories: analysis, convert, clean, generate, hash</li>'),
    ('<li>PC, 태블릿, 스마트폰 모든 기기에서 사용 가능한 반응형 디자인</li>',
     '<li>Responsive design — works on PC, tablet, and smartphone</li>'),
    ('<li>PWA 지원으로 앱처럼 홈 화면에 추가 가능</li>',
     '<li>PWA support — add to home screen like a native app</li>'),
    ('<li>완전 무료, 광고만으로 운영되는 서비스</li>',
     '<li>Completely free, ad-supported service</li>'),
    ('<h2>🛠️ 제공 도구 목록</h2>', '<h2>🛠️ Available Tools</h2>'),
    ('<div class="tools-list-item">🔍 <a href="text-diff.html">텍스트 비교</a></div>',
     '<div class="tools-list-item">🔍 <a href="text-diff.html">Text Diff</a></div>'),
    ('<div class="tools-list-item">🔗 <a href="url-encoder.html">URL 인코딩/디코딩</a></div>',
     '<div class="tools-list-item">🔗 <a href="url-encoder.html">URL Encoder</a></div>'),
    ('<div class="tools-list-item">🔐 <a href="base64.html">Base64 변환</a></div>',
     '<div class="tools-list-item">🔐 <a href="base64.html">Base64</a></div>'),
    ('<div class="tools-list-item">🏷️ <a href="html-entity.html">HTML 엔티티 변환</a></div>',
     '<div class="tools-list-item">🏷️ <a href="html-entity.html">HTML Entity</a></div>'),
    ('<div class="tools-list-item">📋 <a href="line-tools.html">줄 정렬·중복 제거</a></div>',
     '<div class="tools-list-item">📋 <a href="line-tools.html">Line Tools</a></div>'),
    ('<div class="tools-list-item">⬜ <a href="whitespace.html">공백 제거·정리</a></div>',
     '<div class="tools-list-item">⬜ <a href="whitespace.html">Whitespace</a></div>'),
    ('<div class="tools-list-item">📝 <a href="lorem-ipsum.html">Lorem Ipsum 생성</a></div>',
     '<div class="tools-list-item">📝 <a href="lorem-ipsum.html">Lorem Ipsum</a></div>'),
    ('<div class="tools-list-item">🔑 <a href="password-generator.html">비밀번호 생성기</a></div>',
     '<div class="tools-list-item">🔑 <a href="password-generator.html">Password Generator</a></div>'),
    ('<div class="tools-list-item">#️⃣ <a href="hash-generator.html">해시 생성기</a></div>',
     '<div class="tools-list-item">#️⃣ <a href="hash-generator.html">Hash Generator</a></div>'),
    ('<h2>🏠 WooaHouse 네트워크</h2>', '<h2>🏠 WooaHouse Network</h2>'),
    ('<p>WooaText은 WooaHouse가 운영하는 서비스 중 하나입니다. 현재 운영 중인 서비스:</p>',
     '<p>WooaText is one of the services operated by WooaHouse. Currently available services:</p>'),
    ('<h2>📬 문의</h2>', '<h2>📬 Contact</h2>'),
    ('<p>도구 추가 요청, 오류 제보, 제휴 문의 등은 아래 이메일로 연락 주세요.</p>',
     '<p>For tool requests, bug reports, or partnership inquiries, please contact us at:</p>'),
    ('<p>© 2026 WooaText by WooaHouse. 모든 권리 보유.</p>',
     '<p>© 2026 WooaText by WooaHouse. All rights reserved.</p>'),

    # ── privacy.html body content ──
    ('<p class="updated">최종 업데이트: 2026년 3월 15일</p>',
     '<p class="updated">Last updated: March 15, 2026</p>'),
    ('<h2>1. 개인정보 수집 여부</h2>', '<h2>1. Personal Information Collection</h2>'),
    ('<p>WooaText(textkit.wooahouse.com)은 회원가입, 로그인 등의 기능이 없으며, 사용자의 개인정보를 직접 수집하지 않습니다. 본 서비스는 정적 웹사이트로 운영되며, 입력된 텍스트는 브라우저 내에서만 처리되고 서버로 전송되지 않습니다.</p>',
     '<p>WooaText (textkit.wooahouse.com) does not have sign-up or login features and does not directly collect personal information. This service is a static website; entered text is processed only within the browser and never transmitted to a server.</p>'),
    ('<h2>2. 제3자 서비스</h2>', '<h2>2. Third-Party Services</h2>'),
    ('<p>WooaText은 아래 제3자 서비스를 사용하며, 각 서비스의 개인정보 처리방침이 적용됩니다.</p>',
     '<p>WooaText uses the following third-party services. Each service\'s own privacy policy applies.</p>'),
    ('<li><strong>Google AdSense:</strong> 광고 게재를 위해 사용됩니다. Google은 쿠키를 통해 광고 관련 정보를 수집할 수 있습니다.</li>',
     '<li><strong>Google AdSense:</strong> Used for ad serving. Google may collect advertising-related information via cookies.</li>'),
    ('<li><strong>Google Analytics (해당 시):</strong> 익명화된 방문 통계 수집에 사용될 수 있습니다.</li>',
     '<li><strong>Google Analytics (if applicable):</strong> May be used to collect anonymized visit statistics.</li>'),
    ('<h2>3. 쿠키</h2>', '<h2>3. Cookies</h2>'),
    ('<p>WooaText은 자체적으로 쿠키를 사용하지 않습니다. 다만 Google AdSense 등 제3자 서비스에서 광고 목적으로 쿠키를 사용할 수 있습니다. 브라우저 설정에서 쿠키를 비활성화할 수 있습니다.</p>',
     '<p>WooaText does not use its own cookies. However, third-party services such as Google AdSense may use cookies for advertising purposes. You can disable cookies in your browser settings.</p>'),
    ('<h2>4. 입력 데이터 처리</h2>', '<h2>4. Input Data Processing</h2>'),
    ('<p>WooaText의 모든 도구(글자수 세기, URL 인코딩, 해시 생성 등)는 사용자가 입력한 텍스트를 브라우저 내부에서만 처리합니다. 입력 데이터는 어떠한 서버에도 저장되거나 전송되지 않습니다.</p>',
     '<p>All WooaText tools (character counter, URL encoder, hash generator, etc.) process text only within your browser. Input data is never stored or transmitted to any server.</p>'),
    ('<h2>5. 문의</h2>', '<h2>5. Contact</h2>'),
    ('<p>개인정보 처리방침 관련 문의는 아래 이메일로 연락 주세요.</p>',
     '<p>For inquiries regarding this privacy policy, please contact us at:</p>'),

    # ── html lang attribute ──
    ('<html lang="ko">', '<html lang="en">'),

    # ── yaml-json FAQ (Korean FAQ not replaced by build_page since no PAGE_META faq) ──
    ('>YAML과 JSON의 차이는 무엇인가요?<', '>What is the difference between YAML and JSON?<'),
    ('<p>YAML은 들여쓰기 기반으로 사람이 읽기 쉽고, JSON은 중괄호 기반으로 프로그램이 파싱하기 쉽습니다. YAML은 주석을 지원하고 더 간결하지만, JSON은 언어 표준 지원이 더 넓습니다.</p>',
     '<p>YAML is indentation-based and human-readable; JSON uses braces and is easily parsed by programs. YAML supports comments and is more concise, but JSON has broader language support.</p>'),
    ('>주석이 있는 YAML도 변환되나요?<', '>Are YAML comments converted too?<'),
    ('<p>YAML 주석(#으로 시작)은 JSON으로 변환 시 제거됩니다. JSON은 주석을 지원하지 않습니다. 주석 내용을 보존하려면 별도로 관리해야 합니다.</p>',
     '<p>YAML comments (starting with #) are removed when converting to JSON. JSON does not support comments. Preserve comment content separately if needed.</p>'),
    ('>YAML 들여쓰기는 몇 칸으로 변환되나요?<', '>How many spaces does YAML indentation use?<'),
    ('<p>JSON→YAML 변환 시 기본 2칸 들여쓰기로 생성됩니다. JSON 역시 2칸 들여쓰기로 포맷팅됩니다.</p>',
     '<p>JSON→YAML conversion uses 2-space indentation by default. JSON is also formatted with 2-space indentation.</p>'),

    # ── 구조화 데이터 HTML 주석 (여러 파일 공통) ──
    ('<!-- 구조화 데이터 -->', '<!-- Structured Data -->'),

    # ── 공통: 결과 — XYZ (구체적인 것을 먼저) ──
    ('결과 — Base64 인코딩', 'Result — Base64 Encode'),
    ('결과 — Base64 디코딩', 'Result — Base64 Decode'),
    ('결과 — HTML 엔티티 인코딩', 'Result — HTML Entity Encode'),
    ('결과 — HTML 엔티티 디코딩', 'Result — HTML Entity Decode'),
    ('결과 — URL 인코딩', 'Result — URL Encode'),
    ('결과 — URL 디코딩', 'Result — URL Decode'),
    ('결과 — 예쁘게 정렬', 'Result — Pretty Print'),
    ('결과 — 압축 (Minify)', 'Result — Minified'),
    ('결과 — 압축', 'Result — Minified'),
    ('결과 — ${caseNames[type]}', 'Result — ${caseNames[type]}'),
    ('결과 — ${langLabels[lang]} ${count}개 ${typeLabels[type]}', 'Result — ${langLabels[lang]} ${count} ${typeLabels[type]}'),
    ('결과 — Unicode escape (\\\\uXXXX)', 'Result — Unicode Escape (\\\\uXXXX)'),
    ('결과 — HTML entity (&#XXXX;)', 'Result — HTML Entity (&#XXXX;)'),
    ('결과 — 코드포인트 (U+XXXX)', 'Result — Codepoint (U+XXXX)'),
    ('결과 — 복원된 텍스트', 'Result — Restored Text'),
    ("'결과 — '", "'Result — '"),
    ("textContent = '결과'", "textContent = 'Result'"),
    ('<div class="text-panel-title" style="margin-bottom:16px;">결과</div>',
     '<div class="text-panel-title" style="margin-bottom:16px;">Result</div>'),
    ('<div class="text-panel-title" style="margin-bottom:0;">결과</div>',
     '<div class="text-panel-title" style="margin-bottom:0;">Result</div>'),
    ('"id="outputLabel">결과</div>', '"id="outputLabel">Result</div>'),
    ('id="outputLabel">결과<', 'id="outputLabel">Result<'),

    # ── 공통: 지우기 버튼 ──
    ('>🗑️ 지우기<', '>🗑️ Clear<'),

    # ── 공통: 복사됨 버튼 상태 ──
    ("'✅ 복사됨'", "'✅ Copied'"),
    ("'복사됨!'", "'Copied!'"),
    ('>복사됨!<', '>Copied!<'),

    # ── base64.html ──
    ('인코딩 중 오류가 발생했습니다: ', 'Encoding error: '),
    ('디코딩 중 오류가 발생했습니다. 유효한 Base64 형식인지 확인하세요.', 'Decoding error. Please verify it is a valid Base64 string.'),

    # ── url-encoder.html ──
    ('인코딩 중 오류가 발생했습니다: ', 'Encoding error: '),
    ('디코딩 중 오류가 발생했습니다. 유효한 URL 인코딩 형식인지 확인하세요.', 'Decoding error. Please verify it is a valid URL-encoded string.'),

    # ── json-formatter.html ──
    ('유효하지 않은 JSON입니다: ', 'Invalid JSON: '),
    ("showValidation(true, '유효한 JSON입니다.')", "showValidation(true, 'Valid JSON.')"),

    # ── xml-formatter.html ──
    ('유효하지 않은 XML입니다: ', 'Invalid XML: '),
    ("showValidation(true, '유효한 XML입니다.')", "showValidation(true, 'Valid XML.')"),
    ('// 닫는 태그면 레벨 감소 후 출력', '// Closing tag: decrease level then output'),
    ('// XML 선언 / DOCTYPE / 주석 / CDATA / 자기닫힘 태그 / 인라인 태그', '// XML declaration / DOCTYPE / comment / CDATA / self-closing / inline'),
    ('// 여는 태그', '// Opening tag'),
    ('// 텍스트 노드', '// Text node'),
    ('// XML 선언/프롤로그: <?xml ... ?>', '// XML declaration/prolog: <?xml ... ?>'),
    ('// 주석: <!-- ... -->', '// Comment: <!-- ... -->'),
    ('// 속성값 "..." (먼저 치환)', '// Attribute value "..." (replace first)'),
    ('// 속성명 (속성값 앞에 위치한 단어)', '// Attribute name (word before attribute value)'),
    ('// 여는/닫는 태그명', '// Opening/closing tag name'),

    # ── hash-generator.html ──
    ('>#️⃣ 해시 생성<', '>#️⃣ Generate Hash<'),
    ("'❌ 해시를 생성할 텍스트를 입력해주세요.'", "'❌ Enter text to generate a hash.'"),
    ("'❌ 최소 하나의 알고리즘을 선택해주세요.'", "'❌ Select at least one algorithm.'"),
    ("'⏳ 해시 생성 중...'", "'⏳ Generating hash...'"),
    ("'❌ 해시 생성 중 오류: ", "'❌ Hash generation error: "),

    # ── password-generator.html ──
    ("'❌ 최소 하나의 문자 종류를 선택해주세요.'", "'❌ Select at least one character type.'"),
    ("strength = '약함 (Weak)'", "strength = 'Weak'"),
    ("strength = '보통 (Medium)'", "strength = 'Medium'"),
    ("strength = '강함 (Strong)'", "strength = 'Strong'"),
    ("strength = '매우 강함 (Very Strong)'", "strength = 'Very Strong'"),
    ("label.textContent = '강도: ' + strength", "label.textContent = 'Strength: ' + strength"),
    ('<label for="optSpecial">특수문자 (!@#$%^&*)</label>', '<label for="optSpecial">Special chars (!@#$%^&*)</label>'),
    ('? 최소 1개 이상 선택', '? Select at least one'),

    # ── timestamp-converter.html ──
    ("const suffix = diffSec < 0 ? '전' : '후'", "const suffix = diffSec < 0 ? 'ago' : 'later'"),
    ("return abs + '초 ' + suffix", "return abs + 's ' + suffix"),
    ("return Math.round(abs / 60) + '분 ' + suffix", "return Math.round(abs / 60) + 'min ' + suffix"),
    ("return Math.round(abs / 3600) + '시간 ' + suffix", "return Math.round(abs / 3600) + 'hr ' + suffix"),
    ("return Math.round(abs / 86400) + '일 ' + suffix", "return Math.round(abs / 86400) + 'd ' + suffix"),
    ("return Math.round(abs / 2592000) + '개월 ' + suffix", "return Math.round(abs / 2592000) + 'mo ' + suffix"),
    ("return Math.round(abs / 31536000) + '년 ' + suffix", "return Math.round(abs / 31536000) + 'yr ' + suffix"),
    ("'❌ Timestamp 값을 입력해주세요.'", "'❌ Please enter a Timestamp value.'"),
    ("'❌ 유효한 숫자를 입력해주세요.'", "'❌ Please enter a valid number.'"),
    ("'❌ 변환할 수 없는 값입니다. 10자리(초) 또는 13자리(밀리초)를 입력해주세요.'",
     "'❌ Cannot convert this value. Enter 10-digit (seconds) or 13-digit (milliseconds).'"),
    ("? '밀리초(milliseconds) — 13자리 감지'", "? 'Milliseconds (ms) — 13-digit detected'"),
    (": '초(seconds) — 10자리 감지';", ": 'Seconds (s) — 10-digit detected';"),
    ("'❌ 날짜와 시간을 선택해주세요.'", "'❌ Please select a date and time.'"),
    ("'❌ 유효한 날짜/시간이 아닙니다.'", "'❌ Invalid date/time.'"),
    ('// 실시간 현재 시각', '// Live current time'),
    ('// 현재 timestamp를 입력 필드에 적용', '// Apply current timestamp to input field'),
    ('// 초/밀리초 자동 감지', '// Auto-detect seconds/milliseconds'),
    ('// 상대 시간 계산', '// Relative time calculation'),
    ('// Timestamp → 날짜시간 변환', '// Timestamp → datetime conversion'),
    ('// 날짜시간 → Timestamp 변환', '// Datetime → timestamp conversion'),
    ('// 복사 버튼', '// Copy button'),
    ('// datetime-local 기본값: 현재 시각', '// datetime-local default: current time'),

    # ── jwt-decoder.html ──
    ('<!-- Header 카드 -->', '<!-- Header Card -->'),
    ('<!-- Payload 카드 -->', '<!-- Payload Card -->'),
    ('<!-- Signature 카드 -->', '<!-- Signature Card -->'),
    ('// ── JWT 디코딩 ──', '// ── JWT Decoding ──'),
    ("'JWT 형식이 올바르지 않습니다 (헤더.페이로드.서명 3부분 필요)'",
     "'JWT format is invalid (header.payload.signature — 3 parts required)'"),
    ('// ── 문자열 이스케이프 & 구문 강조 ──', '// ── String Escape & Syntax Highlight ──'),
    ('// ── exp 만료 정보 렌더 ──', '// ── exp Expiry Info Render ──'),
    ('// 남은/경과 시간 계산', '// Calculate remaining/elapsed time'),
    ("diffStr += days + '일 '", "diffStr += days + 'd '"),
    ("diffStr += hours + '시간 '", "diffStr += hours + 'h '"),
    ("diffStr += minutes + '분 '", "diffStr += minutes + 'm '"),
    ("diffStr += seconds + '초'", "diffStr += seconds + 's'"),
    ('// 한국시간(KST = UTC+9) 포맷', '// KST (UTC+9) format'),
    ("isExpired ? '만료됨' : '유효'", "isExpired ? 'Expired' : 'Valid'"),
    ("isExpired ? '경과 시간' : '남은 시간'", "isExpired ? 'Elapsed' : 'Remaining'"),
    ('만료 정보 — <strong>', 'Expiry Info — <strong>'),
    ('<span class="exp-label">만료 일시</span>', '<span class="exp-label">Expires</span>'),
    ('// ── 메인 디코딩 & 렌더 ──', '// ── Main Decode & Render ──'),
    ('// ── 복사 ──', '// ── Copy ──'),
    ('// ── 지우기 ──', '// ── Clear ──'),
    ('// ── Enter 키 지원 ──', '// ── Enter Key Support ──'),

    # ── line-tools.html JS opNames ──
    ("'sort-asc': '오름차순 정렬'", "'sort-asc': 'Sort A→Z'"),
    ("'sort-desc': '내림차순 정렬'", "'sort-desc': 'Sort Z→A'"),
    ("'dedup': '중복 줄 제거'", "'dedup': 'Remove Duplicates'"),
    ("'remove-empty': '빈 줄 제거'", "'remove-empty': 'Remove Blank Lines'"),
    ("'reverse': '줄 순서 뒤집기'", "'reverse': 'Reverse Lines'"),
    ("'shuffle': '줄 섞기'", "'shuffle': 'Shuffle Lines'"),

    # ── whitespace.html JS opNames ──
    ("'trim-each': '각 줄 앞뒤 공백 제거'", "'trim-each': 'Trim each line'"),
    ("'collapse': '연속 공백 하나로'", "'collapse': 'Collapse spaces'"),
    ("'remove-all': '모든 공백 제거'", "'remove-all': 'Remove all spaces'"),
    ("'tab-to-space': '탭→스페이스 변환'", "'tab-to-space': 'Tab→Space'"),
    ("'trim-all': '전체 앞뒤 공백 제거'", "'trim-all': 'Trim all'"),

    # ── text-diff.html JS ──
    ("'+ ${addCount}줄 추가'", "'+ ${addCount} lines added'"),
    ("'- ${removeCount}줄 삭제'", "'- ${removeCount} lines removed'"),
    ("'= ${sameCount}줄 동일'", "'= ${sameCount} lines same'"),
    ("`+ ${addCount}줄 추가`", "`+ ${addCount} lines added`"),
    ("`- ${removeCount}줄 삭제`", "`- ${removeCount} lines removed`"),
    ("`= ${sameCount}줄 동일`", "`= ${sameCount} lines same`"),

    # ── text-stats.html ──
    ('<th>순위</th>', '<th>Rank</th>'),
    ('<th>단어</th>', '<th>Word</th>'),
    ('<th>횟수</th>', '<th>Count</th>'),
    ('<th>비율</th>', '<th>Ratio</th>'),
    ("'<div class=\"freq-empty\">단어를 입력하면 빈도를 분석합니다.</div>'",
     "'<div class=\"freq-empty\">Enter text to analyze word frequency.</div>'"),
    ("`약 ${mins}분`", "`~${mins} min`"),
    ("'이','그','저','이것','그것','저것','은','는','가','을','를',",
     "'i','the','a','this','that','those','is','are','was','were','has',"),
    ("'에','에서','로','으로','와','과','도','만','보다','같이',",
     "'have','had','do','does','did','will','would','could','should','may',"),
    ("'처럼','이다','있다','없다','하다','되다','것','수','때',",
     "'might','shall','be','been','being','and','or','but','not','in',"),
    ("'한','등','및','또','또한','하지만','그러나','그리고','그래서',",
     "'on','at','by','for','with','about','to','from','of','as',"),
    ("'즉','따라서','그런데','하여','위해','대해','대한','통해','관한'",
     "'so','if','when','then','than','while','after','before','it','its'"),

    # ── regex-tester.html ──
    ('<!-- 플래그 섹션 -->', '<!-- Flags Section -->'),
    ('<!-- 퀵패턴 섹션 -->', '<!-- Quick Patterns Section -->'),
    ("onclick=\"setPattern('[가-힣]+')\"", "onclick=\"setPattern('[가-힣]+')\""),
    ('<!-- 테스트 입력 -->', '<!-- Test Input -->'),
    ('<!-- 치환 섹션 -->', '<!-- Replace Section -->'),
    ('<div class="text-panel-title" style="margin-bottom:0;">치환 결과</div>',
     '<div class="text-panel-title" style="margin-bottom:0;">Replace Result</div>'),
    ('<span class="text-panel-title" style="margin-bottom:0;">매칭 결과</span>',
     '<span class="text-panel-title" style="margin-bottom:0;">Match Result</span>'),
    ('<div class="replace-result" id="replaceResult">치환 패턴을 입력하면 결과가 표시됩니다.</div>',
     '<div class="replace-result" id="replaceResult">Enter a replace pattern to see the result.</div>'),
    ("|| '(없음)'", "|| '(none)'"),
    ("'<div style=\"color:var(--text-light);font-size:0.88rem;\">패턴을 입력하세요.</div>'",
     "'<div style=\"color:var(--text-light);font-size:0.88rem;\">Enter a pattern.</div>'"),
    ("'0개 매칭'", "'0 matches'"),
    ("'치환 패턴을 입력하면 결과가 표시됩니다.'",
     "'Enter a replace pattern to see the result.'"),
    ("'유효하지 않은 정규식: '", "'Invalid regex: '"),
    ("matchCountEl.textContent = '오류'", "matchCountEl.textContent = 'Error'"),
    ("'<div style=\"color:var(--text-light);font-size:0.88rem;\">테스트 문자열을 입력하세요.</div>'",
     "'<div style=\"color:var(--text-light);font-size:0.88rem;\">Enter test string.</div>'"),
    ("matches.length + '개 매칭'", "matches.length + ' matches'"),
    ("`<div class=\"match-label\">매칭 #${i + 1} (인덱스: ${match.index})</div>`",
     "`<div class=\"match-label\">Match #${i + 1} (index: ${match.index})</div>`"),
    ("html += '<div class=\"match-groups\">그룹: '",
     "html += '<div class=\"match-groups\">Groups: '"),
    ("g !== undefined ? escapeHtml(g) : '(없음)'",
     "g !== undefined ? escapeHtml(g) : '(none)'"),
    ("'<div style=\"color:var(--text-light);font-size:0.88rem;\">매칭되는 결과가 없습니다.</div>'",
     "'<div style=\"color:var(--text-light);font-size:0.88rem;\">No matches found.</div>'"),
    ("replaceResultEl.textContent = '치환 오류: ' + e.message",
     "replaceResultEl.textContent = 'Replace error: ' + e.message"),

    # ── text-replacer.html ──
    ('<!-- 상단 AdSense -->', '<!-- Top AdSense -->'),
    ('<!-- 하단 AdSense -->', '<!-- Bottom AdSense -->'),
    ('<!-- 원본 텍스트 -->', '<!-- Source Text -->'),
    ('<!-- 치환 규칙 -->', '<!-- Replace Rules -->'),
    ('<!-- 열 헤더 -->', '<!-- Column Headers -->'),
    ('<!-- 오류 메시지 -->', '<!-- Error Message -->'),
    ('<!-- 실행 버튼 -->', '<!-- Run Button -->'),
    ('<!-- 결과 -->', '<!-- Result -->'),
    ('<p class="tool-desc">단어·문장을 한번에 치환합니다. 정규식 모드와 대소문자 무시 옵션을 규칙별로 설정하고, 여러 규칙을 순서대로 일괄 적용할 수 있습니다.</p>',
     '<p class="tool-desc">Replace words and sentences in bulk. Set regex mode and case-insensitive options per rule, and apply multiple rules in order.</p>'),
    ('<div class="rules-section-title">치환 규칙</div>', '<div class="rules-section-title">Replace Rules</div>'),
    ('<span style="flex:1;font-size:0.78rem;color:var(--text-light);font-weight:600;">찾기</span>',
     '<span style="flex:1;font-size:0.78rem;color:var(--text-light);font-weight:600;">Find</span>'),
    ('<span style="flex:1;font-size:0.78rem;color:var(--text-light);font-weight:600;">바꾸기</span>',
     '<span style="flex:1;font-size:0.78rem;color:var(--text-light);font-weight:600;">Replace</span>'),
    ('<span style="width:36px;font-size:0.78rem;color:var(--text-light);font-weight:600;text-align:center;">정규식</span>',
     '<span style="width:36px;font-size:0.78rem;color:var(--text-light);font-weight:600;text-align:center;">Regex</span>'),
    ('<button class="btn-add-rule" id="addRuleBtn">＋ 규칙 추가</button>', '<button class="btn-add-rule" id="addRuleBtn">＋ Add Rule</button>'),
    ('<span class="rule-hint">규칙은 위에서 아래 순서로 적용됩니다.</span>',
     '<span class="rule-hint">Rules are applied top to bottom.</span>'),
    ('<span class="result-label">결과</span>', '<span class="result-label">Result</span>'),
    ('🔄 치환 횟수: <span id="countNum">0</span>개',
     '🔄 Replacements: <span id="countNum">0</span>'),
    ('<input class="rule-find" type="text" placeholder="찾기..." autocomplete="off" spellcheck="false">',
     '<input class="rule-find" type="text" placeholder="Find..." autocomplete="off" spellcheck="false">'),
    ('<input class="rule-replace" type="text" placeholder="바꾸기..." autocomplete="off" spellcheck="false">',
     '<input class="rule-replace" type="text" placeholder="Replace..." autocomplete="off" spellcheck="false">'),
    ('<button class="rule-regex-btn toggle-btn" title="정규식 모드 (.*)" aria-pressed="false">.*</button>',
     '<button class="rule-regex-btn toggle-btn" title="Regex mode (.*)" aria-pressed="false">.*</button>'),
    ('<button class="rule-del-btn" title="이 규칙 삭제">✕</button>',
     '<button class="rule-del-btn" title="Delete this rule">✕</button>'),
    ('// toggle 버튼 이벤트', '// toggle button event'),
    ('// 삭제 버튼 이벤트', '// delete button event'),
    ('// 마지막 규칙이면 초기화만', '// if last rule, just reset'),
    ('// Enter 키로 치환 실행', '// run replace on Enter key'),
    ('// 초기 1개 행 추가', '// add initial rule row'),
    ('// 규칙 추가 버튼', '// add rule button'),
    ('// 새 행의 찾기 필드로 포커스', '// focus find field of new row'),
    ('// --- 치환 로직 ---', '// --- Replace Logic ---'),
    ("`규칙 ${idx + 1}: 잘못된 정규식 — ${e.message}`",
     "`Rule ${idx + 1}: invalid regex — ${e.message}`"),
    ('// --- 규칙 수집 ---', '// --- Collect Rules ---'),
    ('// --- 치환 실행 ---', '// --- Run Replace ---'),
    ("'원본 텍스트를 입력해 주세요.'", "'Please enter the source text.'"),
    ("'치환할 찾기 값을 최소 하나 이상 입력해 주세요.'", "'Enter at least one Find value.'"),
    ('// --- 지우기 ---', '// --- Clear ---'),
    ('// 규칙 초기화', '// reset rules'),
    ('// --- 복사 ---', '// --- Copy ---'),

    # ── number-base.html ──
    ("'이진수'", "'Binary'"),
    ("'8진수'", "'Octal'"),
    ("'10진수'", "'Decimal'"),
    ("'16진수'", "'Hex'"),
    ("'입력값이 안전한 정수 범위(2^53-1)를 초과합니다.'",
     "'Value exceeds safe integer range (2^53-1).'"),
    ("`올바른 ${labels[fromBase]} 형식이 아닙니다.`",
     "`Invalid ${labels[fromBase]} format.`"),
    ('// 비트 수', '// Bit count'),
    ('// 부호 있는 32비트 정수', '// Signed 32-bit integer'),
    ('// 비트 OR로 Int32 변환', '// Convert to Int32 via bitwise OR'),
    ("(int32 !== decimal ? ' (※ 32비트 오버플로우)' : '')",
     "(int32 !== decimal ? ' (※ 32-bit overflow)' : '')"),
    ('// 이벤트 연결', '// Bind events'),
    ('// 퀵버튼', '// Quick buttons'),
    ('// 복사', '// Copy'),
    ("btn.textContent = '복사됨!'", "btn.textContent = 'Copied!'"),
    ("btn.textContent = '복사'", "btn.textContent = 'Copy'"),

    # ── slug-generator.html ──
    ('/* ── 한글 음역 테이블 ── */', '/* ── Hangul Romanization Table ── */'),
    ('/* 한글 처리 */', '/* Hangul processing */'),
    ('/* 자모 단독 문자 제거 */', '/* Remove standalone jamo characters */'),
    ('/* hangul === \'keep\' 는 그대로 */', '/* hangul === \'keep\': keep as-is */'),
    ('/* 대소문자 */', '/* Case */'),
    ('/* 한글 그대로 옵션이 아닐 때 비ASCII·비단어 문자 제거 */', '/* Remove non-ASCII/non-word chars unless hangul=keep */'),
    ('/* keep 모드: ASCII 특수문자(단어/공백/한글 제외) 제거 */', '/* keep mode: remove non-ASCII specials (except word/space/hangul) */'),
    ('/* 숫자 제거 */', '/* Remove digits */'),
    ('/* 공백·구분자 정규화 */', '/* Normalize spaces/separators */'),
    ("resultEl.textContent = '텍스트를 입력하면 슬러그가 실시간으로 생성됩니다.'",
     "resultEl.textContent = 'Enter text to generate slug in real time.'"),
    ("resultEl.textContent = '(결과 없음 — 옵션을 조정해보세요)'",
     "resultEl.textContent = '(No result — try adjusting the options)'"),
    ("`${slug.length}자`", "`${slug.length} chars`"),
    ("btn.textContent = '복사됨!'", "btn.textContent = 'Copied!'"),
    ("btn.textContent = '복사'", "btn.textContent = 'Copy'"),
    ('/* 페이지 로드 시 초기화 */', '/* Initialize on page load */'),

    # ── line-numbering.html ──
    ('// 형식 버튼 클릭', '// Format button click'),
    ('// 숫자 형식 여부', '// Is numeric format'),
    ('// 패딩 계산: 번호가 매겨질 줄 수 기준', '// Padding: based on total numbered lines'),
    ('// include: 빈 줄도 번호 부여', '// include: number blank lines too'),
    ('// 기호 형식: -, •, ▸, ★', '// Symbol format: -, •, ▸, ★'),

    # ── lorem-ipsum.html ──
    ("'이 텍스트는 디자인 시안이나 개발 테스트를 위한 더미 텍스트입니다.',",
     "'This text is dummy content for design mockups or development testing.',"),
    ("'실제 콘텐츠가 들어갈 자리를 임시로 채우기 위해 사용됩니다.',",
     "'It is used to temporarily fill the space where real content will go.',"),
    ("'텍스트의 레이아웃과 글꼴이 어떻게 보이는지 확인할 수 있습니다.',",
     "'You can check how the text layout and font appear.',"),
    ("'실제 내용이 아닌 placeholder 텍스트로, 완성 전에 대체될 예정입니다.',",
     "'This is placeholder text, not real content — it will be replaced before completion.',"),
    ("'좋은 디자인은 내용을 명확하게 전달하고 사용자 경험을 향상시킵니다.',",
     "'Good design communicates content clearly and enhances user experience.',"),
    ("'이 문장은 한국어 더미 텍스트 생성기로 만들어진 샘플 문장입니다.',",
     "'This sentence is a sample generated by the Korean dummy text generator.',"),
    ("'프로젝트 초기 단계에서 텍스트 배치를 시뮬레이션하는 데 유용합니다.',",
     "'It is useful for simulating text placement in the early stages of a project.',"),
    ("'글꼴 크기와 줄 간격이 실제 환경에서 어떻게 보이는지 미리 확인하세요.',",
     "'Preview how font size and line spacing look in a real environment.',"),
    ("'사용자 인터페이스 설계 시 실제 텍스트 양과 유사하게 작성해야 합니다.',",
     "'When designing a UI, write text that approximates the actual content volume.',"),
    ("'웹사이트나 앱 화면을 구성할 때 이런 더미 텍스트가 도움이 됩니다.',",
     "'This dummy text is helpful when composing website or app layouts.',"),
    ("'텍스트 영역의 크기와 여백을 조정할 때 참고용으로 활용하십시오.',",
     "'Use it as reference when adjusting text area size and margins.',"),
    ("'브라우저에서 렌더링 결과를 바로 확인할 수 있는 편리한 도구입니다.',",
     "'It is a handy tool for immediately checking rendering results in a browser.',"),
    ("'한국어 폰트의 가독성과 행간을 테스트하는 데 적합한 문장들입니다.',",
     "'These sentences are suitable for testing the readability and line spacing of Korean fonts.',"),
    ("'실제 프로젝트에 투입되기 전에 충분한 테스트를 거쳐야 합니다.',",
     "'Sufficient testing must be done before deploying to a real project.',"),
    ("'디자이너와 개발자 모두에게 유용한 더미 텍스트 도구를 제공합니다.',",
     "'We provide a dummy text tool useful for both designers and developers.',"),
    ("'텍스트','디자인','개발','테스트','콘텐츠','레이아웃','인터페이스','사용자','경험',",
     "'text','design','develop','test','content','layout','interface','user','experience',"),
    ("'프로젝트','시스템','서비스','기능','버튼','화면','데이터','정보','처리','변환',",
     "'project','system','service','feature','button','screen','data','info','process','convert',"),
    ("'결과','입력','출력','설정','관리','분석','검색','저장','삭제','수정','확인',",
     "'result','input','output','setting','manage','analyze','search','save','delete','edit','confirm',"),
    ("'도구','방법','과정','단계','목록','항목','선택','적용','실행','완료',",
     "'tool','method','process','step','list','item','select','apply','run','complete',"),
    ("const typeLabels = { paragraphs: '단락', sentences: '문장', words: '단어' };",
     "const typeLabels = { paragraphs: 'paragraphs', sentences: 'sentences', words: 'words' };"),
    ("const langLabels = { latin: 'Latin', korean: '한국어' };",
     "const langLabels = { latin: 'Latin', korean: 'Korean' };"),

    # ── markdown-editor.html ──
    ("title=\"굵게\"", "title=\"Bold\""),
    ("title=\"기울임\"", "title=\"Italic\""),
    ("title=\"취소선\"", "title=\"Strikethrough\""),
    ("title=\"제목1\"", "title=\"Heading1\""),
    ("title=\"제목2\"", "title=\"Heading2\""),
    ("title=\"제목3\"", "title=\"Heading3\""),
    ("title=\"링크\"", "title=\"Link\""),
    ("title=\"이미지\"", "title=\"Image\""),
    ("title=\"인라인 코드\"", "title=\"Inline Code\""),
    ("title=\"코드 블록\"", "title=\"Code Block\""),
    ("title=\"표\"", "title=\"Table\""),
    ("title=\"수평선\"", "title=\"HR\""),
    ("title=\"인용\"", "title=\"Quote\""),
    ("title=\"목록\"", "title=\"List\""),
    ("title=\"체크리스트\"", "title=\"Checklist\""),
    ("'<div class=\"freq-empty\">텍스트를 입력하면 단어 빈도를 분석합니다.</div>'",
     "'<div class=\"freq-empty\">Enter text to analyze word frequency.</div>'"),
    # markdown default content
    ("const defaultMd = `# 마크다운 에디터에 오신 것을 환영합니다!",
     "const defaultMd = `# Welcome to the Markdown Editor!"),
    ("이것은 **실시간 마크다운 미리보기** 도구입니다.",
     "This is a **real-time Markdown preview** tool."),
    ("## 기본 서식", "## Basic Formatting"),
    ("**굵게**, *기울임*, ~~취소선~~을 사용할 수 있습니다.",
     "**Bold**, *italic*, ~~strikethrough~~ are all supported."),
    ("## 목록", "## Lists"),
    ("- 항목 1", "- Item 1"),
    ("- 항목 2", "- Item 2"),
    ("  - 하위 항목", "  - Sub-item"),
    ("1. 번호 목록", "1. Ordered list"),
    ("2. 두 번째 항목", "2. Second item"),
    ("## 코드", "## Code"),
    ("인라인 코드: \\`console.log(\"Hello\")\\`", "Inline code: \\`console.log(\"Hello\")\\`"),
    ("  return \\`안녕하세요, \\${name}님!\\`;", "  return \\`Hello, \\${name}!\\`;"),
    ("console.log(greet(\"세계\"));", "console.log(greet(\"World\"));"),
    ("## 인용문", "## Blockquote"),
    ("> 마크다운은 읽기 쉽고 쓰기 쉬운 텍스트 포맷입니다.", "> Markdown is an easy-to-read and easy-to-write text format."),
    ("## 표", "## Table"),
    ("| 기능 | 지원 여부 |", "| Feature | Supported |"),
    ("| 굵게 | ✅ |", "| Bold | ✅ |"),
    ("| 기울임 | ✅ |", "| Italic | ✅ |"),
    ("| 코드 블록 | ✅ |", "| Code Block | ✅ |"),
    ("| 표 | ✅ |", "| Table | ✅ |"),
    ("## 링크 & 이미지", "## Links & Images"),
    ("[WooaText 홈](https://textkit.wooahouse.com/)", "[WooaText Home](https://textkit.wooahouse.com/)"),
    ("*WooaText에서 무료로 마크다운을 편집하세요!`", "*Edit Markdown for free on WooaText!`"),
    ("const text = before + (selected || '텍스트') + after",
     "const text = before + (selected || 'text') + after"),
    ("'\\n| 제목1 | 제목2 | 제목3 |\\n|-------|-------|-------|\\n| 내용1 | 내용2 | 내용3 |\\n| 내용4 | 내용5 | 내용6 |\\n'",
     "'\\n| Header1 | Header2 | Header3 |\\n|-------|-------|-------|\\n| Cell1 | Cell2 | Cell3 |\\n| Cell4 | Cell5 | Cell6 |\\n'"),
    ('<!-- 하단 고정 광고 배너 -->', '<!-- Bottom Fixed Ad Banner -->'),
    ('<div style="font-size:0.65rem;color:#9ca3af;position:absolute;left:8px;top:4px;">광고</div>',
     '<div style="font-size:0.65rem;color:#9ca3af;position:absolute;left:8px;top:4px;">Ad</div>'),

    # ── html-css-editor.html CSS comments ──
    ('/* ── 전체 레이아웃 ── */', '/* ── Layout ── */'),
    ('/* ── 툴바 ── */', '/* ── Toolbar ── */'),
    ('/* ── 에디터 & 프리뷰 래퍼 ── */', '/* ── Editor & Preview Wrapper ── */'),
    ('/* ── 에디터 패널 영역 ── */', '/* ── Editor Panel Area ── */'),
    ('/* ── 탭 ── */', '/* ── Tabs ── */'),
    ('/* ── 개별 에디터 패널 ── */', '/* ── Individual Editor Panels ── */'),
    ('/* 수평 레이아웃에서 탭 방식 */', '/* Tab mode in horizontal layout */'),
    ('/* 수직 레이아웃에서 3분할 */', '/* 3-way split in vertical layout */'),
    ('/* ── 프리뷰 패널 ── */', '/* ── Preview Panel ── */'),
    ('/* ── 공유 토스트 ── */', '/* ── Share Toast ── */'),
    ('/* ── 하단 AdSense ── */', '/* ── Bottom AdSense ── */'),
    ('/* ── 모바일: 세로 고정 ── */', '/* ── Mobile: Vertical Fixed ── */'),
    ('/* 헤더/푸터 위에 에디터 */', '/* Editor above header/footer */'),
    # html-css-editor HTML comments
    ('<!-- 툴바 -->', '<!-- Toolbar -->'),
    ('<!-- 에디터 + 프리뷰 -->', '<!-- Editor + Preview -->'),
    ('<!-- 에디터 패널 -->', '<!-- Editor Panel -->'),
    ('<!-- 탭 (수평 레이아웃용) -->', '<!-- Tabs (for horizontal layout) -->'),
    ('<!-- 미리보기 -->', '<!-- Preview -->'),
    # html-css-editor JS comments & code
    ('/* ── 템플릿 ── */', '/* ── Templates ── */'),
    ("html: `<h1>안녕하세요!</h1>\\n<p>HTML, CSS, JS를 작성해보세요.</p>`,",
     "html: `<h1>Hello!</h1>\\n<p>Write your HTML, CSS, JS here.</p>`,"),
    ("js: `// JavaScript를 입력하세요\\nconsole.log('Hello, World!');`",
     "js: `// Write your JavaScript\\nconsole.log('Hello, World!');`"),
    ("<div class=\"header\">헤더</div>", "<div class=\"header\">Header</div>"),
    ("<div class=\"sidebar\">사이드바</div>", "<div class=\"sidebar\">Sidebar</div>"),
    ("<div class=\"main\">메인 콘텐츠</div>", "<div class=\"main\">Main Content</div>"),
    ("<div class=\"aside\">위젯</div>", "<div class=\"aside\">Widget</div>"),
    ("<div class=\"footer\">푸터</div>", "<div class=\"footer\">Footer</div>"),
    ("<span class=\"badge\">여행</span>", "<span class=\"badge\">Travel</span>"),
    ("<h2>제주도 여행기</h2>", "<h2>Jeju Island Travel</h2>"),
    ("<p>파란 하늘, 검은 돌, 초록 들판. 제주의 모든 것이 아름다웠습니다.</p>",
     "<p>Blue sky, black rocks, green fields. Everything about Jeju was beautiful.</p>"),
    ("<button class=\"btn\">자세히 보기</button>", "<button class=\"btn\">Read More</button>"),
    ("alert('카드 클릭!');", "alert('Card clicked!');"),
    ("<h1>나의 블로그</h1>", "<h1>My Blog</h1>"),
    (">🌙 다크모드<", ">🌙 Dark Mode<"),
    ("<h2>오늘의 이야기</h2>", "<h2>Today's Story</h2>"),
    ("<p>다크모드와 라이트모드를 자유롭게 전환할 수 있습니다.</p>",
     "<p>You can freely switch between dark mode and light mode.</p>"),
    ("btn.textContent = '☀️ 라이트모드';", "btn.textContent = '☀️ Light Mode';"),
    ("btn.textContent = '🌙 다크모드';", "btn.textContent = '🌙 Dark Mode';"),
    ('/* ── CodeMirror 초기화 ── */', '/* ── CodeMirror Init ── */'),
    ('/* CodeMirror 컨테이너 높이 설정 */', '/* Set CodeMirror container height */'),
    ('/* ── 자동 실행 디바운스 ── */', '/* ── Auto-run Debounce ── */'),
    ('/* ── 실행 ── */', '/* ── Run ── */'),
    ("status.textContent = '● 실행됨'", "status.textContent = '● Executed'"),
    ('/* ── 탭 전환 (수평 레이아웃) ── */', '/* ── Tab Switch (horizontal layout) ── */'),
    ('/* ── 레이아웃 토글 ── */', '/* ── Layout Toggle ── */'),
    ("btn.textContent = '↕ 수평 레이아웃'", "btn.textContent = '↕ Horizontal layout'"),
    ('/* ── 전체화면 ── */', '/* ── Fullscreen ── */'),
    ("closeBtn.textContent = '✕ 닫기'", "closeBtn.textContent = '✕ Close'"),
    ('/* ── URL 공유 ── */', '/* ── URL Share ── */'),
    ("showToast('🔗 URL이 클립보드에 복사됐어요!')", "showToast('🔗 URL copied to clipboard!')"),
    ("prompt('아래 URL을 복사하세요:', url)", "prompt('Copy this URL:', url)"),
    ("alert('공유 URL 생성 실패')", "alert('Failed to generate share URL')"),
    ('/* ── URL에서 복원 ── */', '/* ── Restore from URL ── */'),
    ('/* ── 템플릿 로드 ── */', '/* ── Load Template ── */'),
    ('/* ── 초기화 ── */', '/* ── Reset ── */'),
    ("confirm('모든 코드를 초기화할까요?')", "confirm('Reset all code?')"),
    ('/* ── 토스트 ── */', '/* ── Toast ── */'),
    ('/* ── 초기 실행 ── */', '/* ── Initial Run ── */'),
    ('title="닫기"', 'title="Close"'),

    # ── html-markdown.html ──
    ('<!-- CDN 라이브러리 -->', '<!-- CDN Libraries -->'),
    ('// 표(table) 지원 플러그인', '// table support plugin'),
    ("document.getElementById('loadingMsg').textContent = '라이브러리 로드 중 오류: ' + e.message",
     "document.getElementById('loadingMsg').textContent = 'Library load error: ' + e.message"),
    ("alert('변환할 HTML을 입력하세요.')", "alert('Please enter HTML to convert.')"),
    ("document.getElementById('outputLabel').textContent = '마크다운'",
     "document.getElementById('outputLabel').textContent = 'Markdown'"),
    ("document.getElementById('outputArea').value = '변환 오류: ' + e.message",
     "document.getElementById('outputArea').value = 'Conversion error: ' + e.message"),
    ("alert('변환할 마크다운을 입력하세요.')", "alert('Please enter Markdown to convert.')"),
    ("document.getElementById('inputLabel').textContent = '마크다운'",
     "document.getElementById('inputLabel').textContent = 'Markdown'"),
    # html-markdown placeholder (inline in attribute)
    ("placeholder=\"여기에 HTML 또는 마크다운을 입력하세요...\n예시 HTML:\n&lt;h1&gt;제목&lt;/h1&gt;\n&lt;p&gt;단락 텍스트입니다.&lt;/p&gt;\n&lt;ul&gt;&lt;li&gt;항목 1&lt;/li&gt;&lt;li&gt;항목 2&lt;/li&gt;&lt;/ul&gt;\n\n예시 마크다운:\n# 제목\n단락 텍스트입니다.\n- 항목 1\n- 항목 2\"",
     "placeholder=\"Enter HTML or Markdown here...\nExample HTML:\n&lt;h1&gt;Title&lt;/h1&gt;\n&lt;p&gt;Paragraph text.&lt;/p&gt;\n&lt;ul&gt;&lt;li&gt;Item 1&lt;/li&gt;&lt;li&gt;Item 2&lt;/li&gt;&lt;/ul&gt;\n\nExample Markdown:\n# Title\nParagraph text.\n- Item 1\n- Item 2\""),

    # ── morse-code.html ──
    ('/* 모스부호 표 */', '/* Morse Code Table */'),
    ('<!-- 왼쪽: 텍스트 -->', '<!-- Left: Text -->'),
    ('<!-- 오른쪽: 모스부호 -->', '<!-- Right: Morse Code -->'),
    ('<!-- 재생 컨트롤 -->', '<!-- Playback Controls -->'),
    ('<!-- 모스부호 표 -->', '<!-- Morse Code Table -->'),
    ('// ——— 모스부호 사전 ———', '// ——— Morse Code Dictionary ———'),
    ('// 한글 → 로마자 근사 변환 (초성 기준)', '// Hangul → Romanization (initial consonant based)'),
    ('// 한글 처리', '// Hangul processing'),
    ("alert('변환할 텍스트를 입력하세요.')", "alert('Please enter text to convert.')"),
    ("alert('변환할 모스부호를 입력하세요.')", "alert('Please enter Morse code to convert.')"),
    ('// ——— 재생 ———', '// ——— Playback ———'),
    ("'매우 느림', '느림', '보통', '빠름', '매우 빠름'",
     "'Very slow', 'Slow', 'Normal', 'Fast', 'Very fast'"),
    ('// 단음 길이 (ms)', '// Dot duration (ms)'),
    ('// 텍스트 영역에서 자동 변환', '// Auto-convert from text area'),
    ("alert('재생할 모스부호 또는 텍스트를 입력하세요.')",
     "alert('Please enter Morse code or text to play.')"),
    ('// 정규화', '// Normalize'),
    ("playBtn.textContent = '▶ 재생 중...'", "playBtn.textContent = '▶ Playing...'"),
    ("document.getElementById('playStatus').textContent = '재생 중...'",
     "document.getElementById('playStatus').textContent = 'Playing...'"),
    ('// 단어 간격: 7 units (글자 간격 3 포함)', '// Word gap: 7 units (includes 3 for char gap)'),
    ('// 각 글자의 각 부호', '// Each symbol of each character'),
    ('// 신호 재생', '// Play signal'),
    ('// 부호 간격: 1 unit', '// Symbol gap: 1 unit'),
    ('// 글자 간격: 3 units (1 already consumed)', '// Char gap: 3 units (1 already consumed)'),
    ("playBtn.textContent = '▶ 재생'", "playBtn.textContent = '▶ Play'"),
    ("document.getElementById('playStatus').textContent = stopFlag ? '정지됨' : '재생 완료'",
     "document.getElementById('playStatus').textContent = stopFlag ? 'Stopped' : 'Done'"),
    ('// ——— 모스부호 표 생성 ———', '// ——— Build Morse Table ———'),
    ("item.title = '클릭해서 모스부호 복사'", "item.title = 'Click to copy Morse code'"),

    # ── unicode-converter.html ──
    ("'❌ 변환할 텍스트를 입력해주세요.'", "'❌ Please enter text to convert.'"),
    ("'❌ 변환 중 오류가 발생했습니다: '", "'❌ Conversion error: '"),

    # ── csv-json.html ──
    ("placeholder=\"CSV 데이터를 붙여넣거나 파일을 업로드하세요...&#10;&#10;예:&#10;이름,나이,도시&#10;홍길동,30,서울&#10;김철수,25,부산\"",
     "placeholder=\"Paste CSV data or upload a file...&#10;&#10;Example:&#10;name,age,city&#10;John,30,Seoul&#10;Jane,25,Busan\""),
    ("placeholder=\"JSON 배열을 붙여넣거나 파일을 업로드하세요...&#10;&#10;예:&#10;[&#10;  {&quot;이름&quot;:&quot;홍길동&quot;,&quot;나이&quot;:30,&quot;도시&quot;:&quot;서울&quot;},&#10;  {&quot;이름&quot;:&quot;김철수&quot;,&quot;나이&quot;:25,&quot;도시&quot;:&quot;부산&quot;}&#10;]\"",
     "placeholder=\"Paste JSON array or upload a file...&#10;&#10;Example:&#10;[&#10;  {&quot;name&quot;:&quot;John&quot;,&quot;age&quot;:30,&quot;city&quot;:&quot;Seoul&quot;},&#10;  {&quot;name&quot;:&quot;Jane&quot;,&quot;age&quot;:25,&quot;city&quot;:&quot;Busan&quot;}&#10;]\""),
    ("showError('csvError', 'CSV 데이터를 입력해주세요.')",
     "showError('csvError', 'Please enter CSV data.')"),
    ("`행 ${e.row + 1}: ${e.message}`", "`Row ${e.row + 1}: ${e.message}`"),
    ("showError('csvError', '파싱 경고:\\n' + errMsgs)",
     "showError('csvError', 'Parse warning:\\n' + errMsgs)"),
    ("`<strong>${rows}</strong>행 × <strong>${cols}</strong>열 변환 완료`",
     "`<strong>${rows}</strong> rows × <strong>${cols}</strong> cols converted`"),
    ("`<th>열 ${i + 1}</th>`", "`<th>Col ${i + 1}</th>`"),
    ("`... 외 ${result.data.length - 20}행</td>`",
     "`... and ${result.data.length - 20} more rows</td>`"),
    ("showError('csvError', 'CSV 파싱 오류: ' + e.message)",
     "showError('csvError', 'CSV parse error: ' + e.message)"),
    ("showError('jsonError', 'JSON 데이터를 입력해주세요.')",
     "showError('jsonError', 'Please enter JSON data.')"),
    ("showError('jsonError', 'JSON은 객체 배열이어야 합니다. 예: [{\"key\":\"value\"}, ...]')",
     "showError('jsonError', 'JSON must be an array of objects. E.g.: [{\"key\":\"value\"}, ...]')"),
    ("showError('jsonError', 'JSON 배열이 비어 있습니다.')",
     "showError('jsonError', 'JSON array is empty.')"),
    ("`<strong>${flatData.length}</strong>행 × <strong>${keys.size}</strong>열 변환 완료`",
     "`<strong>${flatData.length}</strong> rows × <strong>${keys.size}</strong> cols converted`"),
    ("showError('jsonError', 'JSON 파싱 오류: ' + e.message)",
     "showError('jsonError', 'JSON parse error: ' + e.message)"),

    # ── csv-json.html (remaining) ──
    ('변환 결과가 여기에 표시됩니다...', 'Conversion result will appear here...'),
    ('... 외 ${result.data.length - 20}행</td></tr>', '... and ${result.data.length - 20} more rows</td></tr>'),

    # ── hash-generator.html (remaining) ──
    ('#️⃣ 해시 생성', '#️⃣ Generate Hash'),
    ('>⏳ 해시 생성 중...</div>', '>⏳ Generating hash...</div>'),
    ('>❌ 해시 생성 중 오류: ', '>❌ Hash generation error: '),

    # ── html-css-editor.html (remaining) ──
    ('<p>HTML, CSS, JS를 작성해보세요.</p>', '<p>Write your HTML, CSS, JS here.</p>'),
    ('>로딩 중…<', '>Loading…<'),
    ('다크모드와 라이트모드를 자유롭게 전환해 보세요. 사용자 선호도를 localStorage에 저장합니다.',
     'Switch freely between dark mode and light mode. User preference is saved to localStorage.'),
    ('버튼을 눌러 테마를 바꿔보세요!', 'Click the button to toggle the theme!'),
    ("isDark ? '☀️ 라이트모드' : '🌙 다크모드'", "isDark ? '☀️ Light Mode' : '🌙 Dark Mode'"),
    ("btn.textContent = '↔ 수직 레이아웃'", "btn.textContent = '↔ Vertical layout'"),
    ('VS Code 확장 →', 'VS Code Extensions →'),

    # ── html-entity.html FAQ ld+json text fields ──
    ('"text": "HTML 코드에서 <, >, &, \\" 등의 특수문자를 안전하게 표시하기 위해 엔티티로 변환합니다."',
     '"text": "To safely display special characters like <, >, &, \\" in HTML code, convert them to entities."'),
    ('"text": "네, HTML 엔티티 인코딩과 디코딩 양방향 모두 지원합니다."',
     '"text": "Yes, both HTML entity encoding and decoding are supported."'),
    ('"text": "주요 HTML 특수문자 엔티티를 모두 지원합니다."',
     '"text": "All major HTML special character entities are supported."'),

    # ── html-markdown.html (remaining pieces) ──
    ('<!-- 입력 -->', '<!-- Input -->'),
    ('예시 HTML:', 'Example HTML:'),
    ('예시 마크다운:', 'Example Markdown:'),
    ('&lt;h1&gt;제목&lt;/h1&gt;', '&lt;h1&gt;Title&lt;/h1&gt;'),
    ('&lt;p&gt;단락 텍스트입니다.&lt;/p&gt;', '&lt;p&gt;Paragraph text.&lt;/p&gt;'),
    ('&lt;ul&gt;&lt;li&gt;항목 1&lt;/li&gt;&lt;li&gt;항목 2&lt;/li&gt;&lt;/ul&gt;',
     '&lt;ul&gt;&lt;li&gt;Item 1&lt;/li&gt;&lt;li&gt;Item 2&lt;/li&gt;&lt;/ul&gt;'),
    ('단락 텍스트입니다.', 'Paragraph text.'),
    ('💡 HTML→마크다운: Turndown.js 사용 | 마크다운→HTML: marked.js 사용 | 모든 변환은 브라우저 내에서 처리됩니다',
     '💡 HTML→Markdown: Uses Turndown.js | Markdown→HTML: Uses marked.js | All conversions happen in-browser'),
    ('💡 마크다운 실시간 편집이 필요하다면 <a href="markdown-editor.html">마크다운 에디터</a>를 이용하세요.',
     '💡 For real-time Markdown editing, try the <a href="markdown-editor.html">Markdown Editor</a>.'),

    # ── line-numbering.html ──
    ('>▶ 변환<', '>▶ Convert<'),

    # ── line-tools.html / whitespace.html common placeholders ──
    ('각 줄에 텍스트를 입력하세요...', 'Enter text line by line...'),
    ('버튼을 클릭하면 결과가 표시됩니다...', 'Click a button to see the results...'),

    # ── whitespace.html input placeholder ──
    ('공백을 정리할 텍스트를 입력하세요...', 'Enter text to clean up whitespace...'),

    # ── markdown-editor.html fix (asterisk before closing backtick) ──
    ("*WooaText에서 무료로 마크다운을 편집하세요!*`", "*Edit Markdown for free on WooaText!*`"),

    # ── morse-code.html (remaining) ──
    ('>보통<', '>Normal<'),
    ('여기에 텍스트를 입력하세요', 'Enter text here'),
    ('한글은 영어 발음으로 변환됩니다', 'Korean is converted to English pronunciation'),
    ('여기에 모스부호를 입력하거나', 'Enter Morse code here'),
    ('위 버튼으로 변환된 결과가 표시됩니다', 'Result will appear after using the buttons above'),

    # ── number-base.html (HTML comments and placeholder prefix) ──
    ('<!-- 2진수 -->', '<!-- Binary -->'),
    ('<!-- 8진수 -->', '<!-- Octal -->'),
    ('<!-- 10진수 -->', '<!-- Decimal -->'),
    ('<!-- 16진수 -->', '<!-- Hex -->'),
    ('<!-- 퀵버튼 -->', '<!-- Quick Buttons -->'),
    ('<!-- 추가 정보 테이블 -->', '<!-- Info Table -->'),
    ('"margin-bottom:14px;">추가 정보</div>', '"margin-bottom:14px;">Additional Info</div>'),
    ('placeholder="예: 1010"', 'placeholder="e.g. 1010"'),
    ('placeholder="예: 12"', 'placeholder="e.g. 12"'),
    ('placeholder="예: 10"', 'placeholder="e.g. 10"'),
    ('placeholder="예: A"', 'placeholder="e.g. A"'),

    # ── password-generator.html ──
    ('>🔑 비밀번호 생성<', '>🔑 Generate Password<'),

    # ── regex-tester.html (fix wrong comment names & tag mismatch) ──
    ('<!-- 패턴 입력 -->', '<!-- Pattern Input -->'),
    ('<!-- 빠른 패턴 -->', '<!-- Quick Patterns -->'),
    ('<!-- 테스트 문자열 -->', '<!-- Test String -->'),
    ('<!-- 매칭 결과 -->', '<!-- Match Results -->'),
    ('<!-- 치환 -->', '<!-- Replace -->'),
    ('<!-- 통계 -->', '<!-- Statistics -->'),
    ('<div class="text-panel-title" style="margin-bottom:0;">매칭 결과</div>',
     '<div class="text-panel-title" style="margin-bottom:0;">Match Results</div>'),
    ('<span class="text-panel-title" style="margin-bottom:0;">치환 결과</span>',
     '<span class="text-panel-title" style="margin-bottom:0;">Replace Result</span>'),

    # ── text-diff.html (stats spans inside multi-line template literal) ──
    ('${addCount}줄 추가</span>', '${addCount} lines added</span>'),
    ('${removeCount}줄 삭제</span>', '${removeCount} lines removed</span>'),
    ('${sameCount}줄 동일</span>', '${sameCount} lines same</span>'),

    # ── text-replacer.html (backup for tool-desc + remaining) ──
    ('단어·문장을 한번에 치환합니다. 정규식 모드와 대소문자 무시 옵션을 규칙별로 설정하고, 여러 규칙을 순서대로 일괄 적용할 수 있습니다.',
     'Replace words and sentences in bulk. Set regex mode and case-insensitive options per rule, and apply multiple rules in order.'),
    ('// --- 규칙 행 생성 ---', '// --- Build Rule Row ---'),
    ('<h3>정규식 모드는 어떻게 사용하나요?</h3>',
     '<h3>How do I use regex mode?</h3>'),
    ('<p>각 규칙의 <strong>.*</strong> 버튼을 눌러 활성화하면 찾기 필드에 정규식 패턴을 입력할 수 있습니다. 예: <code>\\d+</code>는 숫자를, <code>\\s+</code>는 공백을 매칭합니다.</p>',
     '<p>Activate the <strong>.*</strong> button for each rule to enter a regex pattern in the Find field. E.g. <code>\\d+</code> matches digits, <code>\\s+</code> matches whitespace.</p>'),
    ('<h3>여러 단어를 한번에 바꿀 수 있나요?</h3>',
     '<h3>Can I replace multiple words at once?</h3>'),
    ('<p>네, <strong>+ 규칙 추가</strong> 버튼으로 규칙을 여러 개 추가하면 순서대로 모두 적용됩니다. 규칙은 위에서 아래 순으로 실행됩니다.</p>',
     '<p>Yes, add multiple rules with the <strong>+ Add Rule</strong> button and they are applied in order from top to bottom.</p>'),
    ('<h3>원본 텍스트는 변경되나요?</h3>',
     '<h3>Will the original text be changed?</h3>'),
    ('<p>아니요, 원본은 그대로 유지되고 결과 영역에 치환된 텍스트가 표시됩니다. 원본 영역의 내용을 직접 수정하기 전까지 보존됩니다.</p>',
     '<p>No, the original text is preserved; the replaced text appears in the result area. It stays intact until you manually edit the source field.</p>'),
    ('<h3>대소문자 무시 옵션은 무엇인가요?</h3>',
     '<h3>What is the Ignore Case option?</h3>'),
    ('<p>각 규칙의 <strong>Aa</strong> 버튼을 활성화하면 대소문자를 구분하지 않고 치환합니다. 예: "Hello"를 찾으면 "hello", "HELLO"도 함께 치환됩니다.</p>',
     '<p>Enable the <strong>Aa</strong> button for each rule to replace without case sensitivity. E.g. searching "Hello" also matches "hello" and "HELLO".</p>'),
    ('<h3>바꾸기 필드를 비워두면 어떻게 되나요?</h3>',
     '<h3>What happens if the Replace field is empty?</h3>'),
    ('<p>찾은 텍스트가 빈 문자열로 치환됩니다. 즉, 해당 패턴과 일치하는 텍스트를 모두 삭제하는 효과를 얻을 수 있습니다.</p>',
     '<p>The matched text is replaced with an empty string — effectively deleting all occurrences of the pattern.</p>'),
    ('<label for="sourceText" class="form-label">원본 텍스트</label>',
     '<label for="sourceText" class="form-label">Source Text</label>'),
    ('placeholder="치환할 텍스트를 입력하거나 붙여넣으세요..."',
     'placeholder="Enter or paste the text to replace..."'),
    ('<button class="btn btn-primary" id="runBtn">▶ 치환 실행</button>',
     '<button class="btn btn-primary" id="runBtn">▶ Run Replace</button>'),
    ('placeholder="치환 결과가 여기에 표시됩니다..."',
     'placeholder="Replacement result will appear here..."'),

    # ── text-stats.html (remaining) ──
    ('<th style="min-width:120px;">비율</th>', '<th style="min-width:120px;">Ratio</th>'),
    ('// 빈도 정렬', '// Sort by frequency'),
    ('// 초기 실행', '// Initial run'),
    ('<!-- 입력 영역 -->', '<!-- Input Area -->'),
    ('<!-- 기본 통계 카드 -->', '<!-- Basic Stats Cards -->'),
    ('<!-- 단어 빈도 Top 20 -->', '<!-- Word Frequency Top 20 -->'),

    # ── timestamp-converter.html (HTML comments and button) ──
    ('<!-- 현재 시각 카드 -->', '<!-- Current Time Card -->'),
    ('<!-- 섹션 1: Timestamp → 날짜시간 -->', '<!-- Section 1: Timestamp → Date/Time -->'),
    ('<!-- 섹션 2: 날짜시간 → Timestamp -->', '<!-- Section 2: Date/Time → Timestamp -->'),
    ('>→ 변환<', '>→ Convert<'),

    # ── unicode-converter.html ──
    ('결과가 여기에 표시됩니다.', 'Result will appear here.'),

    # ── yaml-json.html FAQ (plain text nodes, no tag wrappers) ──
    ('YAML과 JSON의 차이는 무엇인가요?', 'What is the difference between YAML and JSON?'),
    ('YAML은 들여쓰기 기반으로 사람이 읽기 쉽고, JSON은 중괄호 기반으로 프로그램이 파싱하기 쉽습니다. YAML은 주석을 지원하고 더 간결하지만, JSON은 언어 표준 지원이 더 넓습니다.',
     'YAML is indentation-based and human-readable; JSON uses braces and is easily parsed. YAML supports comments and is more concise, but JSON has broader language support.'),
    ('주석이 있는 YAML도 변환되나요?', 'Are YAML comments preserved when converting?'),
    ('YAML 주석(#으로 시작)은 JSON으로 변환 시 제거됩니다. JSON은 주석을 지원하지 않습니다. 주석 내용을 보존하려면 별도로 관리해야 합니다.',
     'YAML comments (starting with #) are removed when converting to JSON. JSON does not support comments. Manage comment content separately if needed.'),
    ('YAML 들여쓰기는 몇 칸으로 변환되나요?', 'How many spaces for YAML indentation?'),
    ('JSON→YAML 변환 시 기본 2칸 들여쓰기로 생성됩니다. JSON 역시 2칸 들여쓰기로 포맷팅됩니다.',
     'JSON→YAML conversion uses 2-space indentation by default. JSON is also formatted with 2-space indentation.'),

    # ── yaml-json.html status messages ──
    ("'✅ 변환 완료'", "'✅ Converted'"),
    ("'❌ YAML 오류: '", "'❌ YAML Error: '"),
    ("'❌ JSON 오류: '", "'❌ JSON Error: '"),

    # ── html-markdown.html: fix cross-link (Markdown Editor already replaced by earlier COMMON) ──
    ('💡 마크다운 실시간 편집이 필요하다면 <a href="markdown-editor.html">Markdown Editor</a>를 이용하세요.',
     '💡 For real-time Markdown editing, try the <a href="markdown-editor.html">Markdown Editor</a>.'),
    ('# 제목', '# Title'),

    # ── line-tools.html placeholder examples ──
    ('&#10;예:&#10;바나나&#10;사과&#10;포도&#10;사과&#10;&#10;딸기',
     '&#10;e.g.:&#10;Banana&#10;Apple&#10;Grape&#10;Apple&#10;&#10;Strawberry'),

    # ── whitespace.html inner placeholder examples ──
    ('&#10;예:   안녕하세요   반갑습니다   &#10;  WooaText에   오신  것을  환영합니다  ',
     '&#10;e.g.:   Hello   World   &#10;  Welcome   to  WooaText  '),

    # ── morse-code.html: fix '예:' in placeholders and cross-link ──
    ('예: HELLO WORLD', 'e.g.: HELLO WORLD'),
    ('예: .... . .-.. .-.. --- / .-- --- .-. .-.. -..',
     'e.g.: .... . .-.. .-.. --- / .-- --- .-. .-.. -..'),
    ('💡 문자 인코딩 변환이 필요하다면 <a href="unicode-converter.html">Unicode Converter</a>도 이용해보세요.',
     '💡 For character encoding conversion, try the <a href="unicode-converter.html">Unicode Converter</a> too.'),
    ('// 정규화: 다양한 dash 문자 통일', '// Normalize: unify various dash characters'),
    ('다양한 dash 문자 통일', 'unify various dash characters'),

    # ── password-generator.html: no tag wrappers ──
    ('🔑 비밀번호 생성', '🔑 Generate Password'),

    # ── regex-tester.html: match-label without backtick wrapper ──
    ('매칭 #${i + 1} (인덱스: ${match.index})', 'Match #${i + 1} (index: ${match.index})'),

    # ── slug-generator.html: placeholder and comments ──
    ('placeholder="예: 안녕하세요 세상! Hello World"',
     'placeholder="e.g.: Hello World! Good Morning"'),
    ('<!-- 구분자 -->', '<!-- Separator -->'),
    ('<!-- 대소문자 -->', '<!-- Casing -->'),
    ('<!-- 한글 처리 -->', '<!-- Hangul Processing -->'),
    ('<!-- 기타 옵션 -->', '<!-- Additional Options -->'),

    # ── text-replacer.html: fix tool-desc & FAQ h3 (대소문자 무시 already → Ignore case by earlier COMMON) ──
    ('<p class="tool-desc">단어·문장을 한번에 치환합니다. 정규식 모드와 Ignore case 옵션을 규칙별로 설정하고, 여러 규칙을 순서대로 일괄 적용할 수 있습니다.</p>',
     '<p class="tool-desc">Replace words and sentences in bulk. Set regex mode and case-insensitive options per rule, and apply multiple rules in order.</p>'),
    ('<h3>Ignore case 옵션은 무엇인가요?</h3>',
     '<h3>What is the Ignore Case option?</h3>'),

    # ── unicode-converter.html: labelMap fallback ──
    ("labelMap[mode] || '결과'", "labelMap[mode] || 'Result'"),

    # ── yaml-json.html HTML comments ──
    ('<!-- 좌우 2열 레이아웃 -->', '<!-- Two-column layout -->'),
    ('<!-- 왼쪽: YAML 패널 -->', '<!-- Left: YAML Panel -->'),
    ('<!-- 오른쪽: JSON 패널 -->', '<!-- Right: JSON Panel -->'),
    ('<!-- 탭 2의 내용 -->', '<!-- Tab 2 content -->'),
    ('<!-- 입력: YAML 형식 -->', '<!-- Input: YAML format -->'),
    ('<!-- 결과: JSON 형식 -->', '<!-- Result: JSON format -->'),
]

# ── 3. 언어 선택기 CSS ────────────────────────────────────────────────────────
LANG_SWITCHER_CSS = """    .lang-switcher { display:flex; align-items:center; gap:4px; }
    .lang-switcher a { color:rgba(255,255,255,0.7); text-decoration:none; font-size:0.8rem; font-weight:600; padding:3px 8px; border-radius:12px; transition:background 0.15s; }
    .lang-switcher a.active { color:white; background:rgba(255,255,255,0.25); }
    .lang-switcher a:hover { color:white; background:rgba(255,255,255,0.18); }
    .lang-switcher span { color:rgba(255,255,255,0.3); font-size:0.75rem; }
"""

def build_page(filename, meta):
    ko_path = os.path.join(BASE, filename)
    en_path = os.path.join(EN_DIR, filename)

    with open(ko_path, encoding='utf-8') as f:
        html = f.read()

    # ── 메타 태그 교체 (lambda로 백슬래시 이슈 방지) ──
    _t = meta["title"]; html = re.sub(r'<title>[^<]+</title>', lambda m: f'<title>{_t}</title>', html)
    _d = meta["desc"]; html = re.sub(r'<meta name="description" content="[^"]*"', lambda m: f'<meta name="description" content="{_d}"', html)
    _k = meta["kw"]; html = re.sub(r'<meta name="keywords" content="[^"]*"', lambda m: f'<meta name="keywords" content="{_k}"', html)
    _ot = meta["og_title"]; html = re.sub(r'<meta property="og:title" content="[^"]*"', lambda m: f'<meta property="og:title" content="{_ot}"', html)
    _od = meta["og_desc"]; html = re.sub(r'<meta property="og:description" content="[^"]*"', lambda m: f'<meta property="og:description" content="{_od}"', html)
    html = re.sub(r'<meta property="og:url" content="[^"]*"',
                  f'<meta property="og:url" content="{SITE_URL}/en/{filename}"', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*"',
                  f'<link rel="canonical" href="{SITE_URL}/en/{filename}"', html)

    # ── hreflang 추가 ──
    hreflang = (f'\n  <link rel="alternate" hreflang="ko" href="{SITE_URL}/{filename}">'
                f'\n  <link rel="alternate" hreflang="en" href="{SITE_URL}/en/{filename}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/{filename}">')
    html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + hreflang, html)

    # ── ld+json 업데이트 (lambda로 백슬래시 이슈 방지) ──
    if meta.get('app_name'):
        _an = meta["app_name"]
        html = re.sub(r'"name": "([^"]*[가-힣][^"]*)"',
                      lambda m: f'"name": "{_an}"', html)
    _desc = meta["desc"]
    html = re.sub(r'"description": "([^"]*[가-힣][^"]*)"',
                  lambda m: f'"description": "{_desc}"', html)
    html = re.sub(r'"url": "' + re.escape(SITE_URL) + r'/' + re.escape(filename) + '"',
                  f'"url": "{SITE_URL}/en/{filename}"', html)
    html = re.sub(r'"inLanguage": "ko"', '"inLanguage": "en"', html)

    # ── FAQ 교체 ──
    if meta.get('faq'):
        faq_items = meta['faq']
        faq_html_parts = []
        for i, (q, a) in enumerate(faq_items):
            is_last = (i == len(faq_items) - 1)
            mb = '' if is_last else 'margin-bottom:1.2rem;'
            faq_html_parts.append(
                f'    <div class="faq-item" style="{mb}padding:1rem;background:#f8f9fa;border-radius:8px;">\n'
                f'      <h3 style="font-size:1rem;font-weight:600;margin-bottom:0.5rem;">Q. {q}</h3>\n'
                f'      <p style="color:#555;margin:0;">{a}</p>\n'
                f'    </div>'
            )
        faq_inner = '\n'.join(faq_html_parts)
        _fi = faq_inner
        html = re.sub(
            r'<div class="faq-list">.*?</div>\s*</section>',
            lambda m: f'<div class="faq-list">\n{_fi}\n  </div>\n</section>',
            html, flags=re.DOTALL
        )
        # FAQPage ld+json 교체
        import json as _json
        faq_entities = []
        for q, a in faq_items:
            faq_entities.append({
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a}
            })
        new_faq_json = _json.dumps({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }, ensure_ascii=False, indent=2)
        _nfj = new_faq_json
        html = re.sub(
            r'<script type="application/ld\+json">\s*\{[^<]*"FAQPage"[^<]*\}[^<]*</script>',
            lambda m: f'<script type="application/ld+json">\n{_nfj}\n</script>',
            html, flags=re.DOTALL
        )
        html = re.sub(r'<h2[^>]*>자주 묻는 질문</h2>',
                      '<h2 style="font-size:1.4rem;margin-bottom:1.5rem;">Frequently Asked Questions</h2>',
                      html)

    # ── h1 교체 ──
    if meta.get('h1'):
        _h1 = meta["h1"]
        replaced = re.sub(r'<h1 id="toolTitle">[^<]*</h1>',
                          lambda m: f'<h1 id="toolTitle">{_h1}</h1>', html)
        if replaced == html:
            replaced = re.sub(r'<h1>([^<]*)</h1>', lambda m: f'<h1>{_h1}</h1>', html, count=1)
        html = replaced

    # ── tool_desc 교체 ──
    if meta.get('tool_desc'):
        _td = meta["tool_desc"]
        replaced = re.sub(r'<p id="toolDesc">[^<]*</p>',
                          lambda m: f'<p id="toolDesc">{_td}</p>', html)
        html = replaced

    # ── breadcrumb ──
    if meta.get('breadcrumb'):
        html = re.sub(r'<span id="breadcrumbTitle">[^<]*</span>',
                      f'<span id="breadcrumbTitle">{meta["breadcrumb"]}</span>', html)
        # plain breadcrumb span (no id)
        html = re.sub(
            r'(<span>(?:›\s*)?)</span>',
            lambda m: m.group(0),
            html
        )

    # ── 공통 문자열 치환 ──
    for ko, en in COMMON:
        html = html.replace(ko, en)

    # ── 언어 선택기 CSS 삽입 ──
    if 'lang-switcher' not in html:
        if '</style>' in html:
            html = html.replace('</style>', LANG_SWITCHER_CSS + '</style>', 1)

    # ── 헤더에 언어 선택기 삽입 ──
    html = re.sub(
        r'(\s*</div>\s*</header>)',
        f'\n    <div class="header-right">\n'
        f'      <div class="lang-switcher">\n'
        f'        <a href="../{filename}">KO</a>\n'
        f'        <span>|</span>\n'
        f'        <a href="{filename}" class="active">EN</a>\n'
        f'      </div>\n'
        f'      <a href="../about.html" style="color:rgba(255,255,255,0.85); font-size:0.85rem; text-decoration:none; margin-left:8px;">About</a>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</header>',
        html, count=1
    )

    # ── 쿠팡 제거 ──
    html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
    html = re.sub(r'<script>\s*new PartnersCoupang\.G\([^)]*\);?\s*</script>', '', html)

    # ── og:locale 교체 ──
    html = html.replace('content="ko_KR"', 'content="en_US"')

    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'  ✅ en/{filename}')


def build_simple(filename, en_title, en_desc):
    """about.html / privacy.html 처리"""
    ko_path = os.path.join(BASE, filename)
    en_path = os.path.join(EN_DIR, filename)
    if not os.path.exists(ko_path):
        print(f'  ⚠️  {filename} not found, skipping')
        return

    with open(ko_path, encoding='utf-8') as f:
        html = f.read()

    html = re.sub(r'<title>[^<]+</title>', f'<title>{en_title}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]*"',
                  f'<meta name="description" content="{en_desc}"', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*"',
                  f'<link rel="canonical" href="{SITE_URL}/en/{filename}"', html)

    hreflang = (f'\n  <link rel="alternate" hreflang="ko" href="{SITE_URL}/{filename}">'
                f'\n  <link rel="alternate" hreflang="en" href="{SITE_URL}/en/{filename}">'
                f'\n  <link rel="alternate" hreflang="x-default" href="{SITE_URL}/en/{filename}">')
    html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1' + hreflang, html)

    for ko, en in COMMON:
        html = html.replace(ko, en)

    if 'lang-switcher' not in html and '</style>' in html:
        html = html.replace('</style>', LANG_SWITCHER_CSS + '</style>', 1)

    html = re.sub(
        r'(\s*</div>\s*</header>)',
        f'\n    <div class="header-right">\n'
        f'      <div class="lang-switcher">\n'
        f'        <a href="../{filename}">KO</a>\n'
        f'        <span>|</span>\n'
        f'        <a href="{filename}" class="active">EN</a>\n'
        f'      </div>\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</header>',
        html, count=1
    )

    html = re.sub(r'\s*<script src="https://ads-partners\.coupang\.com/g\.js"></script>\n?', '', html)
    html = re.sub(r'<script>\s*new PartnersCoupang\.G\([^)]*\);?\s*</script>', '', html)
    html = html.replace('content="ko_KR"', 'content="en_US"')

    with open(en_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  ✅ en/{filename}')


# ── 4. 실행 ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Building English pages for TextKit...')

    for filename, meta in PAGE_META.items():
        ko_path = os.path.join(BASE, filename)
        if os.path.exists(ko_path):
            build_page(filename, meta)
        else:
            print(f'  ⚠️  {filename} not found, skipping')

    build_simple(
        'about.html',
        'About WooaText – Free Online Text Tools',
        'WooaText is a free collection of browser-based text tools: character counter, converter, formatter, and more. No sign-up, no upload.',
    )
    build_simple(
        'privacy.html',
        'Privacy Policy – WooaText',
        'WooaText privacy policy. All text processing happens in your browser. No data is stored or transmitted to any server.',
    )

    print('\nDone! Check en/ folder.')
