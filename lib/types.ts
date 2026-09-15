export type HistoryPoint = {
  generation: number;
  best: number;
  average: number;
  hard_penalty?: number;
};

export type BaseResult = {
  best_individual: unknown[];
  best_score: number;
  generation: number;
  solved: boolean;
  history: HistoryPoint[];
  metadata: Record<string, unknown>;
};

