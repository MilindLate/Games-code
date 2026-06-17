# 🕹️ Games Collection Codebase

Welcome to the **Games-code** repository! This is a curated collection of polished, high-performance, and responsive arcade games built from scratch. Designed with robust game loops, object-oriented state machines, and smooth visual feedback, this repository serves as an educational playground and an arcade cabinet for classic gameplay.

---

## 🎮 Included Games & Features

### 1. 🚀 Space Worries (Overdrive Edition)
An advanced, arcade-style space survival shooter built using **Pygame**. 
* **Dynamic Delta-Time ($dt$):** Smooth, frame-rate independent physics engine tailored for high-refresh-rate displays.
* **Meta-Progression Shop:** Collect floating `Scrap` salvage during combat waves to permanently upgrade Engine Inertia, Shield Capacities, and Weapon Cooldown speeds.
* **Juice & Screenshake:** Impact matrices trigger dynamic viewport shaking and fading pixel bursts for visceral game feel.

### 2. ⚡ Pong (Overdrive Edition)
A cyberpunk-themed, modernized recreation of the foundational table tennis classic built using **Turtle Graphics**.
* **Advanced Vector Physics:** Bounce angles vary dynamically based on the exact offset location where the ball strikes the paddle.
* **Compound Velocity Scaling:** The ball accelerates with every single successful volley, amplifying the stakes.
* **Adaptive AI Agent:** Play solo against a reaction-lagged tracking script or compete locally with two players.

---

## 🚀 Getting Started & Installation

### Prerequisites
Make sure you have Python 3.8+ installed on your system. You will need the `pygame` dependency for the advanced space engine.

```bash
# Clone the repository
git clone [https://github.com/MilindLate/Games-code.git](https://github.com/MilindLate/Games-code.git)

# Navigate into the project directory
cd Games-code

# Install required external dependencies
pip install pygame