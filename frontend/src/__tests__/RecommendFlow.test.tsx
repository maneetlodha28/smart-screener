import { fireEvent, render, screen } from '@testing-library/react';
import { rest } from 'msw';
import React from 'react';
import { server } from '../mocks/server';
import Landing from '../pages/Landing';

describe('Recommend flow', () => {
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

  test('uses /recommend when prompt provided and applies overrides', async () => {
    let received: any = null;
    server.use(
      rest.post('/recommend', async (req, res, ctx) => {
        received = await req.json();
        return res(ctx.json(mockResponse));
      }),
    );

    render(<Landing />);
    fireEvent.change(screen.getByLabelText('prompt'), {
      target: { value: 'Invest safely' },
    });
    fireEvent.change(screen.getByLabelText('budget'), {
      target: { value: '10000' },
    });
    fireEvent.change(screen.getByLabelText('horizon'), {
      target: { value: '5' },
    });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    expect(await screen.findByText(/Reliance/)).toBeInTheDocument();
    expect(
      screen.getByText(/not investment advice/i),
    ).toBeInTheDocument();
    expect(received).toMatchObject({
      text: 'Invest safely',
      budget_inr: 10000,
      horizon_years: 5,
    });
  });
});

