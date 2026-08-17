// Accepted Pure Black + Ambient Space background implementation vocabulary.
// Background is atmosphere only: no knowledge, personality, or capability meaning.

export const BACKGROUND_FAMILIES = Object.freeze([
  'almost_empty',
  'cold_filament',
  'broken_cloud',
]);

function hash01(value) {
  let h = 2166136261;
  for (let i = 0; i < value.length; i += 1) {
    h ^= value.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) / 4294967295;
}

export function createBackgroundField(seed = 'knowledge-constellation') {
  const distantStars = Array.from({ length: 180 }, (_, i) => ({
    x: hash01(`${seed}|far-x|${i}`),
    y: hash01(`${seed}|far-y|${i}`),
    r: 0.22 + hash01(`${seed}|far-r|${i}`) * 0.63,
    alpha: 0.018 + hash01(`${seed}|far-a|${i}`) * 0.055,
  }));

  const brokenClouds = Array.from({ length: 24 }, (_, i) => ({
    x: 0.18 + hash01(`${seed}|cloud-x|${i}`) * 0.68,
    y: 0.14 + hash01(`${seed}|cloud-y|${i}`) * 0.68,
    rx: 0.045 + hash01(`${seed}|cloud-rx|${i}`) * 0.085,
    ry: 0.018 + hash01(`${seed}|cloud-ry|${i}`) * 0.038,
    rot: (hash01(`${seed}|cloud-rot|${i}`) - 0.5) * 1.1,
    alpha: 0.010 + hash01(`${seed}|cloud-a|${i}`) * 0.015,
    phase: hash01(`${seed}|cloud-phase|${i}`) * Math.PI * 2,
  }));

  return Object.freeze({ seed, distantStars, brokenClouds });
}

function drawDistantStars(ctx, field, width, height, time, alpha = 1) {
  ctx.save();
  ctx.globalAlpha = alpha;
  for (const s of field.distantStars) {
    const twinkle = 1 + Math.sin(time / 5200 + s.x * 17.3) * 0.08;
    ctx.fillStyle = `rgba(205,220,239,${s.alpha * twinkle})`;
    ctx.beginPath();
    ctx.arc(s.x * width, s.y * height, s.r, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();
}

function drawColdFilament(ctx, width, height, time, alpha = 1) {
  ctx.save();
  ctx.globalCompositeOperation = 'screen';
  ctx.globalAlpha = alpha;
  ctx.filter = 'blur(22px)';

  for (let k = 0; k < 5; k += 1) {
    const y0 = height * (0.20 + k * 0.085);
    const amp = height * (0.042 + k * 0.005);
    const drift = Math.sin(time / (22000 + k * 1700) + k * 0.8) * 2.2;
    ctx.beginPath();
    for (let s = 0; s <= 42; s += 1) {
      const q = s / 42;
      const x = -width * 0.05 + q * width * 1.10;
      const y = y0 +
        Math.sin(q * Math.PI * 1.28 + k * 0.69) * amp +
        Math.sin(q * Math.PI * 4 + k * 0.4) * amp * 0.15 +
        drift;
      if (s === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = `rgba(180,197,218,${0.014 + k * 0.0017})`;
    ctx.lineWidth = 24 + k * 8;
    ctx.stroke();
  }

  ctx.restore();
}

function drawBrokenCloud(ctx, field, width, height, time, alpha = 1) {
  ctx.save();
  ctx.globalCompositeOperation = 'screen';
  ctx.globalAlpha = alpha;
  ctx.filter = 'blur(20px)';

  field.brokenClouds.forEach((c, i) => {
    const dx = Math.sin(time / (18000 + i * 420) + c.phase) * 2.8;
    const dy = Math.cos(time / (24000 + i * 510) + c.phase) * 1.8;
    const x = c.x * width + dx;
    const y = c.y * height + dy;
    const rx = c.rx * Math.min(width, height);
    const ry = c.ry * Math.min(width, height);

    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(c.rot);
    ctx.scale(1, ry / rx);
    const g = ctx.createRadialGradient(0, 0, 0, 0, 0, rx);
    g.addColorStop(0, `rgba(164,183,207,${c.alpha})`);
    g.addColorStop(0.55, `rgba(111,140,176,${c.alpha * 0.45})`);
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, 0, rx, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  });

  ctx.restore();
}

export function drawBackgroundField(ctx, field, time, options) {
  const {
    width,
    height,
    family = 'almost_empty',
    alpha = 1,
  } = options;

  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.fillStyle = '#01030a';
  ctx.fillRect(0, 0, width, height);
  ctx.restore();

  if (family === 'cold_filament') drawColdFilament(ctx, width, height, time, alpha);
  if (family === 'broken_cloud') drawBrokenCloud(ctx, field, width, height, time, alpha);
  drawDistantStars(ctx, field, width, height, time, alpha);
}

export function createAmbientMeteor(now, demo = false) {
  if (demo) {
    return {
      born: now,
      life: 1750,
      demo: true,
      x0: 0.12,
      y0: 0.18,
      x1: 0.82,
      y1: 0.43,
    };
  }

  const left = Math.random() > 0.5;
  return {
    born: now,
    life: 950 + Math.random() * 450,
    demo: false,
    x0: left ? 0.08 : 0.88,
    y0: 0.12 + Math.random() * 0.22,
    x1: left ? 0.55 : 0.42,
    y1: 0.27 + Math.random() * 0.25,
  };
}

export function drawAmbientMeteor(ctx, meteor, time, width, height) {
  if (!meteor) return false;
  const age = time - meteor.born;
  if (age > meteor.life) return false;

  const q = age / meteor.life;
  const fade = Math.sin(Math.PI * q);
  const x = width * (meteor.x0 + (meteor.x1 - meteor.x0) * q);
  const y = height * (meteor.y0 + (meteor.y1 - meteor.y0) * q);
  const dx = width * (meteor.x1 - meteor.x0);
  const dy = height * (meteor.y1 - meteor.y0);
  const length = (meteor.demo ? 0.18 : 0.10) * width;
  const mag = Math.hypot(dx, dy);
  const ux = dx / mag;
  const uy = dy / mag;
  const ex = x - ux * length;
  const ey = y - uy * length;

  const g = ctx.createLinearGradient(ex, ey, x, y);
  g.addColorStop(0, 'rgba(202,221,242,0)');
  g.addColorStop(0.62, `rgba(219,235,250,${(meteor.demo ? 0.18 : 0.065) * fade})`);
  g.addColorStop(1, `rgba(252,253,255,${(meteor.demo ? 0.78 : 0.28) * fade})`);
  ctx.strokeStyle = g;
  ctx.lineWidth = meteor.demo ? 1.35 : 0.75;
  ctx.beginPath();
  ctx.moveTo(ex, ey);
  ctx.lineTo(x, y);
  ctx.stroke();
  return true;
}
