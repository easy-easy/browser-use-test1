from typing import List
import asyncio
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use.controller.service import Controller
from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    # model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
)
controller = Controller()

# class StoreResult(BaseModel):
#     price: str
#     postage: str
#     coupon: str
#     points: str
#     store: str
#     ecName: str
#     time: str


# class StoreResults(BaseModel):
# 	storeResults: List[StoreResult]


# @controller.action('Save Price', param_model=StoreResults)
# def save_price(params: StoreResults):
# 	with open('price.txt', 'a') as f:
# 		for storeResult in params.storeResults:
# 			f.write(f'price:{storeResult.price},postage:{storeResult.postage},coupon:{storeResult.coupon},points:{storeResult.points},store:{storeResult.store},ecName:{storeResult.ecName},time:{storeResult.time}\n')

async def main():
    agent = Agent(
        task="""
            あなたは価格監視のエージェントです。
            以下のサイトから、人気トップ3のSDカードの価格を調べてください。
            - ecName: kakaku url: https://kakaku.com/camera/sd-card/
        """,
        llm=llm,
		# controller=controller
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
