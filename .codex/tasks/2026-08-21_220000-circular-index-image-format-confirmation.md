# 循环索引图片格式确认

## Objective

将读者可见的循环索引记法以用户提供的图片为唯一格式基准：周期长度写在完整圆括号索引的外部下标，例如 \(x\left((n+m)\right)_N\)；禁止使用 `mod N`、`\\bmod N` 或等价形式。

## Scope

- 仅适用于循环索引，不改变相位主值、同余类等具有独立数学语义的模运算。
- 保持完整 LaTeX 与 MathJax 整体渲染。

## Verification

- 扫描有效讲义源码未发现读者可见的 `mod N`、`\\bmod N`、`\\operatorname{mod} N`、`\\mathrm{mod} N` 或 `\\pmod N`。
- 第三章正文的周期延拓、循环移位、循环共轭对称和循环卷积均使用外置周期下标。
- 既有第三章回归禁止旧式记法重新进入组件；非循环的 `\\pmod{2\\pi}` 不在本规则替换范围内。

## Result

当前有效讲义源码已符合图片所示记法；本次补充最终样式确认与持久化记录，不改变循环运算的数学含义。

## Delivery

- 本地提交：`c20cb2a Record circular index notation preference`。
- 已正常推送至 `origin/main`。
