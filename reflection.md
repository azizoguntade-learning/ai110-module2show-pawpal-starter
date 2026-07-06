# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design focused on three core objects: `Task`, `Pet`, and `Scheduler`. 

- What classes did you include, and what responsibilities did you assign to each?
1. **Task**: Represents an individual care activity. It holds attributes like duration, priority, due time, and completion status, and is responsible for managing its own state (e.g., marking itself complete or updating its schedule).
2. **Pet**: Acts as a profile to aggregate care requirements. It holds demographic data (name, species, age) and manages a localized list of `Task` objects specific to that animal.
3. **Scheduler**: Serves as the central logic engine. It aggregates all `Pet` profiles, pools their tasks, and executes constraints (like available time and conflict detection) to generate the final daily plan. We intentionally omitted an `Owner` class to reduce hierarchy depth, passing user constraints directly into the Scheduler methods instead.

**b. Design changes**

- Did your design change during implementation?
Yes, minor adjustments were required for the method signatures to support the user interface.

- If yes, describe at least one change and why you made it.
I changed the return type of the `Scheduler.build_schedule()` method from `List[Task]` to `List[Tuple[str, Task]]`. Initially, returning a flat list of tasks stripped away the context of which pet the task belonged to. By pairing the pet's name (string) with the `Task` object in a tuple, the UI can accurately display statements like "Feed Luna" instead of just "Feed", ensuring clear instructions when managing multiple pets.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project?
I utilized AI tools in a strictly limited capacity, primarily as a basic syntax checker and a formatting reference. I designed the core object-oriented architecture and scheduling logic independently, occasionally using AI to quickly generate standard Python `@dataclass` boilerplate to save typing time.

- What kinds of prompts or questions were most helpful?
Prompts requesting strict syntax formatting or simple API documentation checks were the most useful, as they did not interfere with the core algorithm design.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
I have made the argument that relying on automated logic generation introduces structural flaws. When an AI suggested returning a simple, flat list of tasks from the `build_schedule` method, I immediately recognized the data loss issue and rejected the code. 

- How did you evaluate or verify what the AI suggested?
I analyzed the proposed data flow against the UI requirements. I engineered a context-aware return type (`List[Tuple[str, Task]]`) to guarantee the frontend could correctly associate each scheduled task with its respective pet.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I successfully designed the system architecture to remain flat and efficient. I structured the `Scheduler` to handle user constraints directly, which simplified the data model and reduced unnecessary hierarchy.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would build a more robust priority weighting system inside the `Scheduler` to mathematically score tasks based on urgency and duration, rather than relying on basic string comparisons.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
I learned that while AI can assist with minor syntactical formatting, the developer must retain full control over the system's underlying logic. Strong architectural planning and independent problem-solving are essential for building a functional application.