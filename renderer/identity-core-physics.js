// Identity Core physics: a bounded central mass, not a generic draggable UI element.
// Near the equilibrium point the drag is responsive; resistance increases with
// distance and the target approaches maxRadius asymptotically.

export const CORE_PHYSICS = Object.freeze({
  freeRadius: 18,
  maxRadius: 82,
  resistanceScale: 95,
  dragSpring: 0.24,
  homeSpring: 0.032,
  dragDamping: 0.74,
  homeDamping: 0.79,
  maxReturnSpeed: 2.6,
  fieldRadius: 340,
  fieldStrength: 0.0048,
  velocityWake: 0.018,
  reheatDuringDrag: 0.13,
  releaseAlphaFloor: 0.15,
});

export function createIdentityCoreBody(homeX, homeY) {
  return {
    homeX,
    homeY,
    x: homeX,
    y: homeY,
    vx: 0,
    vy: 0,
    targetX: homeX,
    targetY: homeY,
    dragging: false,
  };
}

export function nonlinearCoreTarget(body, pointerX, pointerY) {
  const dx = pointerX - body.homeX;
  const dy = pointerY - body.homeY;
  const distance = Math.hypot(dx, dy);
  if (distance < 1e-6) return { x: body.homeX, y: body.homeY };

  let mapped;
  if (distance <= CORE_PHYSICS.freeRadius) {
    mapped = distance;
  } else {
    mapped = CORE_PHYSICS.freeRadius +
      (CORE_PHYSICS.maxRadius - CORE_PHYSICS.freeRadius) *
      (1 - Math.exp(-(distance - CORE_PHYSICS.freeRadius) / CORE_PHYSICS.resistanceScale));
  }

  mapped = Math.min(mapped, CORE_PHYSICS.maxRadius);
  return {
    x: body.homeX + (dx / distance) * mapped,
    y: body.homeY + (dy / distance) * mapped,
  };
}

export function setIdentityCorePointer(body, pointerX, pointerY) {
  const target = nonlinearCoreTarget(body, pointerX, pointerY);
  body.targetX = target.x;
  body.targetY = target.y;
}

export function beginIdentityCoreDrag(simulation, body, pointerX, pointerY) {
  body.dragging = true;
  setIdentityCorePointer(body, pointerX, pointerY);
  simulation.alphaTarget(CORE_PHYSICS.reheatDuringDrag).restart();
}

export function endIdentityCoreDrag(simulation, body) {
  body.dragging = false;
  body.targetX = body.homeX;
  body.targetY = body.homeY;
  simulation
    .alpha(Math.max(simulation.alpha(), CORE_PHYSICS.releaseAlphaFloor))
    .alphaTarget(0)
    .restart();
}

export function updateIdentityCoreBody(body) {
  const targetX = body.dragging ? body.targetX : body.homeX;
  const targetY = body.dragging ? body.targetY : body.homeY;
  const spring = body.dragging ? CORE_PHYSICS.dragSpring : CORE_PHYSICS.homeSpring;
  const damping = body.dragging ? CORE_PHYSICS.dragDamping : CORE_PHYSICS.homeDamping;

  body.vx = (body.vx + (targetX - body.x) * spring) * damping;
  body.vy = (body.vy + (targetY - body.y) * spring) * damping;

  if (!body.dragging) {
    const speed = Math.hypot(body.vx, body.vy);
    if (speed > CORE_PHYSICS.maxReturnSpeed) {
      body.vx = (body.vx / speed) * CORE_PHYSICS.maxReturnSpeed;
      body.vy = (body.vy / speed) * CORE_PHYSICS.maxReturnSpeed;
    }
  }

  body.x += body.vx;
  body.y += body.vy;

  const dx = body.x - body.homeX;
  const dy = body.y - body.homeY;
  const distance = Math.hypot(dx, dy);
  if (distance > CORE_PHYSICS.maxRadius) {
    const nx = dx / distance;
    const ny = dy / distance;
    body.x = body.homeX + nx * CORE_PHYSICS.maxRadius;
    body.y = body.homeY + ny * CORE_PHYSICS.maxRadius;
    const outward = body.vx * nx + body.vy * ny;
    if (outward > 0) {
      body.vx -= outward * nx;
      body.vy -= outward * ny;
    }
  }

  if (!body.dragging &&
      Math.hypot(body.x - body.homeX, body.y - body.homeY) < 0.04 &&
      Math.hypot(body.vx, body.vy) < 0.025) {
    body.x = body.homeX;
    body.y = body.homeY;
    body.vx = 0;
    body.vy = 0;
  }
}

export function createIdentityCoreInfluenceForce(body) {
  let nodes = [];

  function force(alpha) {
    const displacementX = body.x - body.homeX;
    const displacementY = body.y - body.homeY;
    const displaced = Math.hypot(displacementX, displacementY);
    const moving = Math.hypot(body.vx, body.vy);
    if (displaced < 0.03 && moving < 0.02) return;

    for (const node of nodes) {
      const dx = node.x - body.x;
      const dy = node.y - body.y;
      const distance = Math.max(1, Math.hypot(dx, dy));
      const near = Math.exp(
        -(distance * distance) /
        (2 * CORE_PHYSICS.fieldRadius * CORE_PHYSICS.fieldRadius),
      );

      node.vx += displacementX * CORE_PHYSICS.fieldStrength * near * alpha;
      node.vy += displacementY * CORE_PHYSICS.fieldStrength * near * alpha;
      node.vx += body.vx * CORE_PHYSICS.velocityWake * near * alpha;
      node.vy += body.vy * CORE_PHYSICS.velocityWake * near * alpha;

      const exclusion = 86;
      if (distance < exclusion) {
        const push = ((exclusion - distance) / exclusion) * 0.20 * alpha;
        node.vx += (dx / distance) * push;
        node.vy += (dy / distance) * push;
      }
    }
  }

  force.initialize = nextNodes => { nodes = nextNodes; };
  return force;
}
