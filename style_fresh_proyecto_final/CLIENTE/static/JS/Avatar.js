function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const config = {
  seed: 'avatar-cliente',
  radius: 0,
  size: 96,
  backgroundType: 'gradientLinear',
  backgroundColor: '4e54c8,8f94fb', // 🌅 Atardecer morado
  backgroundRotation: `${Math.floor(Math.random() * 360)}`,
  beardProbability: 100,
  bodyIcon: 'electric',
  bodyIconProbability: 100,
  isGood: 75,
  gestureProbability: 70,
  glassesProbability: 75,
  glasses: '',
  beard: '',
  gesture: '',
  hair: ''
};

const variantData = {
  beard: ['none', ...Array.from({ length: 12 }, (_, i) => `variant${String(i + 1).padStart(2, '0')}`)],
  body: Array.from({ length: 25 }, (_, i) => `variant${String(i + 1).padStart(2, '0')}`),
  brows: Array.from({ length: 13 }, (_, i) => `variant${String(i + 1).padStart(2, '0')}`),
  eyes: Array.from({ length: 5 }, (_, i) => `variant${String(i + 1).padStart(2, '0')}`),
  gesture: ['none', 'hand', 'handPhone', 'ok', 'okLongArm', 'point', 'pointLongArm', 'waveLongArm', 'waveLongArms', 'waveOkLongArms', 'wavePointLongArms'],
  glasses: ['none', ...Array.from({ length: 11 }, (_, i) => `variant${String(i + 1).padStart(2, '0')}`)],
  hair: Array.from({ length: 63 }, (_, i) => `variant${String(i + 1).padStart(2, '0')}`),
  lips: Array.from({ length: 30 }, (_, i) => `variant${String(i + 1).padStart(2, '0')}`),
  nose: Array.from({ length: 20 }, (_, i) => `variant${String(i + 1).padStart(2, '0')}`)
};

const stateIndex = {};
Object.keys(variantData).forEach(key => stateIndex[key] = 0);

function updateAvatar() {
  const params = new URLSearchParams();
  params.append('seed', config.seed);
  params.append('radius', config.radius);
  params.append('size', config.size);
  params.append('backgroundType', config.backgroundType);
  params.append('backgroundColor', config.backgroundColor);
  params.append('backgroundRotation', config.backgroundRotation);
  params.append('beardProbability', config.beardProbability);
  params.append('bodyIcon', config.bodyIcon);
  params.append('bodyIconProbability', config.bodyIconProbability);
  params.append('isGood', config.isGood);
  if (config.gesture) params.append('gestureProbability', config.gestureProbability);
  if (config.glasses) params.append('glassesProbability', config.glassesProbability);
  for (const key of Object.keys(variantData)) {
    const value = config[key];
    if (value && value !== 'none') {
      params.append(key, value);
    }
  }
  const url = `https://api.dicebear.com/9.x/notionists/svg?${params.toString()}`;
  document.getElementById('avatarImage').src = url;
}

function renderVariant(part, containerId) {
  const track = document.getElementById(containerId);
  track.innerHTML = '';
  const currentIndex = stateIndex[part];
  const variants = variantData[part];
  const displayCount = 8;
  const loopedVariants = [];
  for (let i = 0; i < displayCount; i++) {
    const index = (currentIndex + i) % variants.length;
    loopedVariants.push(variants[index]);
  }
  loopedVariants.forEach((variant) => {
    const wrapper = document.createElement('div');
    wrapper.classList.add('variant-thumb-wrapper');
    const img = document.createElement('img');
    img.src = `https://api.dicebear.com/9.x/notionists/svg?seed=preview&backgroundType=gradientLinear&backgroundColor=4e54c8,8f94fb&${variant !== 'none' ? `${part}=${variant}` : ''}`;
    img.alt = variant;
    img.className = 'variant-thumb';
    if (variant === 'none') img.classList.add('none-option');
    img.onclick = () => {
      config[part] = variant === 'none' ? '' : variant;
      if (part === 'beard') config.beardProbability = variant === 'none' ? 0 : 100;
      if (part === 'glasses') config.glassesProbability = variant === 'none' ? 0 : 75;
      if (part === 'gesture') config.gestureProbability = variant === 'none' ? 0 : 70;
      updateAvatar();
    };
    const label = document.createElement('div');
    label.className = 'variant-number';
    label.textContent = variant === 'none' ? 'Sin' : variant.replace('variant', '');
    wrapper.appendChild(img);
    wrapper.appendChild(label);
    track.appendChild(wrapper);
  });
}

function setupNavigation() {
  const buttons = document.querySelectorAll('.carousel-btn');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const part = btn.getAttribute('data-part');
      const variants = variantData[part];
      const step = 8;
      const dir = btn.classList.contains('prev') ? -1 : 1;
      const newIndex = (stateIndex[part] + dir * step + variants.length) % variants.length;
      stateIndex[part] = newIndex;
      renderVariant(part, `${part}-track`);
    });
  });
}

function randomizeAvatar() {
  for (const part in variantData) {
    const variants = variantData[part];
    const filtered = variants.filter(v => v !== 'none');
    const randomVariant = filtered[Math.floor(Math.random() * filtered.length)];
    config[part] = randomVariant;
  }
  updateAvatar();
  for (const part in variantData) {
    renderVariant(part, `${part}-track`);
  }
}

function init() {
  for (const part in variantData) {
    renderVariant(part, `${part}-track`);
  }
  updateAvatar();
  setupNavigation();
}

document.addEventListener('DOMContentLoaded', () => {
  init();

  document.getElementById('randomizeAvatar')?.addEventListener('click', randomizeAvatar);

  document.getElementById('saveAvatar')?.addEventListener('click', () => {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
      <div class="modal">
        <h2>¿Qué quieres hacer con tu avatar?</h2>
        <div class="modal-buttons">
          <button id="downloadPng">📥 Descargar PNG</button>
          <button id="setProfile">🖼️ Usar como perfil</button>
          <button id="closeModal">❌ Cancelar</button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    document.getElementById('closeModal').onclick = () => modal.remove();

    document.getElementById('downloadPng').onclick = async () => {
      const svgUrl = document.getElementById('avatarImage').src;
      const res = await fetch(svgUrl);
      const svgText = await res.text();
      const svg = new Blob([svgText], { type: 'image/svg+xml;charset=utf-8' });
      const url = URL.createObjectURL(svg);
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(url);
        canvas.toBlob(blob => {
          const pngUrl = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = pngUrl;
          a.download = 'avatar.png';
          a.click();
        });
        modal.remove();
      };
      img.src = url;
    };

    document.getElementById('setProfile').onclick = async () => {
      const svgUrl = document.getElementById('avatarImage').src;
      const res = await fetch(svgUrl);
      const svgText = await res.text();
      const svgBlob = new Blob([svgText], { type: 'image/svg+xml' });
      const url = URL.createObjectURL(svgBlob);
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = 512;
        canvas.height = 512;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(async (blob) => {
          const formData = new FormData();
          formData.append('avatar_png', blob, 'avatar.png');
          const response = await fetch('/cliente/avatar/guardar_foto/', {
            method: 'POST',
            headers: {
              'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
          });
          const result = await response.json();
          if (result.success) {
            mostrarModalExito();
            setTimeout(() => location.reload(), 2500);
          } else {
            alert("❌ Error al guardar el avatar.");
          }
          modal.remove();
        }, 'image/png');
      };
      img.src = url;
    };
  });
});

function mostrarModalExito() {
  const modal = document.createElement('div');
  modal.className = 'modal-exito-overlay';
  modal.innerHTML = `
    <div class="modal-exito">
      <div class="check-icon">✅</div>
      <h2>¡Avatar actualizado!</h2>
      <p>Tu nueva foto de perfil se guardó correctamente.</p>
      <button class="cerrar-modal-exito">Seguir</button>
    </div>
  `;
  document.body.appendChild(modal);
  setTimeout(() => modal.classList.add('show'), 10);
  modal.querySelector('.cerrar-modal-exito').onclick = () => {
    modal.classList.remove('show');
    setTimeout(() => modal.remove(), 300);
  };
}
