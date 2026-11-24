import React, { useState } from 'react';
import { BookingFields } from './BookingFields.jsx';
import { createBooking } from './bookingApi.js';

export function BookingForm() {
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
      const result = await createBooking(payload);
      if ('errors' in result) {
        setFeedback({ type: 'error', fields: result.errors });
        return;
      }

      setFeedback({ type: 'success', id: result.id });
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

        <BookingFields errors={feedback?.fields} />

        <button type="submit" disabled={submitting}>
          {submitting ? 'Sending request…' : 'Request booking'}
        </button>
      </form>
    </main>
  );
}
