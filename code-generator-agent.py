import openai
from toolhouse import Toolhouse
from uagents import Agent, Context, Model, Protocol
from uagents.models import ErrorMessage
from uagents.setup import fund_agent_if_low
from ai_engine import UAgentResponse, UAgentResponseType


# Set the OpenAI API key correctly
openai.api_key = '<YOUR_OPENAI_API_KEY>'
th = Toolhouse(access_token='<YOUR_TOOLHOUSEAI_API_KEY>', provider="openai")
AGENT_MAILBOX_KEY = "911d1aac-059c-4cae-ab16-cfc75362953f"

class ToolHouseAIRequest(Model):
    query: str


agent = Agent(
    name="toolhouseai-test-agent",
    seed="toolhouseai-seed",
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai"
)

fund_agent_if_low(agent.wallet.address())

toolhouseai_proto = Protocol(name="ToolhouseAI-Protocol", version="0.1.0")


async def get_answer(query):
    # Define the OpenAI model we want to use
    MODEL = 'gpt-4o-mini'

    messages = [{
        "role": "user",
        "content": query

    }]

    response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        # Passes Code Execution as a tool
        tools=th.get_tools()
    )

    # Print the generated code first
    generated_code = response.choices[0].message.content
    print("Generated Code:\n", generated_code)

    # Runs the Code Execution tool, gets the result,
    # and appends it to the context
    messages += th.run_tools(response)

    final_response = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=th.get_tools()
    )



    # Prints the execution result
    print("Execution Result:\n", final_response.choices[0].message.content)

    execution_result = final_response.choices[0].message.content

    if "```python" in execution_result and "```" in execution_result:
        start = execution_result.find("```python") + len("```python")
        end = execution_result.find("```", start)
        execution_result_code = execution_result[start:end].strip()



    return execution_result_code


@agent.on_event("startup")
async def introduce(ctx: Context):
    ctx.logger.info(ctx.agent.address)


@toolhouseai_proto.on_message(ToolHouseAIRequest, replies={UAgentResponse, ErrorMessage})
async def handle_request(ctx: Context, sender: str, msg: ToolHouseAIRequest):
    ctx.logger.info(f"Received query : {msg.query}")
    try:
        response = await get_answer(msg.query)
        ctx.logger.info(response)

    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            sender,
            ErrorMessage(
                error=str(err)
            ),
        )
        return
    await ctx.send(
        sender, UAgentResponse(message=response, type=UAgentResponseType.FINAL)
    )


agent.include(toolhouseai_proto, publish_manifest=True)

if __name__ == "__main__":
    agent.run()




