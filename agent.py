from langchain.agents import Tool, initialize_agent
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import os

def set_volumn(args):
    print("set_volumn")
    return f"音量 : {args}"

def set_brightness_status(args):
    print("set_brightness_status")
    return f"亮度 : {args}"

def set_net_status(args):
    print("set_net_status")
    return f"网络 : {'关闭' if args.lower() == 'false' else '开启'}"

tools = [
    Tool(name="set_volumn", func=set_volumn, description="设置声音的高低,0-100"),
    Tool(name="set_net_status", func=set_net_status, description="设置网络状态,true 或者 false"),
    Tool(name="set_brightness_status", func=set_brightness_status, description="设置亮度的高低,0-100")
]

llm = ChatOpenAI(
    model = "ep-20250207110310-m52hl", 
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = "https://ark.cn-beijing.volces.com/api/v3",
    streaming = True,
)

memory = ConversationBufferMemory(memory_key="chat_history")

# 初始化代理
agent = initialize_agent(tools, llm, agent="conversational-react-description", memory=memory)

# 运行代理并执行任务
async def run_agent(input_str, funccallback):
    async for event in agent.astream_events({"input": input_str}, version="v1"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            funccallback.message_response(event['data']['chunk'].content)