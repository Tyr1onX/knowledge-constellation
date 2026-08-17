// Accepted d3-force baseline recovered from the renderer-v1 visual prototype.
// Do not replace this with a page-local physics approximation.

export const PHYSICS_BASELINE = Object.freeze({
  alpha: 0.72,
  alphaMin: 0.001,
  alphaDecay: 0.024,
  velocityDecay: 0.24,
  dragAlphaTarget: 0.20,
  releaseAlphaFloor: 0.16,
});

export function createKnowledgeSimulation(d3, nodes, links, galaxyById) {
  if (!d3?.forceSimulation) {
    throw new Error('d3-force is required by the Knowledge Constellation renderer.');
  }

  const G = galaxyById;

  return d3.forceSimulation(nodes)
    .alpha(PHYSICS_BASELINE.alpha)
    .alphaMin(PHYSICS_BASELINE.alphaMin)
    .alphaDecay(PHYSICS_BASELINE.alphaDecay)
    .velocityDecay(PHYSICS_BASELINE.velocityDecay)
    .force(
      'link',
      d3.forceLink(links)
        .id(d => d.id)
        .distance(d => d.distance)
        .strength(d => d.strength)
        .iterations(2),
    )
    .force(
      'charge',
      d3.forceManyBody()
        .strength(d => {
          if (d.layer === 'secondary') return d.kind === 'trace' ? -26 : -42;
          if (d.kind === 'trace') return -45;
          if (d.kind === 'core') return -128;
          return -88;
        })
        .distanceMin(24)
        .distanceMax(340),
    )
    .force(
      'collide',
      d3.forceCollide()
        .radius(d => d.layer === 'secondary' ? 7 + d.size * 9 : 12 + d.size * 13)
        .strength(0.82)
        .iterations(2),
    )
    .force(
      'x',
      d3.forceX(d => G[d.g].x)
        .strength(d => d.layer === 'secondary' ? 0.018 : d.kind === 'core' ? 0.052 : 0.030),
    )
    .force(
      'y',
      d3.forceY(d => G[d.g].y)
        .strength(d => d.layer === 'secondary' ? 0.018 : d.kind === 'core' ? 0.052 : 0.030),
    );
}

export function beginNodeDrag(simulation, node) {
  node.fx = node.x;
  node.fy = node.y;
  simulation.alphaTarget(PHYSICS_BASELINE.dragAlphaTarget).restart();
}

export function moveDraggedNode(node, worldX, worldY) {
  node.fx = worldX;
  node.fy = worldY;
}

export function endNodeDrag(simulation, node) {
  node.fx = null;
  node.fy = null;
  simulation
    .alpha(Math.max(simulation.alpha(), PHYSICS_BASELINE.releaseAlphaFloor))
    .alphaTarget(0)
    .restart();
}
