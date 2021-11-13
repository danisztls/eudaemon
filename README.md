# Eudaemon
Activity monitor that notifies user about computer usage in real time so it can be more aware about bad habits and take positive action.

## Use case
We increasingly use computers to get things done and for many of us it's also a source of income, entertainment and a hobby.
So we increasingly expend time on virtual space in detriment of real space and possibly compromising our physical and mental well-being.

When immersed our sense of time, urgency and physical needs is distorted. Which can be good because we need this hyper focus to solve complex tasks.
But it can also be bad because certain needs and duties might end unfulfilled.
In real space we have feedback loops that evolved along millennia that regulate our behavior. But suddenly we are living a completely different lifestyle to which we haven't properly adapted our instincts.

In general software does not take user needs and limitations into account or is adversarial and designed to grab it's attention so to maximize time spent and ads revenue.

## Design 
The premise is that lack of awareness is at blame and thoughtful notifications can anchor the user back to reality and improve it's capability for decision making and action. This program does not have **reducing computer usage** as a goal. This isn't a real issue or a target to maximize but a side effect of lack of [consciousness](https://en.wikipedia.org/wiki/Consciousness) when on virtual space.

It logs activeness in small time blocks. For example, if the user was not idle *(any keyboard or mouse event)* in the last minute, that block is logged as active.
Doing that it can effectively monitor computer usage without getting into the trouble of dealing with a high-level of granularity like monitoring activity per-application.
The later would require a more complex/intrusive daemon and active categorization by the user while facing barriers like: **in what category should I put my browser?**
And for that to actually work it would also require multi-platform daemons and a server and the user to spend a lot of time.

What I recommend instead is creating isolated contexts for each cluster of activities because that is easier to manager and better for awareness.
If you play games a lot ideally you can have a rig just for entertainment and one for work or using an user for each on the same rig.

TODO: Time-blocking.

TODO: Periodic pauses.

## Caveats
- It's on a very early stage.
- As it's now, it's non-functional.
- It does not really know your needs and state.
- It's efficacy limited by user desire for change.

## Features
- Runs on the background without GUI.
- Empowers user by notifying instead of acting on it's own.
- It's not a chore to use.
- Supports Gnome on X11/Wayland and any DE/WM on X11.
- Export data to TSDB for analytics and additional monitoring.
- Extensive declarative configuration.

## Usage
...

## Configuration
...
