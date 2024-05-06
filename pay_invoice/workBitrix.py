from fast_bitrix24 import Bitrix
import os
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import dataclass
from datetime import datetime
# import urllib3
import urllib.request
import time
import asyncio
# from workFlask import send_log
import requests
load_dotenv()
webhook = os.getenv('WEBHOOK')
PORT=os.getenv('PORT')
HOST=os.getenv('HOST')

bit = Bitrix(webhook)

def send_log(message, level='INFO'):
    requests.post(f'http://{HOST}:{PORT}/logs', json={'log_entry': message, 'log_level': level})
@dataclass
class Lead:
    userName:str
    title:str='TITLE'
    userID:str='UF_CRM_1709220784686'
    photos:str='UF_CRM_1709223951925'
    urlUser:str='UF_CRM_1709224894080'
    messageURL:str='UF_CRM_1709293438392'

    description:str='COMMENTS'

@dataclass
class Deal:
    id:str='ID'
    title:str='TITLE'
    categoryID:str='CATEGORY_ID'
    statusID:str='STATUS_ID'
    comments:str='COMMENTS'
    responsibleID:str='ASSIGNED_BY_ID'

PAY_ENTY_ID=155
INVOICE_ID=31
# async def te
def find_deal(dealID:str):
    deal = bit.call('crm.deal.get', params={'id': dealID})
    return deal

def find_lead(leadID:str):
    lead = bit.call('crm.lead.get', params={'id': leadID})
    return lead

def find_invoice(number, date):
    invoice = bit.call('crm.invoice.list', items={'filter': 
                                             {'ACCOUNT_NUMBER':number, 'BEGINDATE':date}}, raw=True)['result']
    return invoice


def get_deals():
    prepareDeal=[]
    deals = bit.call('crm.deal.list', items={'filter': 
                                             {'STAGE_SEMANTIC_ID':'S'}}, raw=True)['result']
    for deal in deals:
        
        product=bit.call('crm.deal.productrows.get', items={'id': int(deal['ID'])}, raw=True)['result']
        
        a={'deal':deal,
            'product':product}
        
        prepareDeal.append(a)
    pprint(prepareDeal)
    return prepareDeal

def get_products(poductID):
    products=bit.call('crm.product.get', items={'ID':poductID}, raw=True)['result']

    pprint(products)

    return products

def get_users():
    prepareUser = []
    # users = bit.call('user.get', items={'filter' :{'ACTIVE':False}})
    users = bit.call('user.get', raw=True)['result']
    # for user in users:
        # prepareUser.append(f'[{user["ID"]}] {user["NAME"]} {user["LAST_NAME"]}')
    # pprint(users)
    # print(prepareUser)
    return users

def get_departments():
    departments = bit.call('department.get', raw=True)['result']
    pprint(departments)
    return departments

def get_task_work_time(id)->list:
    # task=bit.call('tasks.task.get', items={'taskId': id}, raw=True)['result']
    task=bit.call('task.elapseditem.getlist', items={'ID': id}, raw=True)['result']
    # pprint(task)
    return task

def get_item(entityID,itemID):
    item=bit.call('crm.item.get', items={'entityTypeId':entityID, 'id': itemID}, raw=True)['result']['item']
    return item

def find_invoice(entityID, number, date):
    """_summary_

    Args:
        entityID (_type_): _description_
        number (_type_):'0000-000014'
        date (_type_): '2024-05-07T03:00:00'

    Returns:
        _type_: _description_
    """

    item = bit.call('crm.item.list', items={'entityTypeId':entityID, 'filter': 
                            { 'accountNumber':number, 'begindate':date}}, raw=True)['result']['items']
    
    return item

# def get_invoice(invoiceID):
#     invoice=bit.call('crm.invoice.get', items={'id': invoiceID}, raw=True)['result']
#     return invoice

def create_item(duretion,taskID, comment, dateClose):
    bit.call('crm.item.add', items={
                            'entityTypeId':179, #биллинг
                            'fields': {'title': comment,
                                'ufCrm9_1713363122': duretion,
                                'ufCrm9_1713363093': dateClose.split('+')[0],}})

def add_new_post_timeline(itemID, entityID, entityType):
    bit.call('crm.timeline.comment.add', items={
                            'fields': {'ENTITY_ID': entityID,
                                'ENTITY_TYPE': entityType,
                                'COMMENT': """Создан новый пост
                                Test comment [URL=/crm/deal/details/26/]test123[/URL]""",}}) #для ссылки в нутри битрикса

def create_product(fields:dict):
    pprint(fields)
    bit.call('crm.product.add', items={'fields':fields},)




def update_product(productID, fields:dict):
    bit.call('crm.product.update', items={'ID':productID, 'fields':fields})

def update_item(entityID, itemID, parentID):
    bit.call('crm.item.update', items={'entityTypeId':entityID, 'id':itemID, 'fields':{"parentId31":parentID}})


# if __name__ == '__main__':
def main(PAY_ENTY_ID:str,PAY_ID:str):

    pay=get_item(PAY_ENTY_ID, PAY_ID)
    pprint(pay) 
    send_log(f"pay: {pay['title']}")
  
    if pay['parentId31'] is None: 0#поле счет не заполнено, тогда заполняем
    
    numberInvoice=pay['ufCrm29Documentnumber']
    try:
        dateInvoice=pay['ufCrm29Documentdate'].split('+')[0] #'2024-05-07T03:00:00+03:00'
    except:
        send_log('ufCrm29Documentdate/Основание платежа: Счет от \nне заполнено', 'ERROR')
        return 'dateInvoice not found'

    invoices=find_invoice(INVOICE_ID, numberInvoice, dateInvoice)
    send_log(f'find_invoice: {len(invoices)}')
    invoice=invoices[0]
    pprint(invoice)
    send_log(f"invoice: {invoice['title']}")
    invoiceID=invoice['id']

    update_item(PAY_ENTY_ID, PAY_ID, invoiceID)    

    send_log(f"update_item: {PAY_ID} {invoiceID}")
    # update_item(PAY_ID, 85, 55)

    
    #СЧЕТА

    # pprint(invoice)

    # pprint(invoice)
    
    


# main()


