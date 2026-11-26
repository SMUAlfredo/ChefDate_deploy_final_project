import React, { useState } from 'react';
import { BookingAddOns, useBookingAddOnDraft } from './BookingAddOns.jsx';
import { BookingFields } from './BookingFields.jsx';
import { createBooking } from './bookingApi.js';

export function BookingForm({ hidden, preferredCuisine, preferredChef, onBrowseCuisines, onClearCuisine }) {
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [needsCuisine, setNeedsCuisine] = useState(false);
  const addOnDraft = useBookingAddOnDraft();
  const fields = feedback?.fields;
  const chefErrors = feedback?.chefSlug === preferredChef?.slug ? fields?.preferred_chef_slug : undefined;
  const hasFieldErrors = chefErrors?.length || Object.keys(fields ?? {}).some((name) => name !== 'preferred_chef_slug');

  async function handleSubmit(event) {
    event.preventDefault();
    if (submitting) return;

    const form = event.currentTarget;
    if (!preferredCuisine) {
      setNeedsCuisine(true);
      form.querySelector('.browse-cuisines').focus();
      return;
    }

    const payload = Object.fromEntries(new FormData(form));
    payload.cuisine_type = preferredCuisine;
    if (preferredChef?.slug) payload.preferred_chef_slug = preferredChef.slug;
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
        setFeedback({ type: 'error', fields: result.errors, chefSlug: payload.preferred_chef_slug });
        return;
      }

      setFeedback({ type: 'success', id: result.id });
      form.reset();
      addOnDraft.reset();
      setNeedsCuisine(false);
      onClearCuisine();
    } catch {
      setFeedback({ type: 'unavailable' });
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main id="booking" className="page" hidden={hidden}>
      <header className="page-heading">
        <h1>Request a booking</h1>
        <p>Tell us about your event and how we can reach you.</p>
      </header>

      <form className="booking" onSubmit={handleSubmit} onChange={addOnDraft.handleGuestCountChange}>
        {feedback?.type === 'success' && (
          <div className="feedback feedback--success" role="status">
            <strong>Booking request received.</strong>
            <p>Booking ID: {feedback.id}</p>
          </div>
        )}
        {feedback?.type === 'error' && (!fields || hasFieldErrors) && (
          <p className="feedback feedback--error" role="alert">
            {fields ? 'Check the highlighted fields and try again.' : 'Check the form and try again.'}
          </p>
        )}
        {feedback?.type === 'unavailable' && (
          <p className="feedback feedback--error" role="alert">We couldn’t send your request. Please try again.</p>
        )}

        <BookingFields
          errors={fields}
          preferredCuisine={preferredCuisine}
          preferredChef={preferredChef?.name}
          chefErrors={chefErrors}
          needsCuisine={needsCuisine && !preferredCuisine}
          onBrowseCuisines={onBrowseCuisines}
        />

        <BookingAddOns
          maxQuantity={addOnDraft.maxQuantity}
          quantities={addOnDraft.quantities}
          onQuantityChange={addOnDraft.setQuantity}
        />

        <button type="submit" disabled={submitting}>
          {submitting ? 'Sending request…' : 'Request booking'}
        </button>
      </form>
    </main>
  );
}
// VA
