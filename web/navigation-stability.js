(function () {
  const WORKSPACE_ROUTES = new Set([
    'overview',
    'candidates',
    'desks',
    'scenarios',
    'journal',
    'resources',
    'about'
  ]);

  function currentRoute() {
    return (location.hash || '#candidates').slice(1).split('?')[0] || 'candidates';
  }

  function resetWorkspaceScroll() {
    const main = document.getElementById('main');
    requestAnimationFrame(() => {
      window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
      if (main) {
        main.scrollTop = 0;
        main.focus({ preventScroll: true });
      }
    });
  }

  document.addEventListener('click', event => {
    const link = event.target.closest('a[data-nav]');
    if (!link || !WORKSPACE_ROUTES.has(link.dataset.nav)) return;
    if (currentRoute() === link.dataset.nav) {
      event.preventDefault();
      resetWorkspaceScroll();
    }
  });

  window.addEventListener('hashchange', resetWorkspaceScroll);
})();
