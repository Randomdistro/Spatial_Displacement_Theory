/**
 * Architect Designer Agent: Breadcrumb Navigation
 * Clear path indication for intuitive navigation
 */

import React from 'react';
import { useNavigationStore } from '../../store/navigationStore';

export default function BreadcrumbNav() {
  const { currentState, currentPath, currentNode } = useNavigationStore();

  if (currentState === 'landing') {
    return null;
  }

  const pathNames: Record<string, string> = {
    path1: 'Quick Tour',
    path2: 'Deep Dive',
    path3: 'Scientific Framework',
  };

  return (
    <nav
      className="absolute top-4 left-1/2 -translate-x-1/2 z-20 bg-black/60 backdrop-blur-md rounded-full px-4 py-2 border border-slate-700/50"
      aria-label="Breadcrumb"
    >
      <ol className="flex items-center gap-2 text-sm">
        <li>
          <button
            onClick={() => useNavigationStore.getState().returnToLanding()}
            className="text-slate-400 hover:text-white transition-colors"
          >
            Home
          </button>
        </li>
        
        {currentPath && (
          <>
            <li className="text-slate-600">/</li>
            <li>
              <span className="text-white font-medium">
                {pathNames[currentPath] || currentPath}
              </span>
            </li>
          </>
        )}

        {currentNode && (
          <>
            <li className="text-slate-600">/</li>
            <li>
              <span className="text-slate-300 truncate max-w-[200px]">
                {currentNode.replace(`${currentPath}-`, '').replace(/-/g, ' ')}
              </span>
            </li>
          </>
        )}
      </ol>
    </nav>
  );
}

