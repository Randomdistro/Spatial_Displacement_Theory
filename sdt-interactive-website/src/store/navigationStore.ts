import { create } from 'zustand';

export type PathType = 'path1' | 'path2' | 'path3' | null;
export type NavigationState = 'landing' | 'path' | 'node';

interface NavigationStore {
  currentPath: PathType;
  currentState: NavigationState;
  currentNode: string | null;
  selectedPath: PathType;
  
  // Actions
  selectPath: (path: PathType) => void;
  navigateToNode: (nodeId: string) => void;
  returnToLanding: () => void;
  returnToPath: () => void;
}

export const useNavigationStore = create<NavigationStore>((set) => ({
  currentPath: null,
  currentState: 'landing',
  currentNode: null,
  selectedPath: null,
  
  selectPath: (path) => set({ 
    selectedPath: path,
    currentPath: path,
    currentState: 'path' 
  }),
  
  navigateToNode: (nodeId) => set({ 
    currentNode: nodeId,
    currentState: 'node' 
  }),
  
  returnToLanding: () => set({ 
    currentPath: null,
    currentState: 'landing',
    currentNode: null,
    selectedPath: null
  }),
  
  returnToPath: () => set({ 
    currentNode: null,
    currentState: 'path' 
  }),
}));





