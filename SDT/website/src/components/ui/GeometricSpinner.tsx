/**
 * Creative Agent: Geometric Spinner
 * 
 * TEKNE: Loading IS transformation
 * 
 * A beautiful loading indicator using sacred geometry:
 * - Nested golden ratio circles
 * - Fibonacci-timed rotation
 * - Organic pulsing animation
 * 
 * The beauty of geometry, the simplicity of geometry,
 * the precision of geometry - in a loading state.
 */

import React from 'react';
import { PHI, PHI_INVERSE } from '../../utils/sacred-geometry';

export interface GeometricSpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  message?: string;
  fullScreen?: boolean;
  variant?: 'rings' | 'flower' | 'spiral';
}

// Size configurations
const SIZES = {
  sm: { container: 32, stroke: 1.5 },
  md: { container: 48, stroke: 2 },
  lg: { container: 64, stroke: 2.5 },
  xl: { container: 96, stroke: 3 },
};

/**
 * GeometricSpinner - Sacred geometry loading animation
 * 
 * Variants:
 * - rings: Nested golden ratio circles
 * - flower: Seed of Life pattern
 * - spiral: Golden spiral
 */
export default function GeometricSpinner({
  size = 'md',
  message,
  fullScreen = false,
  variant = 'rings',
}: GeometricSpinnerProps) {
  const { container, stroke } = SIZES[size];
  const center = container / 2;
  
  // Golden ratio radii
  const radii = [
    center * 0.3,           // Inner
    center * 0.3 * PHI,     // Middle (0.3 * 1.618 = 0.485)
    center * 0.3 * PHI * PHI, // Outer (0.3 * 2.618 = 0.785)
  ];

  const containerClasses = fullScreen
    ? 'fixed inset-0 bg-slate-900/95 backdrop-blur-md z-50 flex flex-col items-center justify-center'
    : 'flex flex-col items-center justify-center p-8';

  return (
    <div className={containerClasses}>
      <div 
        className="relative"
        style={{ width: container, height: container }}
      >
        {variant === 'rings' && (
          <svg 
            viewBox={`0 0 ${container} ${container}`}
            className="w-full h-full"
          >
            {/* Outer ring - slowest rotation */}
            <circle
              cx={center}
              cy={center}
              r={radii[2]}
              fill="none"
              stroke="url(#gold-gradient)"
              strokeWidth={stroke}
              strokeLinecap="round"
              strokeDasharray={`${radii[2] * Math.PI * 0.4} ${radii[2] * Math.PI * 0.6}`}
              className="origin-center"
              style={{
                animation: `spin-slow ${PHI * 3}s linear infinite`,
              }}
            />
            
            {/* Middle ring - medium rotation */}
            <circle
              cx={center}
              cy={center}
              r={radii[1]}
              fill="none"
              stroke="url(#blue-gradient)"
              strokeWidth={stroke}
              strokeLinecap="round"
              strokeDasharray={`${radii[1] * Math.PI * 0.5} ${radii[1] * Math.PI * 0.5}`}
              className="origin-center"
              style={{
                animation: `spin-medium ${PHI * 2}s linear infinite reverse`,
              }}
            />
            
            {/* Inner ring - fastest rotation */}
            <circle
              cx={center}
              cy={center}
              r={radii[0]}
              fill="none"
              stroke="url(#gold-gradient)"
              strokeWidth={stroke * 1.5}
              strokeLinecap="round"
              strokeDasharray={`${radii[0] * Math.PI * 0.3} ${radii[0] * Math.PI * 0.7}`}
              className="origin-center"
              style={{
                animation: `spin-fast ${PHI}s linear infinite`,
              }}
            />
            
            {/* Center dot - pulsing */}
            <circle
              cx={center}
              cy={center}
              r={stroke * 2}
              fill="#d69e2e"
              style={{
                animation: `pulse-golden ${PHI * 1.5}s ease-in-out infinite`,
              }}
            />
            
            {/* Gradients */}
            <defs>
              <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#d69e2e" />
                <stop offset="50%" stopColor="#f6ad55" />
                <stop offset="100%" stopColor="#fbbf24" />
              </linearGradient>
              <linearGradient id="blue-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#1a365d" />
                <stop offset="50%" stopColor="#2d5a87" />
                <stop offset="100%" stopColor="#4299e1" />
              </linearGradient>
            </defs>
          </svg>
        )}

        {variant === 'flower' && (
          <svg 
            viewBox={`0 0 ${container} ${container}`}
            className="w-full h-full"
          >
            {/* Seed of Life - 7 overlapping circles */}
            {[0, 1, 2, 3, 4, 5].map((i) => {
              const angle = (i * Math.PI) / 3;
              const r = center * 0.25;
              const cx = center + Math.cos(angle) * r;
              const cy = center + Math.sin(angle) * r;
              
              return (
                <circle
                  key={i}
                  cx={cx}
                  cy={cy}
                  r={r}
                  fill="none"
                  stroke="url(#gold-gradient)"
                  strokeWidth={stroke}
                  opacity={0.8}
                  style={{
                    animation: `pulse-stagger ${PHI * 2}s ease-in-out infinite`,
                    animationDelay: `${i * PHI_INVERSE * 0.3}s`,
                  }}
                />
              );
            })}
            
            {/* Center circle */}
            <circle
              cx={center}
              cy={center}
              r={center * 0.25}
              fill="none"
              stroke="url(#blue-gradient)"
              strokeWidth={stroke * 1.5}
              style={{
                animation: `pulse-golden ${PHI}s ease-in-out infinite`,
              }}
            />
            
            {/* Outer rotating ring */}
            <circle
              cx={center}
              cy={center}
              r={center * 0.5}
              fill="none"
              stroke="url(#gold-gradient)"
              strokeWidth={stroke * 0.5}
              strokeDasharray={`${center * 0.5 * Math.PI * 0.1} ${center * 0.5 * Math.PI * 0.15}`}
              style={{
                animation: `spin-slow ${PHI * 4}s linear infinite`,
                transformOrigin: 'center',
              }}
            />
            
            <defs>
              <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#d69e2e" />
                <stop offset="100%" stopColor="#fbbf24" />
              </linearGradient>
              <linearGradient id="blue-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#2d5a87" />
                <stop offset="100%" stopColor="#4299e1" />
              </linearGradient>
            </defs>
          </svg>
        )}

        {variant === 'spiral' && (
          <svg 
            viewBox={`0 0 ${container} ${container}`}
            className="w-full h-full"
            style={{
              animation: `spin-slow ${PHI * 5}s linear infinite`,
            }}
          >
            {/* Golden spiral approximation using arcs */}
            {[0, 1, 2, 3, 4].map((i) => {
              const r = center * 0.1 * Math.pow(PHI, i);
              const startAngle = i * Math.PI / 2;
              const endAngle = startAngle + Math.PI / 2;
              
              // Calculate arc points
              const x1 = center + r * Math.cos(startAngle);
              const y1 = center + r * Math.sin(startAngle);
              const x2 = center + r * Math.cos(endAngle);
              const y2 = center + r * Math.sin(endAngle);
              
              return (
                <path
                  key={i}
                  d={`M ${x1} ${y1} A ${r} ${r} 0 0 1 ${x2} ${y2}`}
                  fill="none"
                  stroke="url(#gold-gradient)"
                  strokeWidth={stroke * (1 + i * 0.2)}
                  strokeLinecap="round"
                  opacity={0.6 + i * 0.08}
                />
              );
            })}
            
            {/* Center point */}
            <circle
              cx={center}
              cy={center}
              r={stroke * 2}
              fill="#d69e2e"
            />
            
            <defs>
              <linearGradient id="gold-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#d69e2e" />
                <stop offset="100%" stopColor="#fbbf24" />
              </linearGradient>
            </defs>
          </svg>
        )}
      </div>

      {message && (
        <p className="mt-4 text-slate-300 text-sm font-medium tracking-wide">
          {message}
        </p>
      )}

      {/* CSS Animations */}
      <style>{`
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes spin-medium {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes spin-fast {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        
        @keyframes pulse-golden {
          0%, 100% { 
            opacity: 1; 
            transform: scale(1);
          }
          50% { 
            opacity: 0.7; 
            transform: scale(${PHI_INVERSE});
          }
        }
        
        @keyframes pulse-stagger {
          0%, 100% { 
            opacity: 0.8; 
            stroke-width: ${stroke}px;
          }
          50% { 
            opacity: 1; 
            stroke-width: ${stroke * 1.5}px;
          }
        }
      `}</style>
    </div>
  );
}

