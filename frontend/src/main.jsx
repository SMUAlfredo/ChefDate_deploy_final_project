import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const contactFields = [
  { name: 'customer_name', label: 'Full name', autoComplete: 'name', maxLength: 150 },
  { name: 'customer_email', label: 'Email', type: 'email', autoComplete: 'email', maxLength: 254 },
  { name: 'customer_phone', label: 'Phone', type: 'tel', autoComplete: 'tel', maxLength: 32 },
];

const eventFields = [
  { name: 'event_address', label: 'Event address', autoComplete: 'street-address', maxLength: 255, wide: true },
  { name: 'event_at', label: 'Date and time', type: 'datetime-local', hint: 'Uses your device’s time zone.' },
  { name: 'guest_count', label: 'Guests', type: 'number', min: 1, step: 1 },
  { name: 'cuisine_type', label: 'Preferred cuisine', maxLength: 100 },
  { name: 'allergy_notes', label: 'Allergy notes', multiline: true, wide: true },
];

const fieldMessages = {
  required: 'This field is required.',
  invalid: 'Enter a valid value.',
  invalid_type: 'Enter a valid value.',
  min_value: 'Enter a number of guests greater than zero.',
  max_value: 'Enter a smaller number.',
  max_length: 'Shorten this value and try again.',
};

function Field({ name, label, hint, wide, multiline, errors, ...inputProps }) {
  const errorId = errors?.length ? `${name}-error` : undefined;
  const hintId = hint ? `${name}-hint` : undefined;
  const Control = multiline ? 'textarea' : 'input';

  return (
    <div className={wide ? 'field field--wide' : 'field'}>
      <label htmlFor={name}>{label}{multiline && <span className="optional"> (optional)</span>}</label>
      <Control
        id={name}
        name={name}
        required={!multiline}
        rows={multiline ? 3 : undefined}
        aria-invalid={errorId ? true : undefined}
        aria-describedby={[hintId, errorId].filter(Boolean).join(' ') || undefined}
        {...inputProps}
      />
      {hint && <p className="field-hint" id={hintId}>{hint}</p>}
      {errorId && (
        <p className="field-error" id={errorId}>
          {errors.map((code) => fieldMessages[code] ?? 'Check this value.').join(' ')}
        </p>
      )}
    </div>
  );
}

function BookingForm() {
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);

  async function handleSubmit(event) {
    event.preventDefault();
    if (submitting) return;

    const form = event.currentTarget;
    const payload = Object.fromEntries(new FormData(form));
    const eventDate = new Date(payload.event_at);
    if (Number.isNaN(eventDate.getTime())) {
      setFeedback({ type: 'error', fields: { event_at: ['invalid'] } });
      return;
    }
    payload.event_at = eventDate.toISOString();
    payload.guest_count = Number(payload.guest_count);

    setSubmitting(true);
    setFeedback(null);

    try {
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
        setFeedback({ type: 'error', fields: errors });
        return;
      }
      if (response.status !== 201) throw new Error('Could not submit request');

      const { id } = await response.json();
      setFeedback({ type: 'success', id });
      form.reset();
    } catch {
      setFeedback({ type: 'unavailable' });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="page">
      <header className="page-heading">
        <p className="brand">ChefDate</p>
        <h1>Request a booking</h1>
        <p>Tell us about your event and how we can reach you.</p>
      </header>

      <form className="booking" onSubmit={handleSubmit}>
        {feedback?.type === 'success' && (
          <div className="feedback feedback--success" role="status">
            <strong>Booking request received.</strong>
            <p>Booking ID: {feedback.id}</p>
          </div>
        )}
        {feedback?.type === 'error' && (
          <p className="feedback feedback--error" role="alert">
            {feedback.fields ? 'Check the highlighted fields and try again.' : 'Check the form and try again.'}
          </p>
        )}
        {feedback?.type === 'unavailable' && (
          <p className="feedback feedback--error" role="alert">We couldn’t send your request. Please try again.</p>
        )}

        <fieldset>
          <legend>Contact details</legend>
          <div className="fields">
            {contactFields.map((field) => <Field key={field.name} {...field} errors={feedback?.fields?.[field.name]} />)}
          </div>
        </fieldset>

        <fieldset>
          <legend>Event details</legend>
          <div className="fields">
            {eventFields.map((field) => <Field key={field.name} {...field} errors={feedback?.fields?.[field.name]} />)}
          </div>
        </fieldset>

        <button type="submit" disabled={submitting}>
          {submitting ? 'Sending request…' : 'Request booking'}
        </button>
      </form>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<BookingForm />);
