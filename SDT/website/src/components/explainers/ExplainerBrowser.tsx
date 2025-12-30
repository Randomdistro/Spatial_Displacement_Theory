/**
 * Explainer Browser Component
 * Browse, search, and filter all explainers
 */

import React, { useState, useEffect } from 'react';
import { useExplainerRegistry } from './ExplainerRegistry';
import { searchExplainers } from '../../utils/explainer-loader';
import CrossReferenceGraph from './CrossReferenceGraph';
import type { ExplainerFilter, ExplainerSearchResult } from '../../types/explainers';

export default function ExplainerBrowser() {
  const { registry } = useExplainerRegistry();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<ExplainerSearchResult[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [showGraph, setShowGraph] = useState(false);
  const [selectedExplainer, setSelectedExplainer] = useState<string | null>(null);

  // Perform search
  useEffect(() => {
    if (searchQuery.trim() === '') {
      setSearchResults([]);
      return;
    }

    const filter: ExplainerFilter = {
      searchQuery,
    };

    if (selectedCategory !== 'all') {
      filter.categories = [selectedCategory as any];
    }

    if (selectedDomain !== 'all') {
      filter.domains = [selectedDomain as any];
    }

    searchExplainers(searchQuery, filter).then(results => {
      setSearchResults(results);
    });
  }, [searchQuery, selectedCategory, selectedDomain]);

  const handleExplainerClick = (id: string) => {
    window.location.href = `/explainers/${id}`;
  };

  return (
    <div className="min-h-screen bg-slate-900 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">SDT Visual Explainers</h1>
          <p className="text-slate-300 text-lg">
            Interactive visual explainers for every paper, phase, benchmark, formula, and concept in SDT
          </p>
        </div>

        {/* Search and Filters */}
        <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-6 mb-6">
          <div className="flex flex-col sm:flex-row gap-4 mb-4">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search explainers..."
              className="flex-1 px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-blue-500 focus:outline-none"
            />
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-blue-500 focus:outline-none"
            >
              <option value="all">All Categories</option>
              <option value="paper">Papers</option>
              <option value="phase">Phases</option>
              <option value="benchmark">Benchmarks</option>
              <option value="formula">Formulas</option>
              <option value="rule">Rules</option>
              <option value="element">Elements</option>
            </select>
            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-blue-500 focus:outline-none"
            >
              <option value="all">All Domains</option>
              <option value="foundational">Foundational</option>
              <option value="atomic">Atomic</option>
              <option value="electromagnetic">Electromagnetic</option>
              <option value="gravitational">Gravitational</option>
              <option value="cosmological">Cosmological</option>
              <option value="thermodynamic">Thermodynamic</option>
              <option value="chemistry">Chemistry</option>
              <option value="nuclear">Nuclear</option>
              <option value="universal">Universal</option>
            </select>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => setShowGraph(!showGraph)}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              {showGraph ? 'Hide' : 'Show'} Reference Graph
            </button>
          </div>
        </div>

        {/* Reference Graph */}
        {showGraph && (
          <div className="mb-6">
            <CrossReferenceGraph
              selectedId={selectedExplainer}
              onNodeClick={(id) => {
                setSelectedExplainer(id);
                handleExplainerClick(id);
              }}
              width={800}
              height={600}
            />
          </div>
        )}

        {/* Search Results */}
        {searchQuery && (
          <div className="mb-6">
            <h2 className="text-2xl font-semibold text-white mb-4">
              Search Results ({searchResults.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchResults.map(result => (
                <button
                  key={result.id}
                  onClick={() => handleExplainerClick(result.id)}
                  className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 text-left hover:border-blue-500 transition-colors"
                >
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs capitalize">
                      {result.category}
                    </span>
                    <span className="px-2 py-1 bg-slate-700 text-slate-300 rounded text-xs capitalize">
                      {result.domain}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-1">{result.title}</h3>
                  <p className="text-sm text-slate-400 line-clamp-2">{result.description}</p>
                  <div className="mt-2 text-xs text-slate-500">
                    Relevance: {result.relevanceScore.toFixed(1)}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* All Explainers (when no search) */}
        {!searchQuery && (
          <div>
            <h2 className="text-2xl font-semibold text-white mb-4">All Explainers</h2>
            <div className="text-slate-400">
              <p>Use the search bar above to find specific explainers.</p>
              <p className="mt-2">
                Currently loaded: {Array.from(registry.keys()).length} explainers
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

