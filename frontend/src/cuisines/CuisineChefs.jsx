import React from 'react';
import './chefs.css';

export function CuisineChefs({ chefs, loading, unavailable, onSelectChef }) {
  if (loading) return <p role="status">Loading chefs…</p>;
  if (unavailable) return <p role="status">The live chef list is unavailable.</p>;
  if (!chefs.length) return <p role="status">No chefs are available for this cuisine.</p>;

  return (
    <ul className="chef-list" aria-label="Chefs">
      {chefs.map((chef) => (
        <li key={chef.slug}>
          <h2>{chef.name}</h2>
          <dl>
            <div>
              <dt>Base price</dt>
              <dd>{chef.base_price_cad} CAD per booking</dd>
            </div>
            <div>
              <dt>Demo rating</dt>
              <dd>{chef.rating.toFixed(1)} / 5</dd>
            </div>
          </dl>
          <button type="button" aria-label={`Select chef ${chef.name}`} onClick={() => onSelectChef(chef)}>
            Select chef
          </button>
        </li>
      ))}
    </ul>
  );
}
