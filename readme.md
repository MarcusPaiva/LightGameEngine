# LightGameEngine 🎮✨

**A Swiss Army knife for Pygame — not a replacement for it.**

LightGameEngine is a light Python layer built on top of Pygame: it takes what Pygame already does well and wraps it in the simplest, most reusable way possible, then adds the things Pygame does **not** provide out of the box — ready-made effects, a friendlier input system, and game UI objects (buttons, modals...) that most people end up rebuilding from scratch in every new project.

The goal is not to compete with full game engines (Godot, Unity), and not to hide Pygame from you either. You keep writing plain Pygame code — this library just saves you from repeating the same boilerplate project after project.

## 📦 Installation

LightGameEngine is available on PyPI:

```bash
pip install LightGameEngine
```

## 🎯 Philosophy

LightGameEngine aims to be a **high-level** tool, built to make life easier for people writing games in Python — **not** to replace Pygame. You still have full access to Pygame whenever you need it; the library just stops you from rewriting, every single time, the things that should already be there: collision, input, basic UI, effects.

## 🧰 What the library offers today

- **Geometry and collision**, with no Pygame math dependency (`BoundingBox`, `RectBoundingBox`, `CircleBoundingBox`, circle-vs-circle, rect-vs-rect, and circle-vs-rect collision).
- **Thin, chainable wrappers** around the window, fonts, images, and sound (`SurfaceScreen`, `GameFont`, `Image`, `SoundEffect`, `Music`).
- **Extra effects and features** Pygame doesn't ship with — today: an image fade-in/fade-out effect, ready for splash screens.
- **Better input handling**: keyboard (`Keyboard`, plus a `Keys` enum with readable names for every key) and controllers (`Joystick`, via SDL's GameController API — it recognizes Xbox, PlayStation, Switch, and most third-party controllers under the same button names), plus ready-to-use mouse helpers.
- **Input alias system** (`Alias`) — one of the library's biggest differentiators: map game actions (`"jump"`, `"confirm"`...) to one or more keys/buttons, freely mixing keyboard and controller. Your gameplay code just asks *"was the `jump` action triggered?"* without ever needing to know or care which key or button was pressed — key rebinding without duplicating logic across your code.
- **Ready-to-use objects**: `Button` and `Modal`, UI components almost every game needs (menus, confirmations, dialogs), with built-in controller navigation (focus + confirm button).

Great for quick prototyping, teaching game programming, or just for anyone who likes writing code by hand instead of reinventing the wheel.

## 📌 Coming next

- Fully encapsulated scene management
- More ready-to-use UI objects
- A ready-to-use SplashScreen (the image fade effect is already available today)
- Asset support with caching

> This project is still in an early stage - follow the weekly posts on [my LinkedIn](https://www.linkedin.com/in/marcuspaiva/) to see its progress, and feel free to jump in with feedback!

🚧 **Work in progress - contributions and suggestions are welcome!**
