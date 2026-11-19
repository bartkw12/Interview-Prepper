# Hatch interview cue cards

Interview: **Monday Nov 23, 9 am**. Vision & AI Applications Engineering Trainee, Advanced Automation and Robotics.

<!--
How this file is read by scripts/build_data.py (edit the cards here, then rebuild):

- A card starts with a heading:  ### H01 · The question **(4)** ★
  - H01 is the ID. Its letter is the section; the section name comes from the card's tag.
  - **(4)** is the number of points to hit. The build checks that the card has exactly that many points.
  - ★ at the end marks a must-know card (optional).
- The next line is the tag in backticks:  `[Hatch interview]`
  Optionally followed by a recommended answer time for the stopwatch:  `[Hatch interview]` ⏱ 90s (75–120s)
  (target 90 seconds, aim for 75 to 120). The range is optional:  ⏱ 60s
- Then the back of the card. Each top-level "- " or "1. " line is one point.
  Bold words become the hints. Lines in *italics* or plain paragraphs are extras and are not counted.
- Figures: ![](figs/name.png), with the image saved in web/figs/.
- Cards are separated by a line with three dashes.
- Every "# Sheet N · Title" heading after the cards starts a project sheet, shown in the Sheets tab.
- You can also edit a card in the app (Edit button, or E) when it runs with python run.py; that rewrites the card here.
-->

---

# A. Hatch interview and behavioural

---

### H01 · Tell me about yourself **(4)** ★
`[Hatch interview]` ⏱ 75s (60–90s)

- **Who:** MEng **Computer Engineering**, McMaster, finishing **Dec 2026**; BEng **Engineering Physics**.
- **Capstone:** a robot that finds **Tim Hortons cups** in **mixed recycling** on a **moving conveyor** and lifts them out with a **vacuum gantry**: **YOLOv3**, **95%** removed.
- **Research:** low-light **3D reconstruction**; replaced a **255k-parameter** module with **~70 parameters**; **+2.1 dB** when exposures vary.
- **Industry + why here:** **L3Harris** laser calibration tool, **Hitachi Rail** AI team lead; I want **vision on real equipment, tested on site**.

*Simply:* who I am, the robot, the research, industry, why this job. Under 75 seconds, then stop.

---

### H02 · Why Hatch? Why this role? **(3)** ★
`[Hatch interview]` ⏱ 60s (45–75s)

- **Honest hook:** I knew Hatch for **big mining, metals and energy projects**. This posting showed me **AAR**: **vision and AI on robots in real plants**, which I didn't know you did.
- **Fit:** it's what I've already built: a **vision-guided robot** (capstone) and **imaging in bad light** (research). Mining is **dust, heat, glare and low light**.
- **Motivation:** I'm fascinated by **physical AI**, AI that **acts in the real world**. Your aim of "**a better world through positive change**" here means **safer, cleaner** operations; plus **mentorship** and a path to **P.Eng**.

*Don't say you "never cared" about Hatch before. Say what surprised you.*

---

### H03 · What do you know about Hatch? **(4)** ★
`[Hatch interview]` ⏱ 60s (45–90s)

- **70+ years**, **10,000 colleagues**, **150 countries**; sectors **Metals, Energy, Infrastructure**. Aim: "**a better world through positive change**"; motto: "**entrepreneurs with a technical soul**".
- **AAR** sits in the **Technologies** team under **Business Practices: Equipment Technology**, Mississauga, supporting offices worldwide.
- **Industrial robotics:** robots hardened for **heat, dust, corrosion, impact**; **2D vision, 3D structured light, laser triangulation**; motion synced **"on the fly"**; **telerobotics** with haptic feedback.
- **Recent news:** **AI-Assisted Process Control** at MMG Dugald River (payback **under 3 months**, July 2026); **LayerSense** ultrasonic inspection of furnaces and pipelines (Aug 2026).

---

### H04 · Where do you see yourself in 5 years? **(2)**
`[Hatch interview]` ⏱ 45s (30–60s)

- A **senior AI / computer vision engineer** who **leads a team** and works at the **leading edge of vision**, making these machines **smarter and safer**.
- Having taken systems from **proof-of-concept to commissioning** on client sites, with my **P.Eng**, and **mentoring** new trainees.

*Simply:* lead, stay at the edge of the tech, still hands-on with real machines.

---

### H05 · What is your greatest weakness? **(2)**
`[Hatch interview]` ⏱ 60s (45–90s)

- **Weakness:** I'm drawn to the **exciting part first** (e.g. designing the **multi-agent system** at Hitachi) before the **unglamorous groundwork**: **baselines, A/B tests, regression tests**.
- **What I do now:** **fundamentals first**. At Hitachi I built a **40-defect benchmark** before tuning the agents, which is how we could show **37% → 82%**. In research I **reproduce the baseline and write pass/fail rules before any experiment**.

---

### H06 · STAR: Learned something new quickly **(4)** ★
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** capstone, fall 2022. None of us had built a **vision system**. **ChatGPT launched that semester** and hooked us on AI, but there was **no AI to lean on** for code yet.
- **T:** go from zero to a detector that **drives a robot** on a moving belt by **April**.
- **A:** learned from **docs, tutorials and trial and error**: **YOLO, OpenCV**, labelling, training on **Colab**, and the **control side** from scratch: **ESP32**, **stepper maths** (127 steps per inch), the **serial link**, pick timing.
- **R:** a working robot at the **Capstone Expo** (**95%** removed). It's why I chose **computer vision** for my MEng.

*Backup story:* learning 3D Gaussian Splatting fast enough to reproduce a CVPR 2025 paper (card R05).

---

### H07 · STAR: Working on a cross-disciplinary team **(4)** ★
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** Hitachi Rail AI project: me (**computer engineering**), a **computer science** intern and an **electrical** intern. Different strengths, **uneven software fundamentals**.
- **T:** get all three of us building **one system, the same way**.
- **A:** **in-person whiteboard sessions** on the architecture; **coding-assistant instructions and hooks** in the repo that steer **which libraries, when to merge, how code is structured**; everyone **documents and posts results** often.
- **R:** one consistent codebase everyone could extend, and measurable progress (**recall 37% → 82%**). **Fresh eyes paid off:** the **electrical intern**, new to AI, researched widely and found **AI libraries** that **sped us up**. [Recall: which library?]

*Backup story:* the capstone (mechanical, motor control and vision people on one robot).

---

### H08 · STAR: Leading others **(4)**
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** I led a **3-intern team** building the AI document reviewer at Hitachi Rail.
- **T:** set direction and deliver something **measurable**.
- **A:** **split by component**: one intern on **document preprocessing**, one on the **skills** (the specialist checks), me on the **agents and workers** (orchestration). I **assigned tasks** and **reviewed the PRs**. When the electrical intern was **lost in a huge, messy folder** of cross-linked documents, I built him an **agent that mapped which documents and sections reference each other**, so he could pull out the ones that mattered.
- **R:** he was **unblocked**, and the system reached **recall 37% → 82%** on our fixed benchmark.

---

### H09 · STAR: A failure or a result that didn't go your way **(4)** ★
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** **L3Harris**, laser alignment on the **MX-25** camera. My Python tool told operators **how far to turn each mirror knob**.
- **T:** make it work **on the real bench**, not just in my calculations.
- **A:** the **first real run failed** even though **the maths was right and the code ran**: the **knobs were small, stiff and had no markings**, so nobody could turn them by a set amount. We **3D-printed new knobs** with **more leverage** and **graduation marks**.
- **R / lesson:** alignment then worked: **5 min → 30 s**. Software that works **in a perfect model** can fail on **real hardware**; fix the **whole system**, and **test on the real thing early** (lab vs field at Hatch).

*Backup (research):* H1 not supported: 11 of 12 checks passed, bike was 0.155 dB short of a 0.082 dB bar, and I reported it as a miss.

---

### H10 · STAR: Attention to detail **(4)** ★
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** research code is written to **publish, not to maintain**: **hard-coded values**, little structure, and it **doesn't always match the paper**.
- **T:** know **exactly what the code does** before building on it.
- **A:** compared **paper and code line by line** and logged **14 differences**, e.g. a **hard-coded seed** (the "3 runs" were one seed), colour roles **reversed**, a loss weight of **0.5 not 0.1**, and "**detach**" **silently freezing the colour transform**.
- **R:** made each one a **flag** (default = original); real **3 seeds + noise rule**; a **2×2** showed the curve explains **85 to 100%** of the detach gain.

*Say "research code isn't built for production", not "researchers can't code".*

---

### H11 · STAR: Solving a problem systematically, adapting when plans change **(4)** ★
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** the plan was to build a **monotone curve** first (Rung 1).
- **T:** first **measure** what the original curves actually learn.
- **A:** **30-run diagnostic**: curves were **already monotone**; views differ by **one number** that tracks brightness (**over 99%** of the variation).
- **R:** **dropped Rung 1**, built the **exposure model** instead. Measuring first saved building the wrong thing.

---

### H12 · STAR: Organisation under a deadline **(4)**
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** Hitachi Rail: build a **scheduler** that updates **Excel** reports from several **platform databases**, needed **by month end**.
- **T:** deliver a working tool **fast** without missing anything critical.
- **A:** **broke it down**: gave the sites, data sources and constraints to **Microsoft Copilot** to draft **milestones**; **researched each milestone** to size it; ranked them **must-have vs nice-to-have**; refined the plan, then built in that order.
- **R:** delivered **by month end**. [Recall: the result, e.g. hours saved or how often it runs.] My rule: **milestones → find the essential ones → plan → execute**.

*Backup (research):* ~160 GPU runs before a 5 Dec freeze; a pre-flight checklist and a resumable runner after a batch lost 11 hours to the PC sleeping.

---

### H13 · STAR: Explaining technical work to non-experts **(4)**
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** L3Harris: operators, not engineers, aligned the MX-25 laser by **trial and error**.
- **T:** a tool they would **trust and use**.
- **A:** the output was **"how far to turn each knob"**, not maths; I **tested it with them** on the floor and changed it from their feedback.
- **R:** **5 min → 30 s** per adjustment.

---

### H14 · STAR: A disagreement **(4)**
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** capstone kickoff, **3 people**: one wanted the **mechanical** side, and **two of us wanted software**.
- **T:** split the work so **every part had an owner** and nobody felt sidelined.
- **A:** we **talked it out**: listed every subsystem, split software into **AI/vision** (Shahaan) and **motor control** (me), mechanical and power to Dayyan. **Compromises**: not everyone got their first choice.
- **R:** every subsystem built and integrated for the **Expo**. Lesson: **agree the interfaces early** (ours was **one number over serial**).

---

### H15 · STAR: Safety **(4)**
`[Hatch interview]` ⏱ 90s (75–120s)

- **S:** capstone: a **moving belt**, a **gantry** and **hot motor drivers** running for long test sessions next to people.
- **T:** make it **safe to run and easy to stop**.
- **A:** **instant-stop (kill) switch** and an **easy-to-reach power cord**; **temperature sensors** on the electronics: fans to **max** when hot, a **warning** if too hot; **halt on a jam**; **side barriers** so nothing falls off; **start-up and running warning lights**.
- **R / line to land:** long runs with **no incidents**. "I **stop and ask** before working on equipment I don't know." Hatch's goal: **no harm**.

---

### H16 · "You haven't used PLCs or 3D sensors." How do you answer? **(3)**
`[Hatch interview]` ⏱ 45s (30–60s)

- **Admit it:** I haven't programmed a PLC or used a structured-light or laser scanner.
- **Nearest thing:** **ESP32 motor control** in C++ (steppers, a solenoid valve, a serial handshake with a PC); 3D reconstruction from **multi-view photos with camera poses**; a **3D image processing** course.
- **How I'd close it:** I know where the PLC sits (**logic, I/O, handshake**); I'd learn from the controls engineers; **calibration and triangulation** carry over.

---

### H17 · Design question: "How would you build a vision system for X?" **(8)** ★
`[Hatch interview]` ⏱ 120s (90–180s) *(small font on the print; full version on Sheet 3)*

*Mnemonic:* **R**eally **S**mart **L**ights **D**on't **M**ake **I**ndustrial **V**ision **M**agic.

1. **Requirements:** what must be **seen**, what **decision** follows; smallest feature, **line speed**, latency, **cost of a miss vs a false alarm**.
2. **Sensor:** 2D, 3D or thermal; **resolution** from the smallest feature (**3 to 5 px** across it); **global shutter**; exposure short enough for the speed.
3. **Lighting + protection:** light that makes the feature **pop**; **hood**, sealed enclosure, cooling, **air knife**.
4. **Data:** collect **on site early**, every condition; label; **test set from other days**; plant **known defects**.
5. **Model:** **classical baseline first**, ML when variation is high; sized for **edge latency**.
6. **Integrate:** **encoder or photo-eye trigger**; **calibration** to world and robot; result to the **PLC** with a handshake; **fail-safe**.
7. **Validate:** pass/fail rules **written first**; precision and recall **per condition**; lab → **shadow mode** → commissioning.
8. **Maintain:** watch for **drift**, clean, **retrain**, document.

---

### H18 · Questions to ask them **(4)**
`[Hatch interview]`

- "What is the **hardest imaging condition** you deal with on site: dust, heat, glare, low light?"
- "How do you **validate a vision system** before a client relies on it?"
- "What would a trainee **own in the first six months**, and how is time split between office, lab and site?"
- "What are the **next steps**, and when should I expect to hear?" (Michelle is away Nov 20 to 30.)

*Extra:* "What is AAR working on now: inspection, robotic tapping or sampling, telerobotics?"


---

### H19 · What is your greatest strength? **(3)** ★
`[Hatch interview]` ⏱ 60s (45–75s)

- **Resourcefulness:** when I'm stuck I go **wide**: papers, **the code itself**, docs, forums, colleagues, **AI tools**. Then I **check it with an experiment**.
- **Why it matters here:** AI and vision **move fast**. Knowing **what tools exist** and how to check them is half the job, and I **follow the field for fun**.
- **Example:** the "**detach**" puzzle. The paper didn't explain it, so I read the code, built **diagnostics**, and found the **frozen colour transform** (card H10).

---

### H20 · Tell me what you know about the AAR team **(4)** ★
`[Hatch interview]` ⏱ 60s (45–90s)

- **Where:** **Advanced Automation and Robotics**, in the **Technologies** team (Business Practices: **Equipment Technology**), **Mississauga**, supporting offices **globally**.
- **What:** **vision and AI** for **mining, metals** and other complex operations; robots for "**harsh and unstructured environments**": hardened, **on-the-fly** motion, **force control**, **telerobotics** that move people **out of hazards**.
- **Sensing:** their page calls a robot without sensors "**a one-armed blind man**"; they use **2D vision, 3D structured light, 3D laser triangulation**, chosen by the outcome needed.
- **How they work:** **concept study → proof-of-concept** (small, cheap trials with **ABB** and local colleges: "**get physical fast**") → **design** → **supply and commissioning**. A trainee does **lab trials and field support**.

*Public detail is thin. Ask them what is running now (card H18).*

---

### H21 · Design example: vision on a mining conveyor **(6)** ★
`[Hatch interview]` ⏱ 120s (90–180s) *(small font; full version on Sheet 3)*

*Problem:* find **oversize rocks and tramp metal** on the belt feeding a **crusher**, then stop, divert or pick. It's my capstone at mine scale.

1. **Ask first:** belt **speed** (2 to 6 m/s), smallest object, **cost of a missed bolt (crusher damage) vs a false stop (lost tonnes)**.
2. **Sensor:** **3D laser line profiler** (ore is all grey and dusty, so **shape and height beat colour**) + a 2D camera, **encoder-triggered**; a **metal detector** as a second sensor.
3. **Environment:** **sealed hood** (blocks sun, holds the light), **LED strobe**, **air knife** on the window, **vibration-isolated** mounts.
4. **Data:** rare events, so **anomaly detection** ("not normal ore") + **seeded tests** with known objects; every condition (**day/night, wet/dry, ore type**).
5. **Integration:** **edge PC** on site → **PLC handshake** → stop belt, robot or alarm; time budget = **distance ÷ belt speed**; **fail-safe** if the camera dies.
6. **Validate and run:** **shadow mode** beside operators; **recall on seeded objects**, **false stops per shift**; then **dirty-lens checks**, drift monitoring, retraining.

---

# B. Past experience

---

### E01 · L3Harris: the laser calibration tool (STAR) **(4)** ★
`[Experience]` ⏱ 90s (75–120s)

- **S:** MX-25 camera: operators aligned a **laser** by turning **mirror knobs** by trial and error, about **5 minutes** each time.
- **T:** tell them **how far to turn each knob** so the beam returns along its **incoming path**.
- **A:** in Python, **modelled how each knob turn moves the beam**; when the real knobs proved **hard to turn by a set amount**, we **3D-printed new knobs** with **leverage and markings**, and I **adapted the maths with the operators**.
- **R:** **5 min → 30 s**. [Recall: how the beam offset was measured.]

---

### E02 · Hitachi Rail: AI document review (STAR) **(4)**
`[Experience]` ⏱ 90s (75–120s)

- **S:** hundreds of **cross-referenced engineering documents**, checked for errors by hand.
- **T:** lead a **3-person co-op team** building an AI reviewer.
- **A:** **4 LLM agents** acting as subject experts; a benchmark of **40 planted defects** in **8 categories**, used as a **regression test**.
- **R:** recall **37% → 82%**. Also a RAG chatbot, MRR **0.40 → 0.90**.

*Link to Hatch:* planting known defects is how **inspection systems are validated**.

---

# C. Capstone: vision-guided sorting robot

---

### C01 · Your capstone in one breath **(3)** ★
`[Capstone]`

- **What:** the **CCPU**: a robot that finds **Tim Hortons cups** in **mixed recycling** on a **moving conveyor** and lifts them out with a **suction cup** on an **x–z gantry**.
- **Why:** paper cups have a **plastic liner**, so they **aren't recyclable** and **contaminate** the stream; Hamilton composts them but **sorts by hand**. Tim Hortons sells the most cups in Canada.
- **How + result:** **webcam → YOLOv3 (OpenCV DNN, GPU) → lane over USB serial → ESP32 → steppers + vacuum**. **95%** removed, **under 1%** false positives over **~100 trials**; team of 3; Capstone Expo.

![](figs/capstone_rig.png)

---

### C02 · The pipeline, step by step **(6)** ★
`[Capstone]` *(small font on the print)*

1. **Capture:** webcam **~1 m** above the belt, **LED strips** along both sides, **960×720**, **short exposure + high gain** (no motion blur), autofocus off.
2. **Preprocess:** `blobFromImage`: resize to **416×416**, scale to **0 to 1** (÷255), **BGR → RGB**.
3. **Detect:** **YOLOv3**, one class ("TimsCup"), in **OpenCV DNN** on **CUDA**, ~**0.09 s** per frame.
4. **Filter:** keep **confidence > 0.5**; **NMS** (IoU 0.4) removes duplicate boxes.
5. **Locate + queue:** box centre → **cm on the belt** (~0.7 mm per pixel); each cup reported **once**, from a 7 cm **detection zone**; queued and moved along at belt speed (**22.5 cm/s**).
6. **Act:** the cup's **lane (0 to 17 in)** goes over **USB serial** to the gantry **ESP32**, which **times** the move, **lowers, sucks, carries to the bin, releases**, and replies **"done"**.

![](figs/capstone_system.png)

---

### C03 · Dataset and training **(4)**
`[Capstone]`

- **912 images** in the final set, from our webcam on the **real belt**: cups (new, crushed, lid on or off) **mixed with random recycling**; about **10% with no cups**.
- **Labelled** in **Label Studio** on an **AWS** server so all three of us could label at once; one **box per cup** (YOLO text: class, x, y, w, h); about **225 boxes an hour**.
- **Trained** with **Darknet** on **Google Colab** GPUs from **pretrained Darknet-53** weights (transfer learning); **2,000 iterations**, about **3 h**.
- **10% held out** to check the loss. Three versions (**179 → 311 → 912** images), each fixing the last one's false positives (C11).

---

### C04 · Why YOLOv3 and OpenCV DNN? **(2)**
`[Capstone]`

- **One-stage detector**: the whole image in **one pass**, fast enough for a **moving belt**; in 2022 it was **mature and well documented**.
- **OpenCV DNN** loads **Darknet weights directly** and has a **CUDA backend**, so detection, the live overlay and the **serial link** all live in **one Python script**. *Today:* a newer YOLO exported to ONNX or TensorRT.

---

### C05 · How did you time the pick? **(3)** ★
`[Capstone]`

- **Fixed belt speed:** conveyor stepper at **170 rpm** ≈ **22.5 cm/s**, checked with **timestamped photos and a tape measure**. So **distance = time**.
- From the detection zone to the arm is about **53 cm**, so a cup arrives **~2.3 s** after it's reported.
- **My ESP32 code:** move across to the cup's lane, then **wait = 2.3 s − arm travel time − 0.55 s lowering**, then lower and grab.

*Simply:* get there early, wait, drop exactly when the cup arrives.

![](figs/capstone_timing.png)

---

### C06 · The GPU speed-up **(2)**
`[Capstone]`

- **~0.2 s → ~0.09 s** per detection (about **2.3×**) by switching OpenCV DNN to its **CUDA backend** (two lines of code).
- The hard part was **building OpenCV from source with CUDA and cuDNN** (over a week of setup). It mattered because a detection was needed every **~0.3 s** (each 7 cm of belt); the gain was modest because **960×720** is a small image.

---

### C07 · Results, and how you measured them **(3)** ★
`[Capstone]`

- **~100 trials:** cups mixed with **real recycling** (cardboard, paper, bottles, cans), belt running, **manual checklist**: detected? picked? any false positive on the laptop?
- **95%** detected and removed; **under 1%** false positives. Misses were mostly **picks** (no seal on a crumpled cup or the rim); the final model had **no observed** detection errors.
- **Honest gap:** we never tracked **precision, recall or mAP** during training, and our report says so. Today I'd **fix the metrics and test set first**, as in my research.

---

### C08 · What was your role? **(4)**
`[Capstone]`

- **Lead and bridge:** I **led** the team and was the **bridge** between **hardware (Dayyan)** and **software (Shahaan)**: I knew what each side needed and kept the system **compatible**.
- **Vision:** much of the **hands-on detection work** with Shahaan (he owned it on paper): data, labelling, training, the detection script.
- **Mine alone:** the **gantry design in Inventor** (the 3D-printed parts), the **motor control code** on the **ESP32**, and the **integration** between the systems.
- **Autonomy:** the **no-skip mode**: if too many cups come, the program **freezes the belt** so **no cup is missed**.

*In the interview: say "we" for the detector and "I" for the gantry, control, integration and no-skip mode, and be ready to go deep on any of them.*

---

### C09 · What went wrong? Failure modes **(4)**
`[Capstone]`

- **False positives:** early models called **anything red or orange** a cup (cans, cartons, chip bags). Fixed with **negative examples** (C11).
- **Missed picks:** suction needs a **smooth surface**; a **crumpled cup** or landing on the **rim** → **no seal**.
- **Comms:** wireless **ESP-NOW** sent at **fixed intervals**, so positions that missed a send were **dropped** → switched to **wired USB serial**.
- **Hardware:** steppers **skipped steps** when pushed too fast (lifting had to be **slower** than lowering); **H-bridges overheated** on long runs → **fans**.

---

### C10 · What would you do differently now? **(5)** ★
`[Capstone]`

1. **Metrics from day one:** precision, recall and mAP on a **held-out set from another day**.
2. **Encoder** on the belt instead of an assumed speed; a **hardware trigger** for the camera.
3. **Controlled lighting** in a hood and fixed exposure (my research shows what varying exposure does).
4. **Edge deployment:** a newer YOLO → **ONNX / TensorRT** on a **Jetson**; log every pick.
5. **Industrial controls:** a **PLC** with an **e-stop** and guarding instead of microcontrollers.


---

### C11 · Fixing the false positives **(3)** ★
`[Capstone]`

- **Problem:** the first model (**179 images**, cups only) "**thinks anything you put down is a coffee cup**": cans, cartons and chip bags at **0.77 to 0.99** confidence.
- **Fix:** add **negatives**: **no-cup images** (122) and **random recycling** with cups mixed in (**248 + 281**), for **912 images** in total.
- **Result:** the final model finds **only the real cup (1.0)**. *Lesson:* a model learns **what you show it**, so show it the **look-alikes** (hard negatives).

![](figs/capstone_before_after.png)

---

### C12 · How did YOLO learn to recognise our cups? **(4)**
`[Capstone]`

- **Supervised:** each box we drew says "**cup here**". The network predicts boxes, and a **loss** scores **box position, objectness and class** against our labels.
- **Training:** **gradient descent** nudges the weights to lower the loss; **2,000 iterations**, about 3 h on a Colab GPU.
- **What it learns:** early layers **edges and colours**; deeper layers **parts and patterns** (red sleeve, white logo, rim, tapered shape). The **negatives** taught it **red ≠ cup**.
- **Head start:** a **pretrained Darknet-53** backbone already knew general shapes from **ImageNet**, so ~900 images were enough (**transfer learning**).

![](figs/cnn.png)

---

### C13 · Camera: exposure vs motion blur **(3)**
`[Capstone]`

- At belt speed the default exposure **blurred** the cups; a **shorter exposure** (−8 or −9) made them **sharp but dark**.
- Fix: **LED strips along both sides** of the belt, plus **higher sensor gain**; exposure, gain and autofocus **fixed in code**, so every frame looks the same.
- **Link to my research:** short exposure + gain = **dark, noisy images**, the **low-light problem** I work on now. And the model must see the **same settings** in training and in use.

---

### C14 · How the PC talks to the ESP32s **(2)**
`[Capstone]`

- **USB serial** (115200 baud): PC → gantry ESP32 sends **one number**, the cup's **lane in inches**; gantry → PC sends **"done"**; PC → conveyor ESP32 sends **run / stop**.
- We first tried **wireless ESP-NOW**. It sent at **fixed intervals**, so positions that missed a send were **dropped** and cups went by. **Wired serial** fixed it.

---

### C15 · The queue and no-skip mode **(2)**
`[Capstone]`

- Python keeps a **queue** of cups, each moved along by **belt speed × time** (**dead reckoning**). A new detection runs only every **7 cm** of travel, and **duplicates within ±3 cm** are dropped.
- **No-skip mode:** if a cup gets within **13 cm** of the arm while the arm is busy, the program **freezes the belt** until the arm says "done", so **no cup is missed**. **Continuous mode:** the belt never stops. One pick cycle takes **~8 s**.

---

### C16 · Gantry and suction hardware **(3)**
`[Capstone]`

- **x–z gantry** on **2040 aluminium extrusions** with **belt drives**; **3 NEMA 17 steppers** (across, up/down, conveyor) through **L298N H-bridges**; **3D-printed** brackets.
- **Vacuum:** **oilless pump** (−65 kPa, 12 V, 6 W) + a suction cup; a **3-way solenoid valve** switched by the ESP32: **closed = suction**, **open = vent**, so the cup **drops**.
- **Frame and power:** belt on **PVC rollers and steel axles** in a **wood frame**; an **ATX PC power supply** (12 V); budget about **$590**.

---

# D. Your research project

---

### R01 · What is the purpose of your research project? **(3)** ★
`[Research project]`

- **Take apart** Luminance-GS's **tone-curve machinery** (about **255k parameters**) to find out what it really does.
- **Replace** it with a **simple, explicit, physical model**: **one shared curve + one exposure per photo** (**55 to 76** parameters).
- **Test** it: **match** the original on normal data (**H1**), **beat** it when exposure varies (**H2**).

*Simply:* a big black box was doing something simple. I proved it, then swapped in the simple thing.

---

### R02 · Your model **(2)** ★
`[Research project]`

- **L_k(x) = F(min(1, 2^{s_k} · x))**: scale photo k by its **exposure** 2^{s_k}, **clip** at white, then apply the **shared curve F**.
- **F:** **monotone**, **32 knots** dense near black, F(0) = 0, F(1) = 1. **s_k:** one number per photo, in **stops**, mean 0. **γ:** one global shape prior. Total **K + N + 1**.

*Simply:* the same camera response for every photo; each photo just had a different exposure.

![](figs/rung2_model.png)

---

### R03 · Why do you call it "physically motivated"? **(2)**
`[Research project]`

- A real camera = a **response curve** (the same for every shot) + an **exposure** (changes per shot). That is exactly **F + s_k**.
- It is like **radiometric calibration**; each s_k is **readable** in stops and could be checked against the camera's metadata.

---

### R04 · The rung ladder: what you did, in order **(4)**
`[Research project]`

- **Rung 0:** **measure** what the original curves learn (30 runs).
- **Rung 0.5:** a **2×2 experiment** to untangle why "detach" helps (30 runs).
- **M1:** build the **varying-exposure set** and run the baselines on it (30 runs).
- **Rung 2:** build and test **shared curve + exposure** (65 runs). **Next:** ablations (H3) by 5 Dec.

![](figs/rung_ladder.png)

---

### R05 · Reproduction: what did you find? **(2)**
`[Research project]`

- Reproduced the paper on my **RTX 3080 Ti**: **9 runs** (3 scenes × 3).
- **Same seed → up to 1 dB apart** (GPU nondeterminism), and the seed was **hard-coded to 42**, so: **3 seeds** per setting and the **2× noise rule**.

---

### R06 · Rung 0: what, result, meaning **(3)** ★
`[Research project]`

- **What:** 30 runs (5 scenes × official/detach × 3 seeds) measuring the learned curves.
- **Result:** curves **already monotone**; differences between views are **one number** (**99.2 to 99.8%** of the variation) that tracks **brightness** (|r| **0.97 to 1.00**).
- **Meaning:** monotonicity alone wouldn't help; **one exposure per view** captures the per-view network. Also found the **detach confound**.

---

### R07 · "Detach": what it means and why you used it **(3)** ★
`[Research project]`

- **What:** use a value but **stop the gradient** flowing back into it: the render moves toward the target, but the **target doesn't move toward the render**.
- **Attached:** the image loss also nudges the curve, so the **target chases the render** (a chicken-and-egg loop). **Detached:** only the **render moves**.
- **Why:** detached was **better** on chair, sofa and bike (**+1.9 to +2.2 dB**), so it became the **baseline to beat**.

![](figs/lgs_pipeline.png)

---

### R08 · Rung 0.5: what, result, meaning **(3)** ★
`[Research project]`

- **What:** a **2×2 experiment**: curve **attached or detached** × colour basis **learned or frozen** (60 runs in all).
- **Result:** detaching the **curve** explains **85 to 100%** of the gain and removes the **bike hue flip** (yellow wheel turned red); the colour basis explains little.
- **Meaning:** Rung 2 uses a **detached curve + plain RGB**, compared against **detach**. The old H3 (colour basis) is **not supported**.

---

### R09 · The LOM dataset **(3)**
`[Research project]`

- **5 real scenes:** **buu, chair, sofa, bike, shrub**, photographed in low light from many views.
- **low/** = dark photos (**training**); **high/** = normal-light photos of the same views (**evaluation only**, on held-out views).
- **Camera poses are provided**. Shrub is reported but **not used to decide** (too noisy).

---

### R10 · The varying-exposure set (M1) **(3)** ★
`[Research project]`

- Each training photo multiplied by a **known gain 2^{u_k}**, u_k spread over **−1 to +1 stops**, mean 0; test views unchanged.
- **Why:** real cameras **disagree on exposure**, and a **known answer** lets me check the model.
- **M1 finding:** the original's per-view curves move the **wrong way** (they follow brightness instead of correcting it); both baselines lose **2.2 to 2.7 dB**.

---

### R11 · H1: claim, rule, result **(3)** ★
`[Research project]`

- **Claim:** Rung 2 **matches detach** on LOM with ~255k fewer parameters.
- **Rule, fixed beforehand:** in buu, chair, sofa and bike, no metric worse than **2× seed noise** (12 checks).
- **Result: not supported.** **11 of 12 pass**, pooled **−0.02 dB**; **bike −0.155 dB** against a **−0.082 dB** bar. Follow-up: **F's starting point** matters (+0.3 dB on one seed, exploratory).

---

### R12 · H2: claim and result **(3)** ★
`[Research project]`

- **Claim:** Rung 2 **beats detach** on the varying-exposure set.
- **Result: supported.** **+2.11 dB** brightness-matched PSNR pooled (**5.3× noise**); ahead in all 4 decision scenes; LPIPS better.
- **Robust:** Rung 2 barely moves (**23.23 → 23.11 dB**) while detach drops (**23.25 → 21.03**); seed spread **0.11 vs 0.72 dB**.

![](figs/results_slope.png)

---

### R13 · H3: what it is and its status **(2)**
`[Research project]`

- **Claim:** let the image loss train **only the exposures s_k** (F stays detached). That should recover **buu's LPIPS** lost by detaching, **without hue flips**.
- **Status: next ablation, pending.** One number per view **can't recolour part of an image**, so hue flips shouldn't return. Experiments freeze **5 Dec**, report **18 Dec**.

---

### R14 · Exposure leak (and the fig3_leak figure) **(3)** ★
`[Research project]`

- **Leak** = how much of a photo's **exposure change** shows up in its **pseudo-target**. **Slope 1** = passes straight through (**bad**: views disagree). **Slope 0** = fully corrected (**good**).
- **Reading the figure:** x = the **gain I applied** to each training photo (−1 to +1 stops); y = how much **brighter or darker its pseudo-target** came out than in the normal set. **Official 0.41, detach 0.51**: about **half the gain leaks**. **Rung 2 is flat (0.01)**: the exposure s_k absorbs it before the shared curve.
- **Show it?** **Yes**, as the **mechanism** behind the +2.11 dB: "the networks **couldn't tell the camera from the scene**; my model **separates them by construction**." Bring the **one-panel** version; the 5-scene figure is the backup.

![](figs/leak.png)

---

### R15 · How does Rung 2 get its exposures? **(2)**
`[Research project]`

- Each s_k **starts at log2(m̄ / m_k)**: the photo's mean brightness against the **average of all photos** (geometric mean).
- On my set that **already matches** the true gains; training moves it only **~0.02 stops**. So it's a **sanity check**; the real finding is the **leak**.

---

### R16 · Your experimental discipline **(4)** ★
`[Research project]`

- **3 seeds** per setting; an effect is **real only above 2× seed noise**.
- **Decision rules fixed before** running (H1 and H2 written down first).
- Every change behind a **switch whose default reproduces the original exactly**; **regression tests** and **self-tests** that must give exactly 0.
- **Raw and brightness-matched PSNR** side by side; an **append-only research log**.

---

### R17 · Limitations **(4)** ★
`[Research project]`

- Only **5 scenes, 3 seeds**, so noise estimates are rough.
- Exposure changes were **synthetic** (applied to 8-bit photos), not captured by a real camera.
- **Hue** is worse on bike; the result **depends on F's starting point**.
- In the default, F is fitted from **2D histograms only**: no rendered information reaches it, close to "**2D enhancement, then 3DGS**" with a shared curve.

---

### R18 · Why does this matter for Hatch? **(3)** ★
`[Research project]`

- **Exposure varies in the field** (auto-exposure, many cameras, changing light), so a model that separates **scene from camera** holds up.
- **Small physical models** beat black boxes when the physics is known: **readable, fast, edge-friendly** (40% faster training here).
- The same **test discipline** as lab trials: **known-answer tests**, **acceptance rules fixed beforehand**.


---

### R19 · The tone curve and my project, in one picture **(2)** ★
`[Research project]`

- **Original:** each photo gets its **own 255-number curve** from **two neural networks** (~255k parameters). The curves are free to differ, and **black gets lifted**.
- **Mine:** first **undo the photo's exposure** (×2^{s_k}, one number), then apply **one shared curve F** (32 knots, F(0) = 0) to every photo. **55 to 76 parameters**.

*Simply:* fix the camera difference first, then brighten every photo the same way.

![](figs/tone_design.png)

---

# E. The original paper (Luminance-GS)

---

### L01 · What does Luminance-GS do? **(3)** ★
`[Luminance-GS original]`

- **Input:** dark photos + camera poses. **Output:** a 3D scene that renders **normally lit** from any viewpoint. (Cui, Chu, Harada, **CVPR 2025**.)
- **Never sees a normal-light photo**, so it is **unsupervised**: it invents **pseudo-targets** by brightening each photo with a learned **tone curve**.
- The Gaussians learn **two renders**: one matches the **dark photo**, one matches the **pseudo-target**. The curve is shaped by **histogram equalisation + a gamma prior**, varied per view by **two small networks**.

---

### L02 · Why not brighten each photo in 2D, then run 3DGS? **(2)** ★
`[Luminance-GS original]`

- Enhancing each photo separately gives **slightly different brightness and colour** per photo.
- 3DGS then explains those differences with geometry: **floaters and flicker**. Luminance-GS trains the brightening **together with** the 3D scene to keep it **consistent**.

---

### L03 · Novel view synthesis **(2)**
`[Luminance-GS original]`

- Given photos from **known camera positions**, render the scene from a **new viewpoint**.
- Scored on **held-out test views** against real photos.

---

### L04 · 3D Gaussian Splatting **(3)** ★
`[Luminance-GS original]`

- A scene = **hundreds of thousands of 3D Gaussians** (fuzzy ellipsoids); bike ends with about **230k**.
- Each stores **position** (3), **scale** (3) + **rotation**, **opacity**, and **colour as spherical harmonics** (colour can change with viewing angle).
- **Splatted** (projected) onto the image, so it **trains in minutes and renders in real time** (NeRF instead runs a network along every ray).

![](figs/gaussians.png)

---

### L05 · How is 3DGS trained? **(3)**
`[Luminance-GS original]`

- **Render** a training view, **compare** with the photo (**0.8·L1 + 0.2·(1 − SSIM)**), **backpropagate**, update every Gaussian.
- **Densify** (clone or split where gradients are large) and **prune** (nearly transparent ones) every 100 steps.
- Luminance-GS: **10k steps**, about **8 to 13 minutes** per scene on one GPU.

---

### L06 · COLMAP / Structure-from-Motion **(2)**
`[Luminance-GS original]`

- **Matches features** across photos to get each photo's **camera pose** and a **sparse 3D point cloud**.
- The sparse points **initialise the Gaussians**. For LOM the poses come with the dataset.

---

### L07 · Tone curve **(3)** ★
`[Luminance-GS original]`

- A **function y = L(x)** from input to output brightness, both in **[0, 1]**, applied to **every pixel**.
- Changes **brightness and contrast** but **never moves anything**.
- Its only job is the **pseudo-target**; its brightness and colour get **baked into the Gaussians**.

*Simply:* a dial that says "this dark value becomes that bright value".

![](figs/tone_curve.png)

---

### L08 · Look-up table (LUT) **(2)**
`[Luminance-GS original]`

- Stores the curve as a **list of numbers**: entry i = output for input level i. Luminance-GS uses **255 entries**.
- Applying it = **"find this pixel's entry, read it out"**. Fast, no maths per pixel.

---

### L09 · Monotone curve **(2)**
`[Luminance-GS original]`

- **Non-decreasing**: a brighter input **never gives a darker output**.
- If not monotone, **tones flip** (a darker shade ends up brighter). The original curves were **already monotone** (Rung 0); Rung 2 **enforces** it.

![](figs/gamma_s_monotone.png)

---

### L10 · Histogram and CDF **(3)**
`[Luminance-GS original]`

- **Histogram:** how many pixels have each brightness (**255 bins**).
- **CDF(v):** the **fraction of pixels ≤ v**; rises from **0 to 1**, **never decreases**.
- In a dark photo the histogram is **bunched near black**, so the CDF **shoots up early**.

---

### L11 · Histogram equalisation (HE) **(3)** ★
`[Luminance-GS original]`

- Uses the **CDF as the tone curve**: v → CDF(v). If **90%** of pixels are below 0.15, then **0.15 → 0.9**.
- Spreads values over the **whole range**, so a dark photo gets **much brighter**.
- **Too aggressive alone:** amplifies **noise** and **posterises** (few levels stretched over the whole range), so Luminance-GS **blends it with a smooth gamma prior**. CLAHE = a local version with a clip limit.

![](figs/hist_he.png)

---

### L12 · Gamma curve, S-curve, shape prior **(3)**
`[Luminance-GS original]`

- **Gamma:** y = x^γ. **γ < 1 brightens** the darks; γ = 1 does nothing.
- **S-curve:** darkens below a midpoint α, brightens above it, so **more contrast**; β sets the strength.
- **Shape prior P_k** = S-curve(gamma(identity)) per view; in practice **only γ moves** (to about 0.1).

---

### L13 · Pseudo-target and "unsupervised" **(3)** ★
`[Luminance-GS original]`

- **Pseudo-target:** a stand-in answer = **the dark photo passed through the learned curve**.
- **Unsupervised:** no ground truth; targets come from the **input + priors** (assumptions such as "use the whole range" and "keep the curve smooth").
- The **enhanced render** trains toward it; at test time **only the enhanced Gaussians** are used.

---

### L14 · How the original builds each view's curve **(3)** ★
`[Luminance-GS original]`

- **Global curve L_g:** one learnable **255-value** curve shared by all views, starting at the **identity**.
- **Curve bias L_b,k:** a 255-value **per-view correction** from a **cross-attention network** (photo + pose). L_k = clamp(L_g + L_b,k).
- Plus a per-view **colour basis** and a **shape network** for the prior: about **255k parameters** in all (bias net 143,743 + shape net 111,235).

---

### L15 · Cross-attention in Luminance-GS **(2)**
`[Luminance-GS original]`

- **Query** = the camera **pose**; **keys and values** = **image features** (16 tokens from a small CNN).
- Intuition: **the pose decides which parts of the photo to look at**; the output is the per-view curve bias.

---

### L16 · The dark branch **(2)**
`[Luminance-GS original]`

- The Gaussians also render a **dark version** that must match the **dark photo**, which keeps the scene tied to **real data**.
- It has **one dark colour per Gaussian for all views**, so it fails when photos have **different exposures** (fit drops **3.6 to 11.9 dB**). My fix scales each view's dark render by **2^{−s_k}**: **+5.8 to +7.6 dB** fit.

---

### L17 · The four losses **(4)**
`[Luminance-GS original]`

- **L_low:** dark render vs **dark photo**.
- **L_enh (×0.5):** enhanced render vs **pseudo-target**.
- **L_spa:** keeps the enhanced render's **local contrast** consistent with the dark photo.
- **L_hist (×10):** curve vs **HE-CDF** + **smoothness** + **shape prior**. It **dominates** (about 5× the image terms), so the curve is shaped **mainly by the priors**.

---

# F. Metrics

---

### M01 · PSNR and dB **(3)** ★
`[Metrics]`

- **PSNR = 10 · log10(1 / MSE)** for images in [0, 1]. **Higher = closer** to the ground truth.
- **dB is a log scale:** **+3 dB ≈ half the error**; **+1 dB ≈ 21% less** squared error; +10 dB = 10× less.
- **Pixel by pixel:** ignores structure and **punishes brightness offsets** hard. About 20 dB is fair, 30 dB is very good.

---

### M02 · Brightness-matched PSNR **(2)** ★
`[Metrics]`

- **Scale the render to the ground truth's mean brightness**, then take PSNR.
- **Why:** with no normal-light training images, overall brightness **can't be known**; this separates **detail and colour** from **exposure**. Always shown **next to raw PSNR**.

---

### M03 · SSIM **(2)**
`[Metrics]`

- **Structural similarity:** compares **local mean, contrast and structure** in small windows; **0 to 1**, 1 = identical.
- Closer than PSNR to how people judge **structure**; also part of the 3DGS loss.

---

### M04 · LPIPS **(2)**
`[Metrics]`

- **Learned perceptual distance:** compares **deep-network features** (VGG or AlexNet) of two images; **lower = better**.
- Best of the three at matching **human judgement** of blur and texture.

---

### M05 · Precision, recall, F1 **(3)** ★
`[Metrics]`

- **Precision = TP / (TP + FP):** of what I flagged, **how much was right**.
- **Recall = TP / (TP + FN):** of what was there, **how much I found**.
- **F1** = their harmonic mean. Set the threshold by the **cost of a miss vs a false alarm** (in inspection, misses usually cost more).

![](figs/confusion.png)

---

### M06 · IoU and mAP **(3)**
`[Metrics]`

- **IoU** = overlap area / union area of predicted and true boxes; a detection counts as correct if **IoU ≥ 0.5** (common choice).
- **AP** = area under the **precision-recall curve** for one class.
- **mAP** = **mean AP over classes** (COCO also averages over IoU 0.5 to 0.95).

![](figs/iou.png)


---

### M07 · TP, FP and FN for a detector **(3)** ★
`[Metrics]`

- **TP:** a box on a real cup (IoU ≥ 0.5 with the label). **FP:** a box on **no cup** (a Coke can) or a **duplicate**. **FN:** a cup with **no box**.
- **No TN** in detection: "no box on empty belt" happens everywhere, so we use **precision** (TP ÷ all boxes) and **recall** (TP ÷ all cups) instead of accuracy.
- **Threshold trade-off:** raise confidence → **fewer FPs, more misses**. Capstone: an FP = **picking recycling**. Mine site: an FP = **false belt stop**, an FN = **crusher damage**.

---

# G. Computer vision fundamentals

---

### F01 · Digital image basics **(3)**
`[CV fundamentals]`

- A grid of **pixels**; colour images have **3 channels** (R, G, B).
- **8-bit = 256 levels** (0 to 255) per channel; networks usually use **[0, 1]**.
- **mm per pixel** sets the smallest defect you can see (about **3+ pixels** across it).

---

### F02 · Colour spaces **(2)**
`[CV fundamentals]`

- **RGB** is how sensors store colour. **HSV**: **Hue** (colour angle), **Saturation**, **Value**, so colour thresholds are easier. **Grayscale** for most inspection.
- A **hue flip** (my research) = a colour changing identity, e.g. a **yellow wheel turning red**.

---

### F03 · Exposure and stops **(3)** ★
`[CV fundamentals]`

- Exposure = light collected: **shutter time × aperture**, then **gain (ISO)** amplifies it.
- **1 stop = 2× the light**; 2^{s} scales by s stops (**−1 = half, +1 = double**).
- In inspection, **fix the exposure** so features look the same in every frame; auto-exposure changes the image.

---

### F04 · Dynamic range, clipping, gamma **(3)**
`[CV fundamentals]`

- **Dynamic range:** darkest to brightest the sensor can record; beyond it, **clipping** (detail lost).
- Sensors are **linear**; **gamma / sRGB** compresses values for display.
- Bright welds next to dark background → **HDR** or several exposures.

---

### F05 · Noise in low light **(2)**
`[CV fundamentals]`

- **Shot noise** (random photon arrivals, grows with √signal) + **read noise** (fixed, electronics), so low light = low **SNR**.
- **Brightening amplifies noise**. Fixes: more light, longer exposure, **frame averaging**, denoising.

---

### F06 · Smoothing filters **(2)**
`[CV fundamentals]`

- **Gaussian blur:** a weighted average (a **convolution**); removes fine noise but **softens edges**.
- **Median filter:** the middle value in each window; kills **salt-and-pepper** noise and **keeps edges**.

---

### F07 · Edge detection **(3)**
`[CV fundamentals]`

- **Sobel:** convolution kernels for the **x and y gradients**, giving edge strength and direction.
- **Canny:** blur → gradient → **thin the edges** (non-max suppression) → **two thresholds** (hysteresis).
- Uses: **measure dimensions**, find **cracks**, locate parts.

---

### F08 · Thresholding and blob analysis **(3)**
`[CV fundamentals]`

- **Threshold:** pixel > T → foreground. **Otsu** picks T automatically from the histogram (best split between two peaks).
- **Adaptive threshold** when the lighting is uneven.
- Then **connected components / contours**: count, **area, centroid, bounding box**.

---

### F09 · Morphology **(3)**
`[CV fundamentals]`

- **Erosion** shrinks white regions (removes specks); **dilation** grows them (fills gaps).
- **Opening** = erode then dilate: **removes noise**. **Closing** = dilate then erode: **fills holes**.
- Used to **clean up binary masks** before measuring.

![](figs/morphology.png)

---

### F10 · Features and matching **(3)**
`[CV fundamentals]`

- **Keypoints + descriptors** (**SIFT**, **ORB**) are **matched** across images.
- **RANSAC:** fit the model to random minimal samples, keep the fit with the **most inliers**, so bad matches don't matter.
- Used in **SfM / COLMAP**, image stitching, pose estimation.

---

### F11 · Pinhole camera model **(3)** ★
`[CV fundamentals]`

- A 3D point (X, Y, Z) lands at pixel **x = f · X / Z + cx** (similar triangles).
- **Intrinsics K:** focal length **f**, principal point **(cx, cy)**, plus **lens distortion**.
- **Extrinsics [R | t]:** where the camera **sits and points** in the world.

![](figs/pinhole.png)

---

### F12 · Camera calibration **(3)** ★
`[CV fundamentals]`

- Show a **checkerboard or ChArUco board** in many poses → **cv2.calibrateCamera** (Zhang's method).
- Solves the **intrinsics + distortion** (radial, tangential) and each view's pose.
- Check the **reprojection error** (good: **under ~0.5 px**). **Recalibrate** after any lens or mount change.

---

### F13 · Homography **(2)**
`[CV fundamentals]`

- A **3×3 matrix** that maps one **plane** to another; needs **4 point pairs**.
- Use: **pixel → belt coordinates** on a flat conveyor, or a top-down view.

---

### F14 · Stereo vision **(3)**
`[CV fundamentals]`

- Two cameras a **baseline B** apart see the same point shifted by a **disparity d**.
- **Depth Z = f · B / d**: near = big disparity, far = small.
- Needs **texture** to match; fails on plain or shiny surfaces, so add a **projected pattern** (active stereo).

![](figs/stereo.png)

---

### F15 · Structured light and laser triangulation **(3)** ★
`[CV fundamentals]`

- **Structured light:** project known **patterns**; the camera sees how they **bend** → dense 3D. Accurate **close up**; hurt by **ambient light and shiny parts**.
- **Laser triangulation:** a **laser line** on the part, a camera at an **angle**; height **shifts the line** in the image → **one profile per frame**.
- On a conveyor: profiles + **encoder** = a full 3D scan. **Both are named on Hatch's robotics page.**

![](figs/laser_triangulation.png)

---

### F16 · Time-of-flight and LiDAR **(2)**
`[CV fundamentals]`

- **ToF camera:** measures **light travel time** per pixel → a depth image; fast, **lower resolution**, **multipath** errors.
- **LiDAR:** a scanning laser ToF → **long-range** point clouds (mine vehicles, stockpiles).

---

### F17 · Point cloud processing **(3)**
`[CV fundamentals]`

- **Downsample** (voxel grid) and **remove outliers**.
- **RANSAC plane fit** to remove the floor or belt.
- **ICP** to align two clouds; **clustering** to separate objects.

---

### F18 · Classification vs detection vs segmentation **(3)** ★
`[CV fundamentals]`

- **Classification:** **one label** for the image ("cup").
- **Detection:** a **box + label** per object (YOLO).
- **Segmentation:** a label **per pixel** (semantic = class; instance = each object separately).

![](figs/cls_det_seg.png)

---

### F19 · YOLO and non-max suppression **(4)** ★
`[CV fundamentals]`

- **What:** "**You Only Look Once**", a **one-stage detector**. A **grid** over the image; each cell predicts **boxes + objectness + class** in **one pass**, so it runs in **real time**.
- **Used for:** fast detection of **objects on a line or a site**: parts, people and vehicles, **PPE**, defects, our cups.
- **Non-max suppression (NMS):** of boxes that overlap (**IoU above a threshold**, 0.4 for us), keep the **most confident**.
- The **confidence threshold** (0.5 for us) trades **precision against recall**.

![](figs/yolo_grid.png)

---

### F20 · Anomaly detection for rare defects **(2)**
`[CV fundamentals]`

- Defects are **rare**, so train on **good parts only** and flag anything that looks different.
- Methods: **autoencoder reconstruction error**, **PatchCore** (feature distances). Useful when you can't collect many defect images.

---

### F21 · Motion blur and shutters **(3)** ★
`[CV fundamentals]`

- **Blur (px) = speed × exposure time ÷ (mm per px)**; keep it **under 1 px**. Example: 1 m/s, 1 ms, 0.5 mm/px → **2 px**.
- Fix: **shorter exposure + a strobe** light.
- **Global shutter** (all pixels at once) for moving parts; a **rolling shutter** skews them.

---

### F22 · Machine-vision lighting **(4)** ★
`[CV fundamentals]`

- **Backlight:** a silhouette → **edges and dimensions**.
- **Dome / diffuse:** even light → **shiny or curved** parts without glare.
- **Low-angle (dark-field):** grazing light makes **scratches and dents** light up.
- **Coaxial / polarisers:** cut **glare** on flat shiny surfaces. Rule: **"lighting first, algorithm second"**.

![](figs/lighting.png)


---

### F23 · Image preprocessing: what's necessary? **(4)** ★
`[CV fundamentals]`

- **Must match training:** same **size** (416×416), **scaling** (0 to 1) and **channel order** (RGB). A mismatch is a **silent bug**.
- **Camera side:** **fix exposure, gain, focus and white balance** so images don't drift; **crop to the region of interest**; **undistort** if you measure.
- **Training only, augmentation:** flips, crops, scale, **hue / saturation / exposure jitter** (Darknet's YOLOv3 config does these by default), so the model sees more variety.
- **Classical clean-up** when needed: **denoise** (Gaussian, median), **contrast** (histogram equalisation, CLAHE), **colour space** (HSV for colour thresholds).

![](figs/preprocess.png)

---

### F24 · OpenCV **(3)**
`[CV fundamentals]`

- The standard open-source **computer vision library** (C++ with **Python** bindings).
- Does: **camera capture**, resize, colour conversion, **filters, edges, thresholds, contours**, **calibration**, drawing, and a **DNN module** that runs trained networks.
- **In my capstone:** `VideoCapture` (exposure, gain), `blobFromImage`, `dnn.readNet` + **CUDA**, `NMSBoxes`, then `rectangle` / `putText` / `imshow` for the live overlay.

---

### F25 · Using YOLO, start to finish **(5)**
`[CV fundamentals]`

1. **Collect** images **in the real setting**, including some with **no objects**.
2. **Label** boxes (Label Studio, CVAT, Roboflow) → YOLO text format: class, x, y, w, h (0 to 1).
3. **Train** from **pretrained weights**; hold out a **test set**; watch the **loss and mAP**.
4. **Choose thresholds** (confidence, NMS) on held-out data, by the **cost of misses vs false alarms**.
5. **Deploy and measure:** export (we used Darknet → OpenCV DNN; today **ONNX / TensorRT**), check **latency** on the real hardware, wire the output to the machine.

*Today, in a few lines with Ultralytics:* `model = YOLO("yolo11n.pt")`, `model.train(data="cups.yaml")`, `model.predict(frame)`.

---

# H. Industrial vision and integration

---

### I01 · PLC **(3)** ★
`[Industrial vision]`

- **Programmable Logic Controller:** a rugged industrial computer running the machine's **deterministic logic** in a fast **scan cycle** (read inputs → run logic → write outputs).
- Programmed in **ladder logic or structured text** (IEC 61131-3); main vendors **Allen-Bradley (Rockwell)** and **Siemens**.
- The vision PC sends it **results**; the PLC **decides and actuates**, and owns the **safety interlocks**.

---

### I02 · Industrial communication **(2)**
`[Industrial vision]`

- **Digital I/O** (24 V) for a simple **trigger and pass/fail**.
- Industrial Ethernet: **EtherNet/IP** (Rockwell), **PROFINET** (Siemens), **Modbus TCP** (simple), **OPC UA** (data to plant IT systems).

---

### I03 · Vision-to-PLC handshake **(3)** ★
`[Industrial vision]`

- The PLC sets **Trigger** → vision sets **Busy**, grabs and processes the image.
- Vision writes the **Result** and sets **Result Valid** → the PLC reads it and **acknowledges**.
- A **heartbeat / watchdog** and a **fail-safe default** (no result in time → reject or stop).

![](figs/plc_handshake.png)

---

### I04 · Encoders and hardware triggers **(2)** ★
`[Industrial vision]`

- **Encoder:** pulses per millimetre of belt travel, so you know the **exact position** even if the speed changes.
- A **photo-eye or encoder count triggers the camera** at the right spot, and the part is **tracked from camera to actuator** by counts.

---

### I05 · Edge deployment **(3)** ★
`[Industrial vision]`

- **Export** the model (PyTorch → **ONNX**), optimise it (**TensorRT**, OpenVINO), use **FP16 / INT8**.
- Hardware: **NVIDIA Jetson** or an industrial PC with a GPU; **fanless, sealed**.
- Measure **worst-case latency** (not the average) and **throughput**; add a **watchdog and logging**.

---

### I06 · Hand-eye calibration **(2)**
`[Industrial vision]`

- Find the transform between the **camera frame and the robot frame** (camera on the arm = eye-in-hand; fixed camera = eye-to-hand).
- Solved from several robot poses viewing a target (**AX = XB**, cv2.calibrateHandEye), so the robot can **go where the camera sees**.

---

### I07 · Domain shift: works in the lab, fails on site **(3)** ★
`[Industrial vision]`

- On site the **lighting, dust, angle and wear** differ from the training data.
- Fix: **collect site data early**; augment **brightness, exposure, blur**; test **per condition**.
- **Monitor** confidence and drift; **retrain** on logged images.

---

### I08 · Acceptance testing, shadow mode, commissioning **(3)**
`[Industrial vision]`

- **FAT** = factory acceptance test (in the shop); **SAT** = site acceptance test (after installation).
- **Shadow mode:** the system runs and **logs decisions without acting**, compared against the operators.
- **Commissioning:** install, tune, and prove it meets **acceptance criteria set beforehand**.

---

### I09 · Harsh environments **(3)**
`[Industrial vision]`

- **Dust and steam:** **sealed (IP-rated) enclosures**, **air knives or purge air**, a cleaning schedule.
- **Heat:** cooling jackets, **standoff distance**, calibration **drifts with temperature**.
- **Vibration and changing light:** rigid mounts, **your own lighting**, fixed exposure, regular calibration checks.

---

### I10 · Annotation and synchronisation **(3)**
`[Industrial vision]`

- **Annotation:** clear **labelling guidelines**, a tool (**CVAT**, Label Studio), and **double-check a sample**.
- **Sync sensors:** **hardware trigger** or a shared clock (**PTP / IEEE 1588**); **timestamp everything**.
- Keep **raw data + metadata** (exposure, time, camera) so results can be traced.

---

# I. Machine learning fundamentals

---

### N01 · Convolution **(3)** ★
`[ML fundamentals]`

- Slide a **small kernel** (e.g. 3×3 numbers) over the image; at each spot **multiply the overlapping values and add them up** → one output pixel.
- The kernel's numbers decide **what it finds** (an edge, a blur). In a **CNN the kernel numbers are learned**.
- The **same kernel everywhere**: **few parameters**, and it finds the pattern **anywhere** in the image.

*Simply:* a stencil you slide across the picture. The output lights up wherever the picture matches the stencil.

![](figs/convolution.png)

---

### N02 · ReLU and pooling **(3)**
`[ML fundamentals]`

- **ReLU:** max(0, x); **negatives become 0**. This adds the non-linearity a network needs.
- **Max pooling:** keep the **largest value** in each 2×2 window, so the image is **half the size** but keeps the strongest responses.
- **Adaptive average pooling:** resize to a **fixed grid** (Luminance-GS: 16 tokens).

![](figs/relu_pool.png)

---

### N03 · Linear layer **(2)**
`[ML fundamentals]`

- **y = Wx + b**: a learned **matrix multiply** plus a bias; every input connects to every output.
- In Luminance-GS a final **Linear 128 → 255** outputs the per-view curve bias.

---

### N04 · Attention **(3)**
`[ML fundamentals]`

- A **query** is compared with each **key** (a dot product), giving similarity **scores**.
- **Softmax** turns the scores into **weights that sum to 1**.
- The output is the **weighted average of the values**: "look mostly where the query matches".

![](figs/attention.png)

---

### N05 · Loss, gradient, backpropagation **(3)**
`[ML fundamentals]`

- **Loss:** one number for **how wrong** the model is; training makes it smaller.
- **Gradient:** the **slope** of the loss for each parameter: which way to move it, and how hard.
- **Backpropagation:** the **chain rule** applied **backwards** from the loss through every layer, giving the gradient for **every parameter**.

![](figs/gradient.png)

---

### N06 · Optimiser vocabulary **(4)**
`[ML fundamentals]`

- **Learning rate:** the step size (too big → bounces or diverges; too small → slow).
- **Adam:** keeps **running averages** of each gradient and its square, so **each parameter gets its own step size**.
- **Weight decay:** pulls weights toward 0, a form of **regularisation**.
- **Schedule:** **lower the learning rate** over training (Luminance-GS decays it to **1%**).

---

### N07 · Overfitting **(3)** ★
`[ML fundamentals]`

- The model **memorises the training data** and fails on new data: **training loss falls, validation loss rises**.
- Fixes: **more or augmented data**, **regularisation** (weight decay, dropout), **early stopping**, a smaller model.
- Always judge on a **held-out** set.

---

### N08 · Train / validation / test, and data leakage **(3)** ★
`[ML fundamentals]`

- **Train** fits the weights; **validation** guides choices; **test** is used **once**, at the end.
- **Leakage:** test information sneaks into training, so results look **too good**.
- For video or conveyor frames, **split by session or day**, not by random frame (neighbouring frames are nearly identical).

---

### N09 · Transfer learning and augmentation **(2)**
`[ML fundamentals]`

- **Transfer learning:** start from **pretrained weights** (e.g. COCO) and **fine-tune** on a few hundred of your own images.
- **Augmentation:** flips, crops, **brightness and exposure**, blur, noise, so the model copes with **site conditions**.


---

### N10 · CNN (convolutional neural network) **(3)** ★
`[ML fundamentals]`

- Layers of **small learned filters** that slide over the image (card N01), each followed by **ReLU**, with **downsampling** between stages.
- **Hierarchy:** **edges → textures → parts → objects**; a **head** turns the last maps into **classes or boxes**.
- **Why for images:** the **same filter everywhere** (weight sharing) means **far fewer weights**, and it finds a pattern **anywhere**. YOLOv3's backbone, **Darknet-53**, is a **53-layer** CNN.

![](figs/cnn.png)

---

### N11 · DNN (deep neural network) **(2)**
`[ML fundamentals]`

- A neural network with **many layers** between input and output. **CNNs** and **transformers** are kinds of DNN.
- **OpenCV's DNN module** only **runs** networks trained elsewhere (Darknet, ONNX, TensorFlow); it **can't train**. We **trained in Darknet** and **ran in OpenCV**.

---

### N12 · CUDA, and why vision uses GPUs **(3)** ★
`[ML fundamentals]`

- **CUDA** = NVIDIA's platform for running **general code on the GPU**; **cuDNN** = its library of fast **neural-network** operations.
- **Why vision:** images are **millions of pixels**, and convolution does the **same multiply-add at every pixel**, so the work splits across **thousands of GPU cores** at once.
- **Mine:** capstone, **OpenCV DNN on CUDA** (~0.2 → 0.09 s); research, **PyTorch** + **gsplat's CUDA renderer** on an **RTX 3080 Ti**, about **5 to 8 min** per training run.

![](figs/cpu_gpu.png)

---
---

# Sheet 1 · Research project: low-light 3D reconstruction

**One line:** I showed that a 255,000-parameter brightening module inside a CVPR 2025 3D reconstruction method was really doing something simple, replaced it with a 70-parameter physical model, and tested it with rules fixed in advance.

## What

- **Base method:** Luminance-GS (CVPR 2025) builds a **3D Gaussian Splatting** scene from **dark photos** that renders **normally lit**, with no normal-light training images.
- **Its brightening part:** a learned **tone curve per photo** (255-entry lookup table) from **two neural networks** + a colour transform: about **255k parameters**.
- **My replacement:** **one shared monotone curve F + one exposure s_k per photo**: L_k(x) = F(min(1, 2^{s_k} x)). **55 to 76 parameters**.

![](figs/lgs_pipeline.png)

## Why

- **Research question:** does the big module reduce to a simple, explicit model, and is that model **as good on normal data** and **better when exposure varies**?
- **Industrial angle:** cameras in the field **disagree on exposure** (auto-exposure, several cameras, changing light). A model that **separates the scene from the camera** should hold up where a black box doesn't.

## How

1. **Reproduce** (9 runs): same seed differs by up to **1 dB**, so **3 seeds** per setting and effects count only above **2× seed noise**.
2. **Diagnose before building** (Rung 0, 30 runs): curves already **monotone**; views differ by **one number** that tracks brightness (**over 99%**).
3. **Untangle a confound** (Rung 0.5, 2×2, 60 runs): the "detach" gain is **85 to 100%** from the curve, not the colour transform. "Detach" becomes the **baseline to beat**.
4. **Build a test with a known answer** (M1): each training photo brightened or darkened by a **known gain, up to ±1 stop**. The original's per-view curves go the **wrong way**.
5. **Build and test Rung 2** (65 runs), with **H1 and H2 rules written before any run**.

![](figs/tone_design.png)

## Results

| Test | Rung 2 vs `detach` | Verdict |
|---|---|---|
| **H2:** varying exposure | **+2.11 dB** brightness-matched PSNR pooled (**5.3× noise**); ahead in 4 of 4 decision scenes; LPIPS better | **Supported** |
| Exposure leak (0 = corrected, 1 = passes through) | **0.01** vs 0.51 (official 0.41) | Mechanism confirmed |
| Repeatability, varying set | seed spread **0.11 dB** vs 0.72 dB | Far more repeatable |
| **H1:** even exposure (LOM) | pooled **−0.02 dB**; **11 of 12** checks pass; **bike −0.155 dB** vs a −0.082 dB bar | **Not supported** |
| Cost | **55 to 76** vs ~255,000 curve parameters; **4.6 vs 7.8 min** per run | ~40% faster |

![](figs/results_slope.png)

![](figs/leak.png)

**How to read the leak figure:** x = the gain I applied to a training photo; y = how much of that gain reached the photo's pseudo-target. Dashed (slope 1) = passes straight through; flat (slope 0) = corrected. Official and detach let **about half** through; Rung 2 is **flat**. That is the mechanism behind the +2.11 dB.

## What it means

- The big module's per-photo behaviour **is essentially one exposure number**, and modelling it explicitly **fixes what the networks got wrong** (the leak).
- When exposure varies, the simple model is **clearly better and more stable**. On even lighting it **matches overall** but narrowly **fails one strict per-scene check**, which I report as a miss.
- A pre-declared follow-up showed the result depends on **where the curve starts** (+0.3 dB on one seed, exploratory): the next lever.

## Limits and next

- **5 scenes, 3 seeds**; exposure changes **synthetic**; **hue** worse on bike; F learns from **2D histograms only** by default.
- **Next:** H3 (let only the exposures learn from the render), a colour-preserving variant, the curve's dark end. **Freeze 5 Dec, report 18 Dec.**

## Numbers to have ready

**255k → 55 to 76** parameters · **+2.11 dB** (5.3× noise) · leak **0.01 vs 0.51** · **23.23 → 23.11** vs **23.25 → 21.03** · **11 of 12** checks, bike **−0.155 dB** · **~160** training runs · **40%** faster · **3 seeds, 2× noise rule**

---
---

# Sheet 2 · Capstone: the CCPU, a vision-guided cup-sorting robot

**One line:** Our team of three built a robot that spots Tim Hortons cups in mixed recycling on a moving conveyor and lifts them out with a vacuum gantry timed to the belt: 95% removed, under 1% false positives in about 100 trials.

![](figs/capstone_rig.png)
![](figs/capstone_system.png)

## What

- A **conveyor** carries mixed recycling; a **webcam ~1 m above** watches it; an **x–z gantry** with a **suction cup** downstream lifts **Tim Hortons cups** into a **low-grade compost** bin.
- **Sept 2022 to Apr 2023**, ENGPHYS 4A06, team of **3**: Dayyan (mechanical, power), Shahaan (vision lead), me (**team lead, gantry design, motor control code, integration**, and much of the vision work). Shown at the **Capstone Expo**.

## Why

- Single-use cups **aren't recyclable** (plastic liner). Our report cited **over 1 million a day** thrown out in the GTA. Hamilton uses them as **low-grade compost**, but **sorts by hand**.
- **Tim Hortons cups** are the most common, and a clear first target: **red, distinctive shape**.
- The engineering problem: **see, decide and act on a moving target**, on time.

## How

1. **Capture:** **LED strips** along both sides of the belt; 960×720 at **short exposure + high gain** to stop motion blur; autofocus off.
2. **Preprocess:** resize to **416×416**, ÷255, BGR → RGB.
3. **Detect:** **YOLOv3**, one class, in **OpenCV DNN on CUDA**: ~**0.09 s** per frame (CPU ~0.2 s).
4. **Filter:** confidence > **0.5**, then **NMS** at IoU 0.4.
5. **Locate:** box centre → cm on the belt (~**0.7 mm per pixel**); each cup reported **once**, from a **7 cm zone**; queued and moved along at **belt speed**.
6. **Send:** the cup's **lane (0 to 17 in)** over **USB serial** to the gantry **ESP32**.
7. **Pick (my code):** inches → steps (**127 steps per inch**); move across; **wait = 2.3 s − arm time − 0.55 s**; lower, **valve closes** (suction), lift, carry to the bin, **valve opens** (drop), return, send **"done"**.
8. **No-skip mode (mine):** if too many cups come, the program **freezes the belt** until the arm is free, so **no cup is missed**.

![](figs/capstone_timing.png)

**Training the detector**

- **912 images** from our own webcam on the real belt: cups (new, crushed, lid on or off) **mixed with random recycling**, about 10% with **no cups**.
- **Label Studio** on an **AWS** server (all three labelling at once); **Darknet on Google Colab** from a **pretrained Darknet-53** backbone; 2,000 iterations, about 3 h; 10% held out.
- Three versions: **179 → 311 → 912** images. Each added the **things it confused** with cups.

![](figs/capstone_before_after.png)

## Results

| Measure | Value |
|---|---|
| Cups detected and removed | **95%** (about 100 manual checklist trials) |
| False positives | **under 1%**; final model: none observed |
| Detection time | **~0.2 s CPU → 0.09 s GPU** (about 2.3×) |
| Pick timing | cup under the arm **~2.3 s** after detection; full cycle **~8 s** |
| Main failure | **no seal** on crumpled cups or the rim |
| Budget | about **$590** |

## Safety

- **Instant-stop switch** and an easy-to-reach **power cord**; **temperature sensors** on the electronics (fans to max when hot, a **warning** if too hot); **halt on a jam**; **side barriers** on the belt; **start-up and running warning lights**.

## What it means

- A **full vision-to-actuator loop**: data, model, latency, timing and mechanics all had to work **together**. A **simple interface** (one number over serial) made integration easy.
- **Hard negatives matter:** the model learned **"red ≠ cup"** only after we showed it red cans and cartons.
- **The arm, not the detector, set the throughput** (an 8 s cycle). Same lesson as Hatch's **"on the fly"** robotics: **sync motion with a moving process**.

## What I would do differently now

1. **Metrics from day one:** precision, recall and mAP on a held-out set from **another day**. Our report admits we judged by eye.
2. **Encoder** on the belt instead of an assumed speed; a **hardware trigger** for the camera.
3. **Controlled lighting** in a hood; fixed exposure.
4. **A newer YOLO → ONNX / TensorRT on a Jetson**; log every pick.
5. **PLC, e-stop and guarding** instead of microcontrollers.

## Numbers to have ready

**912** images · **95%** removed · **under 1%** false positives · **~100** trials · **0.2 → 0.09 s** on GPU · **416×416** input · confidence **0.5**, NMS **0.4** · belt **22.5 cm/s** · pick at **~2.3 s** · **127 steps per inch** · pump **−65 kPa** · team of **3** · **$590**

---
---

# Sheet 3 · Designing a vision system: the method, and a mining example

**Use it when they ask:** "How would you design a vision system for X?" Ask two or three questions first, walk the eight steps, then say how you would prove it works.

## The method in 8 steps

*Mnemonic:* **R**eally **S**mart **L**ights **D**on't **M**ake **I**ndustrial **V**ision **M**agic.

| Step | What to decide | A line to say |
|---|---|---|
| 1. **Requirements** | What must be seen, what decision follows, smallest feature, line speed, latency, **cost of a miss vs a false alarm** | "First I'd pin down what a miss costs compared with a false alarm." |
| 2. **Sensor** | 2D, 3D, thermal or line-scan; pixel size = field of view ÷ pixels, with **3 to 5 px** across the smallest feature; **global shutter** | "Exposure must be short enough that the part moves less than a pixel." |
| 3. **Lighting + protection** | Backlight, dark-field, diffuse or structured light; **strobe**; **hood**; sealed enclosure, heating or cooling, **air knife** | "Control the light and you've solved half the problem." |
| 4. **Data** | Collect **on site, early**, in every condition; label; a **test set from other days**; **seeded** known defects | "I'd collect on site before choosing a model." |
| 5. **Model** | **Classical first** (thresholds, blobs, edges, 3D geometry), then ML (detector, segmentation, anomaly detection); fits the **edge latency** | "Start with the simplest thing that could work, and measure it." |
| 6. **Integrate** | Trigger (**encoder** or photo-eye); **calibration** (camera → world → robot); **PLC handshake**; **fail-safe** default; timing budget | "The PLC decides; vision gives it a clear, timed answer." |
| 7. **Validate** | Pass/fail rules **written first**; precision and recall **per condition**; lab → **shadow mode** → commissioning | "Same discipline as my research: rules before results." |
| 8. **Maintain** | Monitoring, **drift**, cleaning, retraining, documentation and handover | "A vision system is never finished at commissioning." |

**Two numbers worth knowing:** max exposure = pixel size ÷ speed (1 mm pixels at 4 m/s → **0.25 ms**). Time budget = distance to the action point ÷ speed (20 m at 4 m/s → **5 s**).

## Worked example: oversize rocks and tramp metal on a crusher feed belt

**Why this one:** it's my capstone at mine scale: detect on a moving belt, then act in time. Tramp metal (bolts, shovel teeth, rebar) and oversize rocks **damage crushers and block chutes**.

![](figs/mining_conveyor.png)

**Questions I'd ask first:** belt speed and width? Which objects, and the smallest size? What action (stop, divert, robot pick, alarm), and how far before the crusher? What does a false stop cost?

| What I'd account for | How I'd deal with it |
|---|---|
| **Dust and mud** on the window | Sealed hood, **air knife** or purge, a wiper; a **dirty-lens self-check** (sharpness drops → alarm); a cleaning schedule |
| **Sun, shadows, night**, or dark underground | Hood to block outside light; **own LED light, strobed** with the exposure; exposure normalisation (my research) |
| **Fast belt** (2 to 6 m/s) → blur | **Global shutter** or line-scan; exposure ≤ pixel ÷ speed; strobe; **encoder trigger** |
| **Everything is grey and dusty**, so colour is useless | **3D laser line profiler**: height and size directly; a **metal detector** for steel; combine both |
| **Rocks overlap and pile up** | 3D segmentation on the height map; measure the visible top; tune thresholds with operations |
| **Rare events**, few examples | **Anomaly detection** on normal ore; synthetic insertion; **seeded tests** with real objects; human review of flags |
| **Vibration, heat, cold** | Isolated mounts; rated housings with heating or cooling; calibration check against a **fixed target** in view |
| **Time to act** | Budget = distance ÷ belt speed; **edge PC on site**, no cloud |
| **Integration and safety** | **PLC handshake** (ready, result, acknowledge) with a heartbeat; **fail-safe** if the camera dies (alarm, fall back to the metal detector); vision is **never a safety device** for people; lock-out before entering the cell |
| **Proving it works** | **Shadow mode** for weeks; **seeded objects** for recall; **false stops per shift**; acceptance rules written **before** commissioning |
| **Ore changes over time** | Watch confidence and false-stop rates; re-label and retrain; version the models |

## If the example is a smelter instead

- **Glare and radiant heat** from molten metal: **narrow-band or near-infrared filters**, ND filters, **HDR**, or a **thermal camera**.
- **Fumes and steam:** longer wavelengths (**thermal**) see through better; air purge on the window.
- **Heat on the hardware:** **water- or air-cooled** housings, distance, heat shields.
- **Typical robot tasks** (industry examples, not confirmed Hatch projects): **tapping and plugging furnaces**, **sampling**, **anode handling**. Vision **locates the target** for the robot; **telerobotics** keeps people back.

## How to say it in the room (2 minutes)

1. **Ask two or three questions** (speed, smallest object, cost of each kind of error).
2. **Walk the 8 steps**, one sentence each, with the example's specifics.
3. **Name the trade-off** (false stops vs misses) and who decides it (operations, with the client).
4. **Close with validation:** "rules written before testing, shadow mode, then commissioning", and link it to my research (rules fixed before any run) and my capstone (a moving belt, timed picks).

---
