### 15 November :
## Signal :
Django Signals can be super simple or stupidly overcomplicated, but you only need to master core practical parts.
Here is the minimal, job-ready, backend-level signals list.

I'll break it into MUST LEARN vs OPTIONAL.

1. **The Concept: decoupled events**
You must understand these two lines:
- A sender sends a signal.
- A receiver listen and reacts.
That's it. Signal = Event Listeners.

