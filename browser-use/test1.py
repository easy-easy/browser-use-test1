from typing import List
import asyncio
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from browser_use import Agent
from browser_use.controller.service import Controller

controller = Controller()

class StoreResult(BaseModel):
    price: str
    postage: str
    coupon: str
    points: str
    store: str
    ecName: str
    time: str


class StoreResults(BaseModel):
	storeResults: List[StoreResult]


@controller.action('Save Price', param_model=StoreResults)
def save_price(params: StoreResults):
	with open('price.txt', 'a') as f:
		for storeResult in params.storeResults:
			f.write(f'price:{storeResult.price},postage:{storeResult.postage},coupon:{storeResult.coupon},points:{storeResult.points},store:{storeResult.store},ecName:{storeResult.ecName},time:{storeResult.time}\n')

async def main():
    agent = Agent(
        task="""
あなたは価格監視のエージェントです。
与えられたURLから商品の監視をしてください
対象商品は: hegehoge商品
- ecName: Sundrug-online url: https://sundrug-online.com/hegehoge
- ecName: Rakuten url: https://item.rakuten.co.jp/sundrug/hegehoge
- ecName: yodobashi url: https://www.yodobashi.com/product/hegehoge

下記の形式でデータを教えてほしい
- 価格
- 送料(なければ0円)
- クーポン(なければ0円)
- ポイント(なければ0円)
- ショップ名
- ECサイトの名称
""",
        llm=ChatOpenAI(
			model="gpt-4o",
        ),
		controller=controller
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
