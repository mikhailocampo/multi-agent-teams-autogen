
import os
import autogen

config_list = [{"model": "gpt-3.5-turbo-16k-0613", "api_key": os.getenv("OPENAI_API_KEY")}]

llm_config = {
    "cache_seed": 42,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get('content', '').strip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "output", "use_docker": True},
    llm_config=llm_config,
    system_message="""
    Reply with TERMINATE when the task has been completed. If the task is not completed, provide a detailed status update or ask for more information. If the task is completed, but the user needs to take further action, provide clear instructions. If the task is completed and no further action is required, reply with TERMINATE.
    """
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""
    Engineer. You write python or shell to complete tasks. You do not execute code. The code you write is given to the user to be executed in a docker environment without any pre-installed libraries. Start with reasoning to solve the task and then provide the code. 
    
    Do not give the user code to modify. Infer that user always need to see the code you write in order to execute it. For example, if installing a library was successful rewrite the entire script for the user to execute.
    
    If a task is completed, do not ask the user if they need further assistance. Ask the user for the next task if any or reply with TERMINATE.
    """,
)

user_proxy.initiate_chat(
    engineer,
    message="""
    Compare the stock trends of MAANG companies: META, AMZN, AAPL, NFLX, and GOOGL. Compare the stock prices for the last 3 months and provide a visual comparison. Save the visual comparison as a PNG file. Then, create a table of the stock prices for the last 3 months. Finally, provide a summary of the stock trends for both companies.
    """,
)