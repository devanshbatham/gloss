import os
import tempfile

import gloss


def test_render_returns_html_string():
    html = gloss.render("# Hello\n\nWorld")
    assert isinstance(html, str)
    assert html.startswith("<!DOCTYPE html>")
    assert "</html>" in html


def test_render_embeds_markdown_as_base64():
    md = "# Test Title\n\nSome paragraph."
    html = gloss.render(md)
    import base64
    b64 = base64.b64encode(md.encode("utf-8")).decode("ascii")
    assert b64 in html


def test_render_does_not_contain_placeholder():
    html = gloss.render("# Hi")
    assert "__MD_B64__" not in html


def test_render_preserves_unicode():
    md = "# Unicod\u00e9\n\n\u00c9l\u00e8ve caf\u00e9"
    html = gloss.render(md)
    import base64
    b64 = base64.b64encode(md.encode("utf-8")).decode("ascii")
    assert b64 in html


def test_render_empty_string():
    html = gloss.render("")
    assert "<!DOCTYPE html>" in html


def test_convert_creates_file():
    with tempfile.TemporaryDirectory() as tmp:
        md_path = os.path.join(tmp, "test.md")
        html_path = os.path.join(tmp, "test.html")
        with open(md_path, "w") as f:
            f.write("# Convert Test\n\nBody text.")

        result = gloss.convert(md_path, html_path)

        assert os.path.isfile(html_path)
        assert isinstance(result, str)
        assert "<!DOCTYPE html>" in result

        with open(html_path) as f:
            assert f.read() == result


def test_convert_default_output_path():
    with tempfile.TemporaryDirectory() as tmp:
        md_path = os.path.join(tmp, "doc.md")
        expected_html = os.path.join(tmp, "doc.html")
        with open(md_path, "w") as f:
            f.write("# Auto Path\n\nTest.")

        gloss.convert(md_path)

        assert os.path.isfile(expected_html)


def test_render_and_convert_produce_same_html():
    with tempfile.TemporaryDirectory() as tmp:
        md = "# Same\n\nContent here."
        md_path = os.path.join(tmp, "same.md")
        html_path = os.path.join(tmp, "same.html")
        with open(md_path, "w") as f:
            f.write(md)

        html_from_render = gloss.render(md)
        html_from_convert = gloss.convert(md_path, html_path)

        assert html_from_render == html_from_convert
