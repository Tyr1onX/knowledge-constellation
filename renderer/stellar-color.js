// Physically inspired stellar color for Knowledge Stars.
// IMPORTANT: temperature is a visual-only deterministic parameter. It MUST NOT
// encode capability, seniority, technology category, or any semantic judgment.

function clamp255(value) {
  return Math.max(0, Math.min(255, Math.round(value)));
}

function hashText(text) {
  let h = 2166136261;
  for (let i = 0; i < text.length; i += 1) {
    h ^= text.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return (h >>> 0) / 4294967295;
}

export function kelvinToRgb(kelvin) {
  const temp = Math.max(1000, Math.min(40000, kelvin)) / 100;
  let r;
  let g;
  let b;

  if (temp <= 66) {
    r = 255;
    g = 99.4708025861 * Math.log(temp) - 161.1195681661;
    b = temp <= 19 ? 0 : 138.5177312231 * Math.log(temp - 10) - 305.0447927307;
  } else {
    r = 329.698727446 * Math.pow(temp - 60, -0.1332047592);
    g = 288.1221695283 * Math.pow(temp - 60, -0.0755148492);
    b = 255;
  }

  return [clamp255(r), clamp255(g), clamp255(b)];
}

export function blendRgb(a, b, t) {
  return [
    Math.round(a[0] + (b[0] - a[0]) * t),
    Math.round(a[1] + (b[1] - a[1]) * t),
    Math.round(a[2] + (b[2] - a[2]) * t),
  ];
}

export function stellarTemperatureForId(id) {
  const u = hashText(`${id}|stellar-temperature`);

  // Most stars deliberately stay in the restrained white / warm-white /
  // cool-white band. Only a minority reaches visibly warm or blue-white ends.
  if (u < 0.16) return 3400 + (u / 0.16) * 1500;
  if (u > 0.84) return 7600 + ((u - 0.84) / 0.16) * 3400;
  return 5000 + ((u - 0.16) / 0.68) * 2400;
}

export function stellarPaletteForNode(nodeId) {
  const temperatureK = stellarTemperatureForId(nodeId);
  const raw = kelvinToRgb(temperatureK);
  const halo = blendRgb(raw, [255, 255, 255], 0.34);
  const inner = blendRgb(raw, [255, 255, 255], 0.68);
  const phase = hashText(`${nodeId}|stellar-micro`) * Math.PI * 2;
  const drift = hashText(`${nodeId}|stellar-drift`);

  return Object.freeze({ temperatureK, raw, halo, inner, phase, drift });
}
