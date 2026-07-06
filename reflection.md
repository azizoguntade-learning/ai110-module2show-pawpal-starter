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
The scheduler evaluates the owner's total available time (in minutes), individual task durations, task priorities (high, medium, low), and strict time intervals to prevent overlapping schedules.

- How did you decide which constraints mattered most?
I have made the argument that hard constraints like available time and interval conflicts must take precedence to ensure a realistic and achievable schedule. Priority serves as a secondary sorting layer, ensuring critical care tasks are slotted into the available time before lower-priority enrichment activities.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
I chose to implement a "Knapsack-lite" greedy algorithm for time management, alongside a strict interval overlap check for conflicts. The scheduler will slot tasks in one by one based on priority and stop evaluating a specific block of time once a conflict is detected, rather than attempting to calculate absolute maximum utilization across concurrent overlapping possibilities (e.g., assuming the owner could walk the dog and brush the cat at the exact same time).

- Why is that tradeoff reasonable for this scenario?
This is reasonable because pet care generally requires sequential, dedicated attention from a single owner. Calculating perfect concurrent multithreading for a single human user adds immense computational complexity for edge cases that do not accurately reflect real-world pet care workflows.

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
I implemented automated tests to verify sorting correctness, recurrence logic, and conflict detection. Specifically, I tested if tasks return in strict chronological order, if marking a daily task complete generates a new instance for the following day, and if the system properly flags overlapping intervals while permitting back-to-back abutting tasks.

- Why were these tests important?
These tests ensure the mathematical and chronological foundation of the application is stable. Validating these edge cases guarantees that the user will not be presented with an impossible schedule or experience data loss during task recurrence.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am highly confident (5/5 stars) in the scheduler's current capabilities, as it consistently passes all automated boundary checks and logical constraints outlined in the testing suite.

- What edge cases would you test next if you had more time?
I would test tasks that bridge across midnight into a new calendar day, evaluate how the system handles null or malformed datetime inputs, and implement load testing to observe performance when an owner manages hundreds of recurring tasks.

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

## 6. AI Strategy and Collaboration

**a. Effective Features**
The most effective AI coding assistant features were syntax validation and boilerplate generation (specifically for Python `@dataclass` structures). Offloading the repetitive typing allowed me to focus cognitive effort strictly on the algorithmic logic and data flow.

**b. Preserving Clean Design**
I have made the argument that AI suggestions often prioritize immediate execution over long-term architectural integrity. For example, the AI suggested utilizing a deeply nested list comprehension to retrieve all pet tasks in the `Owner` class. While syntactically concise, I rejected it in favor of explicit `for` loops. Explicit loops are significantly easier to debug and read for human developers, maintaining the clean design of the application.

**c. Session Organization**
Utilizing separate chat sessions for distinct phases (e.g., one session for UML mapping, a separate one for writing test cases) prevented the AI from conflating context. It kept the AI's output highly targeted and prevented it from prematurely generating UI code while I was still stabilizing the backend logic.

**d. The Lead Architect Role**
I learned that the human developer must act as the absolute filter for all generated code. Powerful AI tools are excellent at producing code rapidly, but they lack an innate understanding of the system's overarching context or constraints. Being the lead architect means rigorously evaluating every line of code against the project requirements and rejecting functional code if it compromises the system's structural logic.