export function fadeSlide(node: HTMLElement, { delay = 0, duration = 250 } = {}) {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (prefersReducedMotion) {
    return {
      duration: 0,
      css: () => ''
    };
  }
  
  return {
    duration,
    delay,
    css: (t: number) => `
      opacity: ${t};
      transform: translateY(${(1 - t) * 12}px);
    `
  };
}

export function scaleIn(node: HTMLElement, { delay = 0, duration = 200 } = {}) {
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  
  if (prefersReducedMotion) {
    return {
      duration: 0,
      css: () => ''
    };
  }
  
  return {
    duration,
    delay,
    css: (t: number) => `
      opacity: ${t};
      transform: scale(${0.95 + (t * 0.05)});
    `
  };
}
