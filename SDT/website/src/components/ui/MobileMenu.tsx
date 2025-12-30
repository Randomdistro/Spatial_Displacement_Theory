/**
 * Architect Designer Agent: Mobile-Friendly Menu
 * Responsive navigation for mobile devices
 */

import React, { useState } from 'react';
import { useNavigationStore } from '../../store/navigationStore';

export default function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false);
  const { currentState, returnToLanding, returnToPath } = useNavigationStore();

  // Only show on mobile
  const [isMobile, setIsMobile] = useState(false);

  React.useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  if (!isMobile) return null;

  return (
    <>
      {/* Menu Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 right-4 z-40 bg-black/80 backdrop-blur-md p-3 rounded-lg border border-slate-700/50 text-white"
        aria-label="Menu"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          {isOpen ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          )}
        </svg>
      </button>

      {/* Menu Overlay */}
      {isOpen && (
        <div className="fixed inset-0 z-30 bg-black/90 backdrop-blur-sm">
          <div className="flex flex-col items-center justify-center h-full gap-6 p-8">
            {currentState === 'landing' && (
              <p className="text-slate-400 text-center">
                Select a path from the rings above
              </p>
            )}

            {currentState === 'path' && (
              <>
                <button
                  onClick={() => {
                    returnToLanding();
                    setIsOpen(false);
                  }}
                  className="w-full max-w-xs px-6 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                >
                  ← Back to Landing
                </button>
                <p className="text-slate-400 text-center text-sm">
                  Tap on a node to explore
                </p>
              </>
            )}

            {currentState === 'node' && (
              <>
                <button
                  onClick={() => {
                    returnToPath();
                    setIsOpen(false);
                  }}
                  className="w-full max-w-xs px-6 py-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors"
                >
                  ← Back to Path
                </button>
                <button
                  onClick={() => {
                    returnToLanding();
                    setIsOpen(false);
                  }}
                  className="w-full max-w-xs px-6 py-4 bg-slate-700 hover:bg-slate-600 text-white rounded-lg font-medium transition-colors"
                >
                  Home
                </button>
              </>
            )}

            <button
              onClick={() => setIsOpen(false)}
              className="mt-8 text-slate-400 hover:text-white transition-colors"
            >
              Close Menu
            </button>
          </div>
        </div>
      )}
    </>
  );
}

