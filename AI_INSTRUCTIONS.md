# AI-Brain Rules for AI Assistants

This project uses AI-Brain for persistent project context. 
Before analyzing the project or starting a large task:

1. Locate and read `.ai-brain/graph.json` to understand the current symbol map.
2. If context drift occurs, ask the user to run `aib inject` and paste the result.
3. This project categorizes logic into [MODELS], [CTRLS], [SERVICES], and [HELPERS]. Use the Symbol Map to find specific logic.
4. When you finish a task, remind the user to run `aib sync` to update the project history.
