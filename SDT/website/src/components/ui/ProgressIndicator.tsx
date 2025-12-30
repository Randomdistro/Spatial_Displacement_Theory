/**
 * Architect Designer Agent: Progress Indicator
 * Shows user progress through current path
 */

import React from 'react';
import { useNavigationStore } from '../../store/navigationStore';
import { loadPathContent } from '../../utils/content-loader';

export default function ProgressIndicator() {
  const { currentPath, currentNode } = useNavigationStore();
  const [progress, setProgress] = React.useState(0);
  const [totalNodes, setTotalNodes] = React.useState(0);

  React.useEffect(() => {
    if (!currentPath) {
      setProgress(0);
      setTotalNodes(0);
      return;
    }

    const updateProgress = async () => {
      try {
        const nodes = await loadPathContent(currentPath);
        setTotalNodes(nodes.length);
        
        if (currentNode) {
          const currentIndex = nodes.findIndex(n => n.id === currentNode);
          if (currentIndex >= 0) {
            setProgress(((currentIndex + 1) / nodes.length) * 100);
          }
        } else {
          setProgress(0);
        }
      } catch (error) {
        console.error('Failed to load progress:', error);
      }
    };

    updateProgress();
  }, [currentPath, currentNode]);

  if (!currentPath || totalNodes === 0) {
    return null;
  }

  return (
    <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-20 bg-black/60 backdrop-blur-md rounded-full px-4 py-2 border border-slate-700/50">
      <div className="flex items-center gap-3 text-xs">
        <span className="text-slate-400 whitespace-nowrap">
          {currentNode ? `${Math.round(progress)}%` : '0%'}
        </span>
        <div className="w-32 h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-blue-500 to-sdt-gold-500 transition-all duration-500 ease-out"
            style={{ width: `${progress}%` }}
          />
        </div>
        <span className="text-slate-400 whitespace-nowrap">
          {totalNodes} nodes
        </span>
      </div>
    </div>
  );
}

