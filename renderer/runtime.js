import {
  createKnowledgeSimulation,
  beginNodeDrag,
  moveDraggedNode,
  endNodeDrag,
  drawKnowledgeStar,
  computeOverviewVisibilityPlan,
  overviewPresenceForNode,
  createIdentityCoreBody,
  setIdentityCorePointer,
  beginIdentityCoreDrag,
  endIdentityCoreDrag,
  updateIdentityCoreBody,
  createIdentityCoreInfluenceForce,
  drawIdentityCore,
  drawIdentityPresence,
  pickProjectAnchor,
  drawProjectAnchor,
  drawProjectProvenanceLinks,
  buildNodeDetailModel,
  createBackgroundField,
  drawBackgroundField,
  nodeSemanticVisibility,
  nextWheelScale,
  pointerZoomCorrection,
  semanticPeel,
} from './index.js';

const $ = id => document.getElementById(id);
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

async function loadScene() {
  const response = await fetch('./scene.json', { cache: 'no-store' });
  if (!response.ok) throw new Error(`scene.json: HTTP ${response.status}`);
  return response.json();
}

function boot(scene) {
  const canvas = $('universe');
  const ctx = canvas.getContext('2d');
  const card = $('detail-card');
  const tooltip = $('tooltip');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const startedAt = performance.now();
  const world = scene.viewport;
  const galaxies = Object.fromEntries(scene.galaxies.map(g => [g.id, { ...g }]));
  const nodes = scene.nodes.map(n => ({ ...n }));
  const nodeById = Object.fromEntries(nodes.map(n => [n.id, n]));
  const links = scene.relations.map(r => ({ ...r }));
  const anchors = scene.anchors.map(a => ({ ...a }));
  const background = createBackgroundField(scene.seed);
  const core = createIdentityCoreBody(scene.identity.x, scene.identity.y);
  const simulation = createKnowledgeSimulation(window.d3, nodes, links, galaxies);
  simulation.force('identity-core-field', createIdentityCoreInfluenceForce(core));

  let dpr = 1, W = 1, H = 1, overviewPlan = null;
  let selected = null, hovered = null, hoveredAnchor = null, galaxyFocus = null;
  let exploring = false, dragNode = null, draggingCore = false, panning = false, moved = false, lastPointer = null;
  let pointer = { x: 0, y: 0 };
  let camera = { x: 0, y: 0, scale: 1 };

  function resize() {
    const rect = canvas.getBoundingClientRect();
    W = Math.max(1, rect.width); H = Math.max(1, rect.height);
    dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    overviewPlan = computeOverviewVisibilityPlan(nodes, { width: W, height: H, galaxyCount: scene.galaxies.length });
  }

  function worldToScreen(x, y) {
    return { x: W / 2 + (x - world.width / 2) * camera.scale + camera.x, y: H / 2 + (y - world.height / 2) * camera.scale + camera.y };
  }
  function screenToWorld(x, y) {
    return { x: world.width / 2 + (x - W / 2 - camera.x) / camera.scale, y: world.height / 2 + (y - H / 2 - camera.y) / camera.scale };
  }
  function visibilityForNode(node) {
    return nodeSemanticVisibility({ layer: node.layer, kind: node.kind, viewScale: camera.scale, overviewPresence: overviewPresenceForNode(overviewPlan, node), galaxyFocused: galaxyFocus, nodeGalaxy: node.g, galaxyDepth: 1 });
  }
  const coreScreenPoint = () => worldToScreen(core.x, core.y);
  function pickCore(x, y) { const p = coreScreenPoint(); return Math.hypot(x - p.x, y - p.y) <= 27 * Math.max(0.86, camera.scale); }

  function pickNode(x, y) {
    let best = null, bestDistance = Infinity;
    for (const node of nodes) {
      if (visibilityForNode(node) < 0.08) continue;
      const p = worldToScreen(node.x, node.y);
      const distance = Math.hypot(x - p.x, y - p.y);
      if (distance <= 7 + node.size * 7 && distance < bestDistance) { best = node; bestDistance = distance; }
    }
    return best;
  }
  const anchorToScreen = anchor => worldToScreen(anchor.x, anchor.y);

  function relatedNodes(node) {
    const ids = [];
    for (const link of links) {
      const source = typeof link.source === 'string' ? link.source : link.source.id;
      const target = typeof link.target === 'string' ? link.target : link.target.id;
      if (source === node.id) ids.push(target); else if (target === node.id) ids.push(source);
    }
    return [...new Set(ids)].map(id => nodeById[id]).filter(Boolean);
  }

  function hideCard() { selected = null; card.classList.remove('show'); }
  function selectNode(node) { selected = node; renderCard(node); }

  function renderCard(node) {
    const detail = buildNodeDetailModel(node, { galaxyLabel: galaxies[node.g]?.name || '', relatedNodes: relatedNodes(node), evidence: node.evidence, sources: node.sources });
    $('detail-galaxy').textContent = detail.galaxy;
    $('detail-title').textContent = detail.title;
    $('detail-subtitle').textContent = detail.subtitle || '';
    $('detail-subtitle').hidden = !detail.subtitle;
    $('detail-project').textContent = detail.project || '';
    $('detail-project-row').hidden = !detail.project;
    $('detail-summary').textContent = detail.summary;
    const related = $('detail-related'); related.replaceChildren();
    for (const item of detail.related) {
      const button = document.createElement('button'); button.className = 'related-chip'; button.textContent = item.label;
      button.addEventListener('click', () => { const target = nodeById[item.id]; if (target) selectNode(target); });
      related.append(button);
    }
    $('detail-related-block').hidden = detail.related.length === 0;
    const evidence = $('detail-evidence'); evidence.replaceChildren();
    for (const item of detail.evidenceDisclosure.evidence) { const row = document.createElement('div'); row.className = 'evidence-item'; row.textContent = item.observation || item.id || ''; evidence.append(row); }
    const sources = $('detail-sources'); sources.replaceChildren();
    for (const source of detail.evidenceDisclosure.sources) { const row = document.createElement('div'); row.className = 'source-item'; row.textContent = source.title || source.id || ''; sources.append(row); }
    $('detail-evidence-label').textContent = detail.evidenceDisclosure.label;
    $('detail-evidence-footnote').textContent = detail.evidenceDisclosure.footnote;
    $('detail-disclosure').open = false;
    card.classList.add('show');
  }

  function showTooltip(title, subtitle, x, y) {
    if (!title) { tooltip.classList.remove('show'); return; }
    $('tooltip-title').textContent = title; $('tooltip-subtitle').textContent = subtitle || '';
    tooltip.style.left = `${x}px`; tooltip.style.top = `${y}px`; tooltip.classList.add('show');
  }
  function resetOverview() { camera = { x: 0, y: 0, scale: 1 }; galaxyFocus = null; hideCard(); }
  function focusGalaxy(gid) { if (gid && galaxies[gid]) { galaxyFocus = gid; exploring = true; } }

  function drawRelations() {
    ctx.save();
    for (const link of links) {
      const source = typeof link.source === 'string' ? nodeById[link.source] : link.source;
      const target = typeof link.target === 'string' ? nodeById[link.target] : link.target;
      if (!source || !target) continue;
      const vis = Math.min(visibilityForNode(source), visibilityForNode(target));
      if (vis < 0.07) continue;
      const sameFocus = galaxyFocus && source.g === galaxyFocus && target.g === galaxyFocus;
      const p1 = worldToScreen(source.x, source.y), p2 = worldToScreen(target.x, target.y);
      ctx.strokeStyle = `rgba(133,153,178,${(sameFocus ? 0.17 : 0.055) * vis})`; ctx.lineWidth = sameFocus ? 0.75 : 0.46;
      ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
    }
    ctx.restore();
  }

  function drawGalaxyLabels() {
    if (camera.scale < 1.12) return;
    ctx.save(); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    for (const g of scene.galaxies) {
      const p = worldToScreen(g.x, g.y - 56), focused = galaxyFocus === g.id;
      const alpha = focused ? 0.50 : clamp((camera.scale - 1.12) / 0.75, 0, 0.24);
      if (alpha < 0.02) continue;
      ctx.fillStyle = `rgba(142,160,181,${alpha})`; ctx.font = `${focused ? 500 : 400} 9px Inter,"PingFang SC","Microsoft YaHei",sans-serif`; ctx.fillText(g.name, p.x, p.y);
    }
    ctx.restore();
  }

  function drawAnchors(time) {
    for (const anchor of anchors) {
      const p = anchorToScreen(anchor), isHover = hoveredAnchor?.id === anchor.id;
      const alpha = drawProjectAnchor(ctx, anchor, time, { screenPoint: p, viewScale: camera.scale, focusedGalaxy: galaxyFocus, hovered: isHover, drawLabel: true });
      if (isHover || galaxyFocus === anchor.g) drawProjectProvenanceLinks(ctx, anchor, nodes, { anchorPoint: p, nodeToScreen: n => worldToScreen(n.x, n.y), anchorAlpha: alpha, visibilityForNode });
    }
  }

  function drawStars(time) {
    for (const node of nodes) {
      const visibility = visibilityForNode(node); if (visibility < 0.012) continue;
      const p = worldToScreen(node.x, node.y), sameGalaxy = galaxyFocus === node.g;
      drawKnowledgeStar(ctx, node, time, { screenPoint: p, viewScale: camera.scale, focusBoost: hovered?.id === node.id || selected?.id === node.id ? 0.58 : 0, galaxyBoost: sameGalaxy ? 0.45 : 0, dim: galaxyFocus && !sameGalaxy ? 0.56 : 0, layerVisibility: visibility, emphasis: selected?.id === node.id });
      const labelVisible = hovered?.id === node.id || selected?.id === node.id || (camera.scale > 1.58 && visibility > 0.62 && sameGalaxy);
      if (labelVisible) { ctx.fillStyle = `rgba(208,219,232,${selected?.id === node.id ? 0.78 : 0.56})`; ctx.font = '500 9px Inter,"PingFang SC","Microsoft YaHei",sans-serif'; ctx.textAlign = 'left'; ctx.textBaseline = 'middle'; ctx.fillText(node.name, p.x + 9, p.y - 1); }
    }
  }

  function frame(now) {
    const time = reducedMotion ? 0 : now;
    updateIdentityCoreBody(core);
    drawBackgroundField(ctx, background, time, { width: W, height: H, family: scene.field.dust_family, alpha: 1 });
    drawRelations(); drawGalaxyLabels(); drawAnchors(time); drawStars(time);
    const cp = coreScreenPoint();
    drawIdentityCore(ctx, scene.identity.family, time, { x: cp.x, y: cp.y, radius: 25 * clamp(camera.scale, 0.86, 1.25), monogram: scene.identity.monogram || scene.identity.label.slice(0, 2).toUpperCase(), viewScale: camera.scale });
    drawIdentityPresence(ctx, { title: scene.identity.title, label: scene.identity.label, subtitle: scene.identity.subtitle, source: scene.identity.source }, { corePoint: cp, viewScale: camera.scale, elapsedMs: now - startedAt, hoveringCore: pickCore(pointer.x, pointer.y), exploring });
    requestAnimationFrame(frame);
  }

  canvas.addEventListener('pointermove', event => {
    const rect = canvas.getBoundingClientRect(); pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    if (dragNode) { const w = screenToWorld(pointer.x, pointer.y); moveDraggedNode(dragNode, w.x, w.y); moved = true; return; }
    if (draggingCore) { const w = screenToWorld(pointer.x, pointer.y); setIdentityCorePointer(core, w.x, w.y); moved = true; return; }
    if (panning && lastPointer) { camera.x += pointer.x - lastPointer.x; camera.y += pointer.y - lastPointer.y; lastPointer = { ...pointer }; moved = true; exploring = true; return; }
    hoveredAnchor = pickProjectAnchor(anchors, pointer, anchorToScreen, { focusedGalaxy: galaxyFocus, viewScale: camera.scale });
    hovered = hoveredAnchor ? null : pickNode(pointer.x, pointer.y);
    if (hoveredAnchor) showTooltip(hoveredAnchor.name, '作品 / 经历锚点', event.clientX, event.clientY);
    else if (hovered) showTooltip(hovered.name, hovered.project || galaxies[hovered.g]?.name, event.clientX, event.clientY);
    else showTooltip(null);
    canvas.style.cursor = hovered || hoveredAnchor || pickCore(pointer.x, pointer.y) ? 'pointer' : 'grab';
  });

  canvas.addEventListener('pointerdown', event => {
    canvas.setPointerCapture(event.pointerId); moved = false; exploring = true;
    const rect = canvas.getBoundingClientRect(); pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    hoveredAnchor = pickProjectAnchor(anchors, pointer, anchorToScreen, { focusedGalaxy: galaxyFocus, viewScale: camera.scale });
    hovered = hoveredAnchor ? null : pickNode(pointer.x, pointer.y);
    if (pickCore(pointer.x, pointer.y)) { const w = screenToWorld(pointer.x, pointer.y); draggingCore = true; beginIdentityCoreDrag(simulation, core, w.x, w.y); return; }
    if (hovered) { dragNode = hovered; beginNodeDrag(simulation, dragNode); return; }
    if (hoveredAnchor) return;
    panning = true; lastPointer = { ...pointer }; canvas.style.cursor = 'grabbing';
  });

  canvas.addEventListener('pointerup', event => {
    if (dragNode) { const node = dragNode; endNodeDrag(simulation, node); dragNode = null; if (!moved) selectNode(node); }
    else if (draggingCore) { endIdentityCoreDrag(simulation, core); draggingCore = false; if (!moved) resetOverview(); }
    else if (hoveredAnchor && !moved) focusGalaxy(hoveredAnchor.g);
    panning = false; lastPointer = null; canvas.releasePointerCapture(event.pointerId);
  });

  canvas.addEventListener('wheel', event => {
    event.preventDefault(); exploring = true;
    const rect = canvas.getBoundingClientRect(), px = event.clientX - rect.left, py = event.clientY - rect.top;
    const before = screenToWorld(px, py), oldScale = camera.scale, nextScale = nextWheelScale(camera.scale, event.deltaY, galaxyFocus);
    camera.scale = nextScale;
    const correction = pointerZoomCorrection({ pointerX: px, pointerY: py, worldBefore: before, worldToScreenAfter: worldToScreen });
    camera.x += correction.dx; camera.y += correction.dy;
    const peel = semanticPeel({ zoomingOut: nextScale < oldScale, viewScale: nextScale, selected, galaxyFocused: galaxyFocus });
    if (peel.leaveDetail) hideCard(); if (peel.leaveGalaxy) galaxyFocus = null;
  }, { passive: false });

  canvas.addEventListener('pointerleave', () => { hovered = null; hoveredAnchor = null; if (!panning && !dragNode && !draggingCore) showTooltip(null); });
  $('detail-close').addEventListener('click', hideCard);
  addEventListener('resize', resize);
  resize(); requestAnimationFrame(frame);
}

loadScene().then(boot).catch(error => {
  const fatal = document.getElementById('fatal'); fatal.hidden = false; fatal.textContent = `Knowledge Constellation 无法加载：${String(error.message || error)}`; console.error(error);
});
