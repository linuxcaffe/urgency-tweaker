- Project: https://github.com/linuxcaffe/urgency-tweaker
- Issues:  https://github.com/linuxcaffe/urgency-tweaker/issues

# urgency-tweaker

An interactive terminal tool for experimenting with Taskwarrior urgency rules.

---

## TL;DR

- ncurses-based TUI for tuning Taskwarrior urgency
- Adjust attributes and weights interactively
- Outputs a plain-text `urgency.rc` you can include in `.taskrc`
- Designed for experimentation, not automation

---

## Why this exists

Taskwarrior’s urgency system is powerful, but opaque. Small changes can have
large effects, and understanding *why* a task floats or sinks often requires
trial and error.

This project exists to make that experimentation fast, visible, and reversible
— without editing config files by hand or restarting Taskwarrior repeatedly.

---

## Core concepts

- **Urgency factors**  
  Individual task attributes (project, tags, priority, dates) that contribute
  to overall urgency.

- **Weights**  
  Numeric values (positive or negative) that increase or decrease the influence
  of a factor.

- **Interactive tuning**  
  Changes are applied live, making it easier to see how different choices affect
  urgency behavior.

- **Generated config**  
  The result is a standard `urgency.rc` file, suitable for inclusion in
  `.taskrc`.

---

## Example workflow

1. Launch the interface
2. Adjust urgency weights for selected attributes
3. Observe how task ordering changes
4. Save the resulting configuration

Result:

```ini
urgency.project.work=5.0
urgency.priority.H=3.0
urgency.tag.waiting=-2.0

