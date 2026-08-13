from full.tools.stamp_main_body_pdf import chapter_for_pages


def test_chapter_for_pages_follows_actual_chapter_titles_after_reflow():
    pages = [
        "第一章 离散时间信号与系统\n正文",
        "第一章的续页",
        "第二章 z 变换与 LSI 系统频域分析\n正文",
        "续页",
        "第七章 FIR 数字滤波器设计\n正文",
    ]

    assert chapter_for_pages(pages) == [
        "第一章 离散时间信号与系统",
        "第一章 离散时间信号与系统",
        "第二章 z 变换与 LSI 系统频域分析",
        "第二章 z 变换与 LSI 系统频域分析",
        "第七章 FIR 数字滤波器设计",
    ]
