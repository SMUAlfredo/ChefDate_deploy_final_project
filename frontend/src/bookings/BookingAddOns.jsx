import React, { useEffect, useState } from 'react';
import './bookingAddOns.css';

const priceFormat = new Intl.NumberFormat('en-CA', {
  style: 'currency',
  currency: 'CAD',
  currencyDisplay: 'code',
});

export function BookingAddOns() {
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
      {addOns?.length > 0 && <p className="field-hint">Selections are for this draft only.</p>}
      {addOns?.map(({ slug, name, price_cad: price }) => (
        <label className="booking-add-on" key={slug}>
          <input type="checkbox" value={slug} />
          <span>{name} · {priceFormat.format(price)} per booking</span>
        </label>
      ))}
    </fieldset>
  );
}
