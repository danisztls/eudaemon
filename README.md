# Eudaemon

Activity monitor that notifies user about computer usage in real time so it can be more aware about bad habits and take positive action.

## Use case

We increasingly use computers to get things done and for many of us it's also a source of income, entertainment and a hobby. So we increasingly expend time on virtual space in detriment of real space possibly compromising our physical and mental well-being.

When immersed our sense of time, urgency and physical needs is distorted. Which can be good because we need this hyper focus to solve complex tasks. But it can also be bad because certain needs and duties might end unfulfilled. In real space we have feedback loops that evolved along a millennia that regulate our behavior. But suddenly we are living a completely different lifestyle to which we haven't properly adapted our instincts.

In general software does not take user needs and limitations into account or is adversarial and designed to grab it's attention so to maximize time spent and ads revenue.

## Design 

The premise is that lack of awareness is at blame and thoughtful notifications can anchor the user back to reality and improve it's capability for decision making and action. This program does not have **reducing computer usage** as a goal. This isn't a real issue or a target to maximize but a side effect of lack of [consciousness](https://en.wikipedia.org/wiki/Consciousness) when on virtual space. So the aim is to remind and provide clues to the user about its computer usage patterns.

### Monitoring computer usage

We can log **activeness** in small time blocks. For example, if the user was not idle *(any keyboard or mouse event)* in the last minute, that block is logged as active. Doing that it can effectively monitor computer usage without getting into the trouble of dealing with a high-level of granularity like monitoring activity per-application. The later would require a more complex/intrusive daemon and active categorization by the user which in my experience is counter-productive and doomed to fail. 

### Remind to do periodic pauses

We can stay sitted for long periods when using a computer which is correlated with obesity and a cluster of health issues. Having a break and exercising from time to time is critical for blood flow and health. The issue is that when focused we can easily forget to do so.

### Preventing distraction

Everything nowadays farms for our attention. We are easily distracted and we can spend way more time than we planned on certain activities. We can help prevent distraction through effective timers and periodic reminders.

An alternative outside the scope of this program is to create isolated contexts for each cluster of activities because that is easier to manager and better for awareness due to the [doorway effect](https://en.wikipedia.org/wiki/Doorway_effect). For example, you can have dedicated rigs or users for entertainment and for work.

Also there are tools to block certain sites and programs while allowing usage on specified periods and conditions. e.g.:

- [proginosko/LeechBlockNG](https://github.com/proginosko/LeechBlockNG)
- [danisztls/steam-killer](https://github.com/danisztls/steam-killer)

### Preventing delayed sleep

[Blue light exposure](https://en.wikipedia.org/wiki/Biological_effects_of_high-energy_visible_light) outside of daytime messes with our [circadian rhythm](https://en.wikipedia.org/wiki/Circadian_rhythm) making us sleeper later than we should. Tools like *f.lux* and *GNOME Night Light* change the color temperature of the screen making colors warmer. Thought that is only half of the equation. Reducing screen brightness at night also helps and don't impair as much color perception and comfort.

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
