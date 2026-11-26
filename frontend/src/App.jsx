import React, { useState, useSyncExternalStore } from 'react';
import { SiteHeader } from './SiteHeader.jsx';
import { BookingForm } from './bookings/BookingForm.jsx';
import { CuisinesPage } from './cuisines/CuisinesPage.jsx';

const cuisinesHash = '#/cuisines';

function subscribeToNavigation(onChange) {
  window.addEventListener('hashchange', onChange);
  return () => window.removeEventListener('hashchange', onChange);
}

function getLocationHash() {
  return window.location.hash;
}

function openCuisines() {
  window.location.hash = cuisinesHash;
}

export function App() {
  const hash = useSyncExternalStore(subscribeToNavigation, getLocationHash);
  const cuisineSlug = hash.startsWith(`${cuisinesHash}/`) ? hash.slice(cuisinesHash.length + 1) : '';
  const browsingCuisines = hash === cuisinesHash || Boolean(cuisineSlug);
  const [preferences, setPreferences] = useState(null);

  function openCuisine(cuisine) {
    setPreferences((current) => current?.cuisine.slug === cuisine.slug ? current : { cuisine, chef: null });
    window.location.hash = `${cuisinesHash}/${cuisine.slug}`;
  }

  function selectChef(cuisine, { slug, name }) {
    setPreferences({ cuisine, chef: { slug, name } });
    window.location.hash = '#booking';
  }

  return (
    <>
      <SiteHeader />
      <BookingForm
        hidden={browsingCuisines}
        preferredCuisine={preferences?.cuisine.name ?? ''}
        preferredChef={preferences?.chef}
        onBrowseCuisines={openCuisines}
        onClearCuisine={() => setPreferences(null)}
      />
      {browsingCuisines && (
        <CuisinesPage cuisineSlug={cuisineSlug} onOpenCuisine={openCuisine} onSelectChef={selectChef} />
      )}
    </>
  );
}
