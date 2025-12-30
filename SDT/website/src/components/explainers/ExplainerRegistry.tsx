/**
 * Explainer Registry Component
 * Central registry mapping every SDT concept to its visual explainer component
 * Supports multiple explainer types per concept and lazy loading
 */

import React, { createContext, useContext, useState, useEffect, useMemo } from 'react';
import type {
  ExplainerMetadata,
  ExplainerRegistryEntry,
  ExplainerCategory,
  Domain,
} from '../../types/explainers';
import { loadExplainerMetadata, loadExplainerMetadataBatch } from '../../utils/explainer-loader';

interface ExplainerRegistryContextValue {
  registry: Map<string, ExplainerRegistryEntry>;
  loading: boolean;
  error: Error | null;
  getExplainer: (id: string) => ExplainerRegistryEntry | undefined;
  loadExplainer: (id: string) => Promise<ExplainerMetadata | null>;
  preloadExplainers: (ids: string[]) => Promise<void>;
}

const ExplainerRegistryContext = createContext<ExplainerRegistryContextValue | null>(null);

export function useExplainerRegistry() {
  const context = useContext(ExplainerRegistryContext);
  if (!context) {
    throw new Error('useExplainerRegistry must be used within ExplainerRegistryProvider');
  }
  return context;
}

interface ExplainerRegistryProviderProps {
  children: React.ReactNode;
  registryPath?: string;
}

export function ExplainerRegistryProvider({
  children,
  registryPath = '/data/explainers/registry.json',
}: ExplainerRegistryProviderProps) {
  const [registry, setRegistry] = useState<Map<string, ExplainerRegistryEntry>>(new Map());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [loadedMetadata, setLoadedMetadata] = useState<Map<string, ExplainerMetadata>>(new Map());

  // Load registry on mount
  useEffect(() => {
    async function loadRegistry() {
      try {
        setLoading(true);
        const response = await fetch(registryPath);
        
        if (!response.ok) {
          throw new Error(`Failed to load registry: ${response.statusText}`);
        }

        const data = await response.json();
        const entries = new Map<string, ExplainerRegistryEntry>();

        // Build registry entries from all categories
        const allIds: string[] = [];
        Object.values(data.categories || {}).forEach((ids: any) => {
          if (Array.isArray(ids)) {
            allIds.push(...ids);
          }
        });

        // Create registry entries
        for (const id of allIds) {
          // Determine category and data path from ID
          const category = determineCategory(id, data.categories);
          const dataPath = `/data/explainers/${category}/${id}.json`;
          
          entries.set(id, {
            id,
            dataPath,
            metadata: null as any, // Will be loaded on demand
          });
        }

        setRegistry(entries);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Unknown error loading registry'));
        console.error('Error loading explainer registry:', err);
      } finally {
        setLoading(false);
      }
    }

    loadRegistry();
  }, [registryPath]);

  // Determine category from ID and registry data
  function determineCategory(
    id: string,
    categories: Record<string, string[]>
  ): ExplainerCategory {
    for (const [category, ids] of Object.entries(categories)) {
      if (ids.includes(id)) {
        return category as ExplainerCategory;
      }
    }
    // Fallback: try to infer from ID pattern
    if (id.startsWith('paper-')) return 'paper';
    if (id.startsWith('phase-')) return 'phase';
    if (id.startsWith('benchmark-') || id.startsWith('b')) return 'benchmark';
    if (id.startsWith('formula-')) return 'formula';
    if (id.startsWith('rule-')) return 'rule';
    if (/^[A-Z][a-z]?$/.test(id)) return 'element'; // Element symbols
    return 'paper'; // Default
  }

  // Get explainer entry
  const getExplainer = React.useCallback((id: string): ExplainerRegistryEntry | undefined => {
    return registry.get(id);
  }, [registry]);

  // Load explainer metadata
  const loadExplainer = React.useCallback(async (id: string): Promise<ExplainerMetadata | null> => {
    // Check if already loaded
    if (loadedMetadata.has(id)) {
      return loadedMetadata.get(id)!;
    }

    // Load from registry
    const entry = registry.get(id);
    if (!entry) {
      console.warn(`Explainer not found in registry: ${id}`);
      return null;
    }

    try {
      const metadata = await loadExplainerMetadata(id);
      if (metadata) {
        setLoadedMetadata(prev => new Map(prev).set(id, metadata));
        return metadata;
      }
    } catch (err) {
      console.error(`Error loading explainer ${id}:`, err);
    }

    return null;
  }, [registry, loadedMetadata]);

  // Preload multiple explainers
  const preloadExplainers = React.useCallback(async (ids: string[]): Promise<void> => {
    const toLoad = ids.filter(id => !loadedMetadata.has(id));
    if (toLoad.length === 0) return;

    const metadataMap = await loadExplainerMetadataBatch(toLoad);
    setLoadedMetadata(prev => {
      const next = new Map(prev);
      metadataMap.forEach((metadata, id) => {
        next.set(id, metadata);
      });
      return next;
    });
  }, [loadedMetadata]);

  const value = useMemo<ExplainerRegistryContextValue>(
    () => ({
      registry,
      loading,
      error,
      getExplainer,
      loadExplainer,
      preloadExplainers,
    }),
    [registry, loading, error, getExplainer, loadExplainer, preloadExplainers]
  );

  return (
    <ExplainerRegistryContext.Provider value={value}>
      {children}
    </ExplainerRegistryContext.Provider>
  );
}

/**
 * Hook to get explainer metadata with loading state
 */
export function useExplainer(id: string | null) {
  const { loadExplainer } = useExplainerRegistry();
  const [metadata, setMetadata] = useState<ExplainerMetadata | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!id) {
      setMetadata(null);
      return;
    }

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const data = await loadExplainer(id);
        setMetadata(data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Failed to load explainer'));
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [id, loadExplainer]);

  return { metadata, loading, error };
}

