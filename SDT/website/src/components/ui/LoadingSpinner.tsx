/**
 * Creative Agent: Enhanced Loading Spinner
 * 
 * Now uses GeometricSpinner for sacred geometry animation,
 * with fallback to simple spinner for compatibility.
 */

import React from 'react';
import GeometricSpinner from './GeometricSpinner';

export interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  message?: string;
  fullScreen?: boolean;
  variant?: 'simple' | 'geometric';
}

export default function LoadingSpinner({ 
  size = 'md', 
  message = 'Loading...',
  fullScreen = false,
  variant = 'geometric'
}: LoadingSpinnerProps) {
  // Use geometric spinner by default
  if (variant === 'geometric') {
    return (
      <GeometricSpinner
        size={size}
        message={message}
        fullScreen={fullScreen}
        variant="rings"
      />
    );
  }

  // Fallback to simple spinner
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12',
  };

  const containerClasses = fullScreen
    ? 'fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex flex-col items-center justify-center'
    : 'flex flex-col items-center justify-center p-8';

  return (
    <div className={containerClasses}>
      {/* Simple spinner */}
      <div className="relative">
        <div
          className={`${sizeClasses[size]} border-4 border-slate-700 border-t-sdt-gold-500 rounded-full animate-spin`}
        />
        <div
          className={`absolute inset-0 ${sizeClasses[size]} border-4 border-sdt-gold-500/30 rounded-full animate-ping`}
        />
      </div>
      
      {message && (
        <p className="mt-4 text-slate-300 text-sm font-medium animate-pulse">
          {message}
        </p>
      )}
    </div>
  );
}

