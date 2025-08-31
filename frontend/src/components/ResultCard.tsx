import React from 'react';
import type {
  Allocation,
  InstrumentPayload,
} from '../types/models';

interface Props {
  loading?: boolean;
  instrument?: InstrumentPayload;
  allocation?: Allocation;
  explanation?: string;
}

const formatInr = (amount: number) =>
  new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount);

const ResultCard: React.FC<Props> = ({
  loading = false,
  instrument,
  allocation,
  explanation,
}) => {
  if (loading) {
    return <div data-testid="result-skeleton">Loading...</div>;
  }
  if (!instrument || !allocation) return null;
  const metric = instrument.metric;
  return (
    <div>
      <h3>
        {instrument.name} ({instrument.symbol})
      </h3>
      <p>
        {instrument.instrument_type.toUpperCase()} - {instrument.sector || 'N/A'}
      </p>
      <p>
        Allocation: {formatInr(allocation.amount_inr)} ({allocation.percent}%)
      </p>
      <ul>
        {metric.price !== undefined && metric.price !== null && (
          <li>Price: {formatInr(metric.price)}</li>
        )}
        {metric.pe !== undefined && metric.pe !== null && <li>PE: {metric.pe}</li>}
        {metric.dividend_yield !== undefined && metric.dividend_yield !== null && (
          <li>Dividend Yield: {metric.dividend_yield}%</li>
        )}
      </ul>
      {explanation && <p>{explanation}</p>}
    </div>
  );
};

export default ResultCard;
