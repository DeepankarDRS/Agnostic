# Prompt Engineering for Generative AI

**Prompt engineering** is the art of asking the right questions to get the best output from a Large Language Model (LLM). Instead of coding, you "program" LLMs with plain language prompts.

---

## 📚 Learning Objectives
- Describe basic prompting techniques  
- Apply prompting best practices to create effective prompts  

---

## 🔑 Best Practices
- Clearly communicate what’s important  
- Structure the prompt: **Role → Context → Instruction**  
- Provide examples to guide output  
- Use constraints (length, format, scope)  
- Break complex tasks into simpler steps  
- Ask the model to evaluate or check its own response  
- Be creative and iterate  

---

## 📝 Types of Prompts

**Zero-shot (Direct):** Give only instruction, no examples  
*Example:* “Give me a list of blog post ideas for tourists visiting NYC for the first time.”

**Role Prompting:** Assign the model a role before giving instructions  
*Example:* “You are a travel expert. Suggest 10 NYC blog topics for first-time visitors with kids.”

**One-/Few-/Multi-shot:** Provide 1+ examples to mimic style/format  
*Example (few-shot sentiment classification):*  

**Chain-of-Thought (CoT):** Ask the model to explain reasoning step by step  
*Example:* “I bought 10 apples, gave away 4, bought 5 more, ate 1. How many left? Let’s think step by step.”

**Zero-shot CoT:** Zero-shot prompt + “Let’s think step by step”  
*Example:* “Solve this word problem. Let’s think step by step.”

---

## 🔄 Iteration Strategies
- Repeat key words/phrases  
- Specify output format (CSV, JSON, Markdown, etc.)  
- Use ALL CAPS for emphasis  
- Try synonyms/alternate phrasing  
- Use the “sandwich technique” (repeat important instructions)  
- Explore prompt libraries (PromptHero, Prompt Gallery)  

---

## 🎯 Key Takeaway
**R.I.C.E. Framework** for better prompts:  
- **R**ole  
- **I**nput  
- **C**onstraints  
- **E**xamples  

> Great prompt engineering = clarity + creativity + iteration.
