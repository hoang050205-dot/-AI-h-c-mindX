/**
 * AI4A BI Counter Animation Engine
 * Ultra-smooth 60fps numerical count-up effect with easing, locale formatting, and IntersectionObserver triggering.
 * Version: 1.0.0
 * Zero Dependencies (Pure Vanilla ES6+)
 */

class CounterEngine {
  /**
   * Easing functions for natural decelerating motion
   */
  static easings = {
    // Standard easeOutCubic: fast start, soft landing
    easeOutCubic: (t) => 1 - Math.pow(1 - t, 3),
    // High-impact easeOutExpo: dramatic deceleration
    easeOutExpo: (t) => (t === 1 ? 1 : 1 - Math.pow(2, -10 * t)),
    // Smooth easeOutQuart
    easeOutQuart: (t) => 1 - Math.pow(1 - t, 4),
  };

  /**
   * Format a numerical value with commas/dots, decimals, prefix and suffix
   */
  static formatNumber(value, options = {}) {
    const {
      decimals = 0,
      separator = ',',
      decimalPoint = '.',
      prefix = '',
      suffix = '',
    } = options;

    const fixed = value.toFixed(decimals);
    const parts = fixed.split('.');
    
    // Format integer part with thousands separator
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, separator);

    // Combine with decimal part if applicable
    const formattedNum = parts.length > 1 ? parts.join(decimalPoint) : parts[0];
    return `${prefix}${formattedNum}${suffix}`;
  }

  /**
   * Animate a single DOM element from start to target value
   */
  static animate(element, customOptions = {}) {
    if (!element) return;

    // Parse options from attributes or custom arguments
    const targetValue = parseFloat(customOptions.target ?? element.getAttribute('data-counter') ?? 0);
    const startValue = parseFloat(customOptions.start ?? element.getAttribute('data-counter-start') ?? 0);
    const duration = parseInt(customOptions.duration ?? element.getAttribute('data-counter-duration') ?? 1600, 10);
    const decimals = parseInt(customOptions.decimals ?? element.getAttribute('data-counter-decimals') ?? 0, 10);
    const prefix = customOptions.prefix ?? element.getAttribute('data-counter-prefix') ?? '';
    const suffix = customOptions.suffix ?? element.getAttribute('data-counter-suffix') ?? '';
    const separator = customOptions.separator ?? element.getAttribute('data-counter-separator') ?? ',';
    const decimalPoint = customOptions.decimalPoint ?? element.getAttribute('data-counter-decimal-point') ?? '.';
    const easingName = customOptions.easing ?? element.getAttribute('data-counter-easing') ?? 'easeOutExpo';

    const easingFunc = CounterEngine.easings[easingName] || CounterEngine.easings.easeOutExpo;
    const formatOpts = { decimals, separator, decimalPoint, prefix, suffix };

    let startTime = null;
    let animFrameId = null;

    // Cancel any running animation on this element
    if (element._counterAnimId) {
      cancelAnimationFrame(element._counterAnimId);
    }

    element.dispatchEvent(new CustomEvent('counter:start', { detail: { targetValue } }));

    const step = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easingFunc(progress);

      const currentValue = startValue + (targetValue - startValue) * easedProgress;
      element.textContent = CounterEngine.formatNumber(currentValue, formatOpts);

      if (progress < 1) {
        element._counterAnimId = requestAnimationFrame(step);
      } else {
        // Guarantee final exact number
        element.textContent = CounterEngine.formatNumber(targetValue, formatOpts);
        element.setAttribute('data-counter-done', 'true');
        element._counterAnimId = null;
        element.dispatchEvent(new CustomEvent('counter:complete', { detail: { targetValue } }));
      }
    };

    element._counterAnimId = requestAnimationFrame(step);
  }

  /**
   * Initialize all counter elements on the page with IntersectionObserver
   */
  static init(selector = '[data-counter]') {
    const elements = document.querySelectorAll(selector);
    if (!elements || elements.length === 0) return;

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const targetEl = entry.target;
            CounterEngine.animate(targetEl);
            obs.unobserve(targetEl); // Animate once on initial scroll view
          }
        });
      }, {
        threshold: 0.15,
        rootMargin: '0px 0px -20px 0px',
      });

      elements.forEach((el) => {
        // Set placeholder before animation begins
        if (!el.getAttribute('data-counter-done')) {
          const prefix = el.getAttribute('data-counter-prefix') ?? '';
          const suffix = el.getAttribute('data-counter-suffix') ?? '';
          const decimals = parseInt(el.getAttribute('data-counter-decimals') ?? 0, 10);
          el.textContent = `${prefix}${(0).toFixed(decimals)}${suffix}`;
        }
        observer.observe(el);
      });
    } else {
      // Fallback for environments without IntersectionObserver
      elements.forEach((el) => CounterEngine.animate(el));
    }
  }

  /**
   * Re-animate all elements (e.g., when switching filters or date ranges)
   */
  static animateAll(selector = '[data-counter]') {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el) => {
      CounterEngine.animate(el);
    });
  }

  /**
   * Smoothly update an element to a new target value
   */
  static updateValue(element, newValue, options = {}) {
    if (!element) return;
    const currentNum = parseFloat(element.getAttribute('data-counter') || 0);
    element.setAttribute('data-counter', newValue);
    CounterEngine.animate(element, {
      start: currentNum,
      target: newValue,
      duration: options.duration || 1200,
      ...options
    });
  }
}

// Auto-initialize when DOM is ready
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => CounterEngine.init());
  } else {
    CounterEngine.init();
  }
}

// Export for module systems or window global
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CounterEngine;
} else if (typeof window !== 'undefined') {
  window.CounterEngine = CounterEngine;
}
