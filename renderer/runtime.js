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
  createAmbientMeteor,
  drawAmbientMeteor,
  nodeSemanticVisibility,
  nextWheelScale,
  semanticPeel,
} from './index.js';

// Canonical page choreography. Generated sites and the repository preview must
// use this runtime instead of rebuilding camera, labels, links or ambience.
export const RUNTIME_BASELINE = Object.freeze({
  worldFit: 'contain',
  galaxyFocusScale: 1.48,
  primaryLabelRevealScale: 1.16,
  faintGalaxyLabelsAtOverview: true,
  persistentWeakProvenance: true,
  rareAmbientMeteor: true,
});

const $ = id => document.getElementById(id);
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

const PALETTES = Object.freeze({
  cool: [[169, 201, 236], [188, 205, 238], [171, 218, 222], [196, 190, 232], [178, 211, 238], [183, 221, 211]],
  cool_neutral: [[171, 201, 235], [213, 190, 232], [178, 222, 214], [225, 199, 176], [190, 207, 239], [207, 194, 226]],
  neutral: [[192, 207, 226], [216, 201, 226], [190, 219, 211], [224, 207, 186], [201, 207, 226], [211, 201, 218]],
  warm_neutral: [[209, 201, 220], [228, 201, 180], [197, 219, 207], [229, 211, 188], [202, 208, 229], [218, 196, 211]],
  warm: [[225, 204, 185], [230, 192, 173], [213, 214, 195], [232, 214, 184], [210, 205, 224], [224, 194, 203]],
});

function paletteForScene(scene) {
  return PALETTES[scene.field?.temperature_bias] || PALETTES.cool_neutral;
}

async function loadScene() {
  if (window.__KC_SCENE__) return window.__KC_SCENE__;
  const source = document.documentElement.dataset.kcScene || './scene.json';
  const response = await fetch(source, { cache: 'no-store' });
  if (!response.ok) throw new Error(`${source}: HTTP ${response.status}`);
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
  const palette = paletteForScene(scene);
  const galaxyList = scene.galaxies.map((g, i) => ({ ...g, color: g.color || palette[i % palette.length], depth: 0.90 + clamp(g.dominance ?? 0.5, 0, 1) * 0.10 }));
  const galaxies = Object.fromEntries(galaxyList.map(g => [g.id, g]));
  const nodes = scene.nodes.map(n => ({ ...n }));
  const nodeById = Object.fromEntries(nodes.map(n => [n.id, n]));
  const links = scene.relations.map(r => ({ ...r }));
  const anchors = scene.anchors.map(a => ({ ...a }));
  const background = createBackgroundField(scene.seed);
  const core = createIdentityCoreBody(scene.identity.x, scene.identity.y);
  const simulation = createKnowledgeSimulation(window.d3, nodes, links, galaxies);
  simulation.force('identity-core-field', createIdentityCoreInfluenceForce(core));

  const densityAlpha = { very_sparse: 0.72, sparse: 0.86, medium: 1, dense: 1.05 }[scene.field?.density] || 0.9;
  const motionScale = reducedMotion ? 0 : ({ quiet: 0.76, balanced: 1, lively: 1.14 }[scene.motion?.temperament] || 1);
  const useStellarTemperature = scene.stars?.temperature_variation !== 'low';

  let dpr = 1, W = 1, H = 1, overviewPlan = null;
  let selected = null, hovered = null, hoveredAnchor = null, galaxyFocus = null;
  let exploring = false, dragNode = null, draggingCore = false, panning = false, moved = false;
  let pointer = { x: 0, y: 0 }, lastPointer = null, pointerDown = { x: 0, y: 0 };
  let camera = { x: 0, y: 0, scale: 1 }, targetCamera = null;
  let meteor = null, nextMeteorAt = startedAt + 9000 + Math.random() * 9000;

  document.title = `${scene.subject?.label || scene.identity.label} · Knowledge Constellation`;

  function resize() {
    const rect = canvas.getBoundingClientRect();
    W = Math.max(1, rect.width); H = Math.max(1, rect.height);
    dpr = Math.max(1, Math.min(2, window.devicePixelRatio || 1));
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    overviewPlan = computeOverviewVisibilityPlan(nodes, { width: W, height: H, galaxyCount: galaxyList.length });
  }

  function sceneScale() { return Math.min(W / world.width, H / world.height); }
  function baseScreen(x, y) {
    const s = sceneScale(), cw = world.width * s, ch = world.height * s;
    return { x: (W - cw) / 2 + x * s, y: (H - ch) / 2 + y * s };
  }
  function worldToScreen(x, y) {
    const p = baseScreen(x, y);
    return {
      x: p.x * camera.scale + camera.x + (1 - camera.scale) * W / 2,
      y: p.y * camera.scale + camera.y + (1 - camera.scale) * H / 2,
    };
  }
  function screenToWorld(x, y) {
    const s = sceneScale(), cw = world.width * s, ch = world.height * s;
    const ox = (W - cw) / 2, oy = (H - ch) / 2;
    const px = (x - camera.x - (1 - camera.scale) * W / 2) / camera.scale;
    const py = (y - camera.y - (1 - camera.scale) * H / 2) / camera.scale;
    return { x: (px - ox) / s, y: (py - oy) / s };
  }
  function cameraForWorld(x, y, scale) {
    const p = baseScreen(x, y);
    return {
      scale,
      x: W / 2 - p.x * scale - (1 - scale) * W / 2,
      y: H / 2 - p.y * scale - (1 - scale) * H / 2,
    };
  }
  function animateTo(next) { targetCamera = next; }
  function tickCamera() {
    if (!targetCamera) return;
    const ease = 0.095;
    camera.x += (targetCamera.x - camera.x) * ease;
    camera.y += (targetCamera.y - camera.y) * ease;
    camera.scale += (targetCamera.scale - camera.scale) * ease;
    if (Math.abs(targetCamera.x - camera.x) < 0.2 && Math.abs(targetCamera.y - camera.y) < 0.2 && Math.abs(targetCamera.scale - camera.scale) < 0.001) {
      camera = { ...targetCamera }; targetCamera = null;
    }
  }

  function visibilityForNode(node) {
    return nodeSemanticVisibility({
      layer: node.layer,
      kind: node.kind,
      viewScale: camera.scale,
      overviewPresence: overviewPresenceForNode(overviewPlan, node),
      galaxyFocused: galaxyFocus,
      nodeGalaxy: node.g,
      galaxyDepth: galaxies[node.g]?.depth || 1,
    });
  }
  const coreScreenPoint = () => worldToScreen(core.x, core.y);
  function pickCore(x, y) { const p = coreScreenPoint(); return Math.hypot(x - p.x, y - p.y) <= 30 * Math.max(0.9, camera.scale); }
  function pickNode(x, y) {
    let best = null, bestDistance = Infinity;
    for (const node of nodes) {
      if (visibilityForNode(node) < 0.08) continue;
      const p = worldToScreen(node.x, node.y);
      const distance = Math.hypot(x - p.x, y - p.y);
      const hit = 10 + Math.max(0.3, node.size) * 5 * camera.scale;
      if (distance <= hit && distance < bestDistance) { best = node; bestDistance = distance; }
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
  function selectNode(node) { selected = node; exploring = true; renderCard(node); }
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
  function resetOverview() {
    galaxyFocus = null; hideCard(); exploring = true;
    animateTo({ x: 0, y: 0, scale: 1 });
  }
  function focusGalaxy(gid) {
    const g = galaxies[gid]; if (!g) return;
    galaxyFocus = gid; exploring = true; hideCard();
    animateTo(cameraForWorld(g.x, g.y, RUNTIME_BASELINE.galaxyFocusScale));
  }

  function drawRelations() {
    ctx.save();
    for (const link of links) {
      const source = typeof link.source === 'string' ? nodeById[link.source] : link.source;
      const target = typeof link.target === 'string' ? nodeById[link.target] : link.target;
      if (!source || !target) continue;
      const vis = Math.min(visibilityForNode(source), visibilityForNode(target));
      if (vis < 0.06) continue;
      const p1 = worldToScreen(source.x, source.y), p2 = worldToScreen(target.x, target.y);
      const selectedLink = selected && (selected.id === source.id || selected.id === target.id);
      const sameFocused = galaxyFocus && source.g === galaxyFocus && target.g === galaxyFocus;
      const cross = source.g !== target.g;
      const alpha = (cross ? 0.012 : 0.028) + (selectedLink ? 0.085 : 0) + (sameFocused ? 0.018 : 0);
      const c1 = galaxies[source.g]?.color || [171, 196, 224], c2 = galaxies[target.g]?.color || c1;
      const grad = ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
      grad.addColorStop(0, `rgba(${c1[0]},${c1[1]},${c1[2]},${alpha * vis})`);
      grad.addColorStop(0.5, `rgba(136,164,196,${alpha * 0.72 * vis})`);
      grad.addColorStop(1, `rgba(${c2[0]},${c2[1]},${c2[2]},${alpha * vis})`);
      ctx.strokeStyle = grad; ctx.lineWidth = selectedLink ? 0.72 : 0.42;
      ctx.beginPath(); ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.stroke();
    }
    ctx.restore();
  }

  function drawGalaxyLabels() {
    ctx.save(); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    for (const g of galaxyList) {
      const p = worldToScreen(g.x, g.y - (88 + (g.mass || 0.5) * 18));
      const focused = galaxyFocus === g.id;
      const alpha = focused ? 0.37 : clamp(0.15 - Math.max(0, camera.scale - 1) * 0.055, 0.075, 0.15);
      const c = g.color;
      ctx.fillStyle = `rgba(${c[0]},${c[1]},${c[2]},${alpha})`;
      ctx.font = `${focused ? 500 : 450} ${focused ? 9.5 : 8.5}px Inter,"PingFang SC","Microsoft YaHei",sans-serif`;
      ctx.fillText(g.name, p.x, p.y);
    }
    ctx.restore();
  }

  function drawAnchors(time) {
    for (const anchor of anchors) {
      const p = anchorToScreen(anchor), isHover = hoveredAnchor?.id === anchor.id;
      const alpha = drawProjectAnchor(ctx, anchor, time, { screenPoint: p, viewScale: camera.scale, focusedGalaxy: galaxyFocus, hovered: isHover, drawLabel: true });
      drawProjectProvenanceLinks(ctx, anchor, nodes, { anchorPoint: p, nodeToScreen: n => worldToScreen(n.x, n.y), anchorAlpha: alpha, visibilityForNode });
    }
  }

  function drawStars(time) {
    for (const node of nodes) {
      const visibility = visibilityForNode(node); if (visibility < 0.012) continue;
      const p = worldToScreen(node.x, node.y), sameGalaxy = galaxyFocus === node.g;
      drawKnowledgeStar(ctx, node, time, {
        screenPoint: p,
        galaxyColor: galaxies[node.g]?.color,
        viewScale: camera.scale,
        focusBoost: selected?.id === node.id ? 1 : hovered?.id === node.id ? 0.48 : 0,
        galaxyBoost: sameGalaxy ? 0.34 : 0,
        dim: galaxyFocus && !sameGalaxy ? 0.52 : 0,
        layerVisibility: visibility,
        emphasis: selected?.id === node.id,
        useStellarTemperature,
      });
      const showLabel = hovered?.id === node.id || selected?.id === node.id || (node.layer === 'primary' && camera.scale > RUNTIME_BASELINE.primaryLabelRevealScale);
      if (showLabel) {
        const alpha = hovered?.id === node.id || selected?.id === node.id ? 0.82 : Math.min(0.34, Math.max(0, camera.scale - 1.05) * 0.34) * visibility;
        if (alpha >= 0.06) {
          ctx.fillStyle = `rgba(197,211,227,${alpha})`; ctx.font = `${hovered?.id === node.id || selected?.id === node.id ? 500 : 450} ${hovered?.id === node.id || selected?.id === node.id ? 9.5 : 8.2}px Inter,"PingFang SC","Microsoft YaHei",sans-serif`;
          ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(node.name, p.x, p.y + 15 + node.size * 3);
        }
      }
    }
  }

  function frame(now) {
    tickCamera(); updateIdentityCoreBody(core);
    const visualTime = motionScale ? (now - startedAt) * motionScale : 0;
    drawBackgroundField(ctx, background, visualTime, { width: W, height: H, family: scene.field.dust_family, alpha: densityAlpha });
    drawGalaxyLabels(); drawRelations(); drawAnchors(visualTime); drawStars(visualTime);
    const cp = coreScreenPoint();
    drawIdentityCore(ctx, scene.identity.family, visualTime, { x: cp.x, y: cp.y, radius: 24 * Math.max(0.86, camera.scale), monogram: scene.identity.monogram || scene.identity.label.slice(0, 2).toUpperCase(), viewScale: camera.scale });
    drawIdentityPresence(ctx, { title: scene.identity.title, label: scene.identity.label, subtitle: scene.identity.subtitle, source: scene.identity.source }, { corePoint: cp, viewScale: camera.scale, elapsedMs: now - startedAt, hoveringCore: pickCore(pointer.x, pointer.y), exploring });
    if (!reducedMotion) {
      if (!meteor && now >= nextMeteorAt) { meteor = createAmbientMeteor(now); nextMeteorAt = now + 16000 + Math.random() * 15000; }
      if (meteor && !drawAmbientMeteor(ctx, meteor, now, W, H)) meteor = null;
    }
    requestAnimationFrame(frame);
  }

  function updateHover(clientX = pointer.x, clientY = pointer.y) {
    hoveredAnchor = pickProjectAnchor(anchors, pointer, anchorToScreen, { focusedGalaxy: galaxyFocus, viewScale: camera.scale });
    hovered = hoveredAnchor ? null : pickNode(pointer.x, pointer.y);
    if (hoveredAnchor) showTooltip(hoveredAnchor.name, '作品 / 经历锚点', clientX, clientY);
    else if (hovered) showTooltip(hovered.name, hovered.project || galaxies[hovered.g]?.name, clientX, clientY);
    else showTooltip(null);
    canvas.style.cursor = hovered || hoveredAnchor || pickCore(pointer.x, pointer.y) ? 'pointer' : (panning || dragNode || draggingCore ? 'grabbing' : 'grab');
  }

  canvas.addEventListener('pointermove', event => {
    const rect = canvas.getBoundingClientRect(); pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    if (Math.hypot(pointer.x - pointerDown.x, pointer.y - pointerDown.y) > 4) moved = true;
    if (dragNode) { const w = screenToWorld(pointer.x, pointer.y); moveDraggedNode(dragNode, w.x, w.y); exploring = true; return; }
    if (draggingCore) { const w = screenToWorld(pointer.x, pointer.y); setIdentityCorePointer(core, w.x, w.y); exploring = true; return; }
    if (panning && lastPointer) { camera.x += pointer.x - lastPointer.x; camera.y += pointer.y - lastPointer.y; lastPointer = { ...pointer }; targetCamera = null; exploring = true; return; }
    updateHover(event.clientX, event.clientY);
  });

  canvas.addEventListener('pointerdown', event => {
    canvas.setPointerCapture(event.pointerId); moved = false; exploring = true; targetCamera = null;
    const rect = canvas.getBoundingClientRect(); pointer = { x: event.clientX - rect.left, y: event.clientY - rect.top }; pointerDown = { ...pointer };
    updateHover(event.clientX, event.clientY);
    if (pickCore(pointer.x, pointer.y)) { const w = screenToWorld(pointer.x, pointer.y); draggingCore = true; beginIdentityCoreDrag(simulation, core, w.x, w.y); return; }
    if (hovered) { dragNode = hovered; beginNodeDrag(simulation, dragNode); return; }
    if (hoveredAnchor) return;
    panning = true; lastPointer = { ...pointer }; canvas.style.cursor = 'grabbing';
  });

  canvas.addEventListener('pointerup', event => {
    const wasNode = dragNode, wasCore = draggingCore, anchor = hoveredAnchor;
    if (dragNode) { endNodeDrag(simulation, dragNode); dragNode = null; }
    if (draggingCore) { endIdentityCoreDrag(simulation, core); draggingCore = false; }
    panning = false; lastPointer = null; canvas.releasePointerCapture(event.pointerId);
    if (!moved) {
      if (wasCore) resetOverview();
      else if (wasNode) selectNode(wasNode);
      else if (anchor) focusGalaxy(anchor.g);
    }
    updateHover(event.clientX, event.clientY);
  });

  canvas.addEventListener('pointercancel', () => {
    if (dragNode) { endNodeDrag(simulation, dragNode); dragNode = null; }
    if (draggingCore) { endIdentityCoreDrag(simulation, core); draggingCore = false; }
    panning = false; lastPointer = null;
  });

  canvas.addEventListener('wheel', event => {
    event.preventDefault(); exploring = true; targetCamera = null;
    const rect = canvas.getBoundingClientRect(), px = event.clientX - rect.left, py = event.clientY - rect.top;
    const before = screenToWorld(px, py), oldScale = camera.scale;
    camera.scale = nextWheelScale(camera.scale, event.deltaY, galaxyFocus);
    const after = worldToScreen(before.x, before.y); camera.x += px - after.x; camera.y += py - after.y;
    const peel = semanticPeel({ zoomingOut: camera.scale < oldScale, viewScale: camera.scale, selected, galaxyFocused: galaxyFocus });
    if (peel.leaveDetail) hideCard(); if (peel.leaveGalaxy) galaxyFocus = null;
    updateHover(event.clientX, event.clientY);
  }, { passive: false });

  canvas.addEventListener('dblclick', event => {
    const rect = canvas.getBoundingClientRect(), x = event.clientX - rect.left, y = event.clientY - rect.top;
    if (!pickNode(x, y) && !pickCore(x, y)) resetOverview();
  });
  canvas.addEventListener('pointerleave', () => { hovered = null; hoveredAnchor = null; if (!panning && !dragNode && !draggingCore) showTooltip(null); });
  $('detail-close').addEventListener('click', hideCard);
  addEventListener('resize', resize);
  resize(); requestAnimationFrame(frame);
}

loadScene().then(boot).catch(error => {
  const fatal = document.getElementById('fatal');
  fatal.hidden = false;
  fatal.textContent = `Knowledge Constellation failed to start: ${error.message}`;
  console.error(error);
});
