/**
 * Architect Designer Agent: Keyboard Shortcuts Hook
 * Provides keyboard navigation for power users
 */

import { useEffect } from 'react';
import { useNavigationStore } from '../store/navigationStore';
import { narrationSystem } from '../utils/narration';

export function useKeyboardShortcuts() {
  const { currentState, currentNode, navigateToNode, returnToPath, returnToLanding } = useNavigationStore();

  useEffect(() => {
    const handleKeyPress = (event: KeyboardEvent) => {
      // Don't trigger if user is typing in an input
      if (
        event.target instanceof HTMLInputElement ||
        event.target instanceof HTMLTextAreaElement ||
        (event.target as HTMLElement).isContentEditable
      ) {
        return;
      }

      switch (event.key) {
        case 'Escape':
          if (currentState === 'node') {
            returnToPath();
          } else if (currentState === 'path') {
            returnToLanding();
          }
          break;

        case 'ArrowLeft':
          if (currentState === 'node' && currentNode) {
            // Navigate to previous node
            event.preventDefault();
            // This would need to load current node to get previousNodeId
            // For now, just go back
            returnToPath();
          }
          break;

        case 'ArrowRight':
          if (currentState === 'node' && currentNode) {
            // Navigate to next node
            event.preventDefault();
            // This would need to load current node to get nextNodeId
          }
          break;

        case ' ':
          // Spacebar: Play/pause narration
          if (narrationSystem.isPlaying) {
            narrationSystem.pause();
          } else {
            narrationSystem.resume();
          }
          event.preventDefault();
          break;
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [currentState, currentNode, navigateToNode, returnToPath, returnToLanding]);
}

