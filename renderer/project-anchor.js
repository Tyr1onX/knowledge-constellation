// Project Anchors turn real experiences / projects into spatial provenance.
// They are not Knowledge Stars, skill badges, or competence signals.

export const PROJECT_ANCHOR_STYLE = Object.freeze({
  overviewAlpha: 0.12,
  focusedBoost: 0.12,
  hoverBoost: 0.34,
  revealStart: 1.0,
  revealRange: 0.55,
  labelRevealScale: 1.14,
  hitRadius: 18,
});

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

export function projectAnchorVisibility({
  viewScale,
  focusedGalaxy = null,
  anchorGalaxy = null,
  hovered = false,
}) {
  const zoom = clamp01((viewScale - PROJECT_ANCHOR_STYLE.revealStart) / PROJECT_ANCHOR_STYLE.revealRange);
  const base = PROJECT_ANCHOR_STYLE.overviewAlpha + zoom * 0.16;
  const focus = focusedGalaxy && focusedGalaxy === anchorGalaxy ? PROJECT_ANCHOR_STYLE.focusedBoost : 0;
  const hover = hovered ? PROJECT_ANCHOR_STYLE.hoverBoost : 0;
  return Math.min(0.72, base + focus + hover);
}

export function projectAnchorLabelVisibility({ viewScale, anchorAlpha }) {
  if (viewScale < PROJECT_ANCHOR_STYLE.labelRevealScale) return anchorAlpha * 1.05;
  return Math.min(0.72, anchorAlpha * 1.7);
}

export function pickProjectAnchor(anchors, pointer, projectToScreen, options = {}) {
  const {
    focusedGalaxy = null,
    viewScale = 1,
  } = options;

  let best = null;
  let bestDistance = Infinity;

  for (const anchor of anchors) {
    if (focusedGalaxy && anchor.g !== focusedGalaxy && viewScale < 1.85) continue;
    const p = projectToScreen(anchor);
    const distance = Math.hypot(pointer.x - p.x, pointer.y - p.y);
    if (distance < PROJECT_ANCHOR_STYLE.hitRadius && distance < bestDistance) {
      best = anchor;
      bestDistance = distance;
    }
  }

  return best;
}

export function drawProjectAnchor(ctx, anchor, time, options) {
  const {
    screenPoint,
    viewScale = 1,
    focusedGalaxy = null,
    hovered = false,
    drawLabel = true,
  } = options;

  const alpha = projectAnchorVisibility({
    viewScale,
    focusedGalaxy,
    anchorGalaxy: anchor.g,
    hovered,
  });

  const p = screenPoint;
  const phase = time / (16000 + (anchor.phaseOffset || 0) * 2300) + (anchor.phaseOffset || 0) * 0.83;
  const radius = 5.2 + (hovered ? 1.2 : 0);

  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(phase * 0.10);
  ctx.scale(1, 0.58);
  ctx.strokeStyle = `rgba(166,188,212,${alpha * 0.42})`;
  ctx.lineWidth = 0.48;
  ctx.beginPath();
  ctx.arc(0, 0, radius * 1.75, 0.25, Math.PI * 1.58);
  ctx.stroke();
  ctx.restore();

  ctx.fillStyle = `rgba(224,235,246,${alpha * 0.82})`;
  ctx.beginPath();
  ctx.arc(p.x, p.y, hovered ? 1.45 : 1.05, 0, Math.PI * 2);
  ctx.fill();

  if (drawLabel) {
    const labelAlpha = projectAnchorLabelVisibility({ viewScale, anchorAlpha: alpha });
    if (labelAlpha > 0.10) {
      ctx.font = `500 ${hovered ? 9.4 : 8.5}px Inter,"PingFang SC",sans-serif`;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = `rgba(165,181,201,${labelAlpha})`;
      ctx.fillText(anchor.name, p.x + 10, p.y + 0.5);
    }
  }

  return alpha;
}

export function drawProjectProvenanceLinks(ctx, anchor, nodes, options) {
  const {
    anchorPoint,
    nodeToScreen,
    anchorAlpha,
    visibilityForNode = () => 1,
  } = options;

  for (const node of nodes) {
    if (node.project !== anchor.name) continue;
    const visibility = visibilityForNode(node);
    if (visibility < 0.08) continue;

    const p = nodeToScreen(node);
    const gradient = ctx.createLinearGradient(anchorPoint.x, anchorPoint.y, p.x, p.y);
    gradient.addColorStop(0, `rgba(118,146,177,${anchorAlpha * 0.075})`);
    gradient.addColorStop(1, 'rgba(118,146,177,0)');
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 0.38;
    ctx.beginPath();
    ctx.moveTo(anchorPoint.x, anchorPoint.y);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
  }
}
