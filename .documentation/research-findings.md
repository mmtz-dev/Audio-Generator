# Audio Generator — Research Findings

Project goal: Generate audio — including voice cloning, music, sound effects, foley, and environmental audio — using open-source, locally-runnable tools.

---

## Music Generation

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **ACE-Step 1.5** | Full songs up to 10 min, Mac/AMD/Intel support, <4 GB VRAM | MIT |
| **DiffRhythm** | Vocals + instruments in one pass, ~10 sec generation | Apache 2.0 |
| **MusicGen / AudioCraft** (Meta) | Text + melodic conditioning, well-documented | MIT |
| **YuE / HeartMuLa** | Open-source Suno alternative, runs fully offline | Open |

---

## Text-to-Speech (TTS)

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **Kokoro TTS** | 82M params, runs CPU-only, OpenAI-compatible API | Apache 2.0 |
| **Fish Speech V1.5** | Best multilingual benchmarks | Open |
| **CosyVoice2-0.5B** | ~150 ms streaming latency, conversational use | Open |
| **Chatterbox Turbo** | Clone voice in 5 sec, supports `[laugh]`/`[cough]` tags | MIT |
| **Bark** (Suno) | Laughter, sighs, non-speech sounds built-in | MIT |
| **Coqui XTTS-v2** | 6-sec clip cloning, 17 languages | Non-commercial |

---

## Voice Cloning & Conversion

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **RVC** | Real-time speech-to-speech, popular for AI vocal covers | MIT |
| **GPT-SoVITS** | Train a voice from just 1 minute of audio | MIT |
| **OpenVoice** | Cross-lingual voice style cloning | MIT |
| **Voicebox** | Polished local-first desktop app, 23 languages | Open |

---

## Sound Effects & General Audio

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **Stable Audio Open 1.0** (Stability AI) | Up to 47s SFX/foley/ambient, fine-tunable on custom audio | Open |
| **AudioGen** (Meta AudioCraft) | Text-to-environmental sounds, part of AudioCraft suite | MIT |
| **AudioLDM 2** | Text-to-audio for speech, SFX, and music; style transfer & inpainting | Open |
| **Tango 2** | Text-to-audio with DPO alignment, strong on animal/nature/human sounds | Open |

---

## Foley & Video-Synced Audio

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **HunyuanVideo-Foley** (Tencent) | 48 kHz foley synced to video, SOTA fidelity & alignment | Open |
| **FoleyCrafter** (OpenMMLab) | Video-to-audio with onset-based temporal sync, text-controllable | Open |

---

## Unified Audio Toolkit

| Tool | Standout Feature | License |
|------|-----------------|---------|
| **Amphion** (OpenMMLab) | Single framework for TTS, text-to-audio, singing voice conversion | MIT |

---

## All-in-One

- **TTS-WebUI** — Single Gradio/React UI bundling MusicGen, RVC, Demucs, Stable Audio, and many TTS engines in one local app.

---

## Key Trends

- Most serious tools require a GPU (NVIDIA CUDA preferred, but Mac MPS and AMD ROCm support is growing).
- **Kokoro TTS** is the go-to if you need CPU-only.
- **RVC + GPT-SoVITS** dominate the voice cloning community.
- **ACE-Step** and **DiffRhythm** are the cutting-edge music generation picks for local use.
- **Tango 2** and **Stable Audio Open** are the top picks for local sound effect generation.
- **HunyuanVideo-Foley** leads for video-synced foley.
- **AudioCraft** (Meta) covers both music (MusicGen) and sound effects (AudioGen) in one MIT-licensed suite.

---

## Speech Science & Psychoacoustics: How Voices Convey Emotion and Personality

Understanding the acoustic fundamentals of emotional speech is essential for evaluating (and eventually controlling) expressive voice synthesis. This section summarizes the research literature on how specific acoustic parameters change with emotion, what gives a voice its perceived "personality," and the key theoretical frameworks used in the field.

### 1. Key Acoustic Parameters and What They Measure

| Parameter | What It Is | How It Is Measured |
|-----------|-----------|-------------------|
| **F0 (Fundamental Frequency)** | Rate of vocal fold vibration; perceived as pitch | Hz; typically 85-180 Hz (male), 165-255 Hz (female) |
| **F0 contour** | Shape of pitch over time (rising, falling, flat) | Time-series of F0 values across an utterance |
| **F0 range / variability** | Spread of pitch; perceived as melodic vs. monotone | Semitones or Hz between min and max F0; standard deviation of F0 |
| **Intensity / loudness** | Acoustic energy; perceived as volume | dB SPL |
| **Speech rate** | Tempo of articulation | Syllables per second (typically 4-6 syl/s in neutral English) |
| **Pause patterns** | Silent intervals between speech segments | Duration, frequency, and placement of pauses |
| **Spectral tilt** | Rate of energy drop-off across harmonics | Measured as H1-H2 (difference between first two harmonics, in dB). Large H1-H2 = steep tilt (breathy). Small H1-H2 = flat tilt (pressed/tense) |
| **High-frequency energy (HFE)** | Energy above ~1 kHz relative to total energy | Spectral balance ratios; long-term average spectrum (LTAS) slope |
| **Jitter** | Cycle-to-cycle variation in F0 period | Percentage; higher = more irregular pitch |
| **Shimmer** | Cycle-to-cycle variation in amplitude | dB; higher = more irregular loudness |
| **HNR (Harmonics-to-Noise Ratio)** | Ratio of periodic to aperiodic energy in the voice | dB; high HNR = clear/modal voice; low HNR = breathy/noisy |
| **Formant frequencies (F1-F4)** | Resonance frequencies of the vocal tract; determine vowel identity and voice "color" | Hz; F1 ~300-800 Hz, F2 ~800-2500 Hz, F3 ~2000-3500 Hz |
| **Cepstral Peak Prominence (CPP)** | Regularity of the harmonic structure | dB; higher = more periodic/modal voice |

### 2. Phonation Types

The larynx can produce several distinct modes of vibration, each with a characteristic acoustic signature. These are the building blocks of voice quality:

| Phonation Type | Vocal Fold Behavior | Acoustic Signature | Perceptual Quality |
|---------------|--------------------|--------------------|-------------------|
| **Modal** | Regular, full vibration; moderate tension; ~50% open quotient | Wide pitch range, high HNR, high CPP, moderate spectral tilt, no turbulent noise | Normal, clear, "default" voice |
| **Breathy** | Incomplete glottal closure; air leaks through; ~66% open quotient | Steep spectral tilt (high H1-H2), low HNR, noise in higher frequencies, low F0, increased aspiration noise | Soft, airy, sighing quality |
| **Creaky / Vocal Fry** | Compressed folds, thick and slack; irregular vibration at 20-50 pulses/sec; ~33% open quotient | Very low F0 (40-90 Hz), high jitter and shimmer, flattened spectral tilt (low H1-H2), lowest CPP, irregular pulse spacing | Low, rough, "frying" sound |
| **Falsetto** | Only ligamentous edges of folds vibrate; thin, stretched | Very high F0 (above modal range), few overtones, relatively breathy, limited dynamic range | Light, flute-like, limited in power |
| **Pressed / Tense** | High adductive tension, strong medial compression | Flat spectral tilt (very low H1-H2), high HNR, strong higher harmonics, elevated F0 | Strained, effortful, tight |
| **Whispery** | Folds abducted (not vibrating); turbulent airflow through glottis | No periodic voicing (no F0), aperiodic noise replaces harmonics, formants shifted higher, higher airflow, longer vowel durations, reduced overall intensity, smaller vowel space area | Hushed, secretive, intimate |

### 3. Acoustic Profiles of Emotions

The following profiles synthesize findings from the major studies in the field, including Banse & Scherer (1996), Juslin & Laukka (2003), and subsequent meta-analyses. Directions are relative to neutral speech.

#### 3.1 Happiness / Joy

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Increased** | Higher pitch register; supported by 5-14 studies |
| F0 range / variability | **Increased** | Wider melodic variation; more pitch excursions |
| F0 contour | **Rising, upward slopes** | Steeper rising movements, especially at phrase ends |
| Speech rate | **Variable** | Some studies find faster, some slower; depends on arousal level of the happiness (elation = faster; contentment = slower) |
| Intensity | **Increased** | Louder voice; higher intensity variability |
| Spectral energy | **More HFE** | Greater power above 1 kHz |
| Formants (F1, F2) | **Increased** | Consistently higher F1 and F2 |
| Voice quality | **Slightly breathy to modal** | Some evidence for higher jitter/shimmer; generally bright timbre |
| Articulation | **Precise** | Clear enunciation |

Recognition note: Happiness requires ~977 ms of speech to be reliably detected by listeners, longer than anger or sadness.

#### 3.2 Elation / Excitement (High-Arousal Joy)

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Strongly increased** | Among the highest F0 values of any emotion |
| F0 range | **Very wide** | Large pitch swings |
| Speech rate | **Fast** | Accelerated tempo, short pauses |
| Intensity | **High** | Louder than neutral and than calm happiness |
| HFE | **Strongly increased** | Bright, energetic spectral balance |
| Pause patterns | **Shorter, fewer pauses** | High speech continuity |

#### 3.3 Anger (Hot Anger / Rage)

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Strongly increased** | High pitch register |
| F0 range / variability | **Increased** | Wide and erratic pitch movements |
| F0 contour | **Abrupt, large movements** | Steep rises and falls |
| Speech rate | **Faster** | Consistently reported across studies |
| Intensity | **Strongly increased** | Among the loudest emotional expressions |
| Spectral energy | **Peak energy around 2000 Hz** | Prominent high-frequency energy; flat spectral tilt |
| Voice quality | **Pressed / tense** | Low H1-H2, strong higher harmonics, increased vocal effort |
| Jitter / Shimmer | **Some increase in shimmer** | Significant shimmer differences distinguish joy from hot anger |
| Formants | **Higher F1** | Consistent finding |
| Pauses | **Fewer, shorter** | High drive and urgency |
| Articulation | **Tense, emphatic** | Consonants may be intensified |

#### 3.4 Cold Anger / Irritation

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Lower than hot anger** | Pitch held at lower register than rage |
| F0 range | **Narrower than hot anger** | More controlled, deliberate |
| Intensity | **Higher than neutral** | But less than hot anger |
| Speech rate | **Slower than hot anger** | Precise, measured delivery |
| Voice quality | **Tense** | Pressed phonation, flat spectral tilt |
| Articulation | **Very precise** | Clipped, controlled |

#### 3.5 Fear / Panic

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Increased** | Higher pitch |
| F0 range / variability | **Increased** | More F0 variance |
| F0 contour | **Irregular, with upward tendency** | Unpredictable pitch movement |
| Speech rate | **Faster** | Rapid articulation |
| Intensity | **Variable** | Some studies report increase, others decrease |
| Spectral energy | **More HFE** | Power above 1 kHz increases |
| Voice quality | **Tense, irregular** | Head voice quality; possibly tremulous |
| Pauses | **More frequent but shorter** | Speech fragmentation |
| Jitter | **Increased** | Greater pitch irregularity |
| Duration | **Shorter overall utterances** | Compressed speech segments |

Fear is highly variable in its acoustic profile; it shows the most inconsistency across studies, likely because it spans a range from mild anxiety to full panic.

#### 3.6 Anxiety (Low-Intensity Fear)

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Mixed results** | Some studies find increase; others no change |
| Intensity | **Decreased** | Quieter voice |
| Pause duration | **Increased** | Longer hesitations |
| Jitter / Shimmer | **Increased** | Voice instability |
| Formants (F1, F2) | **Shifted** | Changes in formant frequencies reported |
| Speech rate | **Variable** | Depends on individual and context |

#### 3.7 Sadness / Grief

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Decreased** | Lower pitch register |
| F0 range / variability | **Decreased** | Narrow, monotonous pitch |
| F0 contour | **Downward / falling** | Flat or gently declining |
| Speech rate | **Slow** | Among the slowest of all emotions |
| Intensity | **Decreased** | Quiet, subdued |
| Spectral energy | **More low-frequency energy** | Reduced HFE; energy concentrated below 1 kHz |
| Voice quality | **Lax, potentially creaky or breathy** | Associated with lax/creaky and whispery voice |
| Pauses | **Longer, more frequent** | Extended silences between phrases |
| Formants | **Lower F1** | Retracted tongue position |
| Articulation | **Imprecise, slurred** | Reduced articulatory effort |

Sadness can be reliably detected from ~576 ms of speech.

#### 3.8 Tenderness / Affection

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Decreased** | Lower than neutral; among the lowest F0 of all emotions |
| F0 range | **Narrow** | Gentle, limited pitch variation |
| Speech rate | **Slow** | Unhurried delivery |
| Intensity | **Low** | Soft, quiet voice |
| Spectral energy | **Reduced HFE** | Warm timbre, low-frequency dominance |
| Voice quality | **Breathy** | High H1-H2, increased aspiration noise, low-pitch breathiness |
| Pauses | **Longer** | Relaxed pacing |
| Articulation | **Soft** | Gentle consonant contacts |

#### 3.9 Boredom

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Decreased** | Low pitch |
| F0 range | **Very narrow** | Near-monotone; "flat" intonation |
| Speech rate | **Slow** | Dragging tempo |
| Intensity | **Decreased** | Low energy |
| Spectral energy | **Low HFE** | Dull timbre |
| Voice quality | **Lax, potentially creaky** | Low vocal effort |
| Pauses | **Longer** | Disengaged pacing |
| Articulation | **Imprecise** | Reduced clarity |

Boredom is perceptually close to depression speech: reduced prosodic variation, monotone intonation, decreased vocal energy, and longer pauses.

#### 3.10 Sarcasm / Irony

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Decreased** | Lower pitch than sincere speech; the most prominent cue |
| F0 range | **Restricted** | Less pitch variation than literal speech |
| Speech rate | **Slower** | Deliberately paced, drawn out |
| Intensity | **Variable** | May increase on key words |
| Voice quality | **Harsher** | Increased laryngeal tension |
| Intonation contour | **Flatter or incongruent** | Mismatch between expected and actual prosody signals ironic intent |

Sarcasm detection relies on a combination of these prosodic cues alongside contextual and linguistic information. The reduction in mean F0 relative to other speaking modes (humor, sincerity) is the single strongest acoustic marker.

#### 3.11 Disgust

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Lower** | Downward-directed pitch |
| Intensity | **Energy concentrated at ~500 Hz** | Low-frequency emphasis |
| Formants | **Lower F1** | Retracted articulation |
| Speech rate | **Relatively fast** | But with less variation and shorter durations |
| Voice quality | **Harsh, pressed** | Fast voice onset (attack) times, similar to anger |

Disgust requires the longest listening duration (~1486 ms) to be reliably recognized.

#### 3.12 Whispering

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 | **Absent** | No vocal fold vibration; no periodic pitch signal |
| Formants | **Shifted higher** | All formant frequencies rise |
| Vowel duration | **Longer** | Compensatory lengthening |
| Intensity | **Greatly reduced** | Loss of voiced energy; consonant-vowel intensity ratio is substantially altered |
| Vowel space | **Smaller** | Despite longer durations, articulation is less distinct |
| Airflow | **Higher glottal airflow** | Significantly increased compared to phonation |
| Subglottal pressure | **Lower** | Reduced compared to modal voice |
| Flow resistance | **Lower** | Less glottal resistance than phonation |
| Noise characteristics | **Turbulent noise replaces harmonics** | Aperiodic energy across the spectrum |

#### 3.13 Yelling / Shouting

| Parameter | Direction | Details |
|-----------|-----------|---------|
| F0 mean | **Strongly increased** | Rises at ~5 Hz per dB of vocal effort |
| Formants | **F1 increases** | Shifts upward at ~3.5 Hz/dB; higher formants shift in content-specific ways |
| Spectral tilt | **Flattened** | High-frequency energy increases disproportionately: per 10 dB increase in overall level, A1 rises 11 dB, A2 rises 12.4 dB, A3 rises 13 dB |
| Spectral emphasis | **Shifts 1-2 octaves higher** | The peak spectral energy region moves upward |
| Vowel duration | **Lengthened** | Vowels stretch; consonants may shorten |
| Voice quality | **Pressed, strained** | High vocal effort, high subglottal pressure, tense laryngeal configuration |
| Articulation | **Hyper-articulated** | Increased jaw opening, wider vowel space |

### 4. Dimensional Framework: The Valence-Arousal Space

The two dominant approaches to classifying vocal emotion are:

**Categorical models** assign discrete labels (happy, angry, sad, etc.). This is the approach used in the tables above.

**Dimensional models** place emotions in a continuous space defined by (at minimum) two axes:

- **Valence** (x-axis): pleasant/positive <---> unpleasant/negative
- **Arousal** (y-axis): calm/low energy <---> excited/high energy

This is Russell's Circumplex Model of Affect (1980), the most widely used dimensional framework.

#### Mapping emotions onto the valence-arousal space:

```
                    HIGH AROUSAL
                        |
          Anger    Fear | Excitement  Elation
          Panic  Stress |   Joy   Amusement
                        |
  NEGATIVE -------------|-------------- POSITIVE
    VALENCE             |               VALENCE
                        |
        Sadness  Boredom| Contentment  Relief
        Depression      |  Tenderness  Calm
                        |
                    LOW AROUSAL
```

#### How acoustic parameters map to dimensions:

| Dimension | Primary Acoustic Correlates |
|-----------|---------------------------|
| **Arousal** (strongest acoustic signal) | F0 mean, F0 range, intensity, speech rate, HFE, pause frequency |
| **Valence** (harder to detect acoustically) | Spectral balance, spectral noise (HNR), voice quality (H1-H2), F3/F4 frequencies |
| **Potency / Dominance** (third dimension, sometimes used) | Intensity, spectral tilt, low-frequency energy, speech rate |

Key finding: Arousal dominates the acoustic signal. High-arousal emotions (anger, fear, elation) share elevated F0, faster rate, and higher intensity regardless of whether their valence is positive or negative. Distinguishing positive from negative valence acoustically is harder and depends on subtler cues like spectral balance, voice quality, and formant characteristics.

### 5. Scherer's Component Process Model (CPM)

Klaus Scherer's CPM (1986, updated through 2019) is the most influential theoretical framework for predicting how emotions affect the voice. Rather than listing emotion-to-parameter mappings empirically, it predicts vocal changes from first principles:

**Core mechanism:** Emotion arises from a sequence of cognitive appraisals (novelty check, pleasantness check, goal conductiveness, coping potential, norm compatibility). Each appraisal triggers physiological changes that mechanically affect the vocal apparatus:

| Appraisal Step | Physiological Effect | Vocal Consequence |
|---------------|---------------------|-------------------|
| **Novelty / Suddenness** | Sympathetic nervous system activation; respiratory interrupt | Raised F0 (increased vocal fold tension), intensity changes, speech fluency disruption |
| **Intrinsic pleasantness** | Relaxation vs. tension of laryngeal muscles | Pleasant = relaxed phonation, wider formant bandwidth; Unpleasant = tense phonation, narrower bandwidth |
| **Goal conduciveness** | If goal-obstructive: increased muscle tension throughout | Higher F0, increased intensity, faster rate, pressed voice quality |
| **Coping potential (high)** | Full muscle engagement; high subglottal pressure | Loud, high-pitched, pressed voice (as in hot anger, triumph) |
| **Coping potential (low)** | Muscle collapse, low tension | Quiet, low-pitched, breathy/creaky voice (as in sadness, resignation) |
| **Norm compatibility** | Variable | Contextual modulation of other parameters |

The CPM generates specific, testable predictions. For example, fear (high novelty, low coping potential) should produce high F0 (novelty response) combined with tense but weak voice (low coping), which is exactly what is observed.

### 6. What Gives a Voice Its "Personality"

Beyond transient emotional expression, voices carry stable individual characteristics that listeners interpret as personality:

#### 6.1 Anatomical / Fixed Factors

| Factor | Acoustic Effect | Perceptual Result |
|--------|----------------|------------------|
| **Vocal tract length** | Determines formant spacing; longer tract = lower formants | Deeper, more resonant voice perceived as larger, more dominant |
| **Vocal fold mass and length** | Determines habitual F0 range | Lower voice = perceived as more dominant, authoritative, mature |
| **Nasal cavity shape** | Affects nasality and formant bandwidth | Moderate nasality is neutral; excess nasality perceived negatively |
| **Subglottal system (lung capacity)** | Affects maximum intensity and breath group length | Larger capacity = perceived as more powerful, confident |

#### 6.2 Habitual / Learned Factors

| Factor | Acoustic Signature | Personality Perception |
|--------|-------------------|----------------------|
| **Habitual pitch level** | Mean F0 across contexts | Lower pitch perceived as dominant, confident, calm; higher pitch perceived as more nervous, less agreeable, higher neuroticism |
| **Pitch range / variability** | F0 SD across utterances | Wide range = expressive, extraverted; narrow range = monotone, disengaged or authoritative |
| **Speaking rate** | Syllables per second | Faster = perceived as more competent, energetic; slower = calmer but potentially less intelligent |
| **Breathiness** | High H1-H2, low HNR | Perceived as intimate, gentle, sometimes sensual; less-modal voice generally enhances personality scores |
| **Creaky voice / vocal fry** | Low F0, high jitter/shimmer, irregular pulses | Mixed perception; can signal casualness/relaxation or receive negative evaluations (especially from female speakers) |
| **Smiling voice** | Raised F1/F2 (shortened vocal tract from lip spreading); brighter timbre | Most consistently positive personality ratings across all Big Five traits |
| **Articulation precision** | Formant clarity, consonant-vowel contrasts | Clear articulation = perceived as more conscientious, educated |

#### 6.3 Voice Quality and Big Five Personality Traits

Research shows acoustic features have the strongest predictive impact on:
- **Agreeableness** (26% acoustic influence) -- correlated with higher pitch
- **Extraversion** (22%) -- dynamic pitch, higher intensity, faster rate
- **Neuroticism** (22%) -- higher pitch, more pitch variability, breathier quality
- **Openness** (19%) -- less well-defined acoustically
- **Conscientiousness** (16%) -- least acoustically determined

### 7. The Role of F0 Contours

F0 contour (the shape of pitch over time) carries critical information beyond just mean pitch:

| Contour Pattern | Typical Context |
|----------------|-----------------|
| **Rising terminal** | Questions, uncertainty, deference, surprise, continued interest |
| **Falling terminal** | Statements, certainty, authority, finality, sadness |
| **Rising-falling (hat pattern)** | Emphasis, focus, assertion, anger |
| **Flat / level** | Boredom, depression, deliberate control, sarcasm |
| **Highly variable / wide excursions** | Excitement, joy, engagement, expressiveness |
| **Steep rising movements** | Happiness (especially at phrase ends); surprise |
| **Abrupt large movements** | Anger, alarm |
| **Narrow, irregular** | Fear, anxiety |

Key finding: The speed and steepness of F0 movements (not just their direction) significantly distinguish emotions. Happy speech has steeper F0 rises; angry speech has abrupt large movements.

### 8. How Modern Voice AI Maps to These Fundamentals

Current expressive TTS systems control emotion through the same acoustic parameters identified in the research literature:

| AI System | Emotion Control Method | Relevant Acoustic Parameters |
|-----------|----------------------|----------------------------|
| **Chatterbox** | Emotion exaggeration slider (first open-source model with this feature) | Scales prosodic variation (F0 range, intensity, rate) |
| **Fish Audio S2 Pro** | Sub-word natural language tags: `[whisper]`, `[excited]`, `[angry]` | Modifies phonation type, F0, rate, spectral balance per tagged segment |
| **Zonos-TTS** | Explicit emotional parameters | Pitch variance, speech rate, spectral features |
| **Spark-TTS** | Prosody parameters (pitch variance, speech rate) | F0 variability, temporal features |
| **SSML-based systems** | `<prosody>` tags for rate, pitch, volume; `<emphasis>`; `<break>` | Maps directly to speech rate, F0, intensity, pause duration |

The fundamental challenge: arousal is acoustically dominant and relatively easy for AI to replicate (just raise pitch/rate/volume for high arousal). Valence is acoustically subtle and depends on fine-grained voice quality (spectral tilt, breathiness, jitter patterns), which current models still struggle to control precisely.

### 9. Key References

| Reference | Contribution |
|-----------|-------------|
| **Banse & Scherer (1996)** "Acoustic profiles in vocal emotion expression" — *J. of Personality and Social Psychology*, 70(3), 614-636 | First comprehensive acoustic analysis of 14 emotions from actor portrayals; established emotion-specific vocal parameter profiles |
| **Juslin & Laukka (2003)** "Communication of emotions in vocal expression and music performance" — *Psychological Bulletin*, 129(5), 770-814 | Meta-analysis of 104 vocal expression studies; systematic summary of acoustic cues per emotion; demonstrated parallel coding in speech and music |
| **Scherer (1986, 2019)** Component Process Model — *Annual Review of Psychology* | Theoretical framework predicting vocal changes from cognitive appraisal sequences; explains *why* specific acoustic patterns occur for each emotion |
| **Russell (1980)** Circumplex Model of Affect | Foundational dimensional model (valence x arousal) widely used in emotion recognition and speech synthesis |
| **Garellek (2022)** "The phonetics of voice" — *Handbook chapter, UC San Diego* | Comprehensive reference on phonation types (modal, breathy, creaky, falsetto) and their acoustic measures (H1-H2, spectral tilt, jitter, shimmer) |
| **Laukka et al. (2011)** "Acoustic correlates and automatic detection of irritation" — *Columbia University* | Bridging speech science and computational detection; acoustic correlates of specific negative emotions |
| **Cheang & Pell (2008)** "The sound of sarcasm" — *Speech Communication* | Identified lower F0 mean and restricted F0 range as primary acoustic markers of sarcasm |
| **Sorokin et al. (2025)** "Measuring negative emotions and stress through acoustic correlates" — *PLOS ONE* | Systematic review finding F0 and intensity as most reliable indicators across negative emotions and stress |

---

## Controlling Emotion in Cloned & Synthesized Voices — Practical Guide

Research date: March 2026

This section covers how to actually get a voice to sound a specific way: what controls exist, how they work under the hood, and their real-world limitations.

---

### 1. Commercial Platform Emotion Controls

#### ElevenLabs

ElevenLabs v3 (released June 2025) is the current benchmark for commercial emotion control. It provides three mechanisms:

**A. Audio Tags (v3 only)** -- inline bracket directives that act as stage directions for the voice:

| Category | Example Tags |
|----------|-------------|
| Emotion/Tone | `[sad]`, `[angry]`, `[excited]`, `[sarcastic]`, `[happy]`, `[fearful]`, `[surprised]`, `[curious]`, `[mischievously]` |
| Delivery | `[whispers]`, `[shouts]`, `[calm]`, `[singing]`, `[deadpan]`, `[playfully]`, `[flatly]` |
| Reactions | `[laughs]`, `[sighs]`, `[exhales]`, `[clears throat]`, `[snorts]`, `[crying]`, `[gasps]` |
| Pacing | `[pause]`, `[rushed]`, `[stammers]`, `[drawn out]`, `[hesitates]` |
| Accents | `[strong French accent]`, `[strong X accent]` |
| Sound Effects | `[applause]`, `[gunshot]`, `[explosion]`, `[door creaks]`, `[footsteps]` |
| Environment | `[forest]`, `[city]`, `[cafe]`, `[rain]` |
| Narrative Style | `[voice-over]`, `[documentary style]`, `[inner monologue]` |
| Audio Effects | `[reverb]`, `[echo]`, `[telephone filter]`, `[megaphone]` |

Tags can be stacked: `[angry][laughing]` produces an angry laugh; `[sad][whispers]` produces sad whispering.

**B. Text Formatting Cues:**
- ALL CAPS for emphasis on specific words
- Exclamation marks increase emotional intensity
- Ellipses (...) create pauses and trailing hesitation
- Dashes (-- or -) create short pauses
- Question marks produce rising intonation
- Narrative context like "she said excitedly" influences delivery

**C. Voice Settings Sliders:**
- **Stability** (0-100%): Lower = more emotional variability; higher = more consistent but potentially monotone. 40-60% is the sweet spot for balanced emotion.
- **Style Exaggeration**: Amplifies the style characteristics of the original voice.
- **Speed**: 0.5x to 2.0x multiplier on speaking rate.

**Key limitation:** The voice you select must support the intended delivery. A whispering voice will not convincingly shout with a `[shout]` tag. Tags work best when matched to the voice's training data.

#### PlayHT

PlayHT provides per-paragraph emotion controls:
- Select emotion per paragraph (cheerful, angry, whispering, etc.)
- Adjust intensity, similarity, and stability via slider bars
- Higher stability adds more variance and expressiveness
- Version 2.0 improved emotion accuracy and multilingual support

#### Resemble.ai

Resemble.ai offers the most granular commercial emotion control:
- **25 discrete emotions** available including happiness, sadness, excitement, concern, urgency, calmness
- Add emotions to any cloned voice without requiring new training data
- Fine-tune emotion intensity, energy, pacing, and style with individual controls
- Supports 120+ languages with emotion control in most of them
- Also released **Chatterbox** as their open-source model (see open-source section)

#### Fish Audio

Fish Audio S2/S2 Pro (2025) has the most extensive tag vocabulary:
- S1 supports 50+ predefined emotion/tone markers: `(angry)`, `(whisper)`, `(chuckling)`, etc.
- S2 Pro supports **15,000+ free-form tags** at sub-word granularity -- not limited to fixed presets
- Tags like `[whisper in small voice]`, `[professional broadcast tone]`, `[pitch up]` are all valid
- Emotion sliders for "warm", "excited", etc. modify personality continuously
- 10-30 seconds of reference audio captures timbre, speaking style, and emotional tendencies
- Dual-AR architecture trained on 10M+ hours of audio across 80+ languages

---

### 2. How Style Tokens, Emotion Embeddings, and Speaker Embeddings Work

These are the three core technical mechanisms that allow voice models to represent and control different aspects of speech independently.

#### Style Tokens (Global Style Tokens / GST)

**What they are:** A bank of learnable embedding vectors, each representing a distinct speaking "style" (which can correspond to emotions, pacing, energy levels, etc.). Introduced by Google in the 2018 paper "Style Tokens: Unsupervised Style Modeling, Control, and Transfer in End-to-End Speech Synthesis."

**How they work:**
1. During training, a **reference encoder** compresses a variable-length audio signal into a fixed-length vector (the "reference embedding")
2. This reference embedding is used as a query to an attention mechanism over a bank of randomly initialized token embeddings
3. The attention learns which tokens correspond to which acoustic qualities -- entirely without labels
4. Each token naturally gravitates toward a distinct style: one may capture slow/calm speech, another fast/energetic speech, etc.
5. At inference time, you can select tokens manually or combine them with weighted sums to create blended styles

**Why they matter:** GSTs were the first mechanism that allowed style transfer in TTS -- take the "style" from one utterance and apply it to any text. They proved that emotional style could be separated from text content in a learned, unsupervised way.

**Modern evolution:** Multi-layer GST architectures show that first-layer tokens learn speaker representations while second-layer tokens capture speaking style features (pause position, duration, stress). Retrieval-based and embedding-based methods are now largely displacing the original fixed-bank GST approach.

#### Emotion Embeddings

**What they are:** Vector representations that encode the emotional characteristics of speech, separate from speaker identity and linguistic content.

**How they work:**
- An emotion feature extractor (often a pre-trained Speech Emotion Recognition model like Emotion2Vec or HuBERT) analyzes audio and produces a fixed-dimensional vector capturing the emotional qualities
- This vector is injected into the TTS model as a conditioning signal alongside text and speaker information
- The model learns to modify its acoustic output (pitch contours, energy, speaking rate, voice quality) based on the emotion vector

**Disentanglement problem:** The hard part is ensuring the emotion embedding captures only emotion and not speaker identity. Techniques include:
- **Orthogonality loss**: Force emotion embeddings to be mathematically orthogonal to speaker embeddings
- **In-batch contrastive learning**: Pull same-emotion/different-speaker embeddings together; push different-emotion/same-speaker apart
- **Gradient-reversal adversarial classifiers**: Penalize the emotion encoder if its output contains speaker-identifying information

**EmoMix approach:** Interpolate between emotion embeddings during the diffusion noise prediction process. This allows mixing emotions (e.g., 70% happy + 30% sad) and controlling intensity continuously rather than being limited to discrete categories.

**EmoSphere-TTS approach (Interspeech 2024):** Maps arousal, valence, and dominance into a spherical coordinate system. This allows continuous interpolation across the entire emotional space without relying on discrete labels. Any point on the sphere represents a valid emotion.

#### Speaker Embeddings

**What they are:** Fixed-dimensional vectors that capture a speaker's vocal identity -- their unique timbre, pitch range, vocal quality, and other identity-specific characteristics.

**How they work:**
- Extracted by speaker verification/identification models (d-vectors from speaker encoders, x-vectors from ECAPA-TDNN, etc.)
- Represent "who" the voice is, independent of "what" they are saying or "how" they are saying it
- In voice cloning, the speaker embedding from a reference clip is injected into the model so that generated speech matches that speaker's identity

**Relationship to emotion:** The key challenge in emotional voice synthesis is keeping speaker embeddings stable while varying emotion embeddings. If emotion changes also shift the speaker embedding, the voice "drifts" and sounds like a different person when expressing different emotions. Modern systems like Marco-Voice (2025) use contrastive learning to disentangle these two embedding types.

---

### 3. Voice Prompt Engineering -- Text Cues That Influence Delivery

"Prompt engineering" for voice means structuring your input text so the TTS model produces the desired delivery. This works because modern models are trained on large corpora where text context correlates with specific vocal qualities.

#### Bracket/Tag Systems (Model-Specific)

Different models use different tag formats:

| Model | Format | Examples |
|-------|--------|----------|
| ElevenLabs v3 | `[tag]` | `[whispers]`, `[excited]`, `[laughs]` |
| Fish Audio S2 | `[tag]` or `(tag)` | `[whisper in small voice]`, `(angry)` |
| Bark | `[tag]` | `[laughs]`, `[sighs]`, `[clears throat]` |
| Chatterbox | `[tag]` | `[laugh]`, `[cough]`, `[chuckle]` |
| Orpheus TTS | `<tag>` | `<laugh>`, `<sigh>`, `<gasp>`, `<yawn>` |
| Dia / Dia2 | `(tag)` | `(laughs)`, `(sighs)`, `(coughs)` |
| Maya1 | inline tags | Inline emotion tags placed at exact text positions |
| EmotiVoice | prefix labels | Prefix text with `Happy`, `Angry`, `Sad`, etc. |

#### Punctuation and Formatting Tricks (Work Across Most Models)

| Technique | Effect | Example |
|-----------|--------|---------|
| ALL CAPS | Emphasis on specific words | "That is ABSOLUTELY incredible" |
| Exclamation marks | Increased energy and intensity | "This is amazing!" vs "This is amazing." |
| Question marks | Rising intonation | "You really think so?" |
| Ellipses (...) | Hesitation, trailing off, dramatic pause | "I thought... maybe... we could try." |
| Dashes (-- or -) | Short breath pauses | "I wanted to -- but I couldn't." |
| Multiple exclamation marks | Greater intensity (diminishing returns) | "No way!!!" |
| Asterisks around words | Emphasis (Parler TTS) | "I *really* want to go" |

#### Narrative Context Cues

Many models (especially LLM-based ones like ElevenLabs v3, Orpheus, Maya1) interpret narrative context:
- "she whispered softly" -- may shift to quieter delivery
- "he shouted across the room" -- may increase volume and intensity
- "speaking nervously" -- may add hesitation
- Dialog attribution: "she said excitedly" can influence tone even for the quoted text

#### Temperature and Generation Parameters

For LLM-based models (Orpheus, Maya1, Bark):
- **Temperature**: Higher values produce more expressive, varied speech; lower values are more predictable and stable
- **Top-p**: Controls diversity of the generation
- **Repetition penalty**: Must be >= 1.1 for Orpheus; increasing it alongside temperature makes speech faster

---

### 4. Reference Audio / Style Transfer -- How It Works

Reference audio style transfer means providing a short audio clip to set the emotional tone, and having the model reproduce those emotional qualities in new speech.

#### How It Works Architecturally

**Step 1 -- Encode the reference:** A reference encoder (typically a convolutional network followed by a GRU or transformer) processes the audio clip and produces a fixed-length style vector that captures the prosodic and emotional characteristics.

**Step 2 -- Condition the generator:** This style vector is injected into the TTS model alongside the text encoding and speaker embedding. The model uses it to set the "how" of speech production -- pitch contours, timing, energy, voice quality.

**Step 3 -- Generate with transferred style:** The model synthesizes the target text with the emotional characteristics of the reference audio but the words of the input text.

#### Systems That Use This Approach

| System | Reference Audio Requirement | What Transfers |
|--------|---------------------------|----------------|
| **OpenVoice** | Any length | Tone color is cloned from reference; emotion/accent/rhythm controlled separately via base TTS model |
| **StyleTTS 2** | Short clip | Full prosodic style including emotion, rhythm, pacing |
| **XTTS-v2** (Coqui) | 6 seconds | Voice identity + emotional tone + speaking style |
| **GPT-SoVITS** | 5 seconds (zero-shot) or 1 min (fine-tuned) | Voice + speed + emotion; reference audio "determines the speed and emotion of the output" |
| **Fish Audio S2** | 10-30 seconds | Timbre, speaking style, and emotional tendencies |
| **CosyVoice 3** | Short clip | Voice identity with separate instruct-mode emotion control |
| **Dia2** | Audio conditioning | Natural conversation continuation with matched style |

#### OpenVoice's Two-Stage Architecture (Most Explicit Decoupling)

OpenVoice uniquely separates voice cloning into two independent stages:
1. **Base Speaker TTS Model** -- controls style parameters (emotion, accent, rhythm, pauses, intonation) and generates speech in a base voice
2. **Tone Color Converter** -- a separate neural network shifts the tone color to match the reference speaker while preserving all style controls

This means you can independently set emotion to "happy" and accent to "British" while using a reference clip only for the voice's timbre. The style controls and the voice identity are fully decoupled.

#### Practical Tips for Reference Audio

- **Quality matters more than length**: A clean 5-10 second clip with the desired emotion is better than a noisy 30-second clip
- **Match the emotion you want**: If you want angry output, provide an angry reference. Most systems transfer the emotion of the reference, not just the timbre
- **Studio recording conditions**: Quiet background, consistent mic distance, no reverb
- **Varied training samples for professional clones**: Include neutral, energetic, and whispered delivery for maximum flexibility
- **Mismatch is the #1 cause of flat output**: Recording a calm meditative reading then trying to generate energetic marketing copy will produce disappointing results

---

### 5. Limitations -- What Emotion Control Cannot Do

#### Training Data Bottleneck

The most fundamental limitation: **a voice model cannot express an emotion it has never heard.** If the training data consists only of neutral read speech, no amount of tags or embeddings will produce convincing anger or fear. The quality of emotional training data directly determines the range and quality of emotional output.

Specific constraints:
- **Female voices have broader emotion support** than male voices in many systems, because evaluation benchmarks pass the 50% recognizability threshold sooner for female emotional speech
- **Emotional speech datasets are small** (typically 5-50 hours) compared to general TTS data (100K+ hours). Systems trained primarily on audiobook data inherit the limited emotional range of audiobook narration
- **Low-resource languages** have even less emotional speech data, making emotion control unreliable outside English and Chinese

#### Voice-Emotion Compatibility

Not every voice can produce every emotion convincingly:
- A voice cloned from a calm, measured speaker will struggle with extreme anger or excitement
- ElevenLabs explicitly warns: "Don't expect a whispering voice to suddenly shout with a [shout] tag"
- Zero-shot cloning (5-30 second clip) captures timbre well but often misses fine-grained emotional range
- Professional voice cloning (30+ minutes of diverse recordings) produces much better emotional flexibility

#### The Disentanglement Problem

When you change the emotion, the voice should still sound like the same person. In practice:
- Many models exhibit "speaker drift" -- the voice sounds subtly different at each emotion
- Contrastive learning and orthogonality losses reduce but do not eliminate this problem
- High-arousal emotions (anger, excitement) cause more speaker drift than low-arousal ones (sadness, calm)

#### Continuous vs. Discrete Emotions

Most commercial systems offer discrete emotion categories (happy, sad, angry). Real human emotion is continuous and mixed:
- Bittersweet (happy + sad) is difficult for most systems
- Sarcasm (surface-level cheerful + underlying contempt) is challenging; ElevenLabs v3 has a `[sarcastic]` tag but results vary
- Subtle emotions (wistful, nostalgic, resigned) are underrepresented in training data and poorly supported

#### Prosody Remains the Hard Problem

Community consensus as of 2025: prosody modeling is the critical gap between synthetic and human speech. Speech covers broad time spans and varies due to linguistic, paralinguistic, and non-linguistic factors. Most systems handle utterance-level emotion but struggle with:
- Emotion transitions within a single utterance (starting calm and becoming angry)
- Contextual prosody (emphasis based on discourse context, not just text)
- Natural speech disfluencies that accompany real emotion (voice breaks, catches, trembling)

#### Whisper and Shout Are Especially Hard

- **Whispering** lacks vocal fold vibration entirely, requiring specialized vocoders trained on whispered audio. Without this, models produce "quiet speech" not true whisper
- **Shouting** involves vocal effort beyond typical training distributions. Studio-recorded TTS data rarely includes actual shouting

---

### 6. Open-Source Tools for Emotional Voice Synthesis

| Model | Params | Emotion Mechanism | Key Capability | License |
|-------|--------|-------------------|----------------|---------|
| **Chatterbox Turbo** (Resemble AI) | 350M | Exaggeration parameter (0.0-1.0+) + paralinguistic tags `[laugh]`, `[cough]`, `[chuckle]` | First open-source model with emotion exaggeration control. Clone voice from 5s audio. | MIT |
| **Orpheus TTS** (Canopy Labs) | 3B (Llama-3b) | Inline tags: `<laugh>`, `<chuckle>`, `<sigh>`, `<cough>`, `<sniffle>`, `<groan>`, `<yawn>`, `<gasp>` | LLM-based, human-level expressiveness, ~200ms streaming latency. 8 voices. | Open |
| **Maya1** (Maya Research) | 3B (Llama) | 20+ inline emotion tags + natural language voice design descriptions | Describe voice as if briefing a voice actor. Laughter, crying, whispering, anger, sighing, gasping. | Apache 2.0 |
| **Dia2** (Nari Labs) | 1B-2B | Nonverbal tags `(laughs)`, `(sighs)`, `(coughs)` + audio conditioning | Streaming dialogue TTS, multi-speaker with `[S1]`/`[S2]` tags. | Apache 2.0 |
| **EmotiVoice** (NetEase Youdao) | - | Emotion label prefix: `Happy`, `Excited`, `Sad`, `Angry` | 2,000+ voices, English + Chinese. OpenAI-compatible API. Docker deployment. | Apache 2.0 |
| **Parler TTS** | - | Natural language descriptions of voice characteristics | Describe age, emotion, speed, environment in plain English. Expresso variant has emotion-specific voices. | Open |
| **Qwen3-TTS** (Alibaba) | 0.6B-1.7B | Natural language instruct descriptions for emotion/prosody | "Speak with excitement", "Sad and tearful voice". 10 languages. Voice design from text descriptions. | Open (Jan 2026) |
| **CosyVoice 3** (Alibaba) | 0.5B | Instruct mode for emotion/speed/volume + reference audio | Commands like "happy", "sad", "angry" + dialect/accent control. | Open (Dec 2025) |
| **Bark** (Suno) | ~1B | Non-verbal tokens: `[laughs]`, `[sighs]`, `[clears throat]`, `...` | Built-in paralinguistic support. Context-driven emotion from GPT architecture. | MIT |
| **OpenVoice** (MyShell) | - | Decoupled tone color + style control (emotion, accent, rhythm) | Change emotion/accent independently from voice identity. V2 adds multilingual. | MIT |
| **GPT-SoVITS** | - | Reference audio determines emotion + speed of output | Train from 1 min of audio. Reference clip sets emotional baseline. | MIT |
| **StyleTTS 2** | - | Style diffusion from reference audio + SLM adversarial training | Full prosodic style transfer. Human-level quality. | MIT |
| **Fish Speech** (Fish Audio) | - | 50+ inline markers; S2 Pro has 15K+ free-form tags | Most granular open tag system. Sub-word level control. | Open |
| **EmoSphere-TTS** | - | Spherical emotion vectors (arousal/valence/dominance) | Continuous emotion interpolation without labels. | Open |

---

### 7. Practical Recipes: How to Make a Voice Sound a Specific Way

#### Recipe: Happy/Excited Voice
1. **Select a voice** cloned from or trained on expressive/upbeat speech
2. **Use tags**: `[excited]`, `[cheerfully]`, `[happily]` (ElevenLabs); `(excited)` (Fish Audio); `Happy` prefix (EmotiVoice)
3. **Text formatting**: Add exclamation marks, use energetic word choices
4. **Parameters**: Increase exaggeration (Chatterbox), lower stability (ElevenLabs), raise temperature (Orpheus)
5. **Reference audio**: Provide a clip of genuinely happy speech (StyleTTS 2, XTTS, GPT-SoVITS)

#### Recipe: Angry Voice
1. **Tags**: `[angry]`, `[frustrated]` (ElevenLabs); `(angry)` (Fish Audio); `Angry` prefix (EmotiVoice)
2. **Text formatting**: Short, punchy sentences. CAPITALIZE key words. Exclamation marks.
3. **Parameters**: High exaggeration, moderate-to-low stability
4. **Reference audio**: Use an angry reference clip; calm recordings will not produce convincing anger

#### Recipe: Whispered Voice
1. **Tags**: `[whispers]` (ElevenLabs); `[whisper]` (Fish Audio); `(whispers)` (Dia2)
2. **Key requirement**: The model or vocoder must have been trained on actual whispered speech
3. **Fallback**: Use SSML `<prosody volume="x-soft" rate="slow">` for a quiet-but-not-whispered approximation
4. **Best open-source**: Train with Expresso dataset whisper samples; or use WhispSynth (2026) for dedicated whisper synthesis

#### Recipe: Sad/Melancholic Voice
1. **Tags**: `[sad]`, `[sorrowful]` (ElevenLabs); `(sad)` (Fish Audio); `Sad` prefix (EmotiVoice)
2. **Text formatting**: Use ellipses for trailing pauses... longer sentences... slower pacing
3. **Parameters**: Lower exaggeration for subtle sadness; higher for dramatic grief
4. **Reference audio**: Provide a soft, slow, low-energy reference clip

#### Recipe: Narrator with Personality Shifts
1. Use **ElevenLabs v3** audio tags inline: `[calm] The forest was quiet. [tense] Then a branch snapped. [whispers] Something was watching.`
2. Or use **Fish Audio S2** free-form tags: `[mysterious narrator tone]` followed by `[urgent and breathless]`
3. Or use **Maya1** / **Qwen3-TTS** natural language descriptions of desired delivery for each segment

#### Recipe: Voice with Laughs and Natural Reactions
1. **Chatterbox**: `[laugh]`, `[cough]`, `[chuckle]` -- performed in the same cloned voice naturally
2. **Orpheus**: `<laugh>`, `<chuckle>`, `<gasp>`, `<sigh>` -- 8 paralinguistic tags
3. **Bark**: `[laughs]`, `[sighs]`, `[clears throat]` -- non-verbal tokens
4. **Dia2**: `(laughs)`, `(coughs)` -- but results may be inconsistent

---
---

# Emotional Expression & Personality in Voice Synthesis — Research Findings

Research date: March 2026

---

## 1. Acoustic Features That Change With Emotion

Human vocal emotion is conveyed through measurable acoustic parameters. Research spanning decades (Juslin & Laukka, 2003; Banse & Scherer, 1996; recent 2025 theater performance studies) has mapped specific parameter profiles to discrete emotions.

### 1.1 Core Acoustic Dimensions

| Parameter | What It Is | Role in Emotion |
|-----------|-----------|-----------------|
| **F0 (Fundamental Frequency / Pitch)** | The base vibration rate of the vocal folds, measured in Hz | Primary carrier of arousal; high-activation emotions raise F0 mean and variability |
| **F0 Range / Variability** | The span between lowest and highest pitch in an utterance | Happy speech shows the broadest F0 range (~173 Hz mean); sad speech the narrowest (~90 Hz mean) |
| **Intensity / Loudness** | Sound pressure level (dB SPL) | Anger and happiness produce significantly higher loudness than sadness or surprise |
| **Speaking Rate** | Syllables or words per second | High-activation emotions (anger, happiness, fear) correlate with faster rate; sadness and tenderness with slower rate |
| **Spectral Tilt / Slope** | Energy distribution across frequency bands | Steeper negative slopes for soft/sad speech; flatter slopes for loud/angry speech |
| **Formant Frequencies (F1, F2, F3)** | Resonance frequencies shaped by the vocal tract | Related to the valence dimension; shifts in formants affect perceived warmth vs. coldness of voice |
| **Formant Bandwidth** | Width of each formant peak | Wider bandwidths in breathy/whispered speech; narrower in tense/angry speech |
| **Harmonic-to-Noise Ratio (HNR)** | Ratio of periodic to aperiodic energy in the voice | Lower HNR = breathier/rougher voice (fear, sadness); higher HNR = clear/modal voice |
| **Jitter & Shimmer** | Cycle-to-cycle variations in pitch and amplitude | Elevated in stressed, fearful, or sad speech; indicators of vocal instability |
| **Timbre / Spectral Envelope** | Overall "color" of the voice independent of pitch | Bright timbre for happiness; dark/muffled timbre for sadness; harsh timbre for anger |

### 1.2 Emotion-Specific Acoustic Profiles

**Happiness / Joy:**
- High F0 mean and the broadest F0 range of all emotions
- Fast speaking rate
- High intensity/loudness
- Bright spectral quality (more high-frequency energy)
- Wide pitch variability with rising intonation patterns

**Anger:**
- High F0 mean with moderate-to-high variability
- Fast speaking rate (fastest of all emotions in some studies)
- Highest intensity/loudness
- Flat spectral tilt (energy maintained across high frequencies)
- Tense voice quality, narrow formant bandwidths
- Abrupt onset of syllables

**Fear / Scared:**
- High F0 mean (comparable to anger and happiness)
- Fastest speaking rate in many studies
- Higher vocal energy but with tremor/instability
- Elevated jitter and shimmer (shaky voice)
- Breathy-to-tense phonation, reduced HNR
- Wide F0 variability with irregular contours

**Sadness:**
- Low F0 mean, narrowest F0 range
- Slowest speaking rate
- Low intensity/loudness
- Steep spectral tilt (less high-frequency energy)
- Breathy voice quality, lower HNR
- Longer pauses, monotone delivery

**Whispering:**
- No vocal fold vibration (aperiodic excitation only)
- No measurable F0 (pitch cue removed entirely)
- Formant frequencies shift: F1/F2 of most vowels shift higher; /u/ shifts lower
- Formant bandwidths are significantly expanded
- Very low intensity
- Breathy, noise-dominated spectrum

**Yelling / Shouting:**
- Very high F0 (pushed to top of speaker's range)
- Maximum intensity/loudness
- Compressed dynamic range
- High spectral energy across all bands (very flat spectral tilt)
- Tense, pressed phonation
- Slower articulation rate than conversational speech despite perceived urgency (due to effort)

### 1.3 Key Insight: Multi-Feature Discrimination

High-activation emotions (happiness, anger, fear) share similar F0 and rate profiles, making them difficult to distinguish from a single feature. Accurate emotion discrimination requires combinations of features: spectral tilt distinguishes anger (flat) from fear (variable); jitter/shimmer distinguishes fear (high) from happiness (low); formant characteristics and voice quality separate valence (positive vs. negative).

---

## 2. How AI/ML Voice Models Are Trained for Emotional Speech

### 2.1 Emotional Speech Datasets

| Dataset | Language | Emotions | Size / Notes |
|---------|----------|----------|-------------|
| **ESD (Emotional Speech Database)** | English + Chinese | 5 (neutral, happy, angry, sad, surprise) | 350 parallel utterances per emotion per speaker |
| **IEMOCAP** | English | Happy, angry, sad, neutral, excited, surprised + valence/arousal/dominance | ~12 hrs; scripted + spontaneous dialogues; the most-cited emotional speech dataset |
| **RAVDESS** | English | 8 emotions (calm, happy, sad, angry, fearful, surprise, disgust, neutral) | Audio + video, 24 actors |
| **CREMA-D** | English | 6 emotions | 7,442 clips, 91 actors, demographic diversity |
| **EMO-DB (Berlin)** | German | 7 emotions (anger, boredom, disgust, fear, happiness, sadness, neutral) | ~500 utterances, 10 actors |
| **CSEMOTIONS** (Marco-Voice) | Mandarin | 7 (neutral, happy, angry, sad, surprise, playful, fearful) | ~10.2 hrs, 6 professional actors |
| **LibriTTS / LibriLight** | English | Not explicitly emotional but provides large-scale clean speech for pre-training | 60K+ hours (LibriLight) |
| **Expresso** | English | Multiple expressive styles including whisper, narration, enunciated, etc. | ~40 hrs |

**Challenge:** Dedicated emotional speech datasets are small (typically 5-50 hours). Most large-scale TTS training data (100K+ hours) is scraped from audiobooks and podcasts and carries implicit but unlabeled emotional variation. Modern approaches use pseudo-labeling: pre-trained speech emotion recognition (SER) models or self-supervised models (e.g., HuBERT, WavLM, Emotion2Vec) automatically annotate large corpora with arousal/valence/dominance scores or discrete emotion labels.

### 2.2 Conditioning Approaches

#### A. Reference Audio Conditioning (Style Transfer)

The model receives a short clip of speech as a "style reference" and reproduces its emotional/prosodic characteristics in the output.

- **Global Style Tokens (GST):** A bank of learnable style embeddings. An attention mechanism over the reference audio selects a weighted combination of tokens. Used in Tacotron-GST, StyleTTS.
- **VAE-based style encoding:** VAE-Tacotron, GMVAE-Tacotron encode style into a disentangled latent space, allowing interpolation between emotions.
- **Speaker/emotion encoders:** Separate encoders for speaker identity (timbre) and emotion, preventing "speaker leakage" when transferring emotion across speakers. Marco-Voice uses in-batch contrastive learning for this disentanglement.

#### B. Text/Prompt Conditioning

The user provides a natural-language description of the desired emotion or style.

- **PromptTTS / InstructTTS:** Takes descriptions like "speak with an excited and happy tone" as conditioning input alongside the text to synthesize.
- **LLM-based emotion detection:** The system uses an LLM to detect emotional intent from the input text itself (e.g., "I'm thrilled!" maps to happiness) and conditions synthesis accordingly. ElevenLabs v3 does this automatically.
- **EmotiVoice:** Uses text prompts with emotion labels (e.g., "happy", "angry") alongside speaker selection to condition a multi-voice, multi-emotion TTS engine.
- **Fish Audio S1/S2:** Supports 50+ emotion/tone markers as inline tags, e.g., `(angry)`, `(whisper)`, `(chuckling)`, with S2 Pro supporting 15,000+ free-form text descriptions.

#### C. Discrete Label / Embedding Conditioning

The model takes an explicit emotion class or continuous emotion vector.

- **One-hot emotion ID:** Simple categorical embedding appended to encoder output. Used in basic emotional TTS.
- **Spherical emotion vectors (EmoSphere-TTS):** Maps arousal, valence, dominance into a spherical coordinate system via Cartesian-to-spherical transformation. Allows continuous emotion interpolation and intensity control without human annotation. Presented at Interspeech 2024.
- **Rotational emotional embeddings (Marco-Voice):** Integrates emotion information via rotation in the embedding space for smooth, controllable blending.

#### D. Factorized Codec Conditioning (NaturalSpeech 3 / FACodec)

Speech is decomposed into five disentangled subspaces via a factorized neural codec: **content, prosody, timbre, acoustic details, and duration**. Each attribute has its own vector quantizer. Different prompts or conditioning signals can independently control each subspace. This enables swapping emotion/prosody from one utterance while keeping the speaker identity from another.

### 2.3 Training Paradigms

| Approach | How It Works | Examples |
|----------|-------------|----------|
| **Multi-task pre-training** | Train on massive unlabeled speech for general capability, then fine-tune on emotional data | CosyVoice2, VALL-E, NaturalSpeech series |
| **Style/emotion fine-tuning** | Take a pre-trained TTS model and fine-tune on a curated emotional dataset | GPT-SoVITS + emotional corpus, XTTS fine-tuning |
| **Adversarial training** | Use discriminators (sometimes pre-trained SLMs like WavLM) to enforce naturalness and style fidelity | StyleTTS 2 (uses SLM discriminators), EmoSphere-TTS (dual conditional adversarial network) |
| **Contrastive learning** | Learn to separate speaker vs. emotion embeddings by pulling same-emotion, different-speaker pairs together and pushing different-emotion pairs apart | Marco-Voice (in-batch contrastive disentanglement) |
| **Flow matching / diffusion** | Iterative denoising conditioned on text + emotion embeddings produces high-quality, controllable audio | VoiceBox, Marco-Voice (flow matching), StyleTTS 2 (diffusion) |
| **Reinforcement learning from human feedback** | Reward-modulated training guards against timbre drift while maximizing emotional expressiveness | Emerging in 2025; used in some closed-source systems |
| **Three-stage training (IndexTTS2)** | Stage 1: pre-train GPT backbone; Stage 2: fine-tune with emotion conditioning; Stage 3: stabilize with duration control | First AR model combining emotion + duration control |

### 2.4 Disentanglement Techniques (Separating Emotion from Speaker Identity)

This is one of the hardest problems in emotional TTS: changing the emotion should not change who the voice sounds like.

| Technique | Mechanism |
|-----------|-----------|
| **Information bottleneck** | Force each encoder branch to have limited capacity, so it can only encode one attribute (e.g., prosody encoder cannot encode speaker info) |
| **Adversarial classifiers** | Add a gradient-reversal speaker classifier to the emotion encoder; penalize it if emotion representations contain speaker-identifying information |
| **Contrastive learning** | Pull together emotion embeddings from different speakers expressing the same emotion; push apart same-speaker, different-emotion pairs |
| **Mutual information minimization** | Explicitly minimize the mutual information between content, speaker, and emotion latent variables |
| **VQ-VAE tokenization** | Quantize speech into discrete tokens that inherently strip timbre, producing content-style tokens. Used as input to language models |
| **Factorized codecs (FACodec)** | Separate vector quantizers for content, prosody, timbre, and acoustic details with supervised losses for each |

---

## 3. Specific Techniques for Emotion Tones

### 3.1 Happy / Excited

**Acoustic targets:** Raise F0 mean by 20-40%, widen F0 range, increase speaking rate by 10-20%, boost intensity, add brightness (more high-frequency energy).

**Model techniques:**
- StyleTTS 2: Use a "happy" reference clip and the style diffusion module generates matching prosody
- ElevenLabs v3: Tags like `[excited]`, `[cheerfully]`, `[happily]`; also responds to punctuation (exclamation marks)
- Azure SSML: `<mstts:express-as style="cheerful" styledegree="2">` (max expressiveness)
- Fish Audio: `(excited)` or `(happy)` inline markers
- Chatterbox: Increase the emotion exaggeration parameter for more dramatic expression
- Bark: Natural prosody from the GPT-based architecture; happy text context produces happy intonation

### 3.2 Angry

**Acoustic targets:** Raise F0 moderately, flatten spectral tilt (maintain energy across all frequencies), increase intensity to maximum, increase speaking rate, tense voice quality with narrow formant bandwidths.

**Model techniques:**
- EmotiVoice: Prompt with "angry" emotion label
- ElevenLabs v3: `[angry]`, `[frustrated]` tags
- Azure SSML: `<mstts:express-as style="angry">` with `styledegree` up to 2
- Fish Audio: `(angry)` tag
- EmoSphere-TTS: Set high arousal, low valence, high dominance on the spherical vector
- IndexTTS2: Natural language emotion description like "speak with anger and frustration"

### 3.3 Scared / Fearful

**Acoustic targets:** High F0 with wide irregular variability, fast rate, elevated jitter/shimmer (voice tremor), breathy-to-tense phonation, reduced HNR.

**Model techniques:**
- Azure SSML: `<mstts:express-as style="fearful">` (nervous tone) or `<mstts:express-as style="terrified">` (extreme fear with faster pace and shakier voice)
- ElevenLabs v3: `[nervous]`, `[scared]`, `[trembling]` tags
- EmoSphere-TTS: High arousal, low valence, low dominance spherical coordinates
- Reference-audio approaches: Use a fearful reference clip with StyleTTS/XTTS for style transfer
- Fish Audio: `(scared)`, `(nervous)` markers

### 3.4 Whispering

**Acoustic targets:** Remove vocal fold vibration entirely (aperiodic excitation), shift formants, expand formant bandwidths, very low intensity, noise-dominated spectrum.

**Technical challenge:** Whispering is fundamentally different from normal speech because it lacks periodic excitation. Standard vocoders struggle because they assume pitched speech.

**Model techniques:**
- Azure SSML: `<mstts:express-as style="whispering">` -- dedicated whisper style
- ElevenLabs v3: `[whispers]` tag around text passages
- Bark: Can produce whispered speech from context; adding "(whispered)" or similar cues in the text
- Fish Audio S2: `[whisper]` tag
- **WhispSynth** (2026 paper): A dedicated framework for multilingual whispered speech synthesis using a pitch-free generative architecture, specifically designed to handle the absence of F0
- Specialized training: Models need whispered speech in training data (e.g., Expresso dataset has whisper style); without it, models produce "quiet" speech rather than true whisper
- Vocoder considerations: Neural vocoders like HiFi-GAN or BigVGAN must be trained on whispered audio to reproduce the aperiodic excitation correctly

### 3.5 Yelling / Shouting

**Acoustic targets:** Maximum F0 (top of range), maximum intensity, flat spectral tilt, tense/pressed phonation, high vocal effort.

**Technical challenge:** Yelling involves vocal effort beyond the typical training distribution. Most TTS datasets are recorded in studio conditions at conversational levels.

**Model techniques:**
- Azure SSML: `<mstts:express-as style="shouting">` -- sounds distant/loud with effort to be heard
- ElevenLabs v3: `[shouts]` tag
- Fish Audio: `(yelling)` marker
- Chatterbox: High exaggeration parameter combined with emphatic text
- SSML prosody: `<prosody pitch="x-high" rate="fast" volume="x-loud">` approximates yelling acoustically
- Training data: Requires recordings of actual shouted speech; data augmentation via pitch-shifting and loudness boosting can partially compensate but misses the tense phonation quality

---

## 4. Prosody, Intonation Contours, and Rhythm

### 4.1 What Prosody Encompasses

Prosody is the suprasegmental structure of speech -- features that extend beyond individual phonemes:

- **Intonation:** The melody of speech (F0 contours over phrases and sentences)
- **Stress:** Prominence given to specific syllables or words
- **Rhythm:** Timing patterns including syllable durations and inter-stress intervals
- **Phrasing:** Grouping of words into prosodic phrases with boundary tones
- **Pausing:** Duration and placement of silences

### 4.2 Intonation Contours and Emotion

Different emotions produce characteristic F0 contour shapes:

| Emotion | Typical Intonation Contour |
|---------|---------------------------|
| Happy | Wide rising-falling patterns, frequent upward inflections, large excursions |
| Sad | Narrow, flat, gradually descending contour with minimal variation |
| Angry | Sharp, abrupt pitch movements, emphatic downward accents, compressed contour at high register |
| Fear | Erratic, irregular contour with sudden jumps and falls, wide but uncontrolled variation |
| Neutral | Moderate declination with standard accent patterns |

### 4.3 Neural Prosody Modeling Approaches

**Autoregressive prosody prediction:** Models like Tacotron 2 and VALL-E predict prosody implicitly through next-token prediction. The prosody emerges from the learned distribution but is not explicitly controllable.

**Explicit prosody predictors (FastSpeech 2, FastPitch):** Separate prediction heads for pitch, energy, and duration at the phoneme level. Allows direct manipulation but produces "average" prosody without reference conditioning.

**ProsodyFlow:** Integrates large self-supervised speech models (WavLM) with conditional flow matching to model pitch, rhythm, and intonation as continuous distributions. Achieves both naturalness and controllability.

**Sketch-conditioned diffusion (DrawSpeech, 2025):** Users draw rough pitch and energy contours, and a diffusion model reconstructs detailed, natural prosody that follows the sketch. Bridges intuitive control with neural naturalness.

**Hierarchical prosody modeling:** Prosody is modeled at multiple scales -- phoneme-level (duration, local F0), word-level (stress), phrase-level (boundary tones), utterance-level (global emotion/style). Systems like NaturalSpeech 3 factorize these into separate representations.

### 4.4 Why Prosody Remains the Hardest Problem

Prosody covers broad time spans and varies due to many factors: linguistic (syntax, focus), paralinguistic (emotion, attitude), and non-linguistic (speaker identity, physiological state). Most current deep neural TTS systems do not explicitly model prosodic features at all scales, which limits expressiveness. The community consensus (2025) is that prosody modeling remains the critical gap between synthetic and human speech, especially for emotional expression.

---

## 5. SSML and Control Mechanisms for Emotion/Style

### 5.1 W3C SSML Standard (v1.1)

The base W3C SSML standard provides:

```xml
<prosody pitch="high" rate="fast" volume="loud">
  This text is spoken with modified prosody.
</prosody>

<emphasis level="strong">This word</emphasis> is emphasized.

<break time="500ms"/>  <!-- Pause -->
```

The standard `<prosody>` element controls: `pitch` (absolute Hz, relative, or keywords), `rate` (multiplier, percentage, or keywords), `volume` (0-100 or keywords), `contour` (time-pitch pairs for F0 curves), `range` (pitch range).

### 5.2 Microsoft Azure Cognitive Services (Most Extensive SSML Emotion Support)

Azure extends SSML with the `mstts:express-as` element supporting 30+ styles:

```xml
<mstts:express-as style="angry" styledegree="1.5">
  I can't believe you did that!
</mstts:express-as>
```

**Emotion styles:** angry, cheerful, depressed, disgruntled, embarrassed, empathetic, envious, excited, fearful, friendly, gentle, hopeful, sad, serious, terrified, unfriendly

**Functional styles:** advertisement_upbeat, assistant, calm, chat, customerservice, documentary-narration, lyrical, narration-professional, narration-relaxed, newscast, newscast-casual, newscast-formal, poetry-reading, shouting, sports_commentary, sports_commentary_excited, whispering

**Key parameters:**
- `styledegree`: 0.01 to 2.0 (controls intensity; 1.0 = default, 2.0 = doubled expressiveness)
- `role`: Girl, Boy, YoungAdultFemale, YoungAdultMale, OlderAdultFemale, OlderAdultMale, SeniorFemale, SeniorMale (voice imitates different age/gender)

**Prosody contour control:**
```xml
<prosody contour="(0%,+20Hz)(10%,-2st)(40%,+10Hz)">
  Fine-grained pitch contour over the utterance.
</prosody>
```

### 5.3 Amazon Alexa SSML Extensions

```xml
<amazon:emotion name="excited" intensity="medium">
  This is exciting news!
</amazon:emotion>
```

Supports emotions: excited, disappointed. Intensities: low, medium, high.

Also provides `<amazon:domain name="news">` for newscast style and `<amazon:domain name="conversational">` for casual style.

### 5.4 ElevenLabs Audio Tags (v3, 2025)

Not SSML-based but a bracket-tag system that the model interprets contextually:

```
[whispers] I have a secret to tell you.
[excited] Oh my gosh, that's amazing!
[sighs] I guess we'll have to try again.
[hesitant] I... I didn't mean to say that. [regretful] It just came out.
```

**Tag categories:**
- Emotions: `[excited]`, `[nervous]`, `[frustrated]`, `[sorrowful]`, `[calm]`, `[curious]`, `[crying]`, `[mischievously]`
- Delivery: `[whispers]`, `[shouts]`, `[cheerfully]`, `[flatly]`, `[deadpan]`, `[playfully]`
- Reactions: `[sigh]`, `[laughs]`, `[gulps]`, `[gasps]`, `[clears throat]`
- Pacing: `[pause]`, `[rushed]`, `[stammers]`, `[drawn out]`, `[hesitates]`
- Tags can be layered and sequenced for emotional arcs within a passage

### 5.5 Fish Audio Emotion Tags (S1/S2, 2025-2026)

Inline parenthetical markers:
```
(angry) Stop doing that right now!
(whisper) Can you keep a secret?
(chuckling) That's actually pretty funny.
```

S1 supports 50+ markers. S2 Pro supports 15,000+ free-form descriptions at sub-word granularity -- not limited to fixed presets.

### 5.6 Bark Non-Verbal Tokens

Bark uses special tokens embedded in the text:
```
[laughs] That's hilarious!
[sighs] I suppose so...
[clears throat] Attention please.
♪ la la la ♪  (singing)
... (hesitation)
```

### 5.7 Chatterbox Exaggeration Parameter

A single float parameter (0.0 to 1.0+) that scales emotional intensity:
- 0.0: Monotone, flat delivery
- 0.25: Subtle emotion
- 0.5: Natural conversational emotion (default)
- 0.75: Expressive, dramatic
- 1.0+: Highly exaggerated theatrical delivery

---

## 6. Modern Systems Comparison for Emotional Expression

### 6.1 Open-Source Models with Emotion Control

| Model | Params | Emotion Approach | Emotion Control Mechanism | License |
|-------|--------|-----------------|--------------------------|---------|
| **IndexTTS2** (Bilibili) | Large AR | Speaker-emotion disentanglement | Natural language emotion descriptions | Open (Sep 2025) |
| **Marco-Voice** (Alibaba) | Multi-component | Contrastive disentanglement + rotational embeddings | Emotion embedding + voice cloning combined | Open (Aug 2025) |
| **Chatterbox** (Resemble AI) | 500M (Llama-based) | Alignment-informed inference | Exaggeration parameter (0-1+) | MIT (May 2025) |
| **CosyVoice2** (Alibaba) | 0.5B | Improved prosody + emotional alignment | Style conditioning, granular emotion controls | Open |
| **Fish Audio S1/S2** | 4B (S1) | Open-domain fine-grained control | 50+ inline markers (S1), 15K+ tags (S2 Pro) | Open / Commercial |
| **EmotiVoice** (NetEase) | - | Multi-voice prompt-controlled | Text emotion labels + speaker selection | Open |
| **EmoSphere-TTS** | - | Spherical emotion vector | Arousal/valence/dominance coordinates | Open (Interspeech 2024) |
| **StyleTTS 2** | - | Style diffusion + SLM adversarial training | Reference audio style transfer | MIT |
| **Bark** (Suno) | ~1B | GPT-based implicit prosody | Non-verbal tokens, context-driven emotion | MIT |
| **Coqui XTTS v2** | 467M | Zero-shot voice cloning with style transfer | Reference audio emotion/style transfer | Non-commercial |

### 6.2 Commercial / Closed-Source Systems

| Service | Emotion Approach | Control Mechanism |
|---------|-----------------|-------------------|
| **ElevenLabs v3** | Contextual emotion inference + audio tags | Bracket tags, speech-to-speech, text context |
| **Microsoft Azure TTS** | Pre-trained neural voice styles | SSML `express-as` with 30+ styles, `styledegree` 0.01-2 |
| **Amazon Polly** | NTTS with limited emotion support | SSML `amazon:emotion` (excited, disappointed) |
| **Google Cloud TTS** | Standard SSML prosody control | `<prosody>` pitch/rate/volume, limited emotion styles |
| **OpenAI TTS** | Instructions-following model | System prompt descriptions of tone/emotion |

---

## 7. Key Papers and References

| Paper / Resource | Year | Key Contribution |
|-----------------|------|-----------------|
| **"Towards Controllable Speech Synthesis in the Era of LLMs: A Systematic Survey"** (Xu et al.) | 2024 (EMNLP 2025) | First comprehensive survey of controllable TTS; categorizes architectures, control strategies, datasets |
| **NaturalSpeech 3** (Microsoft) | 2024 | FACodec for factorized speech representation (content/prosody/timbre/acoustic details) |
| **StyleTTS 2** (Li et al.) | 2024 | Human-level TTS via style diffusion + SLM adversarial training |
| **EmoSphere-TTS** (Cho et al.) | 2024 (Interspeech) | Spherical emotion vectors for continuous emotion control without annotation |
| **EmoSphere++** | 2024 | Zero-shot emotion-controllable TTS with emotion-adaptive spherical vectors |
| **Marco-Voice** (Alibaba AIDC) | 2025 | Unified voice cloning + emotional synthesis with contrastive disentanglement |
| **IndexTTS2** (Bilibili) | 2025 | First AR model combining emotion + duration control in zero-shot TTS |
| **EmoCtrl-TTS** (Microsoft) | 2024 (SLT) | Time-varying emotional state control within a single utterance |
| **DrawSpeech** | 2025 | User-sketched prosodic contour control via diffusion |
| **WhispSynth** | 2026 | Pitch-free generative framework specifically for whispered speech |
| **Affectron** | 2026 | Affectively aligned nonverbal vocalizations in speech synthesis |
| **"The Sound of Emotional Prosody"** (Larrouy-Maestri et al.) | 2025 | 30-year review of emotional prosody research, future directions |
| **"Neural Synthesis of Expressive and Emotional Speech"** (IIT Bombay survey) | 2024 | Comprehensive survey of neural approaches to expressive TTS |

---

## 8. Practical Recommendations

### For a local/open-source emotional TTS pipeline:

1. **Best all-round emotion control (open-source, 2025-2026):** IndexTTS2 or Marco-Voice for speaker-emotion disentangled synthesis with natural language control.

2. **Easiest emotion integration:** Chatterbox (MIT license, single exaggeration parameter, Llama-based, runs on consumer GPUs).

3. **Finest-grained control:** Fish Audio S2 Pro (15,000+ tag vocabulary at sub-word level).

4. **Best for non-verbal sounds (laughs, sighs, gasps):** Bark (MIT, built-in non-verbal token support) or Chatterbox (supports `[laugh]`, `[cough]` tags).

5. **Best for whisper specifically:** Use Azure SSML `style="whispering"` (commercial) or train/fine-tune a model with whisper data from the Expresso dataset. WhispSynth (2026) provides a dedicated open framework.

6. **Best for style transfer from reference audio:** StyleTTS 2 (MIT) or Coqui XTTS v2 (non-commercial) for zero-shot emotion cloning from a reference clip.

7. **Best SSML control:** Microsoft Azure (30+ styles, intensity control 0.01-2, role-playing, prosody contours).

8. **Lightweight/CPU-friendly:** Kokoro TTS (82M params, Apache 2.0) has limited but improving emotional range; pair with SSML-like prosody manipulation for basic emotion.

### Architecture choice depends on the use case:

- **Game/animation dialogue:** Reference-audio conditioning (StyleTTS 2) or tag-based systems (Fish Audio, ElevenLabs) for per-line emotion direction
- **Audiobooks/narration:** Multi-style models with gradual emotion transitions (Azure express-as with styledegree, CosyVoice2)
- **Real-time conversational AI:** Low-latency models with implicit emotion (CosyVoice2 at 150ms first-packet, Chatterbox Turbo)
- **Research/experimentation:** EmoSphere-TTS for continuous emotion space exploration, NaturalSpeech 3 / FACodec for attribute factorization
