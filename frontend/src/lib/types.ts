export interface ActionIdea {
  idea: string;
  team: string;
}

export interface ThemeSummary {
  cluster_id: number;
  size: number;
  avg_rating: number;
  theme_name: string;
  description: string;
  quotes: string[];
  action_ideas: ActionIdea[];
}

export interface Review {
  rating: number;
  text: string;
  thumbs_up: number;
  app_version: string;
  date?: string;
  cluster_id?: number;
}
