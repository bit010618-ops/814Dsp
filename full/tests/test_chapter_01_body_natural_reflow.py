from pathlib import Path


def test_chapter_one_body_components_do_not_force_blank_page_tails(tmp_path: Path):
    from full.tools import (
        build_chapter_01_applications_close_mathjax_component as applications,
        build_chapter_01_causal_stable_mathjax_component as causal_stable,
        build_chapter_01_convolution_properties_mathjax_component as convolution,
        build_chapter_01_sampling_recovery_mathjax_component as recovery,
        build_chapter_01_time_invariance_mathjax_component as time_invariance,
        build_chapter_01_typical_sequences_mathjax_component as typical_sequences,
    )

    components = (
        applications,
        causal_stable,
        convolution,
        recovery,
        time_invariance,
        typical_sequences,
    )
    for component in components:
        html = component.write_html(tmp_path / f"{component.__name__}.html").read_text(
            encoding="utf-8"
        )
        assert "break-after:page" not in html
        assert "break-before:page" not in html
        assert "page-break-after:always" not in html
