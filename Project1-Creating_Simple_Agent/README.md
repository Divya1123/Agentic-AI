
**Tools File**
In this file, we have defined all the external tools that our agent is going to use.
Agent 1 - Tavily Search Tool
- Tavily is public platform to search.
- We registered and got API key to use. Here we saved the API key as env variable, but in real-world, we use keyvault.
- we defined get_agent_tools function define tool and returned a list of defined tools.

**LLM File**
- In this file, we defined the LLM that we are going to use.
- In our case we use openai's gpt-4o model.
- We registered and got API to use. Here we saved the API as env variable, but in real-world, we use keyvault.
- We binded our LLM model with Tools list, so our model can plan and choose correct tool to perform.

**Main Agent File**