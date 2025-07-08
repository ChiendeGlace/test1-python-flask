const steps = [
  {
    question: 'Choose your plan type',
    name: 'plan_type',
    options: ['Full Body', 'Push-Pull', 'Upper-Lower', 'Custom'],
  },
  {
    question: 'Choose your training goal',
    name: 'goal',
    options: [
      'Strength',
      'Hypertrophy',
      'Mobility',
      'Endurance',
      'General Health',
      'Functional Fitness',
    ],
  },
  {
    question: 'Select available equipment',
    name: 'available_equipment',
    options: [
      'Barbell',
      'Dumbbell',
      'Kettlebell',
      'Resistance Band',
      'Pull-Up Bar',
      'Dip Bars',
      'Parallettes',
      'Bench',
      'Squat Rack',
      'Smith Machine',
      'Cable Machine',
      'Leg Press Machine',
      'Pec Deck Machine',
      'Rowing Machine',
      'Treadmill',
      'Stationary Bike',
      'Bodyweight',
      'Medicine Ball',
      'Stability Ball',
      'Box',
    ],
    multi: true,
  },
  {
    question: 'Preferred training method',
    name: 'training_type',
    options: ['Free Weights', 'Machines', 'Bodyweight'],
    multi: true,
  },
  {
    question: 'How many training days per week?',
    name: 'training_days_per_week',
    options: ['1', '2', '3', '4', '5', '6', '7'],
  },
  {
    question: 'How long should each session be (minutes)?',
    name: 'session_length',
    options: ['30', '45', '60', '75', '90', '120'],
  },
  {
    question: "What's your engagement level?",
    name: 'engagement_level',
    options: ['low', 'medium', 'high'],
  },
];

let currentStep = 0;
const userInput = {};

const questionText = document.getElementById('question-text');
const optionsContainer = document.getElementById('options');
const nextBtn = document.getElementById('next-btn');

function renderStep(stepIndex) {
  const step = steps[stepIndex];
  questionText.textContent = step.question;
  optionsContainer.innerHTML = '';
  nextBtn.style.display = 'none';

  const selectedValues = userInput[step.name] || (step.multi ? [] : null);

  step.options.forEach((option) => {
    const div = document.createElement('div');
    div.className = 'option-tile';
    div.textContent = option;

    if (step.multi && selectedValues.includes(option)) {
      div.classList.add('selected');
    } else if (!step.multi && selectedValues === option) {
      div.classList.add('selected');
    }

    div.onclick = () => {
      if (step.multi) {
        if (!userInput[step.name]) userInput[step.name] = [];
        const index = userInput[step.name].indexOf(option);
        if (index === -1) {
          userInput[step.name].push(option);
          div.classList.add('selected');
        } else {
          userInput[step.name].splice(index, 1);
          div.classList.remove('selected');
        }
        nextBtn.style.display =
          userInput[step.name].length > 0 ? 'inline-block' : 'none';
      } else {
        document
          .querySelectorAll('.option-tile')
          .forEach((e) => e.classList.remove('selected'));
        div.classList.add('selected');
        userInput[step.name] = option;
        nextBtn.style.display = 'inline-block';
      }
    };

    optionsContainer.appendChild(div);
  });
}

nextBtn.onclick = () => {
  currentStep++;
  if (currentStep < steps.length) {
    renderStep(currentStep);
  } else {
    // 🔁 Konwersja training_type → bo backend tego oczekuje
    if (Array.isArray(userInput.training_type)) {
      userInput.free_weights = userInput.training_type.includes('Free Weights');
      userInput.machines = userInput.training_type.includes('Machines');
      userInput.bodyweight = userInput.training_type.includes('Bodyweight');
      delete userInput.training_type;
    }

    // 🔢 konwersja training_days_per_week i session_length do liczby
    userInput.training_days_per_week = parseInt(
      userInput.training_days_per_week
    );
    userInput.session_length = parseInt(userInput.session_length);

    fetch('/submit_input', {
      method: 'POST',
      body: JSON.stringify(userInput),
      headers: { 'Content-Type': 'application/json' },
    }).then(() => {
      document.getElementById('form-section').style.display = 'none';
      document.getElementById('planner-section').style.display = 'flex';
      if (typeof window.loadData === 'function') {
        window.loadData();
      }
    });
  }
};

window.addEventListener('DOMContentLoaded', () => {
  renderStep(currentStep);
});
