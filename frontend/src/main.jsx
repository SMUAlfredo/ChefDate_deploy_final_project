import React from 'react';
import { createRoot } from 'react-dom/client';
import { SiteHeader } from './SiteHeader.jsx';
import { BookingForm } from './bookings/BookingForm.jsx';
import './styles.css';

createRoot(document.getElementById('root')).render(
  <>
    <SiteHeader />
    <BookingForm />
  </>,
);
// VA
