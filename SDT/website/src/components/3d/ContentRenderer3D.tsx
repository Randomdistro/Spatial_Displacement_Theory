/**
 * Creative Agent: 3D Content Renderer
 * 
 * TEKNE: Content IS spatial, spatial IS content
 * Renders markdown content in 3D space
 * 
 * Design Philosophy:
 * - Text floats in space
 * - Markdown is parsed and rendered spatially
 * - Formulas are 3D entities
 * - Links are interactive portals
 */

import React, { useMemo } from 'react';
import { Text } from '@react-three/drei';
import { Color } from 'three';
import FormulaRenderer from '../FormulaRenderer';

export interface ContentRenderer3DProps {
  content: string;
  position: [number, number, number];
  maxWidth?: number;
  fontSize?: number;
  color?: string;
  visible?: boolean;
}

/**
 * ContentRenderer3D - Renders markdown content in 3D space
 * 
 * Features:
 * - Parses markdown
 * - Renders text in 3D
 * - Handles formulas
 * - Interactive elements
 */
export default function ContentRenderer3D({
  content,
  position,
  maxWidth = 5,
  fontSize = 0.15,
  color = '#ffffff',
  visible = true,
}: ContentRenderer3DProps) {
  // Parse markdown content
  const parsedContent = useMemo(() => {
    // Simple markdown parser for headings, paragraphs, formulas
    const lines = content.split('\n');
    const elements: Array<{ type: 'heading' | 'paragraph' | 'formula'; content: string; level?: number }> = [];
    
    let currentParagraph = '';
    
    for (const line of lines) {
      // Headings
      const headingMatch = line.match(/^(#{1,6})\s+(.+)$/);
      if (headingMatch) {
        if (currentParagraph) {
          elements.push({ type: 'paragraph', content: currentParagraph.trim() });
          currentParagraph = '';
        }
        elements.push({
          type: 'heading',
          content: headingMatch[2],
          level: headingMatch[1].length,
        });
        continue;
      }
      
      // Formulas (LaTeX)
      const formulaMatch = line.match(/\$\$(.+?)\$\$|\$(.+?)\$/);
      if (formulaMatch) {
        if (currentParagraph) {
          elements.push({ type: 'paragraph', content: currentParagraph.trim() });
          currentParagraph = '';
        }
        elements.push({
          type: 'formula',
          content: formulaMatch[1] || formulaMatch[2] || '',
        });
        continue;
      }
      
      // Regular text
      if (line.trim()) {
        currentParagraph += (currentParagraph ? ' ' : '') + line.trim();
      } else if (currentParagraph) {
        elements.push({ type: 'paragraph', content: currentParagraph.trim() });
        currentParagraph = '';
      }
    }
    
    if (currentParagraph) {
      elements.push({ type: 'paragraph', content: currentParagraph.trim() });
    }
    
    return elements;
  }, [content]);

  if (!visible) return null;

  const textColor = new Color(color);
  const headingColor = new Color(0xd69e2e); // Gold for headings

  return (
    <group position={position}>
      {parsedContent.map((element, index) => {
        const yOffset = -index * 0.3;
        const elementFontSize = element.type === 'heading' 
          ? fontSize * (1.5 - (element.level || 1) * 0.1)
          : fontSize;
        const elementColor = element.type === 'heading' ? headingColor : textColor;

        if (element.type === 'formula') {
          // Render formula in 3D space
          return (
            <group key={index} position={[0, yOffset, 0]}>
              <Text
                position={[0, 0, 0]}
                fontSize={elementFontSize * 1.2}
                color={headingColor.getHex()}
                anchorX="center"
                anchorY="middle"
                maxWidth={maxWidth}
              >
                {element.content}
              </Text>
            </group>
          );
        }

        return (
          <Text
            key={index}
            position={[0, yOffset, 0]}
            fontSize={elementFontSize}
            color={elementColor.getHex()}
            anchorX="center"
            anchorY="top"
            maxWidth={maxWidth}
            textAlign="center"
          >
            {element.content}
          </Text>
        );
      })}
    </group>
  );
}

