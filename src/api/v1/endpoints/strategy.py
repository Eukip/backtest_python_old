from datetime import datetime, timedelta
from enum import IntEnum
import numbers
from typing import List, Literal, Union
from xml.dom import ValidationErr
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from api.v1.endpoints.orders import check_exists_time_interval
from models import Strategy
from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from models.timeinterval import TimeInterval
from schemas.strategy import CreateRequestStrategiesPydantic, CreateResponseStrategiesPydantic, StrategiesPydantic, StrategyPydantic, \
    RequestStrategy
from fastapi_pagination import Page,  Params
from fastapi_pagination.ext.tortoise import paginate
from services.del_png_strategy import delete_png_by_strategy
from services.parse_xmind import parse_xmind
from services.python_tree_strategy import search_children
from tortoise.transactions import atomic
import os
from typing import Optional
from tortoise.functions import Count, Sum
from tortoise import Tortoise
from tortoise.expressions import F as F_object



class Status(BaseModel):
    status: str


router = APIRouter()


@router.get('/sql-tree/')
async def get_all_res_strategy(
    time_interval: Optional[int] = None,
    dealcount: Optional[bool] = None,
    dealinminus: Optional[bool] = None,
    dealinplus: Optional[bool] = None,
    dealinzero: Optional[bool] = None,
    notclosed: Optional[bool] = None,
    profittodeal: Optional[bool] = None,
    profittodepoz: Optional[bool] = None,
    absoluteprofit: Optional[bool] = None,
    base_currency: Optional[str] = None,
    # page_num: int = 1,
    page_size: int = 20,
    offset_number: Union[int, None] = Query(default=0,
        description="Offest с какой строки(id) выдаются элементы, для следующих элементов нужно указывать последнюю строку(id) показанную ранее")
    ):



    # start = (page_num - 1) * page_size
    # end = start + page_size
    conn = Tortoise.get_connection('default')
    order_filter_string = ''
    ordering = ''
    query = f'''
    WITH RECURSIVE tree_view AS (
            SELECT      id,
                        name,
                        count_orders,
                        v_plus,
                        v_minus,
                        v_zero,
                        not_closed,
                        profit_cer_period,
                        profit_to_deposit,
                        absolute_profit,
                        self_master_id,
                        {ordering}
                        1 AS level,
                        CAST(name AS varchar(500)) AS strategy_path
            FROM strategy
            {order_filter_string} 
            WHERE archived=false AND self_master_id IS NULL


        UNION ALL


            SELECT      parent.id,
                        parent.name,
                        parent.count_orders,
                        parent.v_plus,
                        parent.v_minus,
                        parent.v_zero,
                        parent.not_closed,
                        parent.profit_cer_period,
                        parent.profit_to_deposit,
                        parent.absolute_profit,
                        parent.self_master_id,
                        {ordering}
                        level + 1 AS level,
                        CAST (strategy_path || '/' || CAST (parent.name AS VARCHAR (500)) AS VARCHAR(500)) AS strategy_path
            FROM strategy AS parent
            {order_filter_string}
            JOIN tree_view AS tv
            ON parent.self_master_id = tv.id
        )
        SELECT *
        FROM tree_view
        ORDER BY id
        LIMIT {page_size} OFFSET {offset_number};
    '''

    if time_interval is not None:
        await check_exists_time_interval(time_interval)
        values = await TimeInterval.filter(id=time_interval).first().values_list()
        order_filter_string = f"""
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        AND "order"."open_time">={values[1]} 
        AND "order"."close_time"<={values[2]}
        """
    
    if base_currency is not None:
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        LEFT OUTER JOIN "pair" "order__pair" 
        ON "order__pair"."id"="order"."pair_id" 
        AND UPPER(CAST("order__pair"."trading_pair" AS VARCHAR)) 
        LIKE UPPER(f'%{base_currency}%') ESCAPE '\'
        """
    
    if dealcount is not None:
        ordering = 'COUNT("deal"."id") "strategy_deal_count",'
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        GROUP BY "strategy"."id" 
        ORDER BY COUNT("deal"."id") ASC
        """
        
        if dealcount == False:
            order_filter_string = """
            LEFT OUTER JOIN "deal" 
            ON "strategy"."id"="deal"."strategy_id" 
            GROUP BY "strategy"."id" 
            ORDER BY COUNT("deal"."id") DESC
            """
    
    if dealinminus is not None:
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        ORDER BY "order"."absolute_profit" ASC
        """
        if dealinminus == False:
            order_filter_string = """
            LEFT OUTER JOIN "deal" 
            ON "strategy"."id"="deal"."strategy_id" 
            LEFT OUTER JOIN "order" 
            ON "deal"."id"="order"."deal_id" 
            ORDER BY "order"."absolute_profit" DESC
            """

    if dealinplus is not None:
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        ORDER BY "order"."absolute_profit" DESC
        """
        if dealinplus == False:
            order_filter_string = """
            LEFT OUTER JOIN "deal" 
            ON "strategy"."id"="deal"."strategy_id" 
            LEFT OUTER JOIN "order" 
            ON "deal"."id"="order"."deal_id" 
            ORDER BY "order"."absolute_profit" ASC
            """
    
    if dealinzero is not None:
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        WHERE UPPER(CAST("order"."absolute_profit" AS VARCHAR))=UPPER('0') 
        ORDER BY "strategy"."id" ASC
        """
        if dealinzero == False:
            order_filter_string = """
            LEFT OUTER JOIN "deal" 
            ON "strategy"."id"="deal"."strategy_id" 
            LEFT OUTER JOIN "order" 
            ON "deal"."id"="order"."deal_id" 
            WHERE UPPER(CAST("order"."absolute_profit" AS VARCHAR))=UPPER('0') 
            ORDER BY "strategy"."id" DESC
            """
    
    if notclosed is not None:
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        WHERE "order"."close_time" IS NULL 
        ORDER BY "strategy"."id" ASC
        """
        if notclosed == False:
            order_filter_string = """
            LEFT OUTER JOIN "deal" 
            ON "strategy"."id"="deal"."strategy_id" 
            LEFT OUTER JOIN "order" 
            ON "deal"."id"="order"."deal_id" 
            WHERE "order"."close_time" IS NULL 
            ORDER BY "strategy"."id" DESC
            """
    
    if profittodeal is not None:
        ordering = """
        SUM("order"."profit_cer_period") "sum_profit_orders",
        """
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        GROUP BY "strategy"."id" 
        ORDER BY SUM("order"."profit_cer_period") ASC
        """
        if profittodeal == False:
            order_filter_string = """
            LEFT OUTER JOIN "deal" 
            ON "strategy"."id"="deal"."strategy_id" 
            LEFT OUTER JOIN "order" 
            ON "deal"."id"="order"."deal_id" 
            GROUP BY "strategy"."id" 
            ORDER BY SUM("order"."profit_cer_period") DESC
            """

    if profittodepoz is not None:
        ordering = 'SUM("order"."profit_cer_period") "sum_profit_orders",'
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        GROUP BY "strategy"."id" 
        ORDER BY SUM("order"."profit_cer_period") ASC
        """
        if profittodepoz == False:
            order_filter_string = """
            LEFT OUTER JOIN "deal" 
            ON "strategy"."id"="deal"."strategy_id" 
            LEFT OUTER JOIN "order" 
            ON "deal"."id"="order"."deal_id" 
            GROUP BY "strategy"."id" 
            ORDER BY SUM("order"."profit_cer_period") DESC
            """
    
    if absoluteprofit is not None:
        ordering = 'SUM("order"."absolute_profit") "sum_profit_orders",'
        order_filter_string = """
        LEFT OUTER JOIN "deal" 
        ON "strategy"."id"="deal"."strategy_id" 
        LEFT OUTER JOIN "order" 
        ON "deal"."id"="order"."deal_id" 
        GROUP BY "strategy"."id" 
        ORDER BY SUM("order"."absolute_profit") ASC
        """

        if absoluteprofit == False:
            order_filter_string = """
            LEFT OUTER JOIN "deal" 
            ON "strategy"."id"="deal"."strategy_id" 
            LEFT OUTER JOIN "order" 
            ON "deal"."id"="order"."deal_id" 
            GROUP BY "strategy"."id" 
            ORDER BY SUM("order"."absolute_profit") DESC
            """

    re_strategy_orm = await conn.execute_query_dict(query)
    
    final_list = []

    for i in re_strategy_orm:
        print(i["id"])
        if i['self_master_id'] is None:
            print(i['id'])
            final_list.append(i)
    #         re_strategy_orm.remove(i)
    
    for i in final_list:
        await search_children(need_children_list=final_list, all_data_list=re_strategy_orm)


    response = {
        # "data": re_strategy_orm[start:end],
        "data": final_list,
        "total": len(final_list),
        "count": page_size,
        "offset":offset_number
    }
    # if end >= len(re_strategy_orm):
    #     response["pagination"]["next"] = None

    #     if page_num > 1:
    #         response["pagination"]["previous"] = f"/strategy_results?page_num={page_num-1}&page_size{page_size}"
    #     else:
    #         response["pagination"]["previous"] = None
    # else:
    #     if page_num > 1:
    #         response["pagination"]["previous"] = f"/strategy_results?page_num={page_num-1}&page_size{page_size}"
    #     else:
    #         response["pagination"]["previous"] = None
        
    #     response["pagination"]["next"] = f"/strategy_results?page_num={page_num+1}&page_size{page_size}"

    return response


@router.get('/sql-tree/{strategy_id}/')
async def retrieve_tree_strategy(strategy_id: int):
    print(strategy_id)
    print(type(strategy_id))
    conn = Tortoise.get_connection('default')
    func = '''
        CREATE OR REPLACE FUNCTION r(_Id INT) RETURNS JSONB AS
        $$
        BEGIN
        RETURN json_build_object(
            'id',
            'name',
            'count_orders',
            'v_plus',
            'v_minus',
            'v_zero',
            'not_closed',
            'profit_cer_period',
            'profit_to_deposit',
            'absolute_profit',
            _Id,
            'children',
            array(
            SELECT r(Id)
            FROM strategy 
            WHERE self_master_id = _id
            ));
        END;
        $$ LANGUAGE PLPGSQL;
    '''
    query = f"SELECT jsonb_pretty(r({strategy_id}));"
    await conn.execute_query_dict(func)
    re_strategy_orm = await conn.execute_query_dict(query)

    response = {
        "data": re_strategy_orm,
    }
    return response


@router.get('/strategy/',
            response_model=Page[StrategiesPydantic],
            )
async def get_all_res_strategy(
    time_interval: Optional[int] = None,
    dealcount: Optional[bool] = None,
    dealinminus: Optional[bool] = None,
    dealinplus: Optional[bool] = None,
    dealinzero: Optional[bool] = None,
    notclosed: Optional[bool] = None,
    profittodeal: Optional[bool] = None,
    profittodepoz: Optional[bool] = None,
    absoluteprofit: Optional[bool] = None,
    base_currency: Optional[str] = None,
    params: Params = Depends(),
    ):

    re_strategy_orm = Strategy.filter(archived=False).prefetch_related('deal_strategy')

    if time_interval is not None:
        await check_exists_time_interval(time_interval)
        values = await TimeInterval.filter(id=time_interval).first().values_list()
        re_strategy_orm = re_strategy_orm.filter(deal_strategy__order_deal__open_time__gte=values[1]).filter(deal_strategy__order_deal__close_time__lte=values[2])
        # AND "order"."open_time">=f'{values[1]}' 
        # AND "order"."close_time"<=f'{values[2]}'

    if base_currency is not None:
        re_strategy_orm = re_strategy_orm.filter(deal_strategy__order_deal__pair__trading_pair__icontains=base_currency)

    if dealcount is not None:
        re_strategy_orm = re_strategy_orm.annotate(strategy_deal_count=Count('deal_strategy')).order_by('strategy_deal_count')
        
        if dealcount == False:
            re_strategy_orm = re_strategy_orm.annotate(strategy_deal_count=Count('deal_strategy')).order_by('-strategy_deal_count')

    if dealinminus is not None:
        re_strategy_orm = re_strategy_orm.order_by('deal_strategy__order_deal__absolute_profit')

        if dealinminus == False:
            re_strategy_orm = re_strategy_orm.order_by('-deal_strategy__order_deal__absolute_profit')

    if dealinplus is not None:
        re_strategy_orm = re_strategy_orm.order_by('-deal_strategy__order_deal__absolute_profit')

        if dealinplus == False:
            re_strategy_orm = re_strategy_orm.order_by('deal_strategy__order_deal__absolute_profit')
    
    if dealinzero is not None:
        re_strategy_orm = re_strategy_orm.filter(deal_strategy__order_deal__absolute_profit__iexact=0).order_by('id')
        
        if dealinzero == False:
            re_strategy_orm = re_strategy_orm.filter(deal_strategy__order_deal__absolute_profit__iexact=0).order_by('-id')
    
    if notclosed is not None:
        re_strategy_orm = re_strategy_orm.filter(deal_strategy__order_deal__close_time__isnull=True).order_by('id')
        
        if notclosed == False:
            re_strategy_orm = re_strategy_orm.filter(deal_strategy__order_deal__close_time__isnull=True).order_by('-id')
            
    if profittodeal is not None:
        re_strategy_orm = re_strategy_orm.annotate(sum_profit_orders = Sum("deal_strategy__order_deal__profit_cer_period")).order_by('sum_profit_orders')

        if profittodeal == False:
            re_strategy_orm = re_strategy_orm.annotate(sum_profit_orders = Sum("deal_strategy__order_deal__profit_cer_period")).order_by('sum_profit_orders', '-id')

    if profittodepoz is not None:
        re_strategy_orm = re_strategy_orm.annotate(sum_profit_orders = Sum("deal_strategy__order_deal__profit_cer_period")).order_by('sum_profit_orders')

        if profittodepoz == False:
            re_strategy_orm = re_strategy_orm.annotate(sum_profit_orders = Sum("deal_strategy__order_deal__profit_to_deposit")).order_by('sum_profit_orders', '-id')


    if absoluteprofit is not None:
        re_strategy_orm = re_strategy_orm.annotate(sum_profit_orders = Sum("deal_strategy__order_deal__absolute_profit")).order_by('sum_profit_orders')

        if absoluteprofit == False:
            re_strategy_orm = re_strategy_orm.annotate(sum_profit_orders = Sum("deal_strategy__order_deal__absolute_profit")).order_by('sum_profit_orders', '-id')

    return await paginate(re_strategy_orm, params)


@router.post('',
             response_model=CreateResponseStrategiesPydantic
             )
async def create_strategy(
        request: Request,
        strategy: CreateRequestStrategiesPydantic = Depends(),
        xmind_deal_input: Optional[List[UploadFile]] = File(default=None),
        xmind_deal_output: Optional[List[UploadFile]] = File(default=None),
):
    strategy_dict = strategy.dict(exclude_unset=True)
    png_input_dict = {}
    png_output_dict = {}
    
    if not os.path.exists(os.getcwd() + "/xmind/"):
        os.mkdir('xmind')

    if xmind_deal_input is not None:
        number = 0
        for i in xmind_deal_input:
            number = number + 1
            print(type(i))
            xmind_input = f"/app/xmind/{i.filename.replace(' ', '-').replace('.', '_input_' + strategy_dict['name'] + '.')}"
            with open(xmind_input, 'wb+') as out_file:
                content = i.file.read()
                out_file.write(content)
            png_input_dict[f'{number}'] = f"{request.base_url}static/uploads/{await parse_xmind(xmind_input, strategy_dict['name'], 'input', number)}"
            os.remove(xmind_input)

    if xmind_deal_output is not None:
        number = 0
        for i in xmind_deal_output:
            number = number + 1
            print(type(i))
            xmind_output = f"/app/xmind/{i.filename.replace(' ', '-').replace('.', '_output_' + strategy_dict['name'] + '.')}"
            with open(xmind_output, 'wb+') as out_file:
                content = i.file.read()
                out_file.write(content)
            png_output_dict[f'{number}'] = f"{request.base_url}static/uploads/{await parse_xmind(xmind_output, strategy_dict['name'], 'output', number)}"
            os.remove(xmind_output)
    

    strategy_dict["png_from_xmind_input"] = str(png_input_dict)
    strategy_dict["png_from_xmind_output"] = str(png_output_dict)

    strategy_orm = await Strategy.create(**strategy_dict)
    if strategy_orm.id == strategy_orm.self_master_id:
        raise HTTPException(status_code=400, detail="Parent strategy can't be self strategy")
    
    return strategy_orm


@router.get('/strategy/{strategy_id}', response_model=StrategiesPydantic)
async def get_strategy(strategy_id: int):
    strategy_orm = await Strategy.filter(id=strategy_id).first()
    return strategy_orm


@atomic()
@router.post('/archive-strategy/')
async def archive_strategies(
        list_id: list = Query(1)
):
    await check_exists_by_id(list_id)
    for i in list_id:
        strategy_orm = await Strategy.get(id=int(i))
        strategy_orm.archived = True
        await strategy_orm.save()

    return Status(status=f"Strategy with that id's {list_id} was archived")


@atomic()
@router.delete('/archive-strategy/')
async def archive_strategies(
        list_id: list = Query(1)
):
    await check_exists_by_id(list_id)
    for i in list_id:
        strategy_orm = await Strategy.get(id=int(i))
        await delete_png_by_strategy(strategy_orm.name)
        await strategy_orm.delete()

    return Status(status=f"Strategy with that id's {list_id} was deleted")


@atomic()
@router.post('/archive-strategy-reestablish/')
async def archive_strategies(
        list_id: list = Query(1)
):
    await check_exists_by_id(list_id)
    for i in list_id:
        strategy_orm = await Strategy.get(id=int(i))
        strategy_orm.archived = False
        await strategy_orm.save()

    return Status(status=f"Strategy with that id's {list_id} was reestablished")


@router.get('/archived-strategy/', response_model=List[StrategiesPydantic])
async def get_all_archived_strategies():
    strategies_orm = await Strategy.all().filter(archived=True)
    return strategies_orm



# @router.delete('',
#                )
# async def delete_strategy(
#         name: str
# ):
#     await check_exists_by_name(name)

#     strategy_orm = await Strategy.filter(name=name).first()

#     await strategy_orm.delete()

#     return Status(status=f'Strategy with name {name} deleted')




@router.put('/update_strategy',
            response_model=StrategyPydantic
            )
async def update_strategy(
        strategy_id: int,
        strategy: RequestStrategy
):
    await check_exists_strategy(strategy_id)

    update_dict = strategy.dict(exclude_unset=True)

    await Strategy.filter(id=strategy_id).update(**update_dict)

    strategy_orm = await Strategy.get_or_none(id=strategy_id)
    return strategy_orm



# @router.get('/strategy_result/{res_strategy_id}',
#             response_model=ResultStrategyPydantic
#             )
# async def get_res_strategies(
#     res_strategy_id: int
# ):
#     await check_exists_res_strategy(res_strategy_id)

#     strategy_orm = await ResultStrategy.get(id=res_strategy_id).prefetch_related('strategy', 'strategy__master')

#     return strategy_orm







async def check_exists_by_id(id_list: list):
    for i in id_list:
        if not await Strategy.exists(id=int(i)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Strategy with name {id} not found ")


async def check_exists_strategy(strategy_id: int):
    if not await Strategy.exists(id=strategy_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Strategy with id {strategy_id} not found ")
