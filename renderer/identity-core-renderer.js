// Accepted Identity Core renderer families.
// One family = one primary visual subject. Motion is astronomical morphology,
// not a personality, capability, demographic, or seniority metaphor.

export const IDENTITY_CORE_FAMILIES = Object.freeze([
  'monogram',
  'eclipse',
  'quiet_star',
  'minimal_ring',
  'black_hole',
  'pulsar',
  'binary_star',
  'protostar_nebula',
]);

function hash01(value) {
  let h = 2166136261;
  for (let i = 0; i < value.length; i += 1) {
    h ^= value.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) / 4294967295;
}

function haloDisc(ctx, p, radius, alpha = 0.04) {
  const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius);
  g.addColorStop(0, `rgba(220,234,249,${alpha})`);
  g.addColorStop(0.25, `rgba(138,172,212,${alpha * 0.34})`);
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
  ctx.fill();
}

function drawMonogram(ctx, t, p, radius, options) {
  const monogram = options.monogram || 'TY';
  const viewScale = options.viewScale || 1;
  const breathe = 1 + Math.sin(t / 1450) * 0.028 + Math.sin(t / 4600) * 0.010;
  haloDisc(ctx, p, radius * 3.8, 0.033);

  const glow = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 1.85 * breathe);
  glow.addColorStop(0, 'rgba(255,255,255,.145)');
  glow.addColorStop(0.15, 'rgba(211,225,242,.074)');
  glow.addColorStop(0.55, 'rgba(116,146,185,.025)');
  glow.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = glow;
  ctx.beginPath();
  ctx.arc(p.x, p.y, radius * 1.85 * breathe, 0, Math.PI * 2);
  ctx.fill();

  const orbitA = t * (Math.PI * 2 / 11200);
  const orbitB = -t * (Math.PI * 2 / 18600);

  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(orbitA);
  ctx.strokeStyle = 'rgba(233,240,248,.082)';
  ctx.lineWidth = 0.82;
  ctx.beginPath();
  ctx.arc(0, 0, radius * 0.99, Math.PI * 0.10, Math.PI * 1.86);
  ctx.stroke();
  ctx.restore();

  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(orbitB);
  ctx.scale(1, 0.72);
  ctx.strokeStyle = 'rgba(164,190,222,.040)';
  ctx.lineWidth = 0.48 / 0.72;
  ctx.beginPath();
  ctx.arc(0, 0, radius * 1.22, Math.PI * 0.42, Math.PI * 1.52);
  ctx.stroke();
  ctx.restore();

  const disc = ctx.createRadialGradient(
    p.x - radius * 0.18,
    p.y - radius * 0.18,
    0,
    p.x,
    p.y,
    radius * 0.90,
  );
  disc.addColorStop(0, 'rgba(19,27,40,.96)');
  disc.addColorStop(0.50, 'rgba(12,18,29,.95)');
  disc.addColorStop(0.80, 'rgba(8,12,20,.97)');
  disc.addColorStop(1, 'rgba(4,7,13,.995)');
  ctx.fillStyle = disc;
  ctx.beginPath();
  ctx.arc(p.x, p.y, radius * 0.89, 0, Math.PI * 2);
  ctx.fill();

  // Detail Polish: internal material moves while the identity mark stays stable.
  ctx.save();
  ctx.beginPath();
  ctx.arc(p.x, p.y, radius * 0.84, 0, Math.PI * 2);
  ctx.clip();
  const materialRot = t * (Math.PI * 2 / 24000);
  for (let i = 0; i < 8; i += 1) {
    const seed = hash01(`monogram-material-${i}`);
    const a = materialRot * (0.42 + seed * 0.35) + seed * Math.PI * 2;
    const rr = radius * (0.25 + seed * 0.47);
    const cx = p.x + Math.cos(a) * rr * 0.30;
    const cy = p.y + Math.sin(a) * rr * 0.20;
    const arcR = radius * (0.24 + seed * 0.34);
    ctx.strokeStyle = `rgba(159,188,220,${0.010 + seed * 0.015})`;
    ctx.lineWidth = 0.42;
    ctx.beginPath();
    ctx.arc(cx, cy, arcR, a + Math.PI * 0.12, a + Math.PI * (0.52 + seed * 0.42));
    ctx.stroke();
  }
  const sheenX = p.x + Math.cos(t / 3100) * radius * 0.28;
  const sheenY = p.y + Math.sin(t / 3700) * radius * 0.18;
  const sheen = ctx.createRadialGradient(sheenX, sheenY, 0, sheenX, sheenY, radius * 0.72);
  sheen.addColorStop(0, 'rgba(193,216,240,.030)');
  sheen.addColorStop(0.45, 'rgba(104,139,181,.010)');
  sheen.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = sheen;
  ctx.fillRect(p.x - radius, p.y - radius, radius * 2, radius * 2);
  ctx.restore();

  const glint = t * (Math.PI * 2 / 13800) - Math.PI * 0.30;
  ctx.strokeStyle = `rgba(240,247,253,${0.13 + 0.035 * Math.sin(t / 1800)})`;
  ctx.lineWidth = 0.72;
  ctx.beginPath();
  ctx.arc(p.x, p.y, radius * 0.895, glint - 0.18, glint + 0.20);
  ctx.stroke();

  for (let i = 0; i < 4; i += 1) {
    const seed = hash01(`monogram-particle-${i}`);
    const a = t * (Math.PI * 2 / (15000 + seed * 9000)) + seed * Math.PI * 2;
    const rr = radius * (1.03 + seed * 0.34);
    const x = p.x + Math.cos(a) * rr;
    const y = p.y + Math.sin(a) * rr * (0.72 + 0.12 * seed);
    ctx.fillStyle = `rgba(215,231,247,${0.09 + 0.05 * seed})`;
    ctx.beginPath();
    ctx.arc(x, y, 0.55 + 0.32 * seed, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.save();
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.font = `600 ${Math.max(12, 16 * viewScale)}px Inter,"PingFang SC",sans-serif`;
  ctx.fillStyle = 'rgba(239,245,251,.95)';
  ctx.shadowBlur = radius * 0.16;
  ctx.shadowColor = 'rgba(192,215,239,.10)';
  ctx.fillText(monogram, p.x, p.y - 1);
  ctx.restore();
}

function drawEclipse(ctx, t, p, radius) {
  const R = radius * 0.76;
  const phase = t * (Math.PI * 2 / 9000);
  haloDisc(ctx, p, radius * 2.4, 0.023);
  ctx.fillStyle = 'rgba(1,3,8,.999)';
  ctx.beginPath();
  ctx.arc(p.x, p.y, R, 0, Math.PI * 2);
  ctx.fill();

  for (let i = 0; i < 30; i += 1) {
    const a = (i / 30) * Math.PI * 2;
    const d = Math.atan2(Math.sin(a - phase), Math.cos(a - phase));
    const strength = Math.exp(-(d * d) / 0.22);
    if (strength < 0.04) continue;
    ctx.strokeStyle = `rgba(247,251,255,${0.04 + 0.27 * strength})`;
    ctx.lineWidth = 0.70;
    ctx.beginPath();
    ctx.arc(p.x, p.y, R * 1.018, a - 0.055, a + 0.055);
    ctx.stroke();
  }
}

function drawQuietStar(ctx, t, p, radius) {
  const pulse = 1 + Math.sin(t / 780) * 0.065 + Math.sin(t / 2600) * 0.018;
  const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 2.8 * pulse);
  g.addColorStop(0, 'rgba(255,255,255,.48)');
  g.addColorStop(0.025, 'rgba(243,249,255,.27)');
  g.addColorStop(0.15, 'rgba(130,171,218,.052)');
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(p.x, p.y, radius * 2.8 * pulse, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(t * (Math.PI * 2 / 16000));
  ctx.strokeStyle = `rgba(241,247,254,${0.055 + 0.025 * Math.sin(t / 950)})`;
  ctx.lineWidth = 0.48;
  ctx.beginPath();
  ctx.moveTo(-radius * 0.90, 0);
  ctx.lineTo(radius * 0.90, 0);
  ctx.moveTo(0, -radius * 0.52);
  ctx.lineTo(0, radius * 0.52);
  ctx.stroke();
  ctx.restore();

  ctx.fillStyle = 'rgba(255,255,255,.99)';
  ctx.beginPath();
  ctx.arc(p.x, p.y, Math.max(1.6, 2.35 * (optionsViewScale(ctx) || 1) * pulse), 0, Math.PI * 2);
  ctx.fill();
}

function optionsViewScale() {
  return 1;
}

function drawMinimalRing(ctx, t, p, radius) {
  const R = radius * 1.10;
  const flatten = 0.60;
  const theta = t * (Math.PI * 2 / 7200);
  const tilt = -0.30 + Math.sin(t / 6500) * 0.13;

  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(tilt);
  ctx.scale(1, flatten);
  ctx.strokeStyle = 'rgba(198,217,239,.120)';
  ctx.lineWidth = 0.72 / flatten;
  ctx.beginPath();
  ctx.arc(0, 0, R, 0, Math.PI * 2);
  ctx.stroke();
  for (let i = 0; i < 8; i += 1) {
    const offset = i * 0.13;
    const alpha = 0.20 * (1 - i / 8);
    ctx.strokeStyle = `rgba(235,243,251,${alpha})`;
    ctx.lineWidth = (1.05 - i * 0.055) / flatten;
    ctx.beginPath();
    ctx.arc(0, 0, R, theta - 0.26 - offset, theta + 0.13 - offset);
    ctx.stroke();
  }
  ctx.restore();

  const ox = Math.cos(theta) * R;
  const oy = Math.sin(theta) * R * flatten;
  const ax = p.x + ox * Math.cos(tilt) - oy * Math.sin(tilt);
  const ay = p.y + ox * Math.sin(tilt) + oy * Math.cos(tilt);
  const ag = ctx.createRadialGradient(ax, ay, 0, ax, ay, 7);
  ag.addColorStop(0, 'rgba(255,255,255,.90)');
  ag.addColorStop(0.18, 'rgba(211,229,248,.28)');
  ag.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = ag;
  ctx.beginPath();
  ctx.arc(ax, ay, 7, 0, Math.PI * 2);
  ctx.fill();
}

function drawBlackHole(ctx, t, p, radius) {
  const R = radius * 0.88;
  const tilt = -0.10;
  const diskRx = R * 2.08;
  const diskRy = R * 0.43;
  const phase = t * (Math.PI * 2 / 7800);
  haloDisc(ctx, p, radius * 2.7, 0.016);

  for (let k = 0; k < 7; k += 1) {
    const rr = diskRx * (0.72 + k * 0.055);
    ctx.save();
    ctx.translate(p.x, p.y - R * (0.06 + k * 0.005));
    ctx.rotate(tilt);
    ctx.scale(1, (diskRy * (0.79 + k * 0.027)) / rr);
    ctx.strokeStyle = `rgba(193,215,241,${0.028 + k * 0.010})`;
    ctx.lineWidth = 0.58 * (rr / (diskRy * (0.79 + k * 0.027)));
    ctx.beginPath();
    ctx.arc(0, 0, rr, Math.PI, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }

  for (let i = 0; i < 38; i += 1) {
    const a = phase + (i / 38) * Math.PI * 2;
    const rr = R * (1.08 + hash01(`bh-${i}`) * 0.92);
    const x0 = Math.cos(a) * rr;
    const y0 = Math.sin(a) * rr * 0.25;
    const x = p.x + x0 * Math.cos(tilt) - y0 * Math.sin(tilt);
    const y = p.y + x0 * Math.sin(tilt) + y0 * Math.cos(tilt);
    const approach = Math.cos(a) < 0;
    const front = Math.sin(a) > 0;
    const alpha = (front ? 0.10 : 0.035) * (approach ? 1.7 : 0.72);
    ctx.fillStyle = `rgba(${approach ? 232 : 181},${approach ? 240 : 208},${approach ? 249 : 232},${alpha})`;
    ctx.beginPath();
    ctx.ellipse(x, y, 1.45, 0.52, tilt, 0, Math.PI * 2);
    ctx.fill();
  }

  ctx.strokeStyle = 'rgba(239,246,253,.16)';
  ctx.lineWidth = 0.62;
  ctx.beginPath();
  ctx.arc(p.x, p.y, R * 0.73, 0, Math.PI * 2);
  ctx.stroke();
  ctx.fillStyle = 'rgba(1,3,7,1)';
  ctx.beginPath();
  ctx.arc(p.x, p.y, R * 0.67, 0, Math.PI * 2);
  ctx.fill();

  for (let k = 0; k < 4; k += 1) {
    const rr = diskRx * (0.82 + k * 0.06);
    const ry = diskRy * (0.84 + k * 0.025);
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.rotate(tilt);
    ctx.scale(1, ry / rr);
    ctx.strokeStyle = `rgba(215,230,246,${0.048 + k * 0.015})`;
    ctx.lineWidth = 0.66 * (rr / ry);
    ctx.beginPath();
    ctx.arc(0, 0, rr, 0, Math.PI);
    ctx.stroke();
    ctx.restore();
  }
}

function drawBeam(ctx, p, R, axis, dir, length, width, alpha, inner = false) {
  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(axis);
  ctx.scale(dir, 1);
  const g = ctx.createLinearGradient(R * 0.08, 0, length, 0);
  g.addColorStop(0, `rgba(232,244,255,${alpha})`);
  g.addColorStop(0.18, `rgba(174,211,242,${alpha * 0.78})`);
  g.addColorStop(0.55, `rgba(116,171,219,${alpha * 0.34})`);
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.moveTo(R * 0.08, -R * (inner ? 0.045 : 0.10));
  ctx.quadraticCurveTo(length * 0.43, -width * 0.72, length, -width);
  ctx.lineTo(length, width);
  ctx.quadraticCurveTo(length * 0.43, width * 0.72, R * 0.08, R * (inner ? 0.045 : 0.10));
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

function drawPulsePacket(ctx, p, axis, dir, distance, width, intensity) {
  const x = p.x + Math.cos(axis) * distance * dir;
  const y = p.y + Math.sin(axis) * distance * dir;
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(axis);
  const rx = width * 1.65;
  const ry = width * 0.52;
  const g = ctx.createRadialGradient(0, 0, 0, 0, 0, rx);
  g.addColorStop(0, `rgba(246,251,255,${0.40 * intensity})`);
  g.addColorStop(0.18, `rgba(205,229,249,${0.24 * intensity})`);
  g.addColorStop(0.55, `rgba(126,181,226,${0.075 * intensity})`);
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.scale(1, ry / rx);
  ctx.beginPath();
  ctx.arc(0, 0, rx, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function drawPulsar(ctx, t, p, radius) {
  const R = radius * 0.72;
  const axis = t * (Math.PI * 2 / 8600) - 0.58;
  const pulsePeriod = 1120;
  const pulsePhase = (t % pulsePeriod) / pulsePeriod;
  const pulseEnvelope = Math.pow(Math.sin(Math.PI * pulsePhase), 1.7);
  const beamLen = R * 4.7;

  for (const dir of [1, -1]) {
    drawBeam(ctx, p, R, axis, dir, beamLen, R * 0.76, 0.060 + 0.045 * pulseEnvelope, false);
    drawBeam(ctx, p, R, axis, dir, beamLen * 0.92, R * 0.25, 0.14 + 0.11 * pulseEnvelope, true);
  }

  for (let k = 0; k < 3; k += 1) {
    const q = (pulsePhase + k / 3) % 1;
    const travel = 1 - Math.pow(1 - q, 1.35);
    const distance = R * 0.40 + travel * (beamLen * 0.88);
    const intensity = Math.sin(Math.PI * q) * (0.72 + 0.28 * pulseEnvelope);
    for (const dir of [1, -1]) {
      drawPulsePacket(ctx, p, axis, dir, distance, R * (0.12 + 0.10 * q), intensity);
    }
  }

  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(axis * 0.78);
  ctx.scale(1, 0.52);
  ctx.strokeStyle = `rgba(169,203,236,${0.085 + 0.025 * pulseEnvelope})`;
  ctx.lineWidth = 0.56 / 0.52;
  ctx.beginPath();
  ctx.arc(0, 0, R * 0.78, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();

  haloDisc(ctx, p, R * (1.95 + 0.22 * pulseEnvelope), 0.045 + 0.090 * pulseEnvelope);
  const sr = R * 0.19;
  const sphere = ctx.createRadialGradient(p.x - sr * 0.35, p.y - sr * 0.35, 0, p.x, p.y, sr);
  sphere.addColorStop(0, 'rgba(252,253,255,.99)');
  sphere.addColorStop(0.34, `rgba(206,230,249,${0.94 + 0.04 * pulseEnvelope})`);
  sphere.addColorStop(1, 'rgba(76,112,157,.62)');
  ctx.fillStyle = sphere;
  ctx.beginPath();
  ctx.arc(p.x, p.y, sr * (1 + 0.035 * pulseEnvelope), 0, Math.PI * 2);
  ctx.fill();
}

function drawBinary(ctx, t, p, radius) {
  const R = radius * 0.94;
  const theta = t * (Math.PI * 2 / 7600);
  const rot = -0.28;
  const flatten = 0.62;
  const a1 = R * 0.74;
  const a2 = R * 1.15;

  function orbit(rad, alpha) {
    ctx.save();
    ctx.translate(p.x, p.y);
    ctx.rotate(rot);
    ctx.scale(1, flatten);
    ctx.strokeStyle = `rgba(155,182,214,${alpha})`;
    ctx.lineWidth = 0.48 / flatten;
    ctx.beginPath();
    ctx.arc(0, 0, rad, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  }

  function position(rad, angle) {
    const x = Math.cos(angle) * rad;
    const y = Math.sin(angle) * rad * flatten;
    return {
      x: p.x + x * Math.cos(rot) - y * Math.sin(rot),
      y: p.y + x * Math.sin(rot) + y * Math.cos(rot),
    };
  }

  function star(q, r, a, color) {
    const g = ctx.createRadialGradient(q.x, q.y, 0, q.x, q.y, r * 5.7);
    g.addColorStop(0, `rgba(${color[0]},${color[1]},${color[2]},${a * 0.36})`);
    g.addColorStop(0.15, `rgba(${color[0]},${color[1]},${color[2]},${a * 0.12})`);
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(q.x, q.y, r * 5.7, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = `rgba(${color[0]},${color[1]},${color[2]},${a})`;
    ctx.beginPath();
    ctx.arc(q.x, q.y, r, 0, Math.PI * 2);
    ctx.fill();
  }

  orbit(a1, 0.060);
  orbit(a2, 0.038);
  star(position(a1, theta), 2.75, 0.96, [246, 236, 224]);
  star(position(a2, theta + Math.PI), 2.1, 0.84, [210, 231, 251]);
}

function drawProtostar(ctx, t, p, radius) {
  const R = radius * 0.96;
  const phase = t * (Math.PI * 2 / 14500);
  ctx.save();
  ctx.globalCompositeOperation = 'screen';
  for (let i = 0; i < 42; i += 1) {
    const seed = hash01(`proto-${i}`);
    const a = seed * Math.PI * 2 + phase * (0.18 + hash01(`proto-speed-${i}`) * 0.30);
    const rad = R * (0.42 + hash01(`proto-r-${i}`) * 1.72);
    const x = p.x + Math.cos(a) * rad * 0.74;
    const y = p.y + Math.sin(a) * rad * 0.44;
    const rr = R * (0.12 + hash01(`proto-size-${i}`) * 0.31);
    const g = ctx.createRadialGradient(x, y, 0, x, y, rr);
    const alpha = 0.010 + hash01(`proto-a-${i}`) * 0.022;
    g.addColorStop(0, `rgba(149,176,206,${alpha})`);
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(x, y, rr, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();

  const hot = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, R * 0.68);
  hot.addColorStop(0, 'rgba(253,253,250,.31)');
  hot.addColorStop(0.14, 'rgba(223,237,249,.13)');
  hot.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = hot;
  ctx.beginPath();
  ctx.arc(p.x, p.y, R * 0.68, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.translate(p.x, p.y);
  ctx.rotate(-0.06);
  ctx.scale(1, 0.20);
  ctx.strokeStyle = 'rgba(204,224,243,.13)';
  ctx.lineWidth = 2.8;
  ctx.beginPath();
  ctx.arc(0, 0, R * 1.28, phase, phase + Math.PI * 1.35);
  ctx.stroke();
  ctx.restore();
}

export function drawIdentityCore(ctx, family, time, options) {
  const { x, y, radius } = options;
  const p = { x, y };

  switch (family) {
    case 'eclipse': return drawEclipse(ctx, time, p, radius, options);
    case 'quiet_star': return drawQuietStar(ctx, time, p, radius, options);
    case 'minimal_ring': return drawMinimalRing(ctx, time, p, radius, options);
    case 'black_hole': return drawBlackHole(ctx, time, p, radius, options);
    case 'pulsar': return drawPulsar(ctx, time, p, radius, options);
    case 'binary_star': return drawBinary(ctx, time, p, radius, options);
    case 'protostar_nebula': return drawProtostar(ctx, time, p, radius, options);
    case 'monogram':
    default: return drawMonogram(ctx, time, p, radius, options);
  }
}
