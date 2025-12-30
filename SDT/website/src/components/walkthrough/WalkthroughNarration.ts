/**
 * Walkthrough Narration Script
 * Complete narration for the 43-order-of-magnitude journey
 */

import { NarrationScript } from './NarrationSystem';

export const WALKTHROUGH_NARRATION: NarrationScript = {
  segments: [
    {
      time: 0,
      text: "Welcome to Spatial Displacement Theory. We begin at the smallest scales, where space itself is a pressurized medium.",
      highlight: "pressurized medium",
      formula: "K_bulk"
    },
    {
      time: 5,
      text: "At the Planck scale, we find the spation lattice—the fundamental structure of space.",
      highlight: "spation lattice",
      formula: "K_bulk"
    },
    {
      time: 12,
      text: "Moving to atomic scales, we see how pressure balance creates stable electron orbits.",
      highlight: "pressure balance",
      formula: "k-law"
    },
    {
      time: 20,
      text: "The same principle works at all scales—from atoms to galaxies.",
      highlight: "all scales",
      formula: "k-law"
    }
  ],
  totalDuration: 30
};

