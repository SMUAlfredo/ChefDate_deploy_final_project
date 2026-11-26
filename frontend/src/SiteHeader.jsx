import React from 'react';

export function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header__content">
        <p className="brand">ChefDate</p>
        <nav className="site-nav" aria-label="Main navigation">
          <ul>
            <li><a href="#booking" aria-current="location">Book</a></li>
            <li>Profile <small>Unavailable</small></li>
            <li>Booking Status <small>Unavailable</small></li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
