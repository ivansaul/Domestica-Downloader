from domestica.helpers import clean_string  # type: ignore


def test_clean_string():
    assert clean_string("Hello, World!") == "Hello World"
    assert clean_string("<html>Content_</html>") == "htmlContent_html"
    assert clean_string("º~ª Special chars: @#$%^&*()!") == "Special chars"
    assert clean_string("") == ""
    assert clean_string("  Normal text  ") == "Normal text"
    assert clean_string("1234:;<>?{}|") == "1234"
    assert clean_string("Café! Frío?") == "Café Frío"
    assert clean_string("~!@#$%^&*()+`-={}|[  hi  ]\\:\";'<>?,./") == "hi"
    assert clean_string("  -_-  ") == "_"
