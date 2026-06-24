import { getThemeSummaries, getActualReviews } from '@/lib/data';
import DashboardClient from '@/components/DashboardClient';
import Sidebar from '@/components/Sidebar';

export default function Home() {
  const themes = getThemeSummaries();
  const reviews = getActualReviews();

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar />
      <main className="flex-1 ml-20 md:ml-24 p-8 md:p-12 overflow-y-auto">
        <DashboardClient themes={themes} reviews={reviews} />
      </main>
    </div>
  );
}
