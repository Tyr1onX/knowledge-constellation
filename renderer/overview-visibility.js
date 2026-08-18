// Adaptive first-glance visibility for a growing Knowledge Constellation.
// More modeled knowledge may create more visible stars, but density is never competence.

export const OVERVIEW_VISIBILITY = Object.freeze({
  minTarget: 14,
  maxTarget: 48,
  areaPerStar: 30000,
  secondaryMinPresence: 0.20,
  secondaryMaxPresence: 0.58,
  traceMinPresence: 0.07,
  traceMaxPresence: 0.24,
  secondaryRichnessMultiplier: 2.30,
  galaxyRichnessMultiplier: 2.00,
});

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function importanceScore(node) {
  let score = (node.layer === 'primary' ? 4 : 0) + (node.size || 0) * 2;
  if (node.kind === 'core') score += 1.3;
  if (node.kind === 'normal') score += 0.35;
  if (node.kind === 'soft') score += 0.12;
  if (node.kind === 'trace') score -= 0.28;
  return score;
}

export function computeOverviewVisibilityPlan(
  nodes,
  { width = 1440, height = 900, galaxyCount = 0 } = {},
) {
  const primary = nodes.filter((node) => node.layer !== 'secondary');
  const secondary = nodes.filter((node) => node.layer === 'secondary');

  const area = Math.max(320 * 520, width * height);
  const capacity = clamp(
    Math.round(area / OVERVIEW_VISIBILITY.areaPerStar),
    OVERVIEW_VISIBILITY.minTarget,
    OVERVIEW_VISIBILITY.maxTarget,
  );

  const galaxyBonus = Math.round(
    Math.sqrt(Math.max(1, galaxyCount)) * OVERVIEW_VISIBILITY.galaxyRichnessMultiplier,
  );
  const richnessTarget = Math.round(
    primary.length +
      Math.sqrt(secondary.length) * OVERVIEW_VISIBILITY.secondaryRichnessMultiplier +
      galaxyBonus,
  );
  const target = Math.min(
    nodes.length,
    capacity,
    Math.max(primary.length, richnessTarget),
  );

  const ordered = [...secondary].sort((a, b) => {
    const delta = importanceScore(b) - importanceScore(a);
    return Math.abs(delta) > 0.0001 ? delta : a.id.localeCompare(b.id);
  });

  const keep = Math.max(0, target - primary.length);
  const presenceById = {};

  ordered.slice(0, keep).forEach((node, index) => {
    const rank = keep <= 1 ? 0 : index / (keep - 1);
    const trace = node.kind === 'trace';
    const high = trace
      ? OVERVIEW_VISIBILITY.traceMaxPresence
      : OVERVIEW_VISIBILITY.secondaryMaxPresence;
    const low = trace
      ? OVERVIEW_VISIBILITY.traceMinPresence
      : OVERVIEW_VISIBILITY.secondaryMinPresence;
    presenceById[node.id] = high + (low - high) * rank;
  });

  return Object.freeze({
    target,
    capacity,
    primaryCount: primary.length,
    modeledCount: nodes.length,
    presenceById: Object.freeze(presenceById),
  });
}

export function overviewPresenceForNode(plan, node) {
  if (node.layer !== 'secondary') return 1;
  return plan?.presenceById?.[node.id] || 0;
}
