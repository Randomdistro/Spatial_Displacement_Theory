/**
 * Codemonkey Agent: Error Boundary System
 * 
 * TEKNE: Error boundaries ARE exclusion zones
 * All original implementation - handles errors gracefully
 */

import React, { Component, ErrorInfo, ReactNode } from 'react';

export interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

export interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * Error Boundary Component
 * Catches errors in component tree and displays fallback UI
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return {
      hasError: true,
      error,
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    this.setState({
      errorInfo,
    });

    // Call error handler if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // Log error (in production, send to error tracking service)
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div style={{
          padding: '2rem',
          color: '#f7fafc',
          backgroundColor: '#1a202c',
          borderRadius: '0.5rem',
          border: '1px solid #d69e2e',
        }}>
          <h2 style={{ color: '#d69e2e', marginBottom: '1rem' }}>
            Something went wrong
          </h2>
          {this.state.error && (
            <details style={{ marginTop: '1rem' }}>
              <summary style={{ cursor: 'pointer', color: '#cbd5e0' }}>
                Error Details
              </summary>
              <pre style={{
                marginTop: '0.5rem',
                padding: '1rem',
                backgroundColor: '#0a0e1a',
                borderRadius: '0.25rem',
                overflow: 'auto',
                fontSize: '0.875rem',
              }}>
                {this.state.error.toString()}
                {this.state.errorInfo?.componentStack}
              </pre>
            </details>
          )}
        </div>
      );
    }

    return this.props.children;
  }
}

/**
 * Framework Error Class
 * Custom error class with helpful context
 */
export class FrameworkError extends Error {
  constructor(
    message: string,
    public context?: {
      component?: string;
      shader?: string;
      geometry?: string;
      animation?: string;
      suggestion?: string;
      documentation?: string;
    }
  ) {
    super(message);
    this.name = 'FrameworkError';
  }

  toString(): string {
    let message = `${this.name}: ${this.message}`;
    
    if (this.context) {
      if (this.context.component) {
        message += `\nComponent: ${this.context.component}`;
      }
      if (this.context.suggestion) {
        message += `\nSuggestion: ${this.context.suggestion}`;
      }
      if (this.context.documentation) {
        message += `\nDocumentation: ${this.context.documentation}`;
      }
    }
    
    return message;
  }
}

