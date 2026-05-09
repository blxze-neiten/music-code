#!/usr/bin/env python3
"""
PRO KARAOKE PLAYER — VS CODE ONE-CLICK RUN
==========================================

Just hit the ▶ Run button in VS Code. No terminal typing needed.
The script auto-finds any .mp3/.wav/.ogg in the same folder.

If it can't find the song, it prints exactly where it looked.
"""

import sys
import os
import argparse
from time import sleep, time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

# AUDIO
try:
    import pygame.mixer
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

console = Console()


# =========================================================
# AUTO-FIND AUDIO (checks multiple places)
# =========================================================
def find_audio_file():
    """
    Search for audio files in this priority order:
    1. Same folder as this .py script
    2. Current working directory (where VS Code runs from)
    3. Any subfolder of the script directory
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cwd = os.getcwd()

    search_paths = [
        ("script folder", script_dir),
        ("VS Code workspace", cwd),
    ]

    # Also check one level deep in script folder
    for entry in os.listdir(script_dir):
        full = os.path.join(script_dir, entry)
        if os.path.isdir(full):
            search_paths.append((f"subfolder '{entry}'", full))

    found = []
    for label, folder in search_paths:
        if not os.path.isdir(folder):
            continue
        for filename in os.listdir(folder):
            if filename.lower().endswith((".mp3", ".wav", ".ogg", ".flac")):
                path = os.path.join(folder, filename)
                found.append((label, path))

    # Return the first match, prioritizing script folder
    if found:
        label, path = found[0]
        console.print(f"[dim]🔍 Found audio in {label}:[/dim] [cyan]{path}[/cyan]")
        return path

    return None


# =========================================================
# TERMINAL
# =========================================================
def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def clear():
    console.clear()


# =========================================================
# HEADER
# =========================================================
def print_header():
    header_text = Text()
    header_text.append("🎤  KARAOKE MODE  🎤\n", style="bold bright_yellow")
    header_text.append("The Black Eyed Peas", style="bold white")
    header_text.append("  —  ", style="dim")
    header_text.append("Rock That Body", style="bold gold3")

    header = Panel.fit(
        Align.center(header_text),
        border_style="bright_magenta",
        box=box.DOUBLE,
        padding=(1, 6),
        title="[dim]♪ ♫ ♪[/dim]",
        subtitle="[dim]♪ ♫ ♪[/dim]",
    )
    console.print(Align.center(header))
    console.print()


# =========================================================
# COLORS
# =========================================================
def get_section_color(section):
    return {
        "intro": "cyan",
        "pre-chorus": "bright_green",
        "chorus": "bright_yellow",
        "verse": "bright_blue",
        "bridge": "bright_magenta",
        "outro": "bright_cyan",
    }.get(section, "white")


# =========================================================
# SECTION HEADER
# =========================================================
def print_section_header(name, color):
    display = name.upper().replace("-", " ")
    panel = Panel(
        f"[bold {color}]{display}[/bold {color}]",
        border_style=color,
        box=box.ROUNDED,
        width=36,
        padding=(0, 2),
    )
    console.print(Align.center(panel))
    sleep(0.3)


# =========================================================
# KARAOKE TYPING
# =========================================================
def type_line(line, char_delay, section):
    """Type a line with karaoke-style coloring."""
    main_style = get_section_color(section)
    is_hook = "Rock that body" in line or "Rock your body" in line

    in_parens = False
    paren_style = "italic magenta"

    for i, char in enumerate(line):
        if char == "(":
            in_parens = True
            end = line.find(")", i)
            paren_content = line[i + 1 : end] if end != -1 else ""
            if "sat upright" in paren_content.lower():
                paren_style = "dim italic bright_red"
            else:
                paren_style = "italic magenta"

        if in_parens:
            style = paren_style
        elif is_hook:
            style = "bold bright_yellow"
        else:
            style = main_style

        console.print(char, end="", style=style)
        sys.stdout.flush()
        sleep(char_delay)

        if char == ")":
            in_parens = False

    console.print()


# =========================================================
# AUDIO SYNC
# =========================================================
class AudioSync:
    def __init__(self, audio_path=None, offset=0.0):
        self.audio_path = audio_path
        self.offset = offset
        self.use_audio = False
        self._start_time = None

        if audio_path and AUDIO_AVAILABLE and os.path.exists(audio_path):
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            self.use_audio = True
            console.print(f"[green]✓ Audio loaded:[/green] [white]{os.path.basename(audio_path)}[/white]\n")
        elif audio_path and not AUDIO_AVAILABLE:
            console.print("[yellow]⚠ pygame not installed.[/yellow]")
            console.print("[bright_white]  pip install pygame[/bright_white]\n")
            sleep(2)
        elif audio_path and not os.path.exists(audio_path):
            console.print(f"[red]⚠ Audio file not found:[/red]\n  {audio_path}\n")
            sleep(2)

    def play(self):
        if self.use_audio:
            pygame.mixer.music.play()
        self._start_time = time()

    def get_pos(self):
        if self.use_audio:
            pos = pygame.mixer.music.get_pos()
            if pos < 0:
                pos = 0
            return (pos / 1000.0) + self.offset
        return (time() - self._start_time) + self.offset if self._start_time else 0.0

    def is_playing(self):
        if self.use_audio:
            return pygame.mixer.music.get_busy()
        return True


# =========================================================
# MAIN PLAYER
# =========================================================
def play_lyrics(audio_path=None, offset=0.0):
    lyrics = [
        # INTRO
        (1.2, "I wanna rock right now", 0.07, "intro"),
        (3.2, "I wanna, I wanna rock right now", 0.06, "intro"),
        (5.5, "I wanna, I wanna rock right now, now, now, rock right now", 0.055, "intro"),
        (8.7, "I wanna, I wanna rock right now", 0.06, "intro"),
        (10.8, "I wanna, I wanna rock right now", 0.06, "intro"),
        (12.8, "I wanna, I wanna rock right now", 0.06, "intro"),

        # PRE-CHORUS
        (14.8, "I wanna da-, I wanna dance in the lights", 0.06, "pre-chorus"),
        (16.9, "I wanna ro-, I wanna rock your body", 0.06, "pre-chorus"),
        (18.9, "I wanna go, I wanna go for a ride", 0.06, "pre-chorus"),
        (21.0, "Hop in the music and rock your body right", 0.065, "pre-chorus"),

        # CHORUS
        (29.8, "Rock that body, come on, come on, rock that body (rock your body)", 0.05, "chorus"),
        (32.5, "Rock that body, come on, come on, rock that body", 0.05, "chorus"),
        (35.0, "Rock that body, come on, come on, rock that body (rock your body)", 0.05, "chorus"),
        (37.7, "Rock that body, come on, come on, rock that body", 0.05, "chorus"),

        # VERSE
        (58.0, "Let me see your body rock", 0.06, "verse"),
        (59.8, "Shakin' it from the bottom to top", 0.06, "verse"),
        (61.5, "Freak to what the DJ drop", 0.06, "verse"),
        (63.2, "We be the ones to make it hot (to make it hot)", 0.055, "verse"),
        (65.0, "Electric shock, energy like a billion watts", 0.055, "verse"),
        (67.2, "Space be booming, the speakers pop", 0.055, "verse"),
        (69.0, "Galactic, call me Mr. Spock", 0.055, "verse"),
        (70.8, "We bumpin' in your parking lot", 0.055, "verse"),
        (72.4, "When you're comin' up in the spot", 0.055, "verse"),
        (74.0, "Don't bring nothin' we call Pink Dot", 0.055, "verse"),
        (75.8, "'Cause we burnin' around the clock", 0.055, "verse"),
        (77.5, "Hit the lights and then turn them off", 0.055, "verse"),
        (79.0, "If you bring that, don't make you stop", 0.055, "verse"),
        (80.5, "Like the jungle, we run the block", 0.055, "verse"),
        (82.0, "No one rollin' the way we rock, way we rock", 0.05, "verse"),

        # PRE-CHORUS
        (87.0, "I wanna, I wanna rock right now", 0.06, "pre-chorus"),
        (88.5, "I wanna, I wanna rock right now", 0.06, "pre-chorus"),
        (90.0, "I wanna, I wanna rock right now", 0.06, "pre-chorus"),
        (91.5, "I wanna da-, I wanna dance in the lights", 0.06, "pre-chorus"),
        (93.0, "I wanna ro-, I wanna rock your body", 0.06, "pre-chorus"),
        (94.5, "I wanna go, I wanna go for a ride", 0.06, "pre-chorus"),
        (96.0, "Hop in the music and rock your body right", 0.065, "pre-chorus"),

        # CHORUS
        (102.0, "Rock that body, come on, come on, rock that body (rock that body)", 0.05, "chorus"),
        (104.5, "Rock that body, come on, come on, rock that body", 0.05, "chorus"),
        (107.0, "Rock that body, come on, come on, rock that body (rock your body)", 0.05, "chorus"),
        (109.5, "Rock that body, come on, come on, rock that body", 0.05, "chorus"),

        # BRIDGE
        (132.0, "Superfly ladies, all of my superfly ladies", 0.06, "bridge"),
        (134.0, "All of my superfly ladies", 0.06, "bridge"),
        (136.0, "All of my superf-, superfly ladies", 0.06, "bridge"),
        (138.5, "Yeah, you could be big bone, large, you feel like you own", 0.055, "bridge"),
        (141.0, "You could be the model type, skinny with no appetite", 0.055, "bridge"),
        (143.5, "Short stack, black or white", 0.06, "bridge"),
        (145.0, "Long as you do what you like", 0.06, "bridge"),
        (146.5, "Body outta sight, body, body outta sight (yeah)", 0.055, "bridge"),
        (149.0, "She does the two-step and the tongue drop", 0.06, "bridge"),
        (151.0, "She does the cabbage patch and the bus stop", 0.06, "bridge"),
        (153.0, "She like electro (electro), she wrote hip-hop (hip-hop)", 0.055, "bridge"),
        (155.0, "She like the reggae, she feel punk rock (punk rock)", 0.055, "bridge"),
        (157.0, "She love samba and the mambo", 0.06, "bridge"),
        (159.0, "She like to breakdance and calypso (oh)", 0.06, "bridge"),
        (161.0, "Get a lil' crazy, get a lil' stupid", 0.06, "bridge"),
        (163.5, "Get a lil' crazy, crazy, crazy", 0.055, "bridge"),

        # PRE-CHORUS
        (165.0, "I wanna da-, I wanna dance in the lights (I wanna dance in the lights)", 0.06, "pre-chorus"),
        (167.0, "I wanna ro-, I wanna rock your body right (rock your body)", 0.06, "pre-chorus"),
        (169.0, "I wanna go, I wanna go for a ride (you wanna go for a ride)", 0.06, "pre-chorus"),
        (171.0, "Hop in the music and rock your body right", 0.065, "pre-chorus"),
        (173.0, "Rock your body right", 0.07, "pre-chorus"),
        (174.5, "(Sat upright)", 0.08, "pre-chorus"),
        (176.0, "Rock your body right", 0.07, "pre-chorus"),
        (177.5, "Come on, yeah", 0.06, "pre-chorus"),

        # CHORUS
        (179.5, "Rock that body, come on, come on, rock that body", 0.05, "chorus"),
        (181.5, "Come on, yeah", 0.06, "chorus"),
        (183.5, "Rock that body, come on, come on, rock that body", 0.05, "chorus"),

        # OUTRO
        (192.0, "Go, oh, oh, oh, oh-oh-oh", 0.05, "outro"),
        (194.5, "Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro"),
        (197.0, "Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro"),
        (199.5, "Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro"),
        (202.0, "I wanna, I wanna rock right now", 0.06, "outro"),
        (204.0, "I wanna, I wanna rock- (sat upright)", 0.06, "outro"),
        (206.0, "I wanna, I wanna rock-", 0.06, "outro"),
        (208.0, "Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro"),
        (210.0, "I wanna, I wanna rock- (sat upright)", 0.06, "outro"),
        (212.0, "I wanna, I wanna rock-", 0.06, "outro"),
        (214.0, "Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro"),
        (216.5, "Let's go, oh, oh, oh, oh-oh-oh (sat upright)", 0.05, "outro"),
        (219.0, "I wanna, I wanna rock right now", 0.06, "outro"),
        (221.0, "I wanna, I wanna rock right now", 0.06, "outro"),
        (223.0, "I wanna, I wanna rock right now, now, now, rock right now", 0.055, "outro"),
        (226.0, "I wanna, I wanna rock right now", 0.06, "outro"),
        (228.0, "I wanna, I wanna rock right now", 0.06, "outro"),
        (230.0, "I wanna, I wanna rock right now", 0.06, "outro"),
    ]

    audio = AudioSync(audio_path, offset)

    hide_cursor()
    clear()
    print_header()

    # COUNTDOWN
    for i in range(3, 0, -1):
        clear()
        print_header()
        countdown = Panel.fit(
            f"[bold bright_red]{i}[/bold bright_red]",
            border_style="bright_red",
            box=box.DOUBLE,
            padding=(1, 5),
        )
        console.print(Align.center(countdown))
        sleep(1)

    clear()
    print_header()

    if audio.use_audio:
        console.print("[dim]🎵 Starting music...[/dim]\n")
    else:
        console.print("[dim]🎵 Demo mode (no audio)...[/dim]\n")

    sleep(0.5)

    current_section = None
    audio.play()

    try:
        for timestamp, line, char_delay, section in lyrics:
            while audio.get_pos() < timestamp:
                if not audio.is_playing() and audio.use_audio:
                    break
                sleep(0.005)

            if section != current_section:
                current_section = section
                print_section_header(section, get_section_color(section))

            console.print("[bold bright_green]▶ [/bold bright_green]", end="")
            type_line(line, char_delay, section)

        if audio.use_audio:
            while audio.is_playing():
                sleep(0.1)

    except KeyboardInterrupt:
        if audio.use_audio:
            pygame.mixer.music.stop()
        console.print("\n[dim]Stopped.[/dim]")

    finally:
        show_cursor()
        end = Panel.fit(
            "[bold bright_yellow]🎵 Thanks for singing! 🎵[/bold bright_yellow]",
            border_style="bright_green",
            box=box.DOUBLE,
            padding=(1, 4),
        )
        console.print("\n")
        console.print(Align.center(end))


# =========================================================
# MAIN — zero config needed
# =========================================================
def main():
    parser = argparse.ArgumentParser(description="PRO Karaoke Player")
    parser.add_argument(
        "--audio",
        "-a",
        type=str,
        default=None,
        help="Path to audio file (optional — auto-detected if omitted)",
    )
    parser.add_argument(
        "--offset",
        "-o",
        type=float,
        default=0.0,
        help="Timing offset in seconds (positive = delay lyrics)",
    )
    args = parser.parse_args()

    # If user passed --audio, use it. Otherwise auto-find.
    audio_path = args.audio
    if not audio_path:
        audio_path = find_audio_file()

    if not audio_path:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        console.print("[red]❌ No audio file found.[/red]")
        console.print(f"[dim]   Searched in:[/dim] [cyan]{script_dir}[/cyan]")
        console.print("[dim]   Please place an .mp3, .wav, or .ogg in the same folder as this script.[/dim]")
        sys.exit(1)

    play_lyrics(audio_path=audio_path, offset=args.offset)


if __name__ == "__main__":
    main()