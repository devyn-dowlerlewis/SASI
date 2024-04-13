# SASI
Service Agnostic Structured Inferencing (SASI) is a flask app that allows for the easy creation and serving of LLM-powered functions via the Instructor Library.

For each function the user creates a python package based on a provided template that contains the following:

- Pydantic class specifying the input parameters
- System/Instruction prompt that includes the input parameters and explains to the LLM how to use them to generate the output parameters
- Pydantic class specifying the output parameters

Each function can be processed by any AI service supported by Instructor including models from Anthropic, OpenAI, Groq and Mistral. Functions can also be processed locally via Ollama.
