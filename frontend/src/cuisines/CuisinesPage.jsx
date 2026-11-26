import React, { useEffect, useRef, useState } from 'react';
import canadianPhoto from './assets/canadian.jpg';
import frenchPhoto from './assets/french.jpg';
import indianPhoto from './assets/indian.jpg';
import italianPhoto from './assets/italian.jpg';
import mexicanPhoto from './assets/mexican.jpg';
import spanishPhoto from './assets/spanish.jpg';
import './cuisines.css';

const demoCuisines = [
  { slug: 'canadian', name: 'Canadian', photo: canadianPhoto },
  { slug: 'french', name: 'French', photo: frenchPhoto },
  { slug: 'indian', name: 'Indian', photo: indianPhoto },
  { slug: 'italian', name: 'Italian', photo: italianPhoto },
  { slug: 'mexican', name: 'Mexican', photo: mexicanPhoto },
  { slug: 'spanish', name: 'Spanish', photo: spanishPhoto },
];

function CuisineCard({ slug, name, photo, inLiveCatalog, onSelect }) {
  const [photoUnavailable, setPhotoUnavailable] = useState(false);
  const useCatalogPhoto = inLiveCatalog && !photoUnavailable;

  return (
    <li>
      <button type="button" onClick={() => onSelect(name)}>
        <img
          src={useCatalogPhoto ? `/api/catalog/photos/${slug}/` : photo}
          onError={useCatalogPhoto ? () => setPhotoUnavailable(true) : undefined}
          alt=""
        />
        <span>{name}</span>
      </button>
    </li>
  );
}

export function CuisinesPage({ onSelectCuisine }) {
  const heading = useRef(null);
  const [cuisines, setCuisines] = useState(null);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    heading.current.focus();
    const controller = new AbortController();

    async function loadCuisines() {
      try {
        const response = await fetch('/api/catalog/', { signal: controller.signal });
        if (!response.ok) throw new Error('Could not load cuisines');
        const catalog = await response.json();
        setCuisines(new Set(catalog.map(({ slug }) => slug)));
      } catch {
        if (!controller.signal.aborted) setHasError(true);
      }
    }

    loadCuisines();
    return () => controller.abort();
  }, []);

  return (
    <main className="page">
      <a className="cuisines-back" href="#booking">Back to booking</a>
      <h1 ref={heading} tabIndex={-1}>Browse cuisines</h1>

      {hasError && <p role="status">The live catalog is unavailable. You can still choose a cuisine.</p>}
      {!hasError && cuisines === null && <p role="status">Loading cuisines…</p>}
      {cuisines?.size === 0 && <p role="status">The live catalog is empty. You can still choose a cuisine.</p>}
      <ul className="cuisine-grid" aria-label="Cuisines">
        {demoCuisines.map((cuisine) => (
          <CuisineCard
            key={cuisine.slug}
            {...cuisine}
            inLiveCatalog={cuisines?.has(cuisine.slug)}
            onSelect={onSelectCuisine}
          />
        ))}
      </ul>
    </main>
  );
}
