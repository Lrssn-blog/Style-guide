# Color palette

The Lrssn colors come in two themes: **Lrssn Shore**, which is light, and **Lrssn Hearth**, which is dark.
Both are built around the brand orange `#fc6600`.

- Shore is a summer evening on a beach, with a bonfire, clear tropical water and coral.
- Hearth is a cottage on New Year's Eve, warm by the fire while fireworks go off over the forest in the cold outside.

The colors are defined once, in the [Color-theme](https://github.com/Lrssn-blog/Color-theme) repository.
It generates the themes for editors, terminals, the desktop, the website and LaTeX from them.
Its [color guide](https://github.com/Lrssn-blog/Color-theme/blob/main/Theme.md) lists every color, and the [brand guide](https://github.com/Lrssn-blog/Brand-guide) says how to use them.

## Main colors

The roles are the names in Color-theme's palettes.

| Role | Shore | Hearth | Use |
| --- | --- | --- | --- |
| `bg` | `#fdf6ea` | `#101a16` | The page, the editor and the terminal. |
| `bg-dim` | `#f5ead7` | `#0c1411` | Sidebars, panels and boxes. |
| `border` | `#e3d3b9` | `#2e343c` | Borders and rules. |
| `fg` | `#13303d` | `#f0e3d0` | Text. |
| `fg-muted` | `#4f6470` | `#a3aebb` | Secondary text, such as captions. |
| `comment` | `#76664e` | `#8796aa` | Comments in code. |
| `primary` | `#fc6600` | `#fc6600` | The brand orange: fills, rules and the logo, never text. |
| `primary-text` | `#b04600` | `#ff8a3d` | Orange text and links. |
| `primary-soft` | `#ffe3cc` | `#3a1f0e` | A tint behind highlighted text. |
| `secondary` | `#00999a` | `#4d94b8` | The cool accent: fills and rules, never text. |
| `secondary-text` | `#00737a` | `#8cc8e3` | Text in the cool accent. |
| `success` | `#1c7448` | `#a9d48f` | Success. |
| `warning` | `#965a00` | `#ffb547` | Warnings. |
| `error` | `#c4262e` | `#ff6b5e` | Errors and danger. |
| `info` | `#00629c` | `#7fcbe6` | Neutral information. |

## Using the colors

- Use Shore on paper and on light screens, and Hearth on dark screens.
- Write orange text in `primary-text`, and never in `primary`, which is too light to read on a light background.
- Put `#14171c` text on an orange fill, and never white.
- Never use color as the only way to convey information, as some readers cannot see it.
- Do not add colors that are not in the palettes.
  To change a color, change it in Color-theme, whose build checks the contrast of every text color.

In LaTeX, the [Lrssn theme](../latex/Latex.md#the-lrssn-theme) defines these colors for `xcolor`.
