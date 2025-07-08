function loadData() {
  fetch('/get_data')
    .then((res) => {
      if (!res.ok) throw new Error('Bad response from server');
      return res.json();
    })
    .then((data) => {
      renderCurrent(data.current || []);
      renderAvailable(data.available || []);
      renderActivation(data.activation || {});
    })
    .catch((err) => {
      console.error('⚠️ Error loading data:', err);
    });
}

function renderCurrent(exercises) {
  const container = document.querySelector('#current-routine');
  container.innerHTML = '';
  exercises.forEach((ex) => {
    container.innerHTML += `
        <div class="exercise">
          <div class="exercise-inner">
            <span>${ex.name}</span>
            <span class="remove-btn" onclick="updatePlan('remove', ${ex.id})">❌</span>
          </div>
        </div>`;
  });
}

function renderAvailable(exercises) {
  const container = document.querySelector('#available-exercises');
  container.innerHTML = '';
  exercises.forEach((ex) => {
    container.innerHTML += `
        <div class="exercise">
          <div class="exercise-inner">
            <span>${ex.name}</span>
            <span class="add-btn" onclick="updatePlan('add', ${ex.id})">➕</span>
          </div>
        </div>`;
  });
}

function updatePlan(action, id) {
  fetch('/update', {
    method: 'POST',
    body: JSON.stringify({ action, id }),
    headers: { 'Content-Type': 'application/json' },
  })
    .then((res) => res.json())
    .then((data) => {
      renderCurrent(data.current);
      renderAvailable(data.available);
      renderActivation(data.activation);
    });
}

function renderActivation(activation) {
  const container = document.querySelector('#muscle-activation');
  container.innerHTML = '';
  for (const [muscle, value] of Object.entries(activation)) {
    container.innerHTML += `<div class="muscle">${muscle}: ${value}%</div>`;
  }
}


