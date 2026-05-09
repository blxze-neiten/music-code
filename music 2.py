import sys
from time import sleep
from rich import print

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def play_lyrics():
    lines = [
        # Intro
        "I wanna rock right now",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now, now, now, rock right now",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now",
        # Pre-chorus
        "I wanna da-, I wanna dance in the lights",
        "I wanna ro-, I wanna rock your body",
        "I wanna go, I wanna go for a ride",
        "Hop in the music and rock your body right",
        # Chorus
        "Rock that body, come on, come on, rock that body (rock your body)",
        "Rock that body, come on, come on, rock that body",
        "Rock that body, come on, come on, rock that body (rock your body)",
        "Rock that body, come on, come on, rock that body",
        # Verse
        "Let me see your body rock",
        "Shakin' it from the bottom to top",
        "Freak to what the DJ drop",
        "We be the ones to make it hot (to make it hot)",
        "Electric shock, energy like a billion watts",
        "Space be booming, the speakers pop",
        "Galactic, call me Mr. Spock",
        "We bumpin' in your parking lot",
        "When you're comin' up in the spot",
        "Don't bring nothin' we call Pink Dot",
        "'Cause we burnin' around the clock",
        "Hit the lights and then turn them off",
        "If you bring that, don't make you stop",
        "Like the jungle, we run the block",
        "No one rollin' the way we rock, way we rock",
        # Pre-chorus
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now",
        "I wanna da-, I wanna dance in the lights",
        "I wanna ro-, I wanna rock your body",
        "I wanna go, I wanna go for a ride",
        "Hop in the music and rock your body right",
        # Chorus
        "Rock that body, come on, come on, rock that body (rock that body)",
        "Rock that body, come on, come on, rock that body",
        "Rock that body, come on, come on, rock that body (rock your body)",
        "Rock that body, come on, come on, rock that body",
        # Bridge
        "Superfly ladies, all of my superfly ladies",
        "All of my superfly ladies",
        "All of my superf-, superfly ladies",
        "Yeah, you could be big bone, large, you feel like you own",
        "You could be the model type, skinny with no appetite",
        "Short stack, black or white",
        "Long as you do what you like",
        "Body outta sight, body, body outta sight (yeah)",
        "She does the two-step and the tongue drop",
        "She does the cabbage patch and the bus stop",
        "She like electro (electro), she wrote hip-hop (hip-hop)",
        "She like the reggae, she feel punk rock (punk rock)",
        "She love samba and the mambo",
        "She like to breakdance and calypso (oh)",
        "Get a lil' crazy, get a lil' stupid",
        "Get a lil' crazy, crazy, crazy",
        # Pre-chorus
        "I wanna da-, I wanna dance in the lights (I wanna dance in the lights)",
        "I wanna ro-, I wanna rock your body right (rock your body)",
        "I wanna go, I wanna go for a ride (you wanna go for a ride)",
        "Hop in the music and rock your body right",
        "Rock your body right",
        "(Sat upright)",
        "Rock your body right",
        "Come on, yeah",
        # Chorus
        "Rock that body, come on, come on, rock that body",
        "Come on, yeah",
        "Rock that body, come on, come on, rock that body",
        # Outro
        "Go, oh, oh, oh, oh-oh-oh",
        "Let's go, oh, oh, oh, oh-oh-oh",
        "Let's go, oh, oh, oh, oh-oh-oh",
        "Let's go, oh, oh, oh, oh-oh-oh",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock- (sat upright)",
        "I wanna, I wanna rock-",
        "Let's go, oh, oh, oh, oh-oh-oh",
        "I wanna, I wanna rock- (sat upright)",
        "I wanna, I wanna rock-",
        "Let's go, oh, oh, oh, oh-oh-oh",
        "Let's go, oh, oh, oh, oh-oh-oh (sat upright)",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now, now, now, rock right now",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now",
        "I wanna, I wanna rock right now",
    ]

    char_delays = [
        # Intro
        0.07, 0.06, 0.055, 0.06, 0.06, 0.06,
        # Pre-chorus
        0.06, 0.06, 0.06, 0.065,
        # Chorus
        0.05, 0.05, 0.05, 0.05,
        # Verse
        0.06, 0.06, 0.06, 0.055, 0.055, 0.055, 0.055, 0.055,
        0.055, 0.055, 0.055, 0.055, 0.055, 0.055, 0.05,
        # Pre-chorus
        0.06, 0.06, 0.06, 0.06, 0.06, 0.06, 0.065,
        # Chorus
        0.05, 0.05, 0.05, 0.05,
        # Bridge
        0.06, 0.06, 0.06, 0.055, 0.055, 0.06, 0.06, 0.055,
        0.06, 0.06, 0.055, 0.055, 0.06, 0.06, 0.06, 0.055,
        # Pre-chorus
        0.06, 0.06, 0.06, 0.065, 0.07, 0.08, 0.07, 0.06,
        # Chorus
        0.05, 0.05, 0.05,
        # Outro
        0.05, 0.05, 0.05, 0.05, 0.06, 0.06, 0.06, 0.05,
        0.06, 0.06, 0.05, 0.05, 0.06, 0.06, 0.055, 0.06,
        0.06, 0.06,
    ]

    delays = [
        # Intro
        0.3, 0.3, 0.8, 0.25, 0.25, 0.6,
        # Pre-chorus
        0.2, 0.2, 0.2, 0.5,
        # Chorus
        0.3, 0.3, 0.3, 0.8,
        # Verse
        0.25, 0.25, 0.25, 0.4, 0.25, 0.25, 0.25, 0.25,
        0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.8,
        # Pre-chorus
        0.25, 0.25, 0.25, 0.2, 0.2, 0.2, 0.5,
        # Chorus
        0.3, 0.3, 0.3, 0.8,
        # Bridge
        0.3, 0.3, 0.5, 0.3, 0.3, 0.25, 0.25, 0.4,
        0.25, 0.25, 0.3, 0.3, 0.25, 0.3, 0.25, 0.6,
        # Pre-chorus
        0.3, 0.3, 0.3, 0.4, 0.3, 0.4, 0.3, 0.4,
        # Chorus
        0.3, 0.3, 0.6,
        # Outro
        0.25, 0.25, 0.25, 0.5, 0.3, 0.3, 0.3, 0.25,
        0.3, 0.3, 0.25, 0.5, 0.25, 0.25, 0.8, 0.25,
        0.25, 3.0,
    ]

    hide_cursor()

    try:
        for i, line in enumerate(lines):
            in_parens = False
            for char in line:
                if char == "(":
                    in_parens = True

                if in_parens:
                    print(f"[orange4]{char}[/orange4]", end='')
                else:
                    print(f"[bold][gold3]{char}[/bold][/gold3]", end='')

                if char == ")":
                    in_parens = False

                sys.stdout.flush()
                sleep(char_delays[i])
            print()  # New line after each lyric
            sleep(delays[i])  # Delay after each line
    finally:
        show_cursor()

play_lyrics()