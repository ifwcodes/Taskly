const quoteList = [
  { text: 'The secret of getting ahead is getting started.', author: 'Mark Twain' },
  { text: 'Productivity is being able to do things that you were never able to do before.', author: 'Franz Kafka' },
  { text: 'Small actions everyday lead to big results.', author: 'Anonymous' },
  { text: 'Success is the sum of small efforts, repeated day in and day out.', author: 'Robert Collier' },
];

const themeToggle = document.getElementById('themeToggle');
const body = document.body;
const newTaskText = document.getElementById('newTaskText');
const charCount = document.getElementById('charCount');
const quoteText = document.getElementById('quoteText');
const quoteAuthor = document.getElementById('quoteAuthor');
const greeting = document.getElementById('greeting');
const todayDate = document.getElementById('todayDate');
const toastContainer = document.getElementById('toastContainer');

function showToast(message) {
  const toast = document.createElement('div');
  toast.className = 'toast-message';
  toast.textContent = message;
  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.classList.add('visible');
  }, 10);
  setTimeout(() => {
    toast.classList.remove('visible');
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function updateTheme() {
  const saved = localStorage.getItem('dashboardTheme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    body.classList.add('dark-mode');
    themeToggle.textContent = 'Light Mode';
  } else {
    body.classList.remove('dark-mode');
    themeToggle.textContent = 'Dark Mode';
  }
}

function toggleTheme() {
  const isDark = body.classList.toggle('dark-mode');
  localStorage.setItem('dashboardTheme', isDark ? 'dark' : 'light');
  themeToggle.textContent = isDark ? 'Light Mode' : 'Dark Mode';
}

function updateQuote() {
  const quote = quoteList[Math.floor(Math.random() * quoteList.length)];
  quoteText.textContent = quote.text;
  quoteAuthor.textContent = `— ${quote.author}`;
}

function updateGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) greeting.textContent = 'Good Morning';
  else if (hour < 18) greeting.textContent = 'Good Afternoon';
  else greeting.textContent = 'Good Evening';
}

function updateCharCount() {
  charCount.textContent = `${newTaskText.value.length} / 140`;
}

function attachEditToggle() {
  document.querySelectorAll('.edit-toggle').forEach((button) => {
    button.addEventListener('click', () => {
      const taskCard = button.closest('.task-card-item');
      taskCard.classList.toggle('editing');
    });
  });

  document.querySelectorAll('.cancel-edit').forEach((button) => {
    button.addEventListener('click', () => {
      const taskCard = button.closest('.task-card-item');
      taskCard.classList.remove('editing');
    });
  });
}

function updateStreak() {
  const streakCount = document.getElementById('streakCount');
  const storedStreak = localStorage.getItem('taskStreak') || '0';
  streakCount.textContent = storedStreak;
}

function createConfetti() {
  if (body.dataset.allCompleted === 'true') {
    const confettiCount = 80;
    for (let i = 0; i < confettiCount; i++) {
      const confetti = document.createElement('div');
      confetti.className = 'confetti-piece';
      confetti.style.left = `${Math.random() * 100}%`;
      confetti.style.background = `hsl(${Math.random() * 360}, 90%, 60%)`;
      confetti.style.animationDuration = `${Math.random() * 1.5 + 1.5}s`;
      confetti.style.opacity = Math.random() * 0.8 + 0.4;
      document.body.appendChild(confetti);
      setTimeout(() => confetti.remove(), 3000);
    }
  }
}

function init() {
  if (themeToggle) themeToggle.addEventListener('click', toggleTheme);
  if (newTaskText) {
    newTaskText.addEventListener('input', updateCharCount);
    updateCharCount();
  }
  updateTheme();
  updateQuote();
  updateGreeting();
  updateStreak();
  attachEditToggle();
  createConfetti();
  if (todayDate) {
    const date = new Date();
    todayDate.textContent = date.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' });
  }
  if (toastContainer && document.querySelectorAll('.toast-message').length) {
    document.querySelectorAll('.toast-message').forEach((message) => {
      toastContainer.appendChild(message);
      setTimeout(() => {
        message.classList.add('visible');
      }, 10);
      setTimeout(() => {
        message.classList.remove('visible');
        setTimeout(() => message.remove(), 300);
      }, 3500);
    });
  }
}

init();
