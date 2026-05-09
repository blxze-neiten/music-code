import sys
from time import sleep
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()


def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def clear():
    console.clear()


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


def get_section_color(section):
    return {
        "intro": "cyan",
        "pre-chorus": "bright_green",
        "chorus": "bright_yellow",
        "verse": "bright_blue",
        "bridge": "bright_magenta",
        "outro": "bright_cyan",
    }.get(section, "white")


def type_line(line, char_delay, section):
    """Type a line with karaoke-style coloring. Handles inline parenthetical vocals."""
    main_style = get_section_color(section)

    # Highlight the whole line when it contains the main hook
    is_hook = "Rock that body" in line or "Rock your body" in line

    in_parens = False
    paren_style = "italic magenta"

    for i, char in enumerate(line):
        # Detect start of parenthetical section to choose the right paren style
        if char == "(":
            in_parens = True
            end = line.find(")", i)
            paren_content = line[i + 1 : end] if end != -1 else ""
            if "sat upright" in paren_content.lower():
                paren_style = "dim italic bright_red"
            else:
                paren_style = "italic magenta"

        # Choose style for this character
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


def print_section_header(name, color):
    display = name.upper().replace("-", " ")
    panel = Panel(
        f"[bold {color}]{display}[/bold {color}]",
        border_style=color,
        box=box.ROUNDED,
        width=34,
        padding=(0, 2),
    )
    console.print(Align.center(panel))
    sleep(0.3)


def play_lyrics():
    # Format: (lyric_line, char_delay, section_tag, line_delay_after)
    lyrics = [
        # INTRO
        ("I wanna rock right now", 0.07, "intro", 0.3),
        ("I wanna, I wanna rock right now", 0.06, "intro", 0.3),
        ("I wanna, I wanna rock right now, now, now, rock right now", 0.055, "intro", 0.9),
        ("I wanna, I wanna rock right now", 0.06, "intro", 0.25),
        ("I wanna, I wanna rock right now", 0.06, "intro", 0.25),
        ("I wanna, I wanna rock right now", 0.06, "intro", 0.7),
        # PRE-CHORUS
        ("I wanna da-, I wanna dance in the lights", 0.06, "pre-chorus", 0.2),
        ("I wanna ro-, I wanna rock your body", 0.06, "pre-chorus", 0.2),
        ("I wanna go, I wanna go for a ride", 0.06, "pre-chorus", 0.2),
        ("Hop in the music and rock your body right", 0.065, "pre-chorus", 0.6),
        # CHORUS
        ("Rock that body, come on, come on, rock that body (rock your body)", 0.05, "chorus", 0.35),
        ("Rock that body, come on, come on, rock that body", 0.05, "chorus", 0.35),
        ("Rock that body, come on, come on, rock that body (rock your body)", 0.05, "chorus", 0.35),
        ("Rock that body, come on, come on, rock that body", 0.05, "chorus", 1.0),
        # VERSE
        ("Let me see your body rock", 0.06, "verse", 0.25),
        ("Shakin' it from the bottom to top", 0.06, "verse", 0.25),
        ("Freak to what the DJ drop", 0.06, "verse", 0.25),
        ("We be the ones to make it hot (to make it hot)", 0.055, "verse", 0.45),
        ("Electric shock, energy like a billion watts", 0.055, "verse", 0.25),
        ("Space be booming, the speakers pop", 0.055, "verse", 0.25),
        ("Galactic, call me Mr. Spock", 0.055, "verse", 0.25),
        ("We bumpin' in your parking lot", 0.055, "verse", 0.25),
        ("When you're comin' up in the spot", 0.055, "verse", 0.25),
        ("Don't bring nothin' we call Pink Dot", 0.055, "verse", 0.25),
        ("'Cause we burnin' around the clock", 0.055, "verse", 0.25),
        ("Hit the lights and then turn them off", 0.055, "verse", 0.25),
        ("If you bring that, don't make you stop", 0.055, "verse", 0.25),
        ("Like the jungle, we run the block", 0.055, "verse", 0.25),
        ("No one rollin' the way we rock, way we rock", 0.05, "verse", 1.0),
        # PRE-CHORUS
        ("I wanna, I wanna rock right now", 0.06, "pre-chorus", 0.25),
        ("I wanna, I wanna rock right now", 0.06, "pre-chorus", 0.25),
        ("I wanna, I wanna rock right now", 0.06, "pre-chorus", 0.25),
        ("I wanna da-, I wanna dance in the lights", 0.06, "pre-chorus", 0.2),
        ("I wanna ro-, I wanna rock your body", 0.06, "pre-chorus", 0.2),
        ("I wanna go, I wanna go for a ride", 0.06, "pre-chorus", 0.2),
        ("Hop in the music and rock your body right", 0.065, "pre-chorus", 0.6),
        # CHORUS
        ("Rock that body, come on, come on, rock that body (rock that body)", 0.05, "chorus", 0.35),
        ("Rock that body, come on, come on, rock that body", 0.05, "chorus", 0.35),
        ("Rock that body, come on, come on, rock that body (rock your body)", 0.05, "chorus", 0.35),
        ("Rock that body, come on, come on, rock that body", 0.05, "chorus", 1.0),
        # BRIDGE
        ("Superfly ladies, all of my superfly ladies", 0.06, "bridge", 0.3),
        ("All of my superfly ladies", 0.06, "bridge", 0.3),
        ("All of my superf-, superfly ladies", 0.06, "bridge", 0.6),
        ("Yeah, you could be big bone, large, you feel like you own", 0.055, "bridge", 0.3),
        ("You could be the model type, skinny with no appetite", 0.055, "bridge", 0.3),
        ("Short stack, black or white", 0.06, "bridge", 0.25),
        ("Long as you do what you like", 0.06, "bridge", 0.25),
        ("Body outta sight, body, body outta sight (yeah)", 0.055, "bridge", 0.45),
        ("She does the two-step and the tongue drop", 0.06, "bridge", 0.25),
        ("She does the cabbage patch and the bus stop", 0.06, "bridge", 0.25),
        ("She like electro (electro), she wrote hip-hop (hip-hop)", 0.055, "bridge", 0.3),
        ("She like the reggae, she feel punk rock (punk rock)", 0.055, "bridge", 0.3),
        ("She love samba and the mambo", 0.06, "bridge", 0.25),
        ("She like to breakdance and calypso (oh)", 0.06, "bridge", 0.3),
        ("Get a lil' crazy, get a lil' stupid", 0.06, "bridge", 0.25),
        ("Get a lil' crazy, crazy, crazy", 0.055, "bridge", 0.8),
        # PRE-CHORUS
        ("I wanna da-, I wanna dance in the lights (I wanna dance in the lights)", 0.06, "pre-chorus", 0.3),
        ("I wanna ro-, I wanna rock your body right (rock your body)", 0.06, "pre-chorus", 0.3),
        ("I wanna go, I wanna go for a ride (you wanna go for a ride)", 0.06, "pre-chorus", 0.3),
        ("Hop in the music and rock your body right", 0.065, "pre-chorus", 0.45),
        ("Rock your body right", 0.07, "pre-chorus", 0.3),
        ("(Sat upright)", 0.08, "pre-chorus", 0.45),
        ("Rock your body right", 0.07, "pre-chorus", 0.3),
        ("Come on, yeah", 0.06, "pre-chorus", 0.45),
        # CHORUS
        ("Rock that body, come on, come on, rock that body", 0.05, "chorus", 0.35),
        ("Come on, yeah", 0.06, "chorus", 0.35),
        ("Rock that body, come on, come on, rock that body", 0.05, "chorus", 0.8),
        # OUTRO
        ("Go, oh, oh, oh, oh-oh-oh", 0.05, "outro", 0.25),
        ("Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro", 0.25),
        ("Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro", 0.25),
        ("Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro", 0.6),
        ("I wanna, I wanna rock right now", 0.06, "outro", 0.3),
        ("I wanna, I wanna rock- (sat upright)", 0.06, "outro", 0.3),
        ("I wanna, I wanna rock-", 0.06, "outro", 0.3),
        ("Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro", 0.25),
        ("I wanna, I wanna rock- (sat upright)", 0.06, "outro", 0.3),
        ("I wanna, I wanna rock-", 0.06, "outro", 0.3),
        ("Let's go, oh, oh, oh, oh-oh-oh", 0.05, "outro", 0.25),
        ("Let's go, oh, oh, oh, oh-oh-oh (sat upright)", 0.05, "outro", 1.0),
        ("I wanna, I wanna rock right now", 0.06, "outro", 0.25),
        ("I wanna, I wanna rock right now", 0.06, "outro", 0.25),
        ("I wanna, I wanna rock right now, now, now, rock right now", 0.055, "outro", 0.9),
        ("I wanna, I wanna rock right now", 0.06, "outro", 0.25),
        ("I wanna, I wanna rock right now", 0.06, "outro", 0.25),
        ("I wanna, I wanna rock right now", 0.06, "outro", 4.0),
    ]

    hide_cursor()
    clear()
    print_header()

    current_section = None

    try:
        for line, char_delay, section, line_delay in lyrics:
            # Show section banner when section changes
            if section != current_section:
                current_section = section
                print_section_header(section, get_section_color(section))

            # Karaoke play indicator
            console.print("[bold bright_green]▶ [/bold bright_green]", end="")

            # Type the line with smart coloring
            type_line(line, char_delay, section)

            # Pause before next line
            sleep(line_delay)

    except KeyboardInterrupt:
        console.print("\n[dim]Stopped.[/dim]")
    finally:
        show_cursor()
        # End screen
        end = Panel.fit(
            "[bold bright_yellow]🎵 Thanks for singing! 🎵[/bold bright_yellow]",
            border_style="bright_green",
            box=box.DOUBLE,
            padding=(1, 4),
        )
        console.print("\n")
        console.print(Align.center(end))


if __name__ == "__main__":
    play_lyrics()