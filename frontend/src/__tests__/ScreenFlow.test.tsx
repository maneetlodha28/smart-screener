import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import React from 'react';
import { server } from '../mocks/server';
import Landing from '../pages/Landing';

describe('Screen flow', () => {
  const mockResponse = {
    allocations: [
      { symbol: 'RELIANCE.NS', percent: 60, amount_inr: 6000 },
      { symbol: 'NIFTYBEES.NS', percent: 40, amount_inr: 4000 },
    ],
    instruments: [
      {
        symbol: 'RELIANCE.NS',
        name: 'Reliance',
        instrument_type: 'stock',
        sector: 'Energy',
        metric: { price: 2500, pe: 20, dividend_yield: 1.5 },
      },
      {
        symbol: 'NIFTYBEES.NS',
        name: 'NIFTY ETF',
        instrument_type: 'etf',
        sector: null,
        metric: { price: 200, pe: null },
      },
    ],
    explanations: {
      portfolio: 'overall',
      instruments: {
        'RELIANCE.NS': 'Reliance exp',
        'NIFTYBEES.NS': 'ETF exp',
      },
    },
    disclaimer: 'This is not investment advice',
  };

  test('renders result cards on success', async () => {
    server.use(
      rest.post('/screen', (_req, res, ctx) => {
        return res(ctx.json(mockResponse));
      }),
    );

    render(<Landing />);
    fireEvent.change(screen.getByLabelText('budget'), { target: { value: '10000' } });
    fireEvent.change(screen.getByLabelText('horizon'), { target: { value: '5' } });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(await screen.findByText(/Reliance/)).toBeInTheDocument();
    expect(screen.getByText(/Allocation: ₹6,000/)).toBeInTheDocument();
    expect(screen.getByText(/PE: 20/)).toBeInTheDocument();
    expect(screen.getByText(/not investment advice/)).toBeInTheDocument();
  });

  test('shows error message on failure', async () => {
    server.use(
      rest.post('/screen', (_req, res, ctx) => res(ctx.status(500))),
    );

    render(<Landing />);
    fireEvent.change(screen.getByLabelText('budget'), { target: { value: '10000' } });
    fireEvent.change(screen.getByLabelText('horizon'), { target: { value: '5' } });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent('Failed to fetch results');
    });
  });
});
