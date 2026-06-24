"use client";

import { Home, Compass, Settings, Activity } from 'lucide-react';
import Link from 'next/link';
import clsx from 'clsx';
import { useState, useEffect } from 'react';

export default function Sidebar() {
  const [activeHash, setActiveHash] = useState('');

  // Update active hash based on window location
  useEffect(() => {
    setActiveHash(window.location.hash);
    const handleHashChange = () => setActiveHash(window.location.hash);
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const navItems = [
    { name: 'Dashboard', href: '#', icon: Home, hash: '' },
    { name: 'Explorer', href: '#explorer', icon: Compass, hash: '#explorer' },
  ];

  return (
    <aside className="fixed inset-y-0 left-0 w-20 md:w-24 flex flex-col items-center py-6 bg-surface-container-lowest border-r border-white/5 z-50 overflow-y-auto">
      <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center mb-10 neon-glow shrink-0">
        <Activity className="w-7 h-7 text-primary" />
      </div>

      <nav className="flex-1 flex flex-col gap-4 w-full px-3">
        {navItems.map((item) => {
          const isActive = activeHash === item.hash || (activeHash === '' && item.hash === '');
          const Icon = item.icon;
          return (
            <a
              key={item.name}
              href={item.href}
              onClick={(e) => {
                if (item.href.startsWith('#')) {
                  e.preventDefault();
                  const targetId = item.href.substring(1);
                  if (targetId) {
                    document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth' });
                    window.history.pushState(null, '', item.href);
                    setActiveHash(item.href);
                  } else {
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                    window.history.pushState(null, '', window.location.pathname);
                    setActiveHash('');
                  }
                }
              }}
              className={clsx(
                "flex flex-col items-center justify-center gap-1.5 p-3 rounded-xl transition-all duration-300",
                isActive 
                  ? "bg-primary/10 text-primary shadow-[inset_0_1px_1px_rgba(255,255,255,0.1)]" 
                  : "text-on-surface-variant hover:text-on-surface hover:bg-white/5"
              )}
            >
              <Icon className="w-6 h-6" strokeWidth={isActive ? 2.5 : 2} />
              <span className="text-[10px] font-semibold uppercase tracking-wider">{item.name}</span>
            </a>
          );
        })}
      </nav>
    </aside>
  );
}
