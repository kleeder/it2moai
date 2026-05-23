it2moai, version 0.6
====================

Python 3 only.

Use the `example.it` or `example.mptm` file to do your song. When done, run the script to
generate a .🗿 file usable on thirtydollar.website.

Don't change the samples/instruments (.mptm instrument Alternative Tuning may be changed).

Tempo, Ticks/Row and Global Volume are adjustable. Sample Volume does not do anything
(set to 160 by default so that tracker playback sounds closer to Moai website).

Note volume and pan are supported via the volume column. Pan changes are sticky.
Note Cuts ^ will cut all sounds, no matter where they are placed (i.e., be careful with these).

Supported commands:
* Set Speed (`Axx`)
* Set Tempo (`Txx` for `xx` greater than or equal to 32)
* Fine Portamento (`EFx`/`FFx`) and Extra Fine Portamento (`EEx`/`EEx`) - **only** for note triggers
* Set Global Volume (`Vxx`)
* Fine Global Volume Slide (`WFx`/`WxF`)

Version history
---------------

* 0.1: Initial creation of program by kleeder
* 0.2: Added global volume initial setting, note volumes, and updated the soundlist to incorporate the 
       current available sounds (list grows from 131 samples to 191). Samples tuned in example module 
       and appropriate offsets added to the soundlist. Adjusted global/sample volume defaults so that
       tracker playback volume sounds closer to moai playback volume.
* 0.3: Module name is no longer hardcoded and must instead be typed in. Output name remains as is.
       Added ability to xenharmonise files during moai conversion to any tone equal temperament tuning
       system. This may be handy for .mptm files with such a tuning.
* 0.4: Support added for Fine/Extra Fine Portamento Down/Up commands (`EFx`/`FFx`/`EEx`/`FEx`) to detune notes.
       Use only on rows that also contain a note, otherwise the script will break.
* 0.5: Fixed errors on non-existent patterns and notes
* 0.6: Example modules updated with NNA set to Continue.
       Output file is now placed next to input module by default. Added command line parsing.
       Added support for arbitrary ticks/row, panning, new commands (`Axx`, `Txx`, `Vxx`, `WFx`/`WxF`).
       Converter edge case improvements: fixed timing of rows with cuts/effects but no notes,
       fixed handling of notes without an instrument and instrument changes without a note.
       Volume changes are emitted as floating point now.

Additional notes
----------------

`soundlist.json` contains the listing of samples in order along with their IDs
and name fields. Both of those fields can be ingested by thirtydollar.website,
but the tool prefers the emoji icons where available. The soundlist also includes
an order (for readability only) and a tuning offset to account for tuning 
adjustment made in OpenMPT.

The example modules contain all the samples available on thirtydollar.website as of 4/20/23.
These have been rearranged alphabetically by source file name in the module with following prefixes:
* `c_` = chords or multi tonal sounds (fifths, etc.)
* `n_` = note (single tonal) sounds
* `perc_` = percussion sounds
* `r_` = riff sounds
* `sfx_` = sound fx or misc. sounds
