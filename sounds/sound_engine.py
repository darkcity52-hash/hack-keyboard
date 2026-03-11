# sounds/sound_engine.py — Motor de sonidos futuristas generados por código

import threading
import math
import struct
import wave
import io
import os
import tempfile

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import winsound
    PLATFORM = "windows"
except ImportError:
    PLATFORM = "unix"

# ── Generador de ondas ────────────────────────────────────────────────────────

def _generate_wave(freq, duration, sample_rate=44100, wave_type="square",
                   volume=0.4, decay=True):
    """Genera samples PCM de una onda futurista."""
    if not HAS_NUMPY:
        return None
    n = int(sample_rate * duration)
    t = np.linspace(0, duration, n, endpoint=False)
    if wave_type == "square":
        wave = np.sign(np.sin(2 * np.pi * freq * t))
    elif wave_type == "sawtooth":
        wave = 2 * (t * freq - np.floor(t * freq + 0.5))
    elif wave_type == "sine":
        wave = np.sin(2 * np.pi * freq * t)
    elif wave_type == "noise_burst":
        wave = np.random.uniform(-1, 1, n)
    else:
        wave = np.sin(2 * np.pi * freq * t)

    if decay:
        envelope = np.exp(-t * (6.0 / duration))
        wave = wave * envelope

    wave = (wave * volume * 32767).astype(np.int16)
    return wave


def _mix_waves(waves):
    """Mezcla múltiples ondas sumándolas."""
    if not waves:
        return None
    max_len = max(len(w) for w in waves)
    mixed = np.zeros(max_len, dtype=np.float64)
    for w in waves:
        mixed[:len(w)] += w.astype(np.float64)
    mixed = np.clip(mixed, -32767, 32767).astype(np.int16)
    return mixed


def _to_wav_bytes(samples, sample_rate=44100):
    """Convierte samples int16 a bytes WAV en memoria."""
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())
    return buf.getvalue()


def _play_wav_bytes(wav_bytes):
    """Reproduce bytes WAV en un hilo separado."""
    if PLATFORM == "windows":
        threading.Thread(
            target=winsound.PlaySound,
            args=(wav_bytes, winsound.SND_MEMORY),
            daemon=True
        ).start()
    else:
        # Linux/Mac: guardar temp y reproducir con aplay/afplay
        def _play():
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(wav_bytes)
                fname = f.name
            if os.system(f"aplay -q {fname} 2>/dev/null") != 0:
                os.system(f"afplay {fname} 2>/dev/null")
            os.unlink(fname)
        threading.Thread(target=_play, daemon=True).start()


# ── Sonidos predefinidos ──────────────────────────────────────────────────────

def _sound_key_click():
    """Click mecánico con eco digital — tecla normal."""
    if not HAS_NUMPY:
        return
    w1 = _generate_wave(880,  0.04, wave_type="square",   volume=0.35, decay=True)
    w2 = _generate_wave(440,  0.06, wave_type="sawtooth", volume=0.15, decay=True)
    w3 = _generate_wave(1760, 0.02, wave_type="sine",     volume=0.10, decay=True)
    mixed = _mix_waves([w1, w2, w3])
    _play_wav_bytes(_to_wav_bytes(mixed))


def _sound_enter():
    """Sonido de confirmación — arpeggio ascendente."""
    if not HAS_NUMPY:
        return
    sr = 44100
    total = int(sr * 0.18)
    out = np.zeros(total, dtype=np.float64)
    freqs = [523, 659, 784, 1047]
    offset = 0
    step = total // len(freqs)
    for f in freqs:
        w = _generate_wave(f, 0.08, wave_type="sine", volume=0.3, decay=True)
        end = min(offset + len(w), total)
        out[offset:end] += w[:end-offset].astype(np.float64)
        offset += step
    out = np.clip(out, -32767, 32767).astype(np.int16)
    _play_wav_bytes(_to_wav_bytes(out))


def _sound_backspace():
    """Sonido de borrado — descenso rápido."""
    if not HAS_NUMPY:
        return
    w1 = _generate_wave(300, 0.07, wave_type="sawtooth", volume=0.3, decay=True)
    w2 = _generate_wave(150, 0.05, wave_type="square",   volume=0.2, decay=True)
    mixed = _mix_waves([w1, w2])
    _play_wav_bytes(_to_wav_bytes(mixed))


def _sound_space():
    """Sonido de espacio — whoosh suave."""
    if not HAS_NUMPY:
        return
    sr = 44100
    dur = 0.09
    n = int(sr * dur)
    t = np.linspace(0, dur, n)
    # Frecuencia que baja (sweep descendente)
    freq_sweep = 600 * np.exp(-t * 8)
    phase = 2 * np.pi * np.cumsum(freq_sweep) / sr
    wave = np.sin(phase)
    envelope = np.exp(-t * 10)
    wave = (wave * envelope * 0.35 * 32767).astype(np.int16)
    _play_wav_bytes(_to_wav_bytes(wave))


def _sound_modifier():
    """Sonido de tecla modificadora (Ctrl, Alt, Shift)."""
    if not HAS_NUMPY:
        return
    w1 = _generate_wave(1200, 0.03, wave_type="square", volume=0.2, decay=True)
    w2 = _generate_wave(600,  0.05, wave_type="sine",   volume=0.15, decay=True)
    mixed = _mix_waves([w1, w2])
    _play_wav_bytes(_to_wav_bytes(mixed))


def _sound_shortcut():
    """Sonido de atajo activado — electrónico rápido."""
    if not HAS_NUMPY:
        return
    sr = 44100
    total = int(sr * 0.12)
    out = np.zeros(total, dtype=np.float64)
    for i, f in enumerate([1046, 1318, 1568]):
        w = _generate_wave(f, 0.06, wave_type="sine", volume=0.25, decay=True)
        offset = i * int(sr * 0.03)
        end = min(offset + len(w), total)
        out[offset:end] += w[:end-offset].astype(np.float64)
    out = np.clip(out, -32767, 32767).astype(np.int16)
    _play_wav_bytes(_to_wav_bytes(out))


def _sound_error():
    """Sonido de error — buzz grave."""
    if not HAS_NUMPY:
        return
    w1 = _generate_wave(120, 0.15, wave_type="square",   volume=0.4, decay=True)
    w2 = _generate_wave(60,  0.15, wave_type="sawtooth", volume=0.2, decay=True)
    mixed = _mix_waves([w1, w2])
    _play_wav_bytes(_to_wav_bytes(mixed))


# ── API pública ───────────────────────────────────────────────────────────────

SOUND_MAP = {
    "key":       _sound_key_click,
    "enter":     _sound_enter,
    "backspace":  _sound_backspace,
    "space":     _sound_space,
    "modifier":  _sound_modifier,
    "shortcut":  _sound_shortcut,
    "error":     _sound_error,
}

_enabled = True

def set_enabled(val: bool):
    global _enabled
    _enabled = val

def play(sound_name: str):
    """Reproduce un sonido si está habilitado."""
    if not _enabled:
        return
    fn = SOUND_MAP.get(sound_name)
    if fn:
        threading.Thread(target=fn, daemon=True).start()
