## 5 November 2025: 
### What are Django Signals 
A signal is like an event listener. 

When something happens in Django (like saving a model, deleting an object, or user login), you can make another function automatically run in response — without changing the original logic.

It’s Django’s version of an observer pattern.
--- 

### 2. 💬 Real-world analogy:
Think of a doorbell:
- The doorbell press = event (signal is triggered)
- The bell ringing sound = function that listens (receiver)
So when one thing happens, another reacts — **automatically** and **loosely coupled**.
---

### 3. Why Use Signals 
* To decouple logic —— you don't hardcore side effects in main models / views.
* To automate system reactions — like sending, creating profiles, updating stats. 
* To Track or audit actions silently.
.
---

### 4. Core Signal Concepts 
| Concept        | Description                                         |
| -------------- | --------------------------------------------------- |
| **Signal**     | The event emitter (like `post_save`, `post_delete`) |
| **Receiver**   | The function that reacts                            |
| **Sender**     | The model that triggers the signal                  |
| **Dispatcher** | Django’s system managing who listens to what        |
.
--- 

### 5. Most Comman Built-in Django Signals 
| Signal                              | Triggered When                           |
| ----------------------------------- | ---------------------------------------- |
| `pre_save`                          | Before a model’s `save()` runs           |
| `post_save`                         | After a model’s `save()` completes       |
| `pre_delete`                        | Before a model’s `delete()` runs         |
| `post_delete`                       | After a model’s `delete()` completes     |
| `m2m_changed`                       | When a many-to-many relationship changes |
| `user_logged_in`, `user_logged_out` | For authentication events                |

### 6. The Pattern to Create and Use a Signal 
`Step 1 —— Create a receiver function` 
It's a regular function that react to a signal 

`Step 2 —— Connect the receiver to the signal`
Either using the @receiver decorator or signal.connect(). 

#### 7. Example —— E-commerce Order creation Signal

