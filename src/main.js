import './style.css'

const state = {
  focusMinutes: 45,
  breakMinutes: 10,
  sessionMinutesLeft: 45,
  breakMinutesLeft: 10,
  mode: 'focus',
  isRunning: false,
  streak: 6,
  sessionsDone: 14,
  mood: 78,
  energy: 64,
  momentum: 71,
  focusScore: 82,
  selectedIntent: 'Ship a clean landing page',
  noteInput: 'Finalize hero copy, tighten CTA, and avoid context switching during the next sprint.',
}

const intents = [
  'Ship a clean landing page',
  'Deep work on frontend polish',
  'Review a pull request calmly',
  'Study without opening ten tabs',
]

const focusChallenges = [
  {
    title: 'Single-tab sprint',
    detail: 'Keep only one work tab open for the next focus block.',
    reward: '+8 calm points',
  },
  {
    title: 'Zero-scroll commit',
    detail: 'Finish one concrete task before checking notifications again.',
    reward: '+1 streak shield',
  },
  {
    title: 'Momentum lock',
    detail: 'Write down one blocker and one next action before the timer ends.',
    reward: '+6 focus score',
  },
]

const moodTags = ['Drained', 'Calm', 'Steady', 'Locked In', 'Creative']

const app = document.querySelector('#app')
let timerHandle = null

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value))
}

function formatTime(totalMinutes) {
  const hours = Math.floor(totalMinutes / 60)
  const minutes = totalMinutes % 60
  if (hours === 0) return `${minutes}m`
  return `${hours}h ${minutes}m`
}

function getMoodLabel() {
  if (state.mood >= 88) return moodTags[4]
  if (state.mood >= 74) return moodTags[3]
  if (state.mood >= 58) return moodTags[2]
  if (state.mood >= 40) return moodTags[1]
  return moodTags[0]
}

function getCompanionState() {
  if (state.focusScore >= 85) return 'Locked-in'
  if (state.focusScore >= 70) return 'Stable'
  if (state.focusScore >= 55) return 'Recovering'
  return 'Distracted'
}

function stopTimer() {
  if (timerHandle) {
    clearInterval(timerHandle)
    timerHandle = null
  }
}

function completeCurrentMode() {
  if (state.mode === 'focus') {
    state.sessionsDone += 1
    state.streak += 1
    state.mode = 'break'
    state.breakMinutesLeft = state.breakMinutes
    state.energy = clamp(state.energy + 12, 0, 100)
    state.mood = clamp(state.mood + 6, 0, 100)
  } else {
    state.mode = 'focus'
    state.sessionMinutesLeft = state.focusMinutes
    state.energy = clamp(state.energy - 5, 0, 100)
    state.momentum = clamp(state.momentum + 4, 0, 100)
  }
  state.isRunning = false
  stopTimer()
}

function tickTimer() {
  if (!state.isRunning) return

  if (state.mode === 'focus') {
    state.sessionMinutesLeft -= 1
    state.focusScore = clamp(state.focusScore + 1, 0, 100)
    state.momentum = clamp(state.momentum + 1, 0, 100)
    state.energy = clamp(state.energy - 1, 0, 100)

    if (state.sessionMinutesLeft <= 0) {
      completeCurrentMode()
    }
  } else {
    state.breakMinutesLeft -= 1
    state.energy = clamp(state.energy + 2, 0, 100)
    state.mood = clamp(state.mood + 1, 0, 100)

    if (state.breakMinutesLeft <= 0) {
      completeCurrentMode()
    }
  }

  render()
}

function startTimer() {
  stopTimer()
  timerHandle = setInterval(tickTimer, 1000)
}

function getCompanionMessage() {
  if (state.mode === 'break') {
    return 'Recovery window active. Step away for a short reset so your next block lands cleaner.'
  }
  if (state.focusScore >= 85) {
    return 'You are in a high-quality focus lane. Protect it and avoid unnecessary tab hopping.'
  }
  if (state.focusScore >= 70) {
    return 'Momentum looks healthy. One finished task will sharpen the whole session.'
  }
  return 'Noise is creeping in. Cut scope, pick one task, and let the timer do the discipline.'
}

function getRiskLevel() {
  if (state.energy < 45) return 'High distraction risk'
  if (state.energy < 60) return 'Moderate drift risk'
  return 'Low drift risk'
}

function getSuggestedAction() {
  if (state.mode === 'break') return 'Hydrate, stretch, and stay off work chat for 10 minutes.'
  if (state.energy < 50) return 'Reduce scope to one deliverable and silence secondary channels.'
  if (state.mood > 75) return 'Keep the current lane. Push one visible win before the block ends.'
  return 'Clarify the next tiny milestone, then finish it before switching context.'
}

function buildIntentOptions() {
  return intents
    .map(
      (intent) => `
        <button class="intent-pill ${state.selectedIntent === intent ? 'active' : ''}" data-intent="${intent}">
          ${intent}
        </button>
      `,
    )
    .join('')
}

function buildChallenges() {
  return focusChallenges
    .map(
      (challenge, index) => `
        <article class="challenge-card ${index === 0 ? 'highlight' : ''}">
          <div>
            <p class="eyebrow">Challenge ${index + 1}</p>
            <h3>${challenge.title}</h3>
            <p>${challenge.detail}</p>
          </div>
          <span>${challenge.reward}</span>
        </article>
      `,
    )
    .join('')
}

function render() {
  const activeMinutes = state.mode === 'focus' ? state.sessionMinutesLeft : state.breakMinutesLeft
  const progressPercent = state.mode === 'focus'
    ? Math.round((state.sessionMinutesLeft / state.focusMinutes) * 100)
    : Math.round((state.breakMinutesLeft / state.breakMinutes) * 100)

  app.innerHTML = `
    <div class="shell">
      <section class="hero-panel glass-card">
        <div class="hero-copy">
          <div class="hero-topline">
            <span class="dot"></span>
            AI Focus Companion
          </div>
          <h1>Turn work sessions into calm, adaptive AI-powered focus rituals.</h1>
          <p class="hero-text">
            A virtual companion for deep work, lightweight challenges, and smarter recovery windows.
            Built with Xiaomi MiMo V2.5 Pro.
          </p>
          <div class="hero-actions">
            <button id="toggle-session" class="primary-btn">${state.isRunning ? 'Pause session' : 'Start session'}</button>
            <button id="switch-mode" class="ghost-btn">Switch to ${state.mode === 'focus' ? 'break' : 'focus'} mode</button>
          </div>
        </div>
        <div class="companion-card">
          <div class="orb-wrap">
            <div class="orb"></div>
            <div class="orb-ring"></div>
            <div class="orb-core">
              <span>◎</span>
            </div>
          </div>
          <div class="companion-meta">
            <p class="eyebrow">Companion state</p>
            <h2>${getCompanionState()}</h2>
            <p>${getCompanionMessage()}</p>
          </div>
        </div>
      </section>

      <section class="dashboard-grid">
        <article class="glass-card timer-card">
          <div class="card-head">
            <div>
              <p class="eyebrow">Active timer</p>
              <h3>${state.mode === 'focus' ? 'Deep focus block' : 'Recovery break'}</h3>
            </div>
            <span class="badge ${state.mode}">${state.mode}</span>
          </div>
          <div class="timer-readout">${formatTime(activeMinutes)}</div>
          <div class="progress-bar">
            <div class="progress-fill" style="width: ${progressPercent}%"></div>
          </div>
          <div class="timer-meta">
            <div>
              <span>Streak</span>
              <strong>${state.streak} days</strong>
            </div>
            <div>
              <span>Sessions done</span>
              <strong>${state.sessionsDone}</strong>
            </div>
            <div>
              <span>Intent</span>
              <strong>${state.selectedIntent}</strong>
            </div>
          </div>
        </article>

        <article class="glass-card metrics-card">
          <div class="card-head">
            <div>
              <p class="eyebrow">Focus intelligence</p>
              <h3>Session diagnostics</h3>
            </div>
            <span class="badge soft">Live</span>
          </div>
          <div class="metrics-list">
            <div class="metric-row">
              <span>Focus score</span>
              <strong>${state.focusScore}%</strong>
            </div>
            <div class="metric-row">
              <span>Energy</span>
              <strong>${state.energy}%</strong>
            </div>
            <div class="metric-row">
              <span>Mood</span>
              <strong>${state.mood}% · ${getMoodLabel()}</strong>
            </div>
            <div class="metric-row">
              <span>Momentum</span>
              <strong>${state.momentum}%</strong>
            </div>
          </div>
          <div class="insight-box">
            <p class="eyebrow">Risk signal</p>
            <h4>${getRiskLevel()}</h4>
            <p>${getSuggestedAction()}</p>
          </div>
        </article>
      </section>

      <section class="lower-grid">
        <article class="glass-card intent-card">
          <div class="card-head">
            <div>
              <p class="eyebrow">Session setup</p>
              <h3>Pick today’s work lane</h3>
            </div>
          </div>
          <div class="intent-pills">
            ${buildIntentOptions()}
          </div>
          <label class="notes-box">
            <span>Focus note</span>
            <textarea id="focus-note" rows="5" placeholder="What do you want your companion to optimize for?"></textarea>
          </label>
        </article>

        <article class="glass-card challenge-panel">
          <div class="card-head">
            <div>
              <p class="eyebrow">AI challenge feed</p>
              <h3>Adaptive micro-missions</h3>
            </div>
          </div>
          <div class="challenge-list">
            ${buildChallenges()}
          </div>
        </article>
      </section>

      <section class="glass-card footer-panel">
        <div>
          <p class="eyebrow">Why it helps</p>
          <h3>Less context switching. Better focus rituals.</h3>
        </div>
        <p>
          AI Focus Companion blends timers, intent selection, and lightweight challenge cues into a playful
          deep-work dashboard for makers, students, and developers.
        </p>
      </section>
    </div>
  `

  attachEvents()
}

function attachEvents() {
  const noteField = document.querySelector('#focus-note')
  if (noteField) {
    noteField.value = state.noteInput
  }

  document.querySelector('#toggle-session')?.addEventListener('click', () => {
    state.isRunning = !state.isRunning
    state.focusScore = clamp(state.focusScore + (state.isRunning ? 2 : -1), 0, 100)
    state.momentum = clamp(state.momentum + (state.isRunning ? 3 : -2), 0, 100)

    if (state.isRunning) {
      startTimer()
    } else {
      stopTimer()
    }

    render()
  })

  document.querySelector('#switch-mode')?.addEventListener('click', () => {
    state.mode = state.mode === 'focus' ? 'break' : 'focus'
    state.isRunning = false
    stopTimer()
    state.energy = clamp(state.energy + (state.mode === 'break' ? 8 : -4), 0, 100)
    state.mood = clamp(state.mood + (state.mode === 'break' ? 4 : 1), 0, 100)
    if (state.mode === 'focus') {
      state.sessionMinutesLeft = state.focusMinutes
    } else {
      state.breakMinutesLeft = state.breakMinutes
    }
    render()
  })

  document.querySelectorAll('[data-intent]').forEach((button) => {
    button.addEventListener('click', () => {
      state.selectedIntent = button.dataset.intent || state.selectedIntent
      state.focusScore = clamp(state.focusScore + 1, 0, 100)
      render()
    })
  })

  noteField?.addEventListener('input', (event) => {
    state.noteInput = event.target.value
  })
}

render()
