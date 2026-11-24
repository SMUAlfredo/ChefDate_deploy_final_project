import React from 'react';

const contactFields = [
  { name: 'customer_name', label: 'Full name', autoComplete: 'name', maxLength: 150 },
  { name: 'customer_email', label: 'Email', type: 'email', autoComplete: 'email', maxLength: 254 },
  { name: 'customer_phone', label: 'Phone', type: 'tel', autoComplete: 'tel', maxLength: 32 },
];

const eventFields = [
  { name: 'event_address', label: 'Event address', autoComplete: 'street-address', maxLength: 255, wide: true },
  { name: 'event_at', label: 'Date and time', type: 'datetime-local', hint: 'Uses your device’s time zone.' },
  { name: 'guest_count', label: 'Guests', type: 'number', min: 1, step: 1 },
  { name: 'cuisine_type', label: 'Preferred cuisine', maxLength: 100 },
  { name: 'allergy_notes', label: 'Allergy notes', maxLength: 1000, multiline: true, wide: true },
];

const fieldMessages = {
  required: 'This field is required.',
  invalid: 'Enter a valid value.',
  invalid_type: 'Enter a valid value.',
  min_value: 'Enter a number of guests greater than zero.',
  max_value: 'Enter a smaller number.',
  max_length: 'Shorten this value and try again.',
};

function Field({ name, label, hint, wide, multiline, errors, ...inputProps }) {
  const errorId = errors?.length ? `${name}-error` : undefined;
  const hintId = hint ? `${name}-hint` : undefined;
  const Control = multiline ? 'textarea' : 'input';

  return (
    <div className={wide ? 'field field--wide' : 'field'}>
      <label htmlFor={name}>{label}{multiline && <span className="optional"> (optional)</span>}</label>
      <Control
        id={name}
        name={name}
        required={!multiline}
        rows={multiline ? 3 : undefined}
        aria-invalid={errorId ? true : undefined}
        aria-describedby={[hintId, errorId].filter(Boolean).join(' ') || undefined}
        {...inputProps}
      />
      {hint && <p className="field-hint" id={hintId}>{hint}</p>}
      {errorId && (
        <p className="field-error" id={errorId}>
          {errors.map((code) => fieldMessages[code] ?? 'Check this value.').join(' ')}
        </p>
      )}
    </div>
  );
}

const sections = [
  { legend: 'Contact details', fields: contactFields },
  { legend: 'Event details', fields: eventFields },
];

export function BookingFields({ errors }) {
  return sections.map(({ legend, fields }) => (
    <fieldset key={legend}>
      <legend>{legend}</legend>
      <div className="fields">
        {fields.map((field) => (
          <Field key={field.name} {...field} errors={errors?.[field.name]} />
        ))}
      </div>
    </fieldset>
  ));
}
// VA
