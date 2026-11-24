export async function createBooking(payload) {
  const csrf = await fetch('/api/bookings/csrf/', { credentials: 'same-origin' });
  if (!csrf.ok) throw new Error('Could not prepare request');

  const { csrfToken } = await csrf.json();
  const response = await fetch('/api/bookings/', {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
    body: JSON.stringify(payload),
  });

  if (response.status === 400) {
    const { errors } = await response.json();
    return { errors };
  }
  if (response.status !== 201) throw new Error('Could not submit request');

  const { id } = await response.json();
  return { id };
}
