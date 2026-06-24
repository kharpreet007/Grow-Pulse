import fs from 'fs';
import path from 'path';
import { ThemeSummary, Review } from './types';

export function getThemeSummaries(): ThemeSummary[] {
  try {
    const dataPath = path.join(process.cwd(), '../data/phase3_output.json');
    const fileContents = fs.readFileSync(dataPath, 'utf8');
    return JSON.parse(fileContents);
  } catch (error) {
    console.error('Failed to load phase3_output.json:', error);
    return [];
  }
}

export function getActualReviews(): Review[] {
  try {
    const dataPath = path.join(process.cwd(), '../data/actual_reviews.json');
    const fileContents = fs.readFileSync(dataPath, 'utf8');
    return JSON.parse(fileContents);
  } catch (error) {
    console.error('Failed to load actual_reviews.json:', error);
    return [];
  }
}
