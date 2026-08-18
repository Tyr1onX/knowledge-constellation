// Identity Presence gives the universe a visible owner without turning the
// surface into a profile card. It is ephemeral by default and returns on Core hover.

export const IDENTITY_PRESENCE = Object.freeze({
  holdMs: 3600,
  fadeMs: 3600,
  introAlpha: 0.64,
  hoverAlpha: 0.76,
});

export function identityPresenceOpacity({
  elapsedMs,
  hoveringCore = false,
  exploring = false,
}) {
  if (hoveringCore) return IDENTITY_PRESENCE.hoverAlpha;
  if (exploring) return 0;
  if (elapsedMs <= IDENTITY_PRESENCE.holdMs) return IDENTITY_PRESENCE.introAlpha;

  const fadeElapsed = elapsedMs - IDENTITY_PRESENCE.holdMs;
  if (fadeElapsed >= IDENTITY_PRESENCE.fadeMs) return 0;
  return IDENTITY_PRESENCE.introAlpha * (1 - fadeElapsed / IDENTITY_PRESENCE.fadeMs);
}

export function drawIdentityPresence(ctx, identity, options) {
  const {
    corePoint,
    viewScale = 1,
    elapsedMs = 0,
    hoveringCore = false,
    exploring = false,
  } = options;

  if (!identity) return 0;

  const alpha = identityPresenceOpacity({ elapsedMs, hoveringCore, exploring });
  if (alpha < 0.01) return 0;

  const title = identity.title || identity.label || '';
  const subtitle = identity.subtitle || '';
  const source = identity.source || '';
  const y = corePoint.y + Math.max(52, 56 * viewScale);

  ctx.save();
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  if (title) {
    ctx.font = '560 12px Inter,"PingFang SC","Microsoft YaHei",sans-serif';
    ctx.fillStyle = `rgba(229,237,246,${alpha})`;
    ctx.fillText(title, corePoint.x, y);
  }

  if (subtitle) {
    ctx.font = '400 8.5px Inter,"PingFang SC","Microsoft YaHei",sans-serif';
    ctx.fillStyle = `rgba(136,153,174,${alpha * 0.70})`;
    ctx.fillText(subtitle, corePoint.x, y + 17);
  }

  if (source) {
    ctx.font = '500 7.5px Inter,"PingFang SC","Microsoft YaHei",sans-serif';
    ctx.fillStyle = `rgba(95,111,132,${alpha * 0.56})`;
    ctx.fillText(source, corePoint.x, y + 31);
  }

  ctx.restore();
  return alpha;
}
