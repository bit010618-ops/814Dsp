# 项目交接：数字信号处理讲义

## 强制恢复顺序

每次新会话、上下文压缩、摘要恢复或交接后，**先执行以下步骤，再做任何内容改动**：

1. 阅读 `README.md`、本文件、`docs/requirements/2026-07-18-需求访谈与执行方案.md` 与 `docs/requirements/2026-07-18-变更记录.md`。
2. 运行 `git status --short` 和 `git log -1 --oneline`，保留无关用户改动，不隐式暂存。
3. 检查 `sample/` 与 `outputs/` 的实际文件、最近修改时间和可渲染性；不得仅凭对话摘要判断完成状态。
4. 阅读当前任务 `.codex/tasks/2026-07-18_184000-full-dsp-handout.md`，确认全文阶段、验证结果和下一步；样稿任务文件仅用于追溯样稿实现。

## 当前阶段

全文制作已启动，当前正在审计源课件和真题，以确定章节批次与完整真题归属。5 页样稿仅作为已验证的排版基线；不得将其中的 2004 年单题误认为该章真题已经收齐。

## 不能违反的原则

- 不漏任何原课件的唯一信息；顺序、知识结构沿用原课件。
- 所有公式必须数学排版；下标、上标、根号、求和完整；分式必须竖式，禁止 `/`。
- 图内内容精确保留、无水印、打印清晰；图外课件模板元素不得带入讲义。
- 每章另起页；A4 纵版、彩色、传统教材风；页眉左“数字信号处理讲义”、右章节名，页脚居中页码。
- 每次用户建议都追加到变更记录，在一个已验证的阶段后提交并推送 GitHub。

## Latest authoritative update — 2026-07-18

- 展示公式已统一为 STIX 数学字体与 11 pt 基准字号；`f_s ≥ 2f_h` 的下标已在 300 dpi 渲染中确认完整。保留公式框，复杂分式只增加框内行高，不放大公式字号。
- 原课件图的裁切会损失 Ω、单位与坐标标注，因此按用户最终决定完整保留原图。图下保留 `图 3-1 采样参数与频域离散的对应关系`，仅删除“根据原课件第 528 页保留”。
- 新增重申：真题题图逐幅检查水印；有水印必须去除。水印压住题目有效信息时修复或重绘，禁止通过裁切牺牲坐标、曲线、公式、单位或标签。

## Latest layout revision — 2026-07-18

- 课内练习已改为与真题相同的纯白题干页：无黄色背景、边框、横线或“练习”标签；仅在题干下保留自然书写空白。
- 3.6 节首页已将导语、公式、复习提示与完整原课件图连续排版；不再让图单独占用新页。受控图高为 280 pt 上限，实际绘制约 265 pt，未裁掉图内坐标、单位或 Ω。
- 样稿共 7 页；正文页不再预留大面积空白。2004 年真题页右侧答案索引已同步为“答案见 P.7”。
- 验证：PDF 页数与图注检查通过，自动测试 `12 passed`。如恢复上下文，先读取本节，再检查 `git status` 与最新提交。

## Latest natural-flow revision — 2026-07-18

- 用户确认：正文不应按原 PPT 页或固定“两页合并”机械分页；应把下一段中放得下的标题、导语、公式和步骤顺序提入上页，只有确实装不下的内容才在下页标“续”。
- 样稿第 1 页现接入“频谱分析的参数关系”标题、关系式和首段；第 2 页以“（续）”完成剩余参数说明及全部 DFS 例题。第 1、2 页的正文最低位置分别约为 725 pt 和 668 pt，避免非题目页的大面积空白。
- 样稿缩为 5 页；第 3、4 页的留白仅为课内练习与真题书写区，真题答案索引已更新为“答案见 P.5”。

## Latest inline-math revision — 2026-07-18

- 用户继续要求行内公式略大、略低。全局规则：展示公式框仍使用 11 pt 基准；**正文文字之间的所有行内公式**使用 17.5 pt 实际绘制高度，并提高栅格源字号以保证 A4 彩印清晰。
- 行内公式在不改变 17.5 pt 字号的前提下全局下移 3 pt，以贴齐文字基线。
- 已用 PDFium 重新渲染并查看第 2 页；行内公式与正文同量级，无裁切、重叠或原始代码形式。

## Latest full-book exam-scope update — 2026-07-18

- 用户明确指出：样稿只展示了 2004 年一道题，不能遗漏同章其他相关华理 814 真题。
- 全文按两层组织：每章末尾保留 2–3 道“重点精练”题并留自然书写区；该章其余相关题目按年份完整收录为“补充真题”，不设置大面积答题区。
- 所有已收录真题均在全书末尾“真题整理详解”中给出完整步骤，并在题目标题右侧标明最终答案页码。源真题审计完成前，不能声称任何章节的真题已收齐。

## Latest source-audit milestone — 2026-07-18

- 已扫描课件与真题：课件共 1056 页，PDF 书签确认 8 章，自动发现 18 组动画递进候选；真题共 205 页。
- 课件章节范围已锁定为：1–185、186–387、388–559、560–655、656–741、742–865、866–1009、1010–1056 页；详见 `full/source/chapters.json` 和 `full/docs/source-audit.md`。
- 真题原件实际可用年份为 2002–2007、2013–2017、2019–2025。后续只按这些来源收题，不能为缺失年份杜撰题目；逐题章节归属仍在下一阶段人工核对。

## Latest cross-chapter exam-placement rule — 2026-07-18

- 同一大题先核查小题依赖：彼此独立的小题可按各自章节分别放置；共用结果、连续推导或相互依赖的小题不得拆开，整题放在所涉及知识的**最晚章节**。
- 真题记录必须保存 `split_mode`（`independent_subquestions` 或 `linked_whole_question`）、`required_chapters` 及相应的唯一或分小题 `placement_chapter`；前章不得留下因缺少后续知识无法完成的残缺题。

## Latest exam-page audit milestone — 2026-07-18

- 真题正文已按原 PDF 第 5–59 页完成页级人工审阅：共 55 页，51 页含 DSP 内容，4 页（2004-P11、2020-P42、2023-P49、2024-P53）明确范围外。
- `full/source/exam_page_review.json` 与对应测试保证正文页无遗漏；多章内容页仍必须进入题号级依赖判断，不能直接按整页放入某一章。

## Latest question-unit model — 2026-07-18

- `full/tools/question_units.py` 已用测试固定题号归属：`dependency_group = null` 的独立小题生成各自章节单元；同一 `dependency_group` 的关联小题合为完整单元，归入其所需章节最大值。
- 该模型只定义规则，不能替代人工读取真实题号与依赖关系；录入最终 `exam_questions.json` 前不得宣称真题已按章节收齐。

## Latest course-manifest milestone — 2026-07-18

- 8 章课件底稿已生成于 `full/source/chapter_01.json` 至 `chapter_08.json`：总覆盖 1056 个来源页；分章候选数为 2、1、5、1、0、1、8、0，合计 18。
- 所有来源页仍为 `retain_pending_review`。候选只能在 300 dpi 视觉核对确认图、公式、箭头和标注零丢失后才允许合并；文本相似不构成删页依据。

## Latest animation visual-review milestone — 2026-07-18

- `full/source/animation_merge_review.json` 逐组记录了 18 个动画递进候选的视觉审核结论；全部为 `retain`。每一组都包含后续新增的推导、图示、例题或小节过渡，后页并未完整包含前页。
- 新增 `full/tests/test_animation_review.py` 防止遗漏任一候选或写入未决状态；当前完整回归为 16 项测试通过。诊断渲染 PNG 位于未跟踪的 `full/artifacts/animation-review/`，仅用于审阅，不得随此里程碑提交。

## Latest source-figure annotation rule — 2026-07-18

- 课件原图中的公式、曲线和推导优先以干净的教材状态呈现。圆圈、手绘线、强调箭头如仅为课堂视觉强调，须删除；如承担对应关系、步骤方向或条件/结果区分等必要解释作用，才保留或以讲义式标注重绘。每幅图独立判断，不可机械全删或全留。
- 真题中的图执行同一清理规范：不保留水印、学校/课件模板标识或来源性文字；如水印覆盖题目必需内容，使用重绘或无损修复，坐标、曲线、公式、单位和题目必需标注零丢失优先。

## Latest exam-source-section milestone — 2026-07-18

- `full/tools/extract_exam_questions.py` 和 `full/artifacts/exam_question_sections.json` 已将 51 页已归入 DSP 范围的真题正文机械分为 177 个可审阅原文段落（126 个明确题号起点、51 个续接段）。4 页已确认范围外页面不会进入该清单。
- 该产物只保存原文边界和 `pending_dependency_review` 状态，尚未把跨页续接段绑定到题号，也未执行最终分章；不得据此声称真题已经收齐或归位。新的抽取器测试和全量回归共 19 项通过。

## Latest exam-source-question-group milestone — 2026-07-18

- 通过 `group_sections_into_question_candidates`，51 个跨页续接段已按原文顺序归并到前一题号；`full/artifacts/exam_question_candidates.json` 现含 144 个原文题组候选。
- 此归并仅解决跨页连续性，全部候选仍为 `pending_dependency_review`。下一步必须逐题判断独立小题与关联题组，不能将候选题组直接等同于最终章末训练或讲义题目。

## Latest exam-auto-annotation milestone — 2026-07-18

- `full/tools/annotate_exam_candidates.py` 为 144 个原文题组保存章节候选至 `full/artifacts/exam_question_candidates_annotated.json`；这是便于人工审核的索引，绝非最终归属。
- 68 个题组因原 PDF 提取不到关键公式或图形文字而无自动章节结论，必须查看原页后手动判定；不准用关键词或年份缺失来编造归属。

## Latest 2002 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2002.json` 已逐一覆盖 2002 年 10 个原文题组。离散稳定性和奈奎斯特采样为独立小题；采样链三问整体在第 1 章；DFT 卷积与频率分辨率在第 3 章；连续时间题全部明确排除。
- 后续年份继续沿用相同记录粒度：每个原文题组必须写明 `decision`、纳入小题、所需章节和最终放置章节，才能进入最终题库。

## Latest 2003 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2003.json` 覆盖 2003 年 9 个原文题组。采样和差分方程归第 1 章，H(z) 稳定性归第 2 章，DFT 谱分析与相关判断归第 3 章；连续时间题排除。
- 第七题虽包含采样信息，但采样参数、频率分辨率和 DFT 频率对应关系彼此依赖，整题归入第 3 章。第九题三个判断彼此独立，分别归入第 2 或第 3 章。

## Latest 2004 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2004.json` 覆盖 2004 年 9 个原文题组。离散系统方框图和梳状滤波器归第 2 章，离散 LTI 阶跃响应归第 1 章，DFT 分辨率归第 3 章。
- FFT 重叠相加实现题同时涉及 DFT 和 FFT，但运算方案不可拆分，整体归第 4 章；连续时间题排除。

## Latest 2005 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2005.json` 覆盖 2005 年 12 个原文题组。离散系统归第 1 章，z 反变换/DTFT 与采样-数字滤波-重构实现链归第 2 章，DFT 循环卷积归第 3 章。
- 模拟系统离散化综合题的后续计算依赖前置模拟系统结果，整题归第 6 章；脉冲响应不变法与双线性变换法的两个小问互不依赖，可分别记录但均归第 6 章。

## Latest 2006 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2006.json` 覆盖 2006 年 11 个原文题组。z 反变换/DTFT 反变换归第 2 章，离散结构归第 1 章，DFT 与重叠保留法归第 3 章。
- 脉冲响应不变法和双线性变换法是从同一模拟滤波器出发的独立方法题，分别记录、均归第 6 章；连续时间和电路题排除。

## Latest 2007 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2007.json` 覆盖 2007 年 11 个原文题组。原 PDF OCR 将第 8、9、10 题合并，已通过原页视觉核对按实际题号拆为独立单元，分别归第 1/2/3/6/7 章。
- 双线性变换稳定性证明、按时间抽取 FFT 流图和频率采样 FIR 设计各自保持完整题组，分别放第 6、4、7 章；不可由 OCR 边界决定最终题目边界。

## Latest 2013 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2013.json` 覆盖 2013 年 10 个原文题组。OCR 合并的两组独立填空/计算题已按真实小题拆分：采样与离散 LTI 在第 1 章，z 变换在第 2 章，DFS 在第 3 章。
- 零值插入、数字低通和周期采样构成一个完整多采样率链，整体归第 8 章；连续时间题排除。

## Latest 2015 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2015.json` 覆盖 2015 年 10 个原文题组。填空题中采样/基本运算归第 1 章，DTFT 归第 2 章，DFT 归第 3 章，FFT 归第 4 章，FIR 线性相位归第 7 章；四类理想数字滤波器幅频响应归第 6 章。
- 已视觉核对原卷第 29–31 页存在中央半透明水印及推广页眉页脚。含图的第 4、7、8 题已分别登记为重绘：离散结构图、零极点图与多采样率频谱/框图均须保留技术标注并去除水印。

## Latest 2016 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2016.json` 覆盖 2016 年 8 个原文题组。离散卷积归第 1 章，FT/LT/ZT 关系归第 2 章，时分复用归第 8 章；DSP 题的独立小题分入第 1 或第 3 章；一次 DFT 计算两个实序列归第 3 章，频率采样 FIR 设计归第 7 章。
- 原卷第 32–34 页的水印已视觉确认；第一题中两离散序列图登记为重绘，保留所有抽样位置、幅值、坐标轴及 n=0 标注。

## Latest 2017 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2017.json` 覆盖 2017 年 8 个原文题组。离散系统性质归第 1 章，LT/ZT 关系与差分方程系统归第 2 章；第六题独立小题分别归入第 3 或第 4 章；IIR 设计归第 6 章，FIR 窗函数设计归第 7 章。
- 原卷第 35–37 页存在中央水印和推广页眉页脚；后续图形转写必须重绘，不能带入原卷水印。

## Latest 2019 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2019.json` 覆盖 2019 年 7 个原文题组。离散系统性质、离散卷积以及冲激采样—采样保持恢复均归第 1 章，栅栏效应归第 3 章，FIR 零极点和线性相位归第 7 章；连续时间题排除。
- 同时纠正 2016 年第六题：冲激采样、奈奎斯特频率、采样频谱与采样保持恢复是原课件第一章内容，已由“范围外”改为完整归入第 1 章。2019 年离散卷积图登记为重绘并保留抽样位置、幅值和原点。

## Latest 2020 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2020.json` 覆盖 2020 年 4 个原文题组。填空/简答独立分入第 1、2、3、4、5、8 章；两道 DFT 计算题归第 3 章，离散 LTI 频率响应题归第 2 章。
- 原卷有中央水印和推广页眉页脚。本年度题目均以文字和正式数学公式转写；不使用带水印的原卷页面。

## Latest 2021 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2021.json` 覆盖 2021 年 9 个原文题组。离散卷积及采样恢复归第 1 章，离散调制/解调归第 2 章，DFT 题归第 3 章，双线性 IIR 与 FIR 设计分别归第 6、7 章；连续时间题排除。
- 含图离散卷积题和离散调制/解调题均登记为重绘；须完整保留抽样位置、频谱支撑区、系统框图与全部频率标注，去除原卷水印。

## Latest 2022 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2022.json` 覆盖 2022 年 9 个原文题组。采样与 A/D—数字低通—D/A 恢复链归第 1 章，实序列 FFT 归第 4 章，离散 LTI 流图归第 2 章，IIR/FIR 设计分别归第 6/7 章；连续时间题排除。
- 含图的采样恢复链与离散流图均登记为重绘，必须完整保留频谱、延时支路、系数、节点、频率和信号标注，不能带入水印。

## Latest 2023 exam manual-review milestone — 2026-07-18

- 原 PDF 将多题误并为 `2023-qintro-01`；`full/source/exam_question_review_2023.json` 已依据真实小题边界拆为 8 个纳入单元：采样/离散系统归第 1 章，DFT/重叠保留归第 3 章，DIT-FFT 归第 4 章，离散 LSTI 归第 2 章，IIR 设计归第 6 章。
- 原卷带水印，讲义须按拆分后的题干、正式公式和重绘蝶形/必要示意图生成，不得将带水印整页作为题图。

## Latest 2024 exam manual-review milestone — 2026-07-18

- 原 PDF 将多页多题合并为 `2024-qintro-01`；`full/source/exam_question_review_2024.json` 已按真实题目拆为 9 个纳入单元：采样题归第 1 章，DFT 归第 3 章，重叠保留 FFT 归第 4 章，离散系统归第 2 章，线性相位和二阶 FIR 归第 7 章。
- 全部原卷图仅作内容依据；最终以无水印题干、公式及必要的重绘频谱/系统图呈现。

## Latest 2025 exam manual-review milestone — 2026-07-18

- `full/source/exam_question_review_2025.json` 覆盖 2025 年 9 个原文题组：离散系统与采样归第 1 章，采样后的 DTFT、离散 LSI 和 A/D—D/A 链归第 2 章，DFT 归第 3 章，IIR 方法归第 6 章，线性相位高通 FIR 归第 7 章。
- 至此，2002–2007、2013–2017、2019–2025 全部可用年份均已完成题号级人工依赖审核；下一步汇总最终题库、章节训练和末尾详解索引。

## Latest final exam-bank milestone — 2026-07-18

- `full/tools/build_exam_bank.py` 将所有人工审核记录统一生成 `full/source/exam_question_bank.json`。该题库含 156 个可纳入讲义的题目单元：第 1–8 章分别为 41、38、36、12、1、13、11、4 个，并保留年份、原始页码、来源段、依赖章节、落点章节与题图处置。
- 53 个明确连续时间范围外题组保留在 `out_of_scope_candidate_ids` 供审计，但不会进入 DSP 章节训练或末尾详解。测试保证 144 个原始候选均被恰好人工处置，无遗漏。

## Latest chapter drill-selection milestone — 2026-07-18

- `full/source/exam_drill_selection.json` 为第 1–8 章各确定了“重点精练”真题：除第 5 章因原始真题库仅有 1 道直接对应题外，每章均选 3 题，兼顾核心计算、频谱/图形判断与综合应用；其余同章题目进入“补充真题”。
- 第 5 章不为凑数杜撰真题；后续以课内例题补足训练量，并明确来源。测试校验所有精选题均真实存在于对应章节题库。

## Latest visual-reference and training-manifest milestone — 2026-07-22

- 已审阅用户提供的二十四稿参考 PDF（254 页）。视觉上吸收正式教材的深青蓝层级、克制信息框和低饱和黄铜金细线点缀；不直接复用其内容或图形，避免把可能不严谨、带水印或与源课件不一致的图带入新讲义。
- `full/tools/build_exam_training_manifest.py` 已将最终真题题库和已确认的重点精练选择合成为 `full/source/exam_training_manifest.json`。156 个纳入真题均被恰好分配为所属章节的“重点精练”或“补充真题”，并保留原题元数据、书末“真题整理详解”待最终分页回填状态，以及逐幅去水印／修复或重绘指令。
- TDD：先新增 `full/tests/test_build_exam_training_manifest.py` 并确认其因缺失实现而失败；实现后单测通过。下一步：将该清单接入可自然续排的全文生成管线，先完成真题题干转写、图形清理任务清单和书末详解页码回填机制。

## Latest watermarked-exam-figure queue milestone — 2026-07-22

- `full/tools/build_exam_figure_work_queue.py` 已将题库中 17 条带图记录归并为 11 项唯一源题图工作项，写入 `full/source/exam_figure_work_queue.json`。一个源题图若被拆分到多个独立小题／章节，清单会保留所有题号和落点章节，但只创建一项图形重绘工作，避免重复重绘后发生版本不一致。
- 11 项均明确为含水印、`redraw`；每项记录必须保留的坐标、曲线、公式、单位和标签，以及固定验收语句“渲染后逐幅核验：水印消失，且坐标、曲线、公式、单位、标签零丢失”。所有工作项目前均为 `pending_redraw_or_repair`，尚未把任何原卷图直接排入讲义。
- TDD：新增 `full/tests/test_build_exam_figure_work_queue.py` 并确认缺失实现时失败；实现后新增测试与全套 51 项测试通过。
