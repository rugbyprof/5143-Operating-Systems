```yaml
conversation_topic: "Instructor README – Arduino Lessons 1–3"
format: "Instructor prep guide"
audience: "Instructors"
tone: "Neutral, clear, complete"
```

# **Instructor README – Arduino Introduction Lessons (1–3)**

**For Arduino Uno or compatible boards**

This document provides everything needed for an instructor to **prepare, set up, and teach** the three introductory Arduino lessons:

1. **Lesson 1 — Blinking LED (Digital Output)**
2. **Lesson 2 — Potentiometer-Controlled LED (Analog Input)**
3. **Lesson 3 — Pushbutton Interaction (Digital Input)**

It includes:

- Required materials for instructor & students
- Pre-class setup
- Teaching goals and learning outcomes
- Full circuit expectations
- Troubleshooting notes
- Timing suggestions
- Combined wiring guidance (so all components stay connected)

---

# **1. Overview and Purpose**

These lessons introduce students to the core I/O modes in Arduino programming:

| Lesson | Component     | Concept        | Arduino Feature                     |
| ------ | ------------- | -------------- | ----------------------------------- |
| **1**  | LED           | Digital output | `pinMode(OUTPUT)`, `digitalWrite()` |
| **2**  | Potentiometer | Analog input   | `analogRead()`, `map()`             |
| **3**  | Pushbutton    | Digital input  | `digitalRead()`, pull-down resistor |

The lessons can be taught individually or run back-to-back as a full “Intro to Arduino Hardware I/O” module.

---

# **2. Materials and Quantities**

Below is the recommended per-student or per-station supply list.

### **Per student/station**

- **Arduino Uno** (or compatible)
- **USB cable**
- **Solderless breadboard** (half-size is fine)
- **Jumper wires** (8–12 male–male)
- **LED** (1)
- **Resistor 220Ω–330Ω** (1 for LED)
- **Potentiometer** (1) – typically 10kΩ
- **Resistor 10kΩ** (1) – for pushbutton pull-down
- **Pushbutton (momentary)** (1)
- **Optional:** additional LEDs, spare resistors

### **Instructor-only**

- A working demo circuit for each lesson
- Spare wires, resistors, and replacement boards
- Whiteboard diagrams or pre-rendered circuit schematics
- Projector or overhead camera to show breadboard close-ups

---

# **3. Pre-Class Setup**

### **What the instructor should prepare**

- Ensure all Arduinos are recognized by the IDE on instructor machine.
- Pre-test uploading a simple Blink sketch to validate drivers/ports.
- Pre-build **one complete end-of-lesson circuit**, containing:

  - LED on pin 13 (or your chosen digital pin)
  - Potentiometer on A0
  - Pushbutton on pin 2 with pull-down resistor
    This ensures you can demonstrate how all parts coexist.

### **Classroom logistics**

- Students should work in pairs if supplies are limited.
- Provide printed or digital copies of the student handouts for Lessons 1–3.
- Prepare a troubleshooting slide or handout.
- Make sure USB ports at student stations are functional.

---

# **4. Learning Objectives (Instructor Reference)**

### **Lesson 1 – Blinking an LED**

Students will:

- Understand breadboard basics
- Wire a simple LED + resistor circuit
- Upload code using `pinMode()`, `digitalWrite()`, `delay()`
- Identify common wiring mistakes

### **Lesson 2 – Potentiometer**

Students will:

- Wire a 3-pin analog sensor (potentiometer)
- Understand 0–1023 ADC range
- Use `analogRead()`
- Use `map()` to convert analog values to usable ranges
- Control blink speed or brightness

### **Lesson 3 – Pushbutton**

Students will:

- Understand digital input
- Build a pull-down resistor network
- Use `digitalRead()`
- Combine digital input + digital output in one sketch

---

# **5. Circuit Schematics (Instructor Reference)**

Below are textual diagrams to help with quick verification.

---

## **5.1 LED Circuit (Lesson 1)**

```
PIN 13 → Resistor (220–330Ω) → LED (long leg) → LED (short leg) → GND
```

---

## **5.2 Potentiometer Circuit (Lesson 2)**

```
5V  → Pot pin 1
A0  → Pot pin 2 (middle)
GND → Pot pin 3
```

---

## **5.3 Pushbutton Circuit (Lesson 3)**

Pushbutton across the breadboard “valley.”

```
5V → Button leg A
Digital pin 2 → Button leg B
GND → 10kΩ resistor → Button leg B
```

**Important:**
The pull-down resistor ensures the input reads **LOW** when the button is not pressed.

---

## **5.4 All Components Together**

All three circuits can coexist without removing any component:

- LED uses **digital pin 13**
- Potentiometer uses **A0**
- Button uses **digital pin 2**

No pin conflicts occur.

---

# **6. Example Code (Instructor Reference)**

### **Lesson 1 – Blink**

```cpp
const int LED_PIN = 13;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}
```

---

### **Lesson 2 – Potentiometer Controlled Blink**

```cpp
const int LED_PIN = 13;
const int POT_PIN = A0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  int potValue = analogRead(POT_PIN);
  int delayTime = map(potValue, 0, 1023, 100, 1000);

  digitalWrite(LED_PIN, HIGH);
  delay(delayTime);
  digitalWrite(LED_PIN, LOW);
  delay(delayTime);
}
```

---

### **Lesson 3 – Button Control**

```cpp
const int LED_PIN = 13;
const int BUTTON_PIN = 2;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);
}

void loop() {
  int state = digitalRead(BUTTON_PIN);

  if (state == HIGH) {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
}
```

---

# **7. Timing Breakdown (Instructor Guide)**

| Section                                 | Duration  |
| --------------------------------------- | --------- |
| Intro & hardware overview               | 5 min     |
| Lesson 1 wiring + upload                | 15–20 min |
| Lesson 2 wiring + analog theory         | 20 min    |
| Lesson 3 wiring + pull-down explanation | 15–20 min |
| Combined circuit demo                   | 5 min     |
| Open exploration / Q&A                  | 10+ min   |

Total: **~60–75 minutes**, adjustable to class needs.

---

# **8. Common Student Mistakes (Instructor Quick Reference)**

### **Wiring**

- LED inserted backward
- LED and resistor placed in same row (creates a short)
- No GND connection
- Pot outer pins swapped (still works, but direction reverses)
- Misaligned pushbutton (inserted wrong direction)
- Pull-down resistor connected incorrectly (pin floats → button unreliable)

### **Code**

- Wrong pin number
- Replacing `setup` with `Setup` or `loop` with `Loop`
- Missing semicolons
- Uploading to the wrong COM port

### **Hardware**

- Loose jumper wires
- Using 5V instead of a digital pin for LED
- USB port not supplying power (dead hub, laptop power settings)

---

# **9. Tips for Teaching**

- Demonstrate each circuit **slowly and visually**.
- Have students test the **built-in LED** before wiring their own.
- Encourage experimentation:

  - Change delays
  - Try different `map()` ranges
  - Reverse potentiometer orientation

- Emphasize **incremental testing**:

  - Get the button reading correctly before adding LED logic.

- Allow time for students to help each other; this is a great learning opportunity.

---

# **10. Optional Extensions (Instructor Options)**

Once all lessons are complete, consider these add-ons:

- **Mini project:** “LED Dimmer” using `analogWrite()` (PWM).
- **Button + Pot combo:** Button toggles blinking; potentiometer sets blink speed.
- **Two-LED patterns:** Pot controls which pattern runs.
- **Add a buzzer:** Basic tones or alarms.
- **Add a small OLED display:** Show analog values numerically.

---

# **11. Instructor Final Notes**

- These three lessons form a strong foundation for **all future Arduino work**.
- Students will leave understanding:

  - Digital output
  - Analog input
  - Digital input
  - Breadboard logic
  - Serial communication (if you choose to introduce it)

If you want, I can generate:

- A **one-page printable cheat sheet**
- A **slide deck** matching all three lessons
- A **combined student packet PDF**
- A **fourth lesson** that ties everything together (mini-project)

Just let me know!
riffin