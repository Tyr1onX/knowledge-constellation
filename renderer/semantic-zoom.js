// Semantic Zoom baseline for a growing Knowledge Constellation.
// Focus is a boost, not a gate: deeper stars may reveal naturally through spatial zoom.

export const SEMANTIC_ZOOM = Object.freeze({
  overviewMinScale: 0.72,
  overviewMaxScale: 2.10,
  galaxyMaxScale: 2.45,
  enterGalaxyScale: 1.62,
  secondaryRevealStart: 1.04,
  secondaryRevealRange: 0.54,
  traceRevealStart: 1.28,
  traceRevealRange: 0.58,
  focusedRevealStart: 1.08,
  focusedRevealRange: 0.34,
  detailExitScale: 1.43,
  galaxyExitScale: 1.12,
});

function clamp01(value) {
  return Math.max(0, Math.min(1, value));
}

function smooth01(value) {
  const x = clamp01(value);
  return x * x * (3 - 2 * x);
}

export function secondaryReveal(viewScale, galaxyDepth = 1) {
  return (
    smooth01(
      (viewScale - SEMANTIC_ZOOM.secondaryRevealStart) /
        SEMANTIC_ZOOM.secondaryRevealRange,
    ) * galaxyDepth
  );
}

export function nodeSemanticVisibility({
  layer,
  kind,
  viewScale,
  overviewPresence = 0,
  galaxyFocused = null,
  nodeGalaxy = null,
  galaxyDepth = 1,
}) {
  if (layer !== 'secondary') return 1;

  const trace = kind === 'trace';
  const start = trace
    ? SEMANTIC_ZOOM.traceRevealStart
    : SEMANTIC_ZOOM.secondaryRevealStart;
  const range = trace
    ? SEMANTIC_ZOOM.traceRevealRange
    : SEMANTIC_ZOOM.secondaryRevealRange;

  const globalReveal = smooth01((viewScale - start) / range) * (trace ? 0.82 : 1);
  const focusedReveal =
    galaxyFocused && galaxyFocused === nodeGalaxy
      ? smooth01(
          (viewScale - SEMANTIC_ZOOM.focusedRevealStart) /
            SEMANTIC_ZOOM.focusedRevealRange,
        ) * galaxyDepth
      : 0;

  return Math.max(overviewPresence, globalReveal, focusedReveal);
}

export function nextWheelScale(currentScale, deltaY, galaxyFocused) {
  const maxScale = galaxyFocused
    ? SEMANTIC_ZOOM.galaxyMaxScale
    : SEMANTIC_ZOOM.overviewMaxScale;
  const factor = deltaY < 0 ? 1.075 : 0.935;
  return Math.max(
    SEMANTIC_ZOOM.overviewMinScale,
    Math.min(maxScale, currentScale * factor),
  );
}

// Spatial zoom invariant: callers must keep the world point under the cursor fixed.
// This helper returns the camera correction after the caller has applied nextScale.
export function pointerZoomCorrection({ pointerX, pointerY, worldBefore, worldToScreenAfter }) {
  const projected = worldToScreenAfter(worldBefore.x, worldBefore.y);
  return {
    dx: pointerX - projected.x,
    dy: pointerY - projected.y,
  };
}

export function semanticPeel({ zoomingOut, viewScale, selected, galaxyFocused }) {
  if (!zoomingOut) return { leaveDetail: false, leaveGalaxy: false };
  return {
    leaveDetail: Boolean(selected && viewScale < SEMANTIC_ZOOM.detailExitScale),
    leaveGalaxy: Boolean(galaxyFocused && viewScale < SEMANTIC_ZOOM.galaxyExitScale),
  };
}

// Interaction invariants:
// - inspecting a node inside the current Galaxy MUST NOT recenter the camera;
// - zoom-out MUST NOT reset the camera transform;
// - Identity Core owns explicit return-to-overview / recentering;
// - entering another Galaxy is a large-scale navigation action and MAY animate the camera;
// - clicking a Galaxy may strengthen local detail, but is NOT required to reveal secondary stars.
export const CAMERA_INVARIANTS = Object.freeze({
  inspectNodeRecenters: false,
  zoomOutRecenters: false,
  identityCoreOwnsReset: true,
  galaxyNavigationMayAnimate: true,
  galaxyFocusRequiredForSecondaryReveal: false,
});
