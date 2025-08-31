export type RiskProfile = 'safe' | 'balanced' | 'aggressive';
export type Goal = 'income' | 'growth';

export interface ScreenRequest {
  budget_inr: number;
  horizon_years: number;
  risk_profile: RiskProfile;
  goal: Goal;
}

export interface RecommendRequest {
  text: string;
  budget_inr?: number;
  horizon_years?: number;
  risk_profile?: RiskProfile;
  goal?: Goal;
}

export interface Allocation {
  symbol: string;
  percent: number;
  amount_inr: number;
}

export interface MetricPayload {
  as_of_date?: string;
  price?: number;
  pe?: number | null;
  roe?: number | null;
  dividend_yield?: number | null;
  debt_to_equity?: number | null;
  revenue_growth?: number | null;
  earnings_growth?: number | null;
}

export interface InstrumentPayload {
  symbol: string;
  name: string;
  instrument_type: string;
  sector?: string | null;
  metric: MetricPayload;
}

export interface ExplanationsPayload {
  portfolio: string;
  instruments: Record<string, string>;
}

export interface ScreenResponse {
  allocations: Allocation[];
  instruments: InstrumentPayload[];
  explanations: ExplanationsPayload;
  disclaimer: string;
}
