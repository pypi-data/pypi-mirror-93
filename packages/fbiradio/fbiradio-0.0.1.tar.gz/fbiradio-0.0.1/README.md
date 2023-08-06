# FBi Radio currently playing

Find out which track is currently playing on [FBi Radio](https://fbiradio.com),
Australia's best radio station.

## Installation

Install from PyPI:

    pip install fbiradio

Or clone this repository and install locally:

    git clone https://github.com/cchristiansen/fbiradio/
    cd fbiradio
    pip install .

## Usage in console

List the last `N` tracks by

    $ fbiplaying -n N

replacing `N` for 5 or any other positive integer. If `N` is 0, all tracks
that have been played in the current radio show are displayed. If no number is
given, the latest track is displayed.

    $ fbiplaying
    01:37 pm: SOPHIE - UNISIL

## Import as library

    import fbiradio

    # Get the last three tracks
    tracks = fbiradio.currently_playing(n=3)

    # Find the artist name of the first track
    print(tracks[0].artist)

    # Find when the second track was played
    print(tracks[1].played_at)

    # What was the track name of the latest track?
    print(tracks[-1].track)

    # Show all information on the latest three tracks
    for track in tracks:
        print(track)

## Disclaimer

Aside from supporting the radio station and loving the music FBi plays, I am
not affiliated with the station in any way, shape or form.

## Copyright

Copyright 2021, Christian Christiansen.

Code is distributed under
[GNU Affero Public License 3](https://www.gnu.org/licenses/agpl-3.0.en.html).

Listen to 94.5 FM. Peace out.
