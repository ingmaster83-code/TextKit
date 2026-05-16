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
