

EXTENSION_TO_TEST = (
    (
        # abbr
        {
            "index.md": (
                "The HTML specification\nis maintained by the W3C.\n\n"
                "*[HTML]: Hyper Text Markup Language\n"
                "*[W3C]: World Wide Web Consortium"
            )
        },
        {
            "es/index.md.po": {
                "The HTML specification is maintained by the W3C.": "La espcificación HTML es mantenida por la W3C.",
                "*[HTML]: Hyper Text Markup Language *[W3C]: World Wide Web Consortium": "",
            },
        },
        None,
        "en",
        ["en", "es"],
        None,
        None,
        None,
        {
            "index.html": ["<p>foo</p>"],
            "es/index.html": ["<p>foo es</p>"],
        },
    ),
)

OFFICIALLY_SUPPORTED_EXTENSIONS_TESTS = (
    (
        # abbr
        {
            "index.md": (
                "The HTML specification\nis maintained by the W3C.\n\n"
                "*[HTML]: Hyper Text Markup Language\n"
                "*[W3C]:  World Wide Web Consortium"
            )
        },
        {
            "es/index.md.po": {
                "foo": "foo es",
            },
        },
        None,
        "en",
        ["en", "es"],
        None,
        None,
        None,
        {
            "index.html": ["<p>foo</p>"],
            "es/index.html": ["<p>foo es</p>"],
        },
    ),
)
