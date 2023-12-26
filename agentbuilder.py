import autogen
from autogen.agentchat.contrib.agent_builder import AgentBuilder
from database import Database
import pandas as pd


db = Database()
# 1. Configuration
config_path = 'OAI_CONFIG_LIST'
default_llm_config = {
    'temperature': 0
}

model = 'openchat_openchat-3.5-1210'
# 2. Initialsiing Builder
builder = AgentBuilder(config_path=config_path, builder_model=model, agent_model=model)
city = "Gwangju"
topic = "광주 여행"

# 3. specify the building task
building_task = f"""Write blog for the Korea {city} travel. 
                First find best spots for traveler and explain the spots.
                Second, find top 5 hotels by reviewers from hotel.com, expedia, airbnb considered the best spots what you provided. 
                And give me the comparison table of hotels.
                Third, find good foods in {city}.
                Every item requires image for the blog. 
                Therefore, the images are provided with description. 
                Pick one of them and put the id like {id} at the proper position in the blog. 
                """
markdown = pd.read_sql(f"SELECT id, description FROM blog_images WHERE topic = '{topic}'", db.conn).to_markdown()

# 4. build group chat agents
agent_list, agent_configs = builder.build(building_task, default_llm_config, coding=True)

# 5. execute the task​
def start_task(execution_task: str, agent_list: list, llm_config: dict):
    config_list = autogen.config_list_from_json(config_path, filter_dict={"model": ["gpt-4-1106-preview"]})

    group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)
    manager = autogen.GroupChatManager(
        groupchat=group_chat, llm_config={"config_list": config_list, **llm_config}
    )
    agent_list[0].initiate_chat(manager, message=execution_task)


start_task(
    execution_task=f"""Write blog for the Korea {city} travel. 
                First find best spots for traveler and explain the spots.
                Second, find top 5 hotels by reviewers from hotel.com, expedia, airbnb considered the best spots what you provided. 
                And give me the comparison table of hotels. The table should have pros, cons, average reviews, cost range and so on. 
                Third, find good foods in {city}. Write in {city}.md. This is the images you can chooose ```{markdown}```""",
    agent_list=agent_list,
    llm_config=default_llm_config
)

# 6. clear all agents and prepare for the next task​
builder.clear_all_agents(recycle_endpoint=True)

saved_path = builder.save()
