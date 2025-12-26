/**
 * Narration System
 * Synchronized narration with visual content
 * Supports Web Speech API and pre-recorded audio
 */

export interface NarrationSegment {
  time: number; // Start time in seconds
  text: string;
  highlight?: string; // Text to highlight
  formula?: string; // Formula to display
  visualCue?: string; // Visual action to trigger
}

export interface NarrationScript {
  segments: NarrationSegment[];
  totalDuration: number;
}

export class NarrationSystem {
  private synth: SpeechSynthesis | null = null;
  private currentUtterance: SpeechSynthesisUtterance | null = null;
  private isPlaying: boolean = false;
  private currentSegmentIndex: number = 0;
  private script: NarrationScript | null = null;
  private onSegmentChangeCallbacks: Array<(segment: NarrationSegment) => void> = [];
  private speed: number = 1.0;
  private volume: number = 1.0;

  constructor() {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      this.synth = window.speechSynthesis;
    }
  }

  loadScript(script: NarrationScript): void {
    this.script = script;
    this.currentSegmentIndex = 0;
  }

  play(): void {
    if (!this.script || !this.synth) return;
    
    this.isPlaying = true;
    this.playSegment(0);
  }

  pause(): void {
    if (this.currentUtterance && this.synth) {
      this.synth.pause();
      this.isPlaying = false;
    }
  }

  resume(): void {
    if (this.currentUtterance && this.synth) {
      this.synth.resume();
      this.isPlaying = true;
    }
  }

  stop(): void {
    if (this.currentUtterance && this.synth) {
      this.synth.cancel();
      this.isPlaying = false;
      this.currentSegmentIndex = 0;
    }
  }

  setSpeed(speed: number): void {
    this.speed = Math.max(0.5, Math.min(2.0, speed));
    if (this.currentUtterance) {
      this.currentUtterance.rate = this.speed;
    }
  }

  setVolume(volume: number): void {
    this.volume = Math.max(0, Math.min(1, volume));
    if (this.currentUtterance) {
      this.currentUtterance.volume = this.volume;
    }
  }

  private playSegment(index: number): void {
    if (!this.script || index >= this.script.segments.length) {
      this.isPlaying = false;
      return;
    }

    const segment = this.script.segments[index];
    this.currentSegmentIndex = index;

    // Notify segment change
    this.onSegmentChangeCallbacks.forEach(cb => cb(segment));

    // Create utterance
    const utterance = new SpeechSynthesisUtterance(segment.text);
    utterance.rate = this.speed;
    utterance.volume = this.volume;
    utterance.pitch = 1.0;
    
    // Use a high-quality voice if available
    const voices = this.synth?.getVoices() || [];
    const preferredVoice = voices.find(v => 
      v.name.includes('Google') || v.name.includes('Microsoft') || v.lang.startsWith('en')
    );
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    utterance.onend = () => {
      // Move to next segment
      setTimeout(() => {
        if (this.isPlaying) {
          this.playSegment(index + 1);
        }
      }, 200); // Small pause between segments
    };

    utterance.onerror = (error) => {
      console.error('Narration error:', error);
      // Continue to next segment on error
      if (this.isPlaying) {
        this.playSegment(index + 1);
      }
    };

    this.currentUtterance = utterance;
    this.synth?.speak(utterance);
  }

  onSegmentChange(callback: (segment: NarrationSegment) => void): () => void {
    this.onSegmentChangeCallbacks.push(callback);
    return () => {
      const index = this.onSegmentChangeCallbacks.indexOf(callback);
      if (index > -1) {
        this.onSegmentChangeCallbacks.splice(index, 1);
      }
    };
  }

  getCurrentSegment(): NarrationSegment | null {
    if (!this.script) return null;
    return this.script.segments[this.currentSegmentIndex] || null;
  }

  getProgress(): number {
    if (!this.script) return 0;
    return this.currentSegmentIndex / this.script.segments.length;
  }

  isCurrentlyPlaying(): boolean {
    return this.isPlaying;
  }
}

// Narration scripts are now in separate files
// See WalkthroughNarration.ts for the comprehensive 10-minute script

