// Accepted Semantic Zoom rules recovered from the renderer-v1 interaction baseline.

export const SEMANTIC_ZOOM = Object.freeze({
  overviewMinScale: 0.72,
  overviewMaxScale: 1.78,
  galaxyMaxScale: 2.35,
  enterGalaxyScale: 1.62,
  secondaryRevealStart: 1.22,
  secondaryRevealRange: 0.34,
  detailExitScale: 1.43,
  galaxyExitScale: 1.12,
});

export function secondaryReveal(viewScale, galaxyDepth) {
  return Math.max(0, Math.min(1, (viewScale - SEMANTIC_ZOOM.secondaryRevealStart) / SEMANTIC_ZOOM.secondaryRevealRange)) * galaxyDepth;
}

export function nextWheelScale(currentScale, deltaY, galaxyFocused) {
  const maxScale = galaxyFocused ? SEMANTIC_ZOOM.galaxyMaxScale : SEMANTIC_ZOOM.overviewMaxScale;
  const factor = deltaY < 0 ? 1.075 : 0.935;
  return Math.max(SEMANTIC_ZOOM.overviewMinScale, Math.min(maxScale, currentScale * factor));
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
// - entering another Galaxy is a large-scale navigation action and MAY animate the camera.
export const CAMERA_INVARIANTS = Object.freeze({
  inspectNodeRecenters: false,
  zoomOutRecenters: false,
  identityCoreOwnsReset: true,
  galaxyNavigationMayAnimate: true,
});
