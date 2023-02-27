



async def search_children(need_children_list: list, all_data_list: list):
    
    for i in need_children_list:
        children = []
        for g in all_data_list:
            if g['self_master_id'] == i["id"]:
                children.append(g)
        i['children'] = children
    
    if children != []:
        return search_children(need_children_list=children, all_data_list=all_data_list)
    
    if children == []:
        return  