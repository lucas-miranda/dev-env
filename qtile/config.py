import os, subprocess
from libqtile.config import Key, Screen, Group, Match, Click, Drag
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

#

audio_card_id = 0

# media

def is_spotify_running():
    spotify_processes_b = subprocess.run(["pgrep", "-x", "spotify"], capture_output=True)
    spotify_processes = spotify_processes_b.stdout.decode("utf-8")
    return len(spotify_processes) > 0

def media_playpause(qtile):
    if is_spotify_running():
        qtile.cmd_spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")

def media_next(qtile):
    if not is_spotify_running():
        return

    qtile.cmd_spawn('dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next')

def media_previous(qtile):
    if not is_spotify_running():
        return

    qtile.cmd_spawn('dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous')

# desktop

def set_wallpaper(path):
    os.system('feh --bg-scale %s' % path)

#

super_key = "mod4"
alt_key = "mod1"

keys = [
    Key([super_key], "r", lazy.spawncmd()),
    Key([super_key, alt_key], "Delete", lazy.shutdown()),
    Key([super_key, alt_key], "Insert", lazy.restart()), # reload qtile configs

    # groups
    Key([super_key, "shift"], "Right", lazy.screen.next_group()),
    Key([super_key, "shift"], "Left", lazy.screen.prev_group()),

    # layout
    Key([alt_key], "Tab", lazy.layout.next()),
    Key([super_key], "h", lazy.layout.left()),
    Key([super_key], "l", lazy.layout.right()),
    Key([super_key], "j", lazy.layout.up()),
    Key([super_key], "k", lazy.layout.down()),
    Key([super_key, "shift"], "h", lazy.layout.swap_left()),
    Key([super_key, "shift"], "l", lazy.layout.swap_right()),
    Key([super_key, "shift"], "j", lazy.layout.shuffle_down()),
    Key([super_key, "shift"], "k", lazy.layout.shuffle_up()),
    Key([super_key], "i", lazy.layout.grow()),
    Key([super_key], "m", lazy.layout.shrink()),
    Key([super_key], "n", lazy.layout.normalize()),
    Key([super_key], "o", lazy.layout.maximize()),
    Key([super_key, "shift"], "space", lazy.layout.flip()),

    # layouts
    Key([super_key], "Down", lazy.prev_layout()),
    Key([super_key], "Up", lazy.next_layout()),

    # window handling
    Key([alt_key], "F4", lazy.window.kill()),
    Key([super_key], "x", lazy.window.kill()),
    Key([super_key], "w", lazy.window.toggle_floating()),
    Key([super_key], "m", lazy.layout.maximize()),

    # ~ Audio
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer --card %d --quiet set Master 2dB+" % audio_card_id)),
    Key([super_key], "equal", lazy.spawn("amixer --card %d --quiet set Master 2dB+" % audio_card_id)),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer --card %d --quiet set Master 2dB-" % audio_card_id)),
    Key([super_key], "minus", lazy.spawn("amixer --card %d --quiet set Master 2dB-" % audio_card_id)),
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master toggle")),
    Key([], "XF86AudioPlay", lazy.function(media_playpause)),
    Key([], "XF86AudioNext", lazy.function(media_next)),
    Key([super_key], "bracketleft", lazy.function(media_next)),
    Key([], "XF86AudioPrev", lazy.function(media_previous)),
    Key([super_key], "bracketright", lazy.function(media_previous)),
    Key([super_key], "v", lazy.spawn("pavucontrol")),

    # quick launch
    Key([super_key], "t", lazy.spawn("kitty"))
]

widget_defaults = dict(
    font = 'Fira Code',
    fontsize = 13,
    padding = 3
)

screens = [
    #Screen(),
    Screen(
        top=bar.Bar(
            [
                #widget.CurrentLayout(),
                widget.GroupBox(
                    active='878787',
                    inactive='2E2E2E',
                    disable_drag=True,
                    this_current_screen_border='DB6EFF',
                    this_screen_border='DB6EFF',
                    highlight_method='text',
                    urgent_alert_method='text'
                ),
                widget.Spacer(length=5),
                widget.CurrentLayoutIcon(
                    scale=.6
                ),
                widget.Spacer(length=20),
                widget.WindowName(
                    foreground='C4C4C4'
                ),
                widget.Prompt(
                    ignore_dups_history=True,
                    prompt='λ ',
                    **widget_defaults
                ),
                #widget.Mpris2(
                #    name='spotify',
                #    objname="org.mpris.MediaPlayer2.spotify",
                #    display_metadata=['xesam:title', 'xesam:artist', 'xesam:album'],
                #    scroll_chars=None,
                #    stop_pause_text='',
                #    **widget_defaults
                #),
                #widget.Spacer(length=20),
                widget.Systray(),
                widget.Spacer(length=20),
                widget.Clock(
                    format=' %H:%M, %a %d/%m/%Y', 
                    **widget_defaults
                ),
                widget.Volume(
                    card_id=audio_card_id, 
                    **widget_defaults
                ),
                widget.Spacer(length=10),
                #widget.QuickExit(
                #    default_text='[ S ]', 
                #    countdown_format='[ {} ]'
                #),
            ],
            24,
        )
    )
]

mouse = [
    # move window around
    Drag(
        [super_key], "Button1", lazy.window.set_position_floating(),
        start = lazy.window.get_position()
    ),

    # resize window
    Drag(
        [super_key], "Button3", lazy.window.set_size_floating(),
        start = lazy.window.get_size()
    ),

    # bring window to front
    Click(
        [super_key, alt_key], "Button1", lazy.window.bring_to_front()
    )
]

groups = [Group(i) for i in 'asdf']

# throw away groups for random stuff
for i in groups:
    # super + letter of group = switch to group
    keys.append(
            Key([super_key], i.name, lazy.group[i.name].toscreen())
    )

    # super + shift + letter of group = switch to & move focused window to group
    keys.append(
            Key([super_key, 'shift'], i.name, lazy.window.togroup(i.name))
    )

groups.extend([
    Group(
        'music', 
        spawn='spotify', 
        layout='max', 
        init=True,
        exclusive=True,
        persist=True,
        matches=[
            Match(wm_class=['spotify', 'Spotify'], wm_instance_class=['spotify', 'Spotify'])
        ]
    )
])

layouts = [
    layout.Max(),
    layout.Floating(
        float_rules=[
            dict(role='About'),
            dict(wmclass='file_progress'),
            dict(wmclass='megasync')
        ],
        auto_float_types={
            'toolbar', 
            'utility', 
            'splash', 
            'dialog', 
            'notification'
        },
        border_focus='#572b66',
        border_normal='#878787',
        border_width=1
    ),
    layout.MonadTall(
        border_focus='#572b66',
        border_normal='#878787',
        border_width=1
    )
]

focus_on_window_activation = 'never'

#

@hook.subscribe.startup
def autostart():
    set_wallpaper('~/Imagens/1086871-persona-5-wallpapers-1920x1080-for-ipad.jpg')