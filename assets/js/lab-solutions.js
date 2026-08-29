(() => {
  const STATUS = document.getElementById('lab-solutions-status');
  const FORM = document.getElementById('lab-solutions-form');
  const OUTPUT = document.getElementById('lab-solutions-output');
  const ENC_URL = 'files/data-612/lab-1-solutions.enc.json';

  function setStatus(text, isError) {
    if (!STATUS) return;
    STATUS.textContent = text;
    STATUS.classList.toggle('is-error', Boolean(isError));
  }

  function b64ToBytes(b64) {
    const bin = atob(b64);
    const out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i += 1) out[i] = bin.charCodeAt(i);
    return out;
  }

  async function deriveKey(password, salt, iterations) {
    const material = await crypto.subtle.importKey(
      'raw',
      new TextEncoder().encode(password),
      'PBKDF2',
      false,
      ['deriveKey']
    );
    return crypto.subtle.deriveKey(
      { name: 'PBKDF2', salt, iterations, hash: 'SHA-256' },
      material,
      { name: 'AES-GCM', length: 256 },
      false,
      ['decrypt']
    );
  }

  async function unlock(password) {
    const res = await fetch(ENC_URL, { cache: 'no-store' });
    if (!res.ok) throw new Error('Could not load the locked file.');
    const payload = await res.json();
    const key = await deriveKey(password, b64ToBytes(payload.salt), payload.iter);
    const plain = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: b64ToBytes(payload.iv) },
      key,
      b64ToBytes(payload.ct)
    );
    return new TextDecoder().decode(plain);
  }

  if (!FORM) return;

  FORM.addEventListener('submit', async (event) => {
    event.preventDefault();
    const input = FORM.querySelector('input[name="passphrase"]');
    const password = input ? String(input.value) : '';
    if (!password) {
      setStatus('Enter the password.', true);
      return;
    }
    setStatus('Opening…');
    try {
      const html = await unlock(password);
      OUTPUT.innerHTML = html;
      OUTPUT.hidden = false;
      FORM.hidden = true;
      FORM.style.display = 'none';
      setStatus('');
    } catch (err) {
      setStatus('That password did not open the solutions.', true);
    }
  });
})();
