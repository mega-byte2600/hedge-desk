(() => {
  const internalRoutes = new Set(['controls']);

  function normalizePublicRoute() {
    const route = (location.hash || '').slice(1).split('?')[0];
    if (internalRoutes.has(route)) {
      history.replaceState(null, '', '#overview');
    }
  }

  normalizePublicRoute();
  window.addEventListener('hashchange', normalizePublicRoute);

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-nav="controls"]').forEach(node => node.remove());
  });
})();
