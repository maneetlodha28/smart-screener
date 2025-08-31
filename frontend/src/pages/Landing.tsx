import React, { useState } from 'react';
import ResultCard from '../components/ResultCard';
import { postRecommend, postScreen } from '../api/client';
import type {
  Goal,
  RecommendRequest,
  RiskProfile,
  ScreenResponse,
} from '../types/models';

const examplePrompts = [
  'I want safe income for 5 years with 10k SIP',
  'Aggressive growth with 1 lakh budget',
];

const Landing: React.FC = () => {
  const [prompt, setPrompt] = useState('');
  const [budget, setBudget] = useState('');
  const [horizon, setHorizon] = useState('');
  const [risk, setRisk] = useState<RiskProfile>('balanced');
  const [goal, setGoal] = useState<Goal>('growth');
  const [errors, setErrors] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [result, setResult] = useState<ScreenResponse | null>(null);
  const disclaimer = result?.disclaimer;
  const portfolioMsg = result?.explanations.portfolio;

  const handleExample = (text: string) => {
    setPrompt(text);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const errs: string[] = [];
    const trimmedPrompt = prompt.trim();
    const hasPrompt = trimmedPrompt.length > 0;
    const budgetNum = Number(budget);
    const horizonNum = Number(horizon);
    if (hasPrompt) {
      if (budget !== '' && (!budgetNum || budgetNum <= 0)) {
        errs.push('Budget must be greater than 0');
      }
      if (
        horizon !== '' &&
        (!horizonNum || horizonNum < 1 || horizonNum > 10)
      ) {
        errs.push('Horizon must be between 1 and 10 years');
      }
    } else {
      if (!budgetNum || budgetNum <= 0) {
        errs.push('Budget must be greater than 0');
      }
      if (!horizonNum || horizonNum < 1 || horizonNum > 10) {
        errs.push('Horizon must be between 1 and 10 years');
      }
    }
    setErrors(errs);
    if (errs.length === 0) {
      setLoading(true);
      setApiError(null);
      setResult(null);
      try {
        let resp: ScreenResponse;
        if (hasPrompt) {
          const req: RecommendRequest = { text: trimmedPrompt };
          if (budget !== '') req.budget_inr = budgetNum;
          if (horizon !== '') req.horizon_years = horizonNum;
          req.risk_profile = risk;
          req.goal = goal;
          resp = await postRecommend(req);
        } else {
          resp = await postScreen({
            budget_inr: budgetNum,
            horizon_years: horizonNum,
            risk_profile: risk,
            goal,
          });
        }
        setResult(resp);
      } catch {
        setApiError('Failed to fetch results');
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div>
      <h2>Describe your investment goals</h2>
      <textarea
        aria-label="prompt"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <div>
        {examplePrompts.map((ex) => (
          <button key={ex} type="button" onClick={() => handleExample(ex)}>
            {ex}
          </button>
        ))}
      </div>
      <form onSubmit={handleSubmit} noValidate>
        <div>
          <label htmlFor="budget">Budget (INR)</label>
          <input
            id="budget"
            aria-label="budget"
            type="number"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="horizon">Horizon (years)</label>
          <input
            id="horizon"
            aria-label="horizon"
            type="number"
            value={horizon}
            onChange={(e) => setHorizon(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="risk">Risk Profile</label>
          <select
            id="risk"
            aria-label="risk"
            value={risk}
            onChange={(e) => setRisk(e.target.value as RiskProfile)}
          >
            <option value="safe">Safe</option>
            <option value="balanced">Balanced</option>
            <option value="aggressive">Aggressive</option>
          </select>
        </div>
        <div>
          <label htmlFor="goal">Goal</label>
          <select
            id="goal"
            aria-label="goal"
            value={goal}
            onChange={(e) => setGoal(e.target.value as Goal)}
          >
            <option value="income">Income</option>
            <option value="growth">Growth</option>
          </select>
        </div>
        {errors.length > 0 && (
          <ul>
            {errors.map((err) => (
              <li key={err}>{err}</li>
            ))}
          </ul>
        )}
        <button type="submit">Submit</button>
      </form>
      {loading && (
        <div>
          {[0, 1, 2].map((i) => (
            <ResultCard key={i} loading />
          ))}
        </div>
      )}
      {apiError && (
        <p role="alert">{apiError}</p>
      )}
      {result && (
        <div>
          {portfolioMsg && <p>{portfolioMsg}</p>}
          {result.instruments.map((instrument) => {
            const allocation = result.allocations.find(
              (a) => a.symbol === instrument.symbol,
            );
            const explanation =
              result.explanations.instruments[instrument.symbol];
            return (
              <ResultCard
                key={instrument.symbol}
                instrument={instrument}
                allocation={allocation}
                explanation={explanation}
              />
            );
          })}
          {disclaimer && <p>{disclaimer}</p>}
        </div>
      )}
    </div>
  );
};

export default Landing;
