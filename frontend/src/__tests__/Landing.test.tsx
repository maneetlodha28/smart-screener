import { fireEvent, render, screen } from '@testing-library/react';
import React from 'react';
import Landing from '../pages/Landing';

describe('Landing page', () => {
  test('shows validation errors for invalid inputs', () => {
    render(<Landing />);
    fireEvent.change(screen.getByLabelText('budget'), { target: { value: '-100' } });
    fireEvent.change(screen.getByLabelText('horizon'), { target: { value: '11' } });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(screen.getByText(/Budget must be greater than 0/)).toBeInTheDocument();
    expect(
      screen.getByText(/Horizon must be between 1 and 10 years/),
    ).toBeInTheDocument();
  });

  test('clicking example prompt populates text area', () => {
    render(<Landing />);
    const example = 'Aggressive growth with 1 lakh budget';
    fireEvent.click(screen.getByRole('button', { name: example }));
    expect(screen.getByLabelText('prompt')).toHaveValue(example);
  });
});
