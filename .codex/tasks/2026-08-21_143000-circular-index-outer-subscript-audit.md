# 循环索引外置下标复核

## Objective

将读者可见的循环索引统一为完整圆括号外的周期下标，例如 \(x\left((n+m)\right)_N\)；禁止使用 `mod N` 表示循环索引。

## Verification

- 已扫描 `full/source`、`full/tools` 与 `full/tests` 的可读源文件：未发现 `mod N`、`\\bmod N`、`\\operatorname{mod} N`、`\\mathrm{mod} N` 或 `\\pmod N`。
- 非循环相位主值中的 `\\pmod{2\\pi}` 不属于本规则，保持不变。
- 第三章 DFT 组件回归通过：`4 passed`；测试锁定 `x\left((n-n_0)\right)_N`、`x^*\left((N-n)\right)_N` 与循环移位示例，并禁止旧 `mod` 命令进入该组件。
- 已把遗留的文字表述“按模 \(N\)”和“按模 8”分别改为“按 \(N\) 周期理解”和“按 8 周期下标取值”，避免正文文字与公式记法冲突。
- 137 页全书候选 PDF 导出结果为 math=3890、unrendered=[]、pageErrors=[]；150 dpi 视觉复核第三章循环移位、共轭对称和循环卷积所在页，外置周期下标清晰且未见 mod N、公式源码、裁切或重叠。

## Result

当前有效讲义源码已经采用用户指定的外置周期下标记号；本次仅统一读者可见的循环索引表述，不改动题干或数学含义。
