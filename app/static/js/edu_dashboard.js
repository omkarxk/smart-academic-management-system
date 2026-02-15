(() => {
  const dayTabs = document.querySelectorAll('.day-tab');
  const dayPanels = document.querySelectorAll('.day-panel');

  dayTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const day = tab.dataset.day;
      dayTabs.forEach((node) => node.classList.toggle('active', node === tab));
      dayPanels.forEach((panel) => {
        panel.classList.toggle('active', panel.dataset.panel === day);
      });
    });
  });

  const sectionSelect = document.getElementById('section-select');
  if (sectionSelect) {
    sectionSelect.addEventListener('change', () => {
      const url = new URL(window.location.href);
      url.searchParams.set('section', sectionSelect.value);

      const facultySelectId = sectionSelect.dataset.facultySelect;
      if (facultySelectId) {
        const facultySelect = document.getElementById(facultySelectId);
        if (facultySelect && facultySelect.value) {
          url.searchParams.set('faculty', facultySelect.value);
        }
      }
      window.location.href = url.toString();
    });
  }

  const facultySelect = document.getElementById('faculty-select');
  if (facultySelect) {
    facultySelect.addEventListener('change', () => {
      const url = new URL(window.location.href);
      const section = document.getElementById('section-select');
      if (section && section.value) {
        url.searchParams.set('section', section.value);
      }
      url.searchParams.set('faculty', facultySelect.value);
      window.location.href = url.toString();
    });
  }
})();
