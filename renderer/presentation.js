// Product-surface presentation helpers.
// Recognition audit language remains available in deeper evidence inspection,
// but must not dominate the default node detail card.

function normalizeText(value) {
  return typeof value === 'string' ? value.trim() : '';
}

function sameMeaning(a, b) {
  const x = normalizeText(a).toLowerCase().replace(/[\s/_-]+/g, '');
  const y = normalizeText(b).toLowerCase().replace(/[\s/_-]+/g, '');
  return Boolean(x && y && x === y);
}

export function dedupeNodeSubtitle(title, subtitle) {
  const clean = normalizeText(subtitle);
  if (!clean || sameMeaning(title, clean)) return null;
  return clean;
}

export function buildNodeDetailModel(node, options = {}) {
  const {
    galaxyLabel = '',
    relatedNodes = [],
    evidence = node?.evidence || [],
    sources = node?.sources || [],
  } = options;

  if (!node) return null;

  return Object.freeze({
    title: normalizeText(node.name || node.label || node.id),
    subtitle: dedupeNodeSubtitle(node.name || node.label || node.id, node.en),
    galaxy: normalizeText(galaxyLabel),
    project: normalizeText(node.project || node.anchor || ''),
    summary: normalizeText(node.summary || node.reason || ''),
    related: relatedNodes.slice(0, 6).map((other) => ({
      id: other.id,
      label: normalizeText(other.name || other.label || other.id),
    })),
    evidenceDisclosure: Object.freeze({
      label: '查看依据',
      evidence: Array.isArray(evidence) ? [...evidence] : [],
      sources: Array.isArray(sources) ? [...sources] : [],
      footnote: '这些痕迹用于解释为什么这颗星存在，不等同于能力评分或独立实现证明。',
    }),
  });
}

// These are Recognition / audit concepts. They can exist in evidence tooling,
// but are deliberately excluded from the default product detail surface.
export const DEFAULT_DETAIL_EXCLUDES = Object.freeze([
  'state',
  'confidence',
  'reliability',
  'known',
  'unknown',
  'nextStep',
  'modelVersion',
]);
