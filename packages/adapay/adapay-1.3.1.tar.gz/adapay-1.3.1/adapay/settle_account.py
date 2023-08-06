"""

结算账户对象
"""

from adapay.request_tools import request_get, request_post, settle_account_create, settle_account_query,\
    settle_account_delete, settle_account_balance_query, settle_account_detail_query, settle_account_modify,\
    settle_account_commissions_list, settle_account_commissions_create


class SettleAccount:

    @classmethod
    def create_settle(cls, **kwargs):
        """
        创建结算账户
        """
        return request_post(settle_account_create, kwargs)

    @classmethod
    def query_settle(cls, **kwargs):
        """
        查询结算账户
        """
        url = settle_account_query.format(settle_account_id=kwargs.get('settle_account_id'))
        return request_get(url, kwargs)

    @classmethod
    def modify_settle(cls, **kwargs):
        """
        修改结算配置
        """
        return request_post(settle_account_modify, kwargs)

    @classmethod
    def delete_settle(cls, **kwargs):
        """
        删除结算账户
        """
        return request_post(settle_account_delete, kwargs)

    @classmethod
    def query_settle_details(cls, **kwargs):
        """
        查询结算账户明细
        """
        return request_get(settle_account_detail_query, kwargs)

    @classmethod
    def query_balance(cls, **kwargs):
        """
        查询账户余额
        """
        return request_get(settle_account_balance_query, kwargs)

    @classmethod
    def create_commissions_settle(cls, **kwargs):
        """
        创建
        """
        return request_post(settle_account_commissions_create, kwargs)

    @classmethod
    def list_commissions_settle(cls, **kwargs):
        """
        查询列表
        """
        return request_get(settle_account_commissions_create, kwargs)
