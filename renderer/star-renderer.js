import { stellarPaletteForNode } from './stellar-color.js';

// Accepted Knowledge Star visual baseline recovered from renderer-v1 and
// extended by Detail Polish v1. The visual subject is a tiny point source,
// not a circular UI node.

export function secondaryLayerVisibility({ layer, viewScale, galaxyFocused, nodeGalaxy, galaxyDepth }) {
  if (layer !== 'secondary') return 1;
  if (galaxyFocused !== nodeGalaxy) return 0;
  const reveal = Math.max(0, Math.min(1, (viewScale - 1.22) / 0.34));
  return galaxyDepth * reveal;
}

export function drawKnowledgeStar(ctx, node, time, options) {
  const {
    screenPoint,
    galaxyColor = [218, 228, 240],
    viewScale,
    focusBoost = 0,
    galaxyBoost = 0,
    dim = 0,
    layerVisibility = 1,
    emphasis = false,
    useStellarTemperature = true,
  } = options;

  if (layerVisibility < 0.012) return;

  const p = screenPoint;
  const stellar = stellarPaletteForNode(node.id);
  const group = useStellarTemperature ? stellar.halo : galaxyColor;
  const inner = useStellarTemperature ? stellar.inner : [239, 244, 250];

  const slowPeriod = 1650 + stellar.drift * 1150;
  const longPeriod = 4700 + stellar.drift * 1800;
  const pulse =
    1 +
    Math.sin(time / slowPeriod + stellar.phase) * 0.011 +
    Math.sin(time / longPeriod + stellar.phase * 1.71) * 0.005;

  const base = Math.max(0.9, (0.92 + node.size * 1.42) * viewScale);
  const dimFactor = 1 - dim * 0.52;
  const visibleFactor = Math.max(0.42, dimFactor) * layerVisibility;
  const microX = Math.sin(time / (3900 + stellar.drift * 1100) + stellar.phase) * base * 0.055;
  const microY = Math.cos(time / (4700 + stellar.drift * 1300) + stellar.phase * 0.82) * base * 0.035;
  const microRot = Math.sin(time / (7200 + stellar.drift * 1800) + stellar.phase) * 0.045;

  ctx.save();
  ctx.globalAlpha = Math.max(0.03, layerVisibility);

  // Soft, slightly off-center elliptical halo. Avoid spherical / UI-circle appearance.
  const haloShiftX = (node.kind === 'trace' ? 0.06 : 0.18) * base + microX;
  const haloShiftY = (node.kind === 'soft' ? -0.12 : -0.07) * base + microY;
  const haloRX = base * (node.kind === 'trace' ? 3.4 : node.kind === 'core' ? 5.2 : 4.7) * (1 + focusBoost * 0.06);
  const haloRY = base * (node.kind === 'trace' ? 2.8 : node.kind === 'core' ? 4.0 : 3.6) * (1 + focusBoost * 0.04);

  ctx.save();
  ctx.translate(p.x + haloShiftX, p.y + haloShiftY);
  ctx.rotate(
    (node.kind === 'soft' ? 0.65 : node.kind === 'trace' ? 0.2 : 0.38) +
    Math.sin(node.x * 0.013) * 0.04 +
    microRot,
  );
  ctx.scale(1, haloRY / haloRX);

  const outer = ctx.createRadialGradient(0, 0, 0, 0, 0, haloRX);
  const outerAlphaBase = node.kind === 'trace' ? 0.012 : node.kind === 'soft' ? 0.026 : node.kind === 'core' ? 0.055 : 0.038;
  const outerAlpha = (outerAlphaBase + focusBoost * 0.022 + galaxyBoost * 0.010) * visibleFactor;
  outer.addColorStop(0, `rgba(${group[0]},${group[1]},${group[2]},${outerAlpha})`);
  outer.addColorStop(0.26, `rgba(${group[0]},${group[1]},${group[2]},${outerAlpha * 0.40})`);
  outer.addColorStop(0.58, `rgba(${group[0]},${group[1]},${group[2]},${outerAlpha * 0.11})`);
  outer.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = outer;
  ctx.beginPath();
  ctx.arc(0, 0, haloRX, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  // A whisper halo on one side breaks perfect radial symmetry.
  if (node.kind !== 'trace') {
    const sideX = p.x - base * 0.55 + microX * 0.30;
    const sideY = p.y + base * 0.12 + microY * 0.30;
    const side = ctx.createRadialGradient(sideX, sideY, 0, sideX, sideY, base * (2.2 + focusBoost * 0.18));
    const sideAlpha = ((node.kind === 'soft' ? 0.018 : 0.012) + focusBoost * 0.008 + galaxyBoost * 0.004) * visibleFactor;
    side.addColorStop(0, `rgba(${group[0]},${group[1]},${group[2]},${sideAlpha})`);
    side.addColorStop(0.5, `rgba(${group[0]},${group[1]},${group[2]},${sideAlpha * 0.35})`);
    side.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = side;
    ctx.beginPath();
    ctx.arc(sideX, sideY, base * 2.2, 0, Math.PI * 2);
    ctx.fill();
  }

  // A tiny partial corona filament becomes visible only on close inspection.
  if (node.kind !== 'trace') {
    const filamentAngle = stellar.phase + time * (Math.PI * 2 / (21000 + stellar.drift * 9000));
    ctx.strokeStyle = `rgba(${group[0]},${group[1]},${group[2]},${(0.040 + focusBoost * 0.025) * visibleFactor})`;
    ctx.lineWidth = 0.34;
    ctx.beginPath();
    ctx.arc(
      p.x + microX * 0.18,
      p.y + microY * 0.18,
      base * (1.72 + stellar.drift * 0.14),
      filamentAngle,
      filamentAngle + Math.PI * (0.26 + stellar.drift * 0.16),
    );
    ctx.stroke();
  }

  // Much smaller, brighter core: the eye must read a point source first.
  // Temperature tints the inner transition, while the center stays near-white.
  const coreR = (node.kind === 'trace' ? 0.42 : node.kind === 'soft' ? 0.48 : 0.52) * base * (1 + focusBoost * 0.05);
  const core = ctx.createRadialGradient(p.x - coreR * 0.16, p.y - coreR * 0.15, 0, p.x, p.y, coreR * pulse);
  core.addColorStop(0, `rgba(255,255,255,${0.99 * visibleFactor})`);
  core.addColorStop(0.13, `rgba(${inner[0]},${inner[1]},${inner[2]},${(0.94 + focusBoost * 0.03) * visibleFactor})`);
  core.addColorStop(0.52, `rgba(${group[0]},${group[1]},${group[2]},${(0.105 + focusBoost * 0.03 + galaxyBoost * 0.015) * visibleFactor})`);
  core.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = core;
  ctx.beginPath();
  ctx.arc(p.x, p.y, coreR * pulse, 0, Math.PI * 2);
  ctx.fill();

  // Tiny overexposed pinprick at the center.
  ctx.beginPath();
  ctx.arc(p.x, p.y, Math.max(0.65, base * (node.kind === 'trace' ? 0.15 : 0.18) * (1 + focusBoost * 0.10)), 0, Math.PI * 2);
  ctx.fillStyle = `rgba(255,255,255,${(0.84 + focusBoost * 0.12) * visibleFactor})`;
  ctx.fill();

  // Only core stars get a barely visible short diffraction cross.
  if (node.kind === 'core') {
    const crossRot = Math.sin(time / (9500 + stellar.drift * 2400) + stellar.phase) * 0.055;
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.rotate(crossRot);
    ctx.strokeStyle = `rgba(${inner[0]},${inner[1]},${inner[2]},${(0.050 + focusBoost * 0.035) * visibleFactor})`;
    ctx.lineWidth = 0.5;
    const len = base * (1.6 + focusBoost * 0.30);
    ctx.beginPath();
    ctx.moveTo(-len, 0);
    ctx.lineTo(len, 0);
    ctx.moveTo(0, -len * 0.68);
    ctx.lineTo(0, len * 0.68);
    ctx.stroke();
    ctx.restore();
  }

  // Soft / veiled stars use an incomplete whisper arc, never a full ring.
  // The material arc precesses slowly instead of remaining frozen.
  if (node.kind === 'soft') {
    const arcOffset = time * (Math.PI * 2 / (18000 + stellar.drift * 9000));
    ctx.save();
    ctx.globalAlpha = (0.10 + galaxyBoost * 0.05 + focusBoost * 0.04) * visibleFactor;
    ctx.strokeStyle = `rgba(${group[0]},${group[1]},${group[2]},.20)`;
    ctx.lineWidth = 0.45;
    ctx.beginPath();
    ctx.arc(
      p.x + base * 0.08,
      p.y - base * 0.04,
      base * (1.6 + focusBoost * 0.08),
      Math.PI * 0.28 + arcOffset,
      Math.PI * 1.60 + arcOffset,
    );
    ctx.stroke();
    ctx.restore();
  }

  if (emphasis || focusBoost > 0.42) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, Math.max(10, base * (4.0 + focusBoost * 0.25)), 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(227,236,247,${0.07 + focusBoost * 0.11})`;
    ctx.lineWidth = 0.62;
    ctx.stroke();
  }

  ctx.restore();
}
