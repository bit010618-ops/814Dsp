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

function decodeHtmlEntitiesInLatex(latex) {
  const entities = {
    amp: "&",
    gt: ">",
    lt: "<",
    quot: '"',
    "#39": "'",
  };
  let decoded = latex;
  for (let pass = 0; pass < 2; pass += 1) {
    const next = decoded.replace(/&(amp|gt|lt|quot|#39);/g, (_, name) => entities[name]);
    if (next === decoded) break;
    decoded = next;
  }
  return decoded;
}

function renderFormula(MathJax, latex, display) {
  const node = MathJax.tex2svg(decodeHtmlEntitiesInLatex(latex).trim(), { display });
  return MathJax.startup.adaptor
    .outerHTML(node)
    .replace('<svg ', '<svg class="mathjax-svg" ')
    .replace('<mjx-container ', '<mjx-container data-mathjax-static="true" ');
}

function externalizeSvgForeignObjectMath(document) {
  return document.replace(
    /<foreignObject\b([^>]*)>([\s\S]*?)<\/foreignObject>/gi,
    (foreignObject, attributes, content) => {
      const mathSvg = content.match(/<svg\b[^>]*class="mathjax-svg"[\s\S]*?<\/svg>/i);
      if (!mathSvg) {
        return foreignObject;
      }
      const opening = mathSvg[0].match(/^<svg\b([^>]*)>/i);
      if (!opening) {
        return foreignObject;
      }
      const mathAttributes = opening[1].replace(
        /\s(?:width|height|style)="[^"]*"/gi,
        "",
      );
      const inner = mathSvg[0].slice(opening[0].length, -"</svg>".length);
      return `<svg${attributes}${mathAttributes} preserveAspectRatio="xMidYMid meet">${inner}</svg>`;
    },
  );
}

function collectSvgStyles(document) {
  return [...document.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)].map((match) => match[1]);
}

function matchingRules(styles, className) {
  const needle = `.${className}`;
  return styles.flatMap((style) =>
    [...style.matchAll(/([^{}]+)\{([^{}]*)\}/g)]
      .filter((rule) => rule[1].includes(needle))
      .map((rule) => `${rule[1]}{${rule[2]}}`),
  );
}

function inlineStylesForStaticSvg(document) {
  const styles = collectSvgStyles(document);
  return document.replace(/<svg\b([^>]*)>/gi, (openingTag, attributes) => {
    const classAttribute = attributes.match(/\bclass="([^"]+)"/i);
    if (!classAttribute) {
      return openingTag;
    }
    const rootClass = classAttribute[1]
      .split(/\s+/)
      .find((className) => className.endsWith("-svg") && className !== "mathjax-svg");
    if (!rootClass) {
      return openingTag;
    }
    const rules = matchingRules(styles, rootClass);
    if (rules.length === 0) {
      return openingTag;
    }
    return `${openingTag}<style data-static-svg-style="${rootClass}">${rules.join("")}</style>`;
  });
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
    const svgMathExternalized = externalizeSvgForeignObjectMath(rendered);
    const svgStylesInlined = inlineStylesForStaticSvg(svgMathExternalized);
    fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    const isolated = svgStylesInlined.replace(
      'svg{max-width:100%;height:auto}',
      'svg:not(.mathjax-svg){max-width:100%;height:auto}',
    );
    const staticStyle = '<style data-mathjax-static-style="true">mjx-container{font-size:17.5pt}mjx-container[display="true"]{font-size:18pt}mjx-container[display="true"] svg.mathjax-svg{max-width:100%;height:auto}</style>';
    const styled = isolated.includes('</head>')
      ? isolated.replace('</head>', `${staticStyle}</head>`)
      : /<body\b[^>]*>/i.test(isolated)
        ? isolated.replace(/<body\b[^>]*>/i, (bodyTag) => `${staticStyle}${bodyTag}`)
        : isolated.replace(/<html\b[^>]*>/i, (htmlTag) => `${htmlTag}${staticStyle}`);
    fs.writeFileSync(outputPath, styled, "utf8");
  })
  .catch((error) => {
    console.error(error.stack || error);
    process.exit(1);
  });
