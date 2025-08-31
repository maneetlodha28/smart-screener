import React from 'react';
import { render, screen } from '@testing-library/react';
import { rest } from 'msw';
import HealthCheck from '../components/HealthCheck';
import { server } from '../mocks/server';

describe('HealthCheck', () => {
  it('renders backend status', async () => {
    server.use(
      rest.get('/health', (_req, res, ctx) => {
        return res(ctx.json({ status: 'ok' }));
      })
    );

    render(<HealthCheck />);
    expect(await screen.findByText(/Backend: ok/i)).toBeInTheDocument();
  });

  it('handles error', async () => {
    server.use(
      rest.get('/health', (_req, res) => {
        return res.networkError('failed');
      })
    );

    render(<HealthCheck />);
    expect(await screen.findByText(/Backend: error/i)).toBeInTheDocument();
  });
});
