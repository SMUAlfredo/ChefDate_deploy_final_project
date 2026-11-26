import React, { useEffect, useState } from 'react';
import './bookingAddOns.css';

const guestsPerAddOn = 5;
const emptyDraft = { maxQuantity: 0, quantities: {} };
const priceFormat = new Intl.NumberFormat('en-CA', {
  style: 'currency',
  currency: 'CAD',
  currencyDisplay: 'code',
});

export function useBookingAddOnDraft() {
  const [draft, setDraft] = useState(emptyDraft);

  function handleGuestCountChange(event) {
    if (event.target.name !== 'guest_count') return;
    const count = event.target.valueAsNumber;
    const maxQuantity = Number.isSafeInteger(count) && count > 0 ? Math.ceil(count / guestsPerAddOn) : 0;

    setDraft((current) => ({
      maxQuantity,
      quantities: maxQuantity === 0 ? current.quantities : Object.fromEntries(
        Object.entries(current.quantities).map(([slug, quantity]) => [slug, Math.min(quantity, maxQuantity)]),
      ),
    }));
  }

  function setQuantity(slug, quantity) {
    setDraft((current) => ({
      ...current,
      quantities: { ...current.quantities, [slug]: quantity },
    }));
  }

  return { ...draft, handleGuestCountChange, setQuantity, reset: () => setDraft(emptyDraft) };
}

export function BookingAddOns({ maxQuantity, quantities, onQuantityChange }) {
  const [addOns, setAddOns] = useState(null);
  const [unavailable, setUnavailable] = useState(false);

  useEffect(() => {
    const controller = new AbortController();

    async function loadAddOns() {
      try {
        const response = await fetch('/api/catalog/add-ons/', { signal: controller.signal });
        if (!response.ok) throw new Error('Could not load booking add-ons');
        setAddOns(await response.json());
      } catch {
        if (!controller.signal.aborted) setUnavailable(true);
      }
    }

    loadAddOns();
    return () => controller.abort();
  }, []);

  return (
    <fieldset>
      <legend>Optional add-ons</legend>
      {unavailable && <p role="status">Add-ons are temporarily unavailable.</p>}
      {!unavailable && !addOns && <p role="status">Loading add-ons…</p>}
      {addOns?.length === 0 && <p role="status">No add-ons are available.</p>}
      {addOns?.length > 0 && (
        <>
          <p className="field-hint">Each add-on unit covers up to {guestsPerAddOn} guests. Selections are for this draft only.</p>
          <p className="field-hint" role="status">
            {maxQuantity > 0 ? `Maximum per add-on for this booking: ${maxQuantity}.` : 'Enter the number of guests to choose add-ons.'}
          </p>
        </>
      )}
      {addOns?.map(({ slug, name, price_cad: price }) => {
        const quantity = maxQuantity > 0 ? quantities[slug] ?? 0 : 0;

        return (
          <div className="booking-add-on" key={slug}>
            <span>{name} · {priceFormat.format(price)} per unit</span>
            <div className="booking-add-on__quantity" role="group" aria-label={`${name} quantity`}>
              <button
                type="button"
                aria-label={`Decrease ${name} quantity`}
                disabled={quantity === 0}
                onClick={() => onQuantityChange(slug, quantity - 1)}
              >
                −
              </button>
              <output aria-label={`${name} units`}>{quantity}</output>
              <button
                type="button"
                aria-label={`Increase ${name} quantity`}
                disabled={quantity >= maxQuantity}
                onClick={() => onQuantityChange(slug, quantity + 1)}
              >
                +
              </button>
            </div>
          </div>
        );
      })}
    </fieldset>
  );
}
