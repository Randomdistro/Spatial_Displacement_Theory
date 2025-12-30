/**
 * Architect Designer Agent: Keyboard Shortcuts Helper
 * Shows available keyboard shortcuts for power users
 */

import React, { useState, useEffect } from 'react';

const SHORTCUTS = [
  { key: 'Esc', action: 'Close/Go back' },
  { key: '←', action: 'Previous node' },
  { key: '→', action: 'Next node' },
  { key: 'Space', action: 'Play/Pause narration' },
];

export default function KeyboardShortcuts() {
  const [showHelp, setShowHelp] = useState(false);
  const [isVisible, setIsVisible] = useState(true);

  // Hide after 5 seconds, show on hover
  useEffect(() => {
    const timer = setTimeout(() => setIsVisible(false), 5000);
    return () => clearTimeout(timer);
  }, []);

  if (!isVisible && !showHelp) {
    return (
      <button
        onClick={() => setShowHelp(true)}
        onMouseEnter={() => setIsVisible(true)}
        className="fixed bottom-4 right-4 z-30 bg-black/60 backdrop-blur-md text-slate-400 hover:text-white px-3 py-2 rounded-lg border border-slate-700/50 text-xs transition-all"
        title="Show keyboard shortcuts"
      >
        ⌨️
      </button>
    );
  }

  return (
    <div
      className="fixed bottom-4 right-4 z-30 bg-black/80 backdrop-blur-md rounded-lg border border-slate-700/50 p-4 text-xs max-w-xs"
      onMouseLeave={() => !showHelp && setIsVisible(false)}
    >
      <div className="flex items-center justify-between mb-3">
        <span className="text-white font-semibold">Keyboard Shortcuts</span>
        <button
          onClick={() => {
            setShowHelp(false);
            setIsVisible(false);
          }}
          className="text-slate-400 hover:text-white"
        >
          ×
        </button>
      </div>
      <div className="space-y-2">
        {SHORTCUTS.map((shortcut) => (
          <div key={shortcut.key} className="flex items-center justify-between">
            <kbd className="px-2 py-1 bg-slate-700 rounded text-slate-300 font-mono">
              {shortcut.key}
            </kbd>
            <span className="text-slate-400 ml-4">{shortcut.action}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

