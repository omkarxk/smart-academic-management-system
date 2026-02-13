(() => {
  const state = {
    role: "student",
  };

  const screens = document.querySelectorAll(".screen");
  let currentScreen = document.querySelector(".screen.active") || screens[0];
  let isTransitioning = false;
  const navButtons = document.querySelectorAll("[data-next]");
  const roleTabs = document.querySelectorAll(".role-tab");
  const toggleButtons = document.querySelectorAll("[data-toggle]");

  const roleCopy = {
    student: {
      welcome: "Welcome back, Student!",
      loginLabel: "Student Email / Roll Number",
      loginPlaceholder: "Enter student email or roll no",
      loginButton: "Login as Student",
      signupNameLabel: "Student Name",
      signupIdLabel: "Student Email / Roll Number",
      signupIdPlaceholder: "Enter student email or roll no",
      signupButton: "Sign Up as Student",
      forgotLabel: "Student Email / Roll Number",
      forgotPlaceholder: "Enter student email or roll no",
      detailTitle: "Student quick details",
      detailBody:
        "Use your college email and roll number format like 24CSE103. You will see attendance, timetable, and notifications after login.",
    },
    faculty: {
      welcome: "Welcome back, Faculty!",
      loginLabel: "Faculty Email / Employee ID",
      loginPlaceholder: "Enter faculty email or employee id",
      loginButton: "Login as Faculty",
      signupNameLabel: "Faculty Name",
      signupIdLabel: "Faculty Email / Employee ID",
      signupIdPlaceholder: "Enter faculty email or employee id",
      signupButton: "Sign Up as Faculty",
      forgotLabel: "Faculty Email / Employee ID",
      forgotPlaceholder: "Enter faculty email or employee id",
      detailTitle: "Faculty quick details",
      detailBody:
        "Use official faculty email and employee ID format like FAC-1024. You will manage sections, attendance, and class schedule updates.",
    },
  };

  function showScreen(name) {
    const nextScreen = [...screens].find((screen) => screen.dataset.screen === name);
    if (!nextScreen || nextScreen === currentScreen || isTransitioning) return;

    isTransitioning = true;
    currentScreen.classList.add("is-leaving");
    currentScreen.classList.remove("active");

    nextScreen.classList.add("active");

    window.setTimeout(() => {
      currentScreen.classList.remove("is-leaving");
      currentScreen = nextScreen;
      isTransitioning = false;
    }, 360);
  }

  function setRole(role) {
    state.role = role;

    roleTabs.forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.role === role);
    });

    const copy = roleCopy[role];
    const updates = [
      ["roleWelcome", "textContent", copy.welcome],
      ["loginIdLabel", "textContent", copy.loginLabel],
      ["loginId", "placeholder", copy.loginPlaceholder],
      ["loginAction", "textContent", copy.loginButton],
      ["signupNameLabel", "textContent", copy.signupNameLabel],
      ["signupIdLabel", "textContent", copy.signupIdLabel],
      ["signupId", "placeholder", copy.signupIdPlaceholder],
      ["signupAction", "textContent", copy.signupButton],
      ["forgotLabel", "textContent", copy.forgotLabel],
      ["forgotInput", "placeholder", copy.forgotPlaceholder],
      ["detailTitle", "textContent", copy.detailTitle],
      ["detailBody", "textContent", copy.detailBody],
    ];

    updates.forEach(([id, key, value]) => {
      const el = document.getElementById(id);
      if (el) el[key] = value;
    });
  }

  navButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const next = button.dataset.next;
      if (button.id === "signupAction") {
        showScreen("created");
        return;
      }
      if (next) showScreen(next);
    });
  });

  roleTabs.forEach((tab) => {
    tab.addEventListener("click", () => setRole(tab.dataset.role));
  });

  toggleButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const input = document.getElementById(button.dataset.toggle);
      if (!input) return;

      const hidden = input.type === "password";
      input.type = hidden ? "text" : "password";
      button.textContent = hidden ? "Hide" : "Show";
    });
  });

  document.querySelectorAll(".otp").forEach((input, index, all) => {
    input.addEventListener("input", () => {
      input.value = input.value.replace(/\D/g, "").slice(0, 1);
      if (input.value && index < all.length - 1) all[index + 1].focus();
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Backspace" && !input.value && index > 0) {
        all[index - 1].focus();
      }
    });
  });

  setRole("student");
})();
