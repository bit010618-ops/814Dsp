#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const [inputPath, outputPath] = process.argv.slice(2);
if (!inputPath || !outputPath) {
  console.error("Usage: prerender_mathjax_svg.js INPUT.html OUTPUT.html");
  process.exit(2);
}

const mathjaxPath = path.resolve(__dirname, "..", "vendor", "mathjax", "es5", "node-main.js");
const mathjax = require(mathjaxPath);

function renderFormula(MathJax, latex, display) {
  const node = MathJax.tex2svg(latex.trim(), { display });
  return MathJax.startup.adaptor
    .outerHTML(node)
    .replace('<svg ', '<svg class="mathjax-svg" ')
    .replace('<mjx-container ', '<mjx-container data-mathjax-static="true" ');
}

mathjax
  .init({ loader: { load: ["input/tex", "output/svg"] } })
  .then((MathJax) => {
    const source = fs.readFileSync(inputPath, "utf8");
    const withDisplay = source.replace(/\\\[([\s\S]*?)\\\]/g, (_, latex) =>
      renderFormula(MathJax, latex, true),
    );
    const rendered = withDisplay.replace(/\\\(([\s\S]*?)\\\)/g, (_, latex) =>
      renderFormula(MathJax, latex, false),
    );
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    const isolated = rendered.replace(
      'svg{max-width:100%;height:auto}',
      'svg:not(.mathjax-svg){max-width:100%;height:auto}',
    );
    const staticStyle = '<style data-mathjax-static-style="true">mjx-container{font-size:17.5pt}mjx-container[display="true"]{font-size:18pt}mjx-container[display="true"] svg.mathjax-svg{max-width:100%;height:auto}</style>';
    const styled = isolated.includes('</head>')
      ? isolated.replace('</head>', `${staticStyle}</head>`)
      : `${staticStyle}${isolated}`;
    fs.writeFileSync(outputPath, styled, "utf8");
  })
  .catch((error) => {
    console.error(error.stack || error);
    process.exit(1);
  });
