(() => {
  const state = {
    role: 'student',
  };

  const screens = document.querySelectorAll('.screen');
  let currentScreen = document.querySelector('.screen.active') || screens[0];
  let isTransitioning = false;
  const navButtons = document.querySelectorAll('[data-next]');
  const roleTabs = document.querySelectorAll('.role-tab');
  const toggleButtons = document.querySelectorAll('[data-toggle]');

  const roleCopy = {
    student: {
      welcome: 'Welcome back, Student!',
      loginLabel: 'Student Roll Number',
      loginPlaceholder: 'Enter roll number (e.g. 323506402089)',
      loginButton: 'Login as Student',
      signupNameLabel: 'Student Name',
      signupIdLabel: 'Student Roll Number',
      signupIdPlaceholder: 'Enter roll number (e.g. 323506402089)',
      signupButton: 'Sign Up as Student',
      forgotLabel: 'Student Roll Number',
      forgotPlaceholder: 'Enter student roll number',
      detailTitle: 'Student quick details',
      detailBody:
        'If your roll number is in your section list, your timetable and faculty details are mapped automatically.',
    },
    faculty: {
      welcome: 'Welcome back, Faculty!',
      loginLabel: 'Faculty Email / Employee ID',
      loginPlaceholder: 'Enter faculty email or employee id',
      loginButton: 'Login as Faculty',
      signupNameLabel: 'Faculty Name',
      signupIdLabel: 'Faculty Email / Employee ID',
      signupIdPlaceholder: 'Enter faculty email or employee id',
      signupButton: 'Sign Up as Faculty',
      forgotLabel: 'Faculty Email / Employee ID',
      forgotPlaceholder: 'Enter faculty email or employee id',
      detailTitle: 'Faculty quick details',
      detailBody:
        'Faculty accounts can view section timetable and assigned subjects by section.',
    },
  };

  function showScreen(name) {
    const nextScreen = [...screens].find((screen) => screen.dataset.screen === name);
    if (!nextScreen || nextScreen === currentScreen || isTransitioning) return;

    isTransitioning = true;
    currentScreen.classList.add('is-leaving');
    currentScreen.classList.remove('active');
    nextScreen.classList.add('active');

    window.setTimeout(() => {
      currentScreen.classList.remove('is-leaving');
      currentScreen = nextScreen;
      isTransitioning = false;
    }, 360);
  }

  function setRole(role) {
    state.role = role;

    roleTabs.forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.role === role);
    });

    const copy = roleCopy[role];
    const updates = [
      ['roleWelcome', 'textContent', copy.welcome],
      ['loginIdLabel', 'textContent', copy.loginLabel],
      ['loginId', 'placeholder', copy.loginPlaceholder],
      ['loginAction', 'textContent', copy.loginButton],
      ['signupNameLabel', 'textContent', copy.signupNameLabel],
      ['signupIdLabel', 'textContent', copy.signupIdLabel],
      ['signupId', 'placeholder', copy.signupIdPlaceholder],
      ['signupAction', 'textContent', copy.signupButton],
      ['forgotLabel', 'textContent', copy.forgotLabel],
      ['forgotInput', 'placeholder', copy.forgotPlaceholder],
      ['detailTitle', 'textContent', copy.detailTitle],
      ['detailBody', 'textContent', copy.detailBody],
    ];

    updates.forEach(([id, key, value]) => {
      const el = document.getElementById(id);
      if (el) el[key] = value;
    });

    const loginRole = document.getElementById('loginRole');
    const signupRole = document.getElementById('signupRole');
    if (loginRole) loginRole.value = role;
    if (signupRole) signupRole.value = role;
  }

  navButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const next = button.dataset.next;
      if (next) showScreen(next);
    });
  });

  roleTabs.forEach((tab) => {
    tab.addEventListener('click', () => setRole(tab.dataset.role));
  });

  toggleButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const input = document.getElementById(button.dataset.toggle);
      if (!input) return;
      const hidden = input.type === 'password';
      input.type = hidden ? 'text' : 'password';
      button.textContent = hidden ? 'Hide' : 'Show';
    });
  });

  const hasFlash = document.querySelector('.flash-wrap');
  if (hasFlash) {
    showScreen('login');
  }

  setRole('student');
})();
