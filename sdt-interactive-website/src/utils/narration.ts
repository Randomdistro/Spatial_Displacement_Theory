/**
 * Narration System for SDT Interactive Website
 * 
 * Provides Veritasium-style narration with:
 * - Web Speech API synthesis (real-time)
 * - Pre-recorded audio support
 * - Synchronized text highlighting
 * - Playback controls (speed, pause, skip)
 */

// Narration state
export interface NarrationState {
  isPlaying: boolean;
  isPaused: boolean;
  currentTime: number;
  duration: number;
  speed: number;
  volume: number;
  currentSegment: number;
}

// Narration data from content
export interface NarrationData {
  script: string;
  duration: number;
  timing: number[]; // Segment timestamps in seconds
  audioFile?: string;
}

// Callbacks for narration events
export interface NarrationCallbacks {
  onStart?: () => void;
  onEnd?: () => void;
  onPause?: () => void;
  onResume?: () => void;
  onProgress?: (currentTime: number, segment: number) => void;
  onSegmentChange?: (segment: number) => void;
}

/**
 * NarrationController - Manages text-to-speech and audio narration
 */
export class NarrationController {
  private synth: SpeechSynthesis | null = null;
  private utterance: SpeechSynthesisUtterance | null = null;
  private audioElement: HTMLAudioElement | null = null;
  private state: NarrationState;
  private callbacks: NarrationCallbacks;
  private segmentTiming: number[] = [];
  private progressInterval: number | null = null;

  constructor(callbacks: NarrationCallbacks = {}) {
    this.callbacks = callbacks;
    this.state = {
      isPlaying: false,
      isPaused: false,
      currentTime: 0,
      duration: 0,
      speed: 1,
      volume: 1,
      currentSegment: 0,
    };

    // Initialize Web Speech API if available
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      this.synth = window.speechSynthesis;
    }
  }

  /**
   * Start narration with given script
   */
  async speak(data: NarrationData): Promise<void> {
    this.stop();
    this.segmentTiming = data.timing;

    // Use pre-recorded audio if available
    if (data.audioFile) {
      await this.playAudio(data.audioFile, data.duration);
      return;
    }

    // Fall back to TTS
    if (!this.synth) {
      console.warn('Speech synthesis not available');
      return;
    }

    return new Promise((resolve, reject) => {
      this.utterance = new SpeechSynthesisUtterance(data.script);
      
      // Configure voice
      this.utterance.rate = this.state.speed;
      this.utterance.volume = this.state.volume;
      this.utterance.pitch = 1;
      
      // Select a good voice (prefer English, natural-sounding)
      const voices = this.synth!.getVoices();
      const preferredVoice = voices.find(
        (v) => v.lang.startsWith('en') && v.name.includes('Natural')
      ) || voices.find(
        (v) => v.lang.startsWith('en-US')
      ) || voices[0];
      
      if (preferredVoice) {
        this.utterance.voice = preferredVoice;
      }

      // Event handlers
      this.utterance.onstart = () => {
        this.state.isPlaying = true;
        this.state.isPaused = false;
        this.state.duration = data.duration;
        this.startProgressTracking();
        this.callbacks.onStart?.();
      };

      this.utterance.onend = () => {
        this.state.isPlaying = false;
        this.stopProgressTracking();
        this.callbacks.onEnd?.();
        resolve();
      };

      this.utterance.onerror = (event) => {
        console.error('Speech synthesis error:', event.error);
        this.state.isPlaying = false;
        reject(event.error);
      };

      this.synth!.speak(this.utterance);
    });
  }

  /**
   * Play pre-recorded audio file
   */
  private async playAudio(audioFile: string, duration: number): Promise<void> {
    return new Promise((resolve, reject) => {
      this.audioElement = new Audio(audioFile);
      this.audioElement.volume = this.state.volume;
      this.audioElement.playbackRate = this.state.speed;

      this.audioElement.onloadedmetadata = () => {
        this.state.duration = this.audioElement!.duration || duration;
      };

      this.audioElement.onplay = () => {
        this.state.isPlaying = true;
        this.state.isPaused = false;
        this.startProgressTracking();
        this.callbacks.onStart?.();
      };

      this.audioElement.onended = () => {
        this.state.isPlaying = false;
        this.stopProgressTracking();
        this.callbacks.onEnd?.();
        resolve();
      };

      this.audioElement.onerror = () => {
        reject(new Error('Failed to load audio file'));
      };

      this.audioElement.play().catch(reject);
    });
  }

  /**
   * Track progress and segment changes
   */
  private startProgressTracking(): void {
    this.stopProgressTracking();
    
    this.progressInterval = window.setInterval(() => {
      let currentTime = 0;
      
      if (this.audioElement) {
        currentTime = this.audioElement.currentTime;
      } else {
        // Estimate progress for TTS (not as accurate)
        this.state.currentTime += 0.1;
        currentTime = this.state.currentTime;
      }
      
      this.state.currentTime = currentTime;
      
      // Determine current segment
      let newSegment = 0;
      for (let i = this.segmentTiming.length - 1; i >= 0; i--) {
        if (currentTime >= this.segmentTiming[i]) {
          newSegment = i;
          break;
        }
      }
      
      if (newSegment !== this.state.currentSegment) {
        this.state.currentSegment = newSegment;
        this.callbacks.onSegmentChange?.(newSegment);
      }
      
      this.callbacks.onProgress?.(currentTime, this.state.currentSegment);
    }, 100);
  }

  private stopProgressTracking(): void {
    if (this.progressInterval) {
      clearInterval(this.progressInterval);
      this.progressInterval = null;
    }
  }

  /**
   * Pause narration
   */
  pause(): void {
    if (!this.state.isPlaying) return;

    if (this.audioElement) {
      this.audioElement.pause();
    } else if (this.synth) {
      this.synth.pause();
    }

    this.state.isPaused = true;
    this.stopProgressTracking();
    this.callbacks.onPause?.();
  }

  /**
   * Resume narration
   */
  resume(): void {
    if (!this.state.isPaused) return;

    if (this.audioElement) {
      this.audioElement.play();
    } else if (this.synth) {
      this.synth.resume();
    }

    this.state.isPaused = false;
    this.startProgressTracking();
    this.callbacks.onResume?.();
  }

  /**
   * Stop narration completely
   */
  stop(): void {
    if (this.audioElement) {
      this.audioElement.pause();
      this.audioElement = null;
    }

    if (this.synth) {
      this.synth.cancel();
    }

    this.stopProgressTracking();
    this.state = {
      ...this.state,
      isPlaying: false,
      isPaused: false,
      currentTime: 0,
      currentSegment: 0,
    };
  }

  /**
   * Set playback speed
   */
  setSpeed(speed: number): void {
    this.state.speed = Math.max(0.5, Math.min(2, speed));

    if (this.audioElement) {
      this.audioElement.playbackRate = this.state.speed;
    }
    // TTS rate can only be set before speaking
  }

  /**
   * Set volume
   */
  setVolume(volume: number): void {
    this.state.volume = Math.max(0, Math.min(1, volume));

    if (this.audioElement) {
      this.audioElement.volume = this.state.volume;
    }
    if (this.utterance) {
      this.utterance.volume = this.state.volume;
    }
  }

  /**
   * Skip to segment
   */
  skipToSegment(segment: number): void {
    if (segment < 0 || segment >= this.segmentTiming.length) return;

    const targetTime = this.segmentTiming[segment];
    
    if (this.audioElement) {
      this.audioElement.currentTime = targetTime;
    }
    // TTS doesn't support seeking, would need to restart from segment

    this.state.currentTime = targetTime;
    this.state.currentSegment = segment;
    this.callbacks.onSegmentChange?.(segment);
  }

  /**
   * Get current state
   */
  getState(): NarrationState {
    return { ...this.state };
  }

  /**
   * Check if speech synthesis is available
   */
  static isAvailable(): boolean {
    return typeof window !== 'undefined' && 'speechSynthesis' in window;
  }

  /**
   * Get available voices
   */
  static getVoices(): SpeechSynthesisVoice[] {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      return window.speechSynthesis.getVoices();
    }
    return [];
  }
}

/**
 * Parse narration script into segments for highlighting
 */
export function parseNarrationScript(
  script: string,
  timing: number[]
): { text: string; startTime: number; endTime: number }[] {
  // Split script into sentences/segments
  const sentences = script.split(/(?<=[.!?])\s+/);
  const segments: { text: string; startTime: number; endTime: number }[] = [];

  sentences.forEach((sentence, index) => {
    const startTime = timing[index] || timing[timing.length - 1] || 0;
    const endTime = timing[index + 1] || startTime + 10; // Default 10 seconds per segment

    segments.push({
      text: sentence.trim(),
      startTime,
      endTime,
    });
  });

  return segments;
}

/**
 * Create highlighted text with current segment emphasized
 */
export function createHighlightedScript(
  script: string,
  timing: number[],
  currentTime: number
): { before: string; current: string; after: string } {
  const segments = parseNarrationScript(script, timing);
  
  let before = '';
  let current = '';
  let after = '';
  let foundCurrent = false;

  for (const segment of segments) {
    if (currentTime >= segment.startTime && currentTime < segment.endTime) {
      current = segment.text;
      foundCurrent = true;
    } else if (!foundCurrent) {
      before += segment.text + ' ';
    } else {
      after += segment.text + ' ';
    }
  }

  return {
    before: before.trim(),
    current: current.trim(),
    after: after.trim(),
  };
}

export default NarrationController;


