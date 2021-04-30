CONFIGURATION_TESTS = (
    (
        # basic example with default configuration
        {
            'index.md': '# Foo\n\nbar\n',
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
                'bar': 'bar es',
            },
        },
        None,
        'en',
        ['en', 'es'],
        None,
        None,
        None,
        {
            'index.html': [
                '<h1 id="foo">Foo</h1>',
                '<p>bar</p></div>',
            ],
            'es/index.html': [
                '<h1 id="foo-es">Foo es</h1>',
                '<p>bar es</p>',
            ],
        },
    ),
    (
        # nested files
        {
            'index.md': 'foo\n',
            'foo/bar/baz.md': 'hello\n',
        },
        {
            'es/index.md.po': {
                'foo': 'foo es',
            },
            'es/foo/bar/baz.md.po': {
                'hello': 'hola',
            },
        },
        None,
        'en',
        ['en', 'es'],
        None,
        None,
        None,
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': ['<p>foo es</p>'],
            'foo/bar/baz/index.html': ['<p>hello</p>'],
            'es/foo/bar/baz/index.html': ['<p>hola</p>'],
        },
    ),
    (
        # custom locale_dir
        {
            'index.md': 'foo\n',
        },
        {
            'locales/es/index.md.po': {
                'foo': 'foo es',
            },
        },
        'locales',
        'en',
        ['en', 'es'],
        None,
        None,
        None,
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # custom dest_filename_template
        {
            'index.md': 'foo\n',
        },
        {
            'es/index.md.po': {
                'foo': 'foo es',
            },
        },
        '',
        'en',
        ['en', 'es'],
        "{{page.file.dest_path|replace(\".html\", \"\")}}-{{language}}.html",
        None,
        None,
        {
            'index.html': ['<p>foo</p>'],
            'index-es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # custom locale_dir + dest_filename_template
        {
            'index.md': 'foo\n',
        },
        {
            'locales/es/index.md.po': {
                'foo': 'foo es',
            },
        },
        'locales',
        'en',
        ['en', 'es'],
        "{{page.file.dest_path|replace(\".html\", \"\")}}_{{language}}.html",
        None,
        None,
        {
            'index.html': ['<p>foo</p>'],
            'index_es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # configuration from 'material' theme
        {
            'index.md': '# Foo\n\nbar\n',
        },
        {
            'es/index.md.po': {
                'Foo': 'Foo es',
                'bar': 'bar es',
            },
        },
        None,
        None,
        None,
        None,
        None,
        {
            'theme': {
                'name': 'material',
                'language': 'en',
            },
            'extra': {
                'alternate': [
                    {
                        'name': 'English',
                        'link': None,
                        'lang': 'en',
                    },
                    {
                        'name': 'Español',
                        'link': 'es',
                        'lang': 'es',
                    },
                ],
            },
        },
        {
            'es/index.html': [
                '<h1 id="foo-es">Foo es</h1>',
                '<p>bar es</p>',
            ],
        },
    ),
    (
        # default_language from languages
        {
            'index.md': 'foo\n',
        },
        {
            'es/index.md.po': {
                'foo': 'foo es',
            },
        },
        None,
        None,
        ['en', 'es'],
        None,
        None,
        None,
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # boolean lc_messages
        {
            'index.md': '# Foo\n\nbar\n',
        },
        {
            'es/LC_MESSAGES/index.md.po': {
                'Foo': 'Foo es',
                'bar': 'bar es',
            },
        },
        None,
        'en',
        ['en', 'es'],
        None,
        True,
        None,
        {
            'index.html': [
                '<h1 id="foo">Foo</h1>',
                '<p>bar</p></div>',
            ],
            'es/index.html': [
                '<h1 id="foo-es">Foo es</h1>',
                '<p>bar es</p>',
            ],
        },
    ),
    (
        # custom lc_messages
        {
            'index.md': 'foo\n',
        },
        {
            'es/barbaz/index.md.po': {
                'foo': 'foo es',
            },
        },
        None,
        'en',
        ['en', 'es'],
        None,
        'barbaz',
        None,
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': ['<p>foo es</p>'],
        },
    ),
    (
        # title translation
        {
            'index.md': 'foo\n',
        },
        {
            'es/index.md.po': {
                'foo': 'foo es',
                'Introduction': 'Introducción',
            },
        },
        None,
        'en',
        ['en', 'es'],
        None,
        None,
        {
            'nav': [
                {'Introduction': 'index.md'},
            ],
        },
        {
            'index.html': ['<p>foo</p>'],
            'es/index.html': [
                '<p>foo es</p>',
                '<title>Introducción - foo</title>',
            ],
        },
    ),
)
