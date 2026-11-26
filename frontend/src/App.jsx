import React, { useState, useSyncExternalStore } from 'react';
import { SiteHeader } from './SiteHeader.jsx';
import { BookingForm } from './bookings/BookingForm.jsx';
import { CuisinesPage } from './cuisines/CuisinesPage.jsx';

const cuisinesHash = '#/cuisines';

function subscribeToNavigation(onChange) {
  window.addEventListener('hashchange', onChange);
  return () => window.removeEventListener('hashchange', onChange);
}

function isBrowsingCuisines() {
  return window.location.hash === cuisinesHash;
}

function openCuisines() {
  window.location.hash = cuisinesHash;
}

export function App() {
  const browsingCuisines = useSyncExternalStore(subscribeToNavigation, isBrowsingCuisines);
  const [preferredCuisine, setPreferredCuisine] = useState('');

  function selectCuisine(name) {
    setPreferredCuisine(name);
    window.location.hash = '#booking';
  }

  return (
    <>
      <SiteHeader />
      <BookingForm
        hidden={browsingCuisines}
        preferredCuisine={preferredCuisine}
        onBrowseCuisines={openCuisines}
        onClearCuisine={() => setPreferredCuisine('')}
      />
      {browsingCuisines && <CuisinesPage onSelectCuisine={selectCuisine} />}
    </>
  );
}
