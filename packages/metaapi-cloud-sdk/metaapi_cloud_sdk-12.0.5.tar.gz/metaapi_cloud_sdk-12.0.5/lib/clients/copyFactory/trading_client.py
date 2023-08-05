from ..metaApi_client import MetaApiClient
from .copyFactory_models import CopyFactoryStrategyStopout, CopyFactoryUserLogRecord
from typing import List
from httpx import Response
from datetime import datetime
from ...metaApi.models import date, format_date


class TradingClient(MetaApiClient):
    """metaapi.cloud CopyFactory history API (trade copying history API) client (see
    https://trading-api-v1.project-stock.agiliumlabs.cloud/swagger/#/)"""

    def __init__(self, http_client, token: str, domain: str = 'agiliumtrade.agiliumtrade.ai'):
        """Inits CopyFactory history API client instance.

        Args:
            http_client: HTTP client.
            token: Authorization token.
            domain: Domain to connect to, default is agiliumtrade.agiliumtrade.ai.
        """
        super().__init__(http_client, token, domain)
        self._host = f'https://trading-api-v1.{domain}'

    async def resynchronize(self, account_id: str, strategy_ids: List[str] = None) -> Response:
        """Resynchronizes the account. See
        https://trading-api-v1.agiliumtrade.agiliumtrade.ai/swagger/#!/default
        /post_users_current_accounts_accountId_resynchronize

        Args:
            account_id: Account id.
            strategy_ids: Optional array of strategy ids to recynchronize. Default is to synchronize all strategies.

        Returns:
            A coroutine which resolves when resynchronization is scheduled.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('resynchronize')
        qs = {}
        if strategy_ids:
            qs['strategyId'] = strategy_ids
        opts = {
          'url': f'{self._host}/users/current/accounts/{account_id}/resynchronize',
          'method': 'POST',
          'headers': {
            'auth-token': self._token
          },
          'params': qs,
        }
        return await self._httpClient.request(opts)

    async def get_stopouts(self, account_id: str) -> 'Response[List[CopyFactoryStrategyStopout]]':
        """Returns subscriber account stopouts. See
        https://trading-api-v1.agiliumtrade.agiliumtrade.ai/swagger/#!/default
        /get_users_current_accounts_accountId_stopouts

        Args:
            account_id: Account id.

        Returns:
            A coroutine which resolves with stopouts found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_stopouts')
        opts = {
            'url': f'{self._host}/users/current/accounts/{account_id}/stopouts',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def reset_stopouts(self, account_id: str, strategy_id: str, reason: str) -> Response:
        """Resets strategy stopouts. See
        https://trading-api-v1.agiliumtrade.agiliumtrade.ai/swagger/#!/default/post_users_current_accounts_accountId_
        strategies_subscribed_strategyId_stopouts_reason_reset


        Args:
            account_id: Account id.
            strategy_id: Strategy id.
            reason: Stopout reason to reset. One of yearly-balance, monthly-balance, daily-balance, yearly-equity,
            monthly-equity, daily-equity, max-drawdown.

        Returns:
            A coroutine which resolves when the stopouts are reset.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('reset_stopouts')
        opts = {
            'url': f'{self._host}/users/current/accounts/{account_id}/strategies-subscribed/{strategy_id}' +
                   f'/stopouts/{reason}/reset',
            'method': 'POST',
            'headers': {
                'auth-token': self._token
            }
        }
        return await self._httpClient.request(opts)

    async def get_user_log(self, account_id: str, start_time: datetime = None, end_time: datetime = None,
                           offset: int = 0, limit: int = 1000) -> 'Response[List[CopyFactoryUserLogRecord]]':
        """Returns copy trading user log for an account and time range. See
        https://trading-api-v1.project-stock.v2.agiliumlabs.cloud/swagger/#!/default
        /get_users_current_accounts_accountId_user_log


        Args:
            account_id: Account id.
            start_time: Time to start loading data from.
            end_time: Time to stop loading data at.
            offset: Pagination offset. Default is 0.
            limit: Pagination limit. Default is 1000.

        Returns:
            A coroutine which resolves with log records found.
        """
        if self._is_not_jwt_token():
            return self._handle_no_access_exception('get_user_log')
        qs = {
            'offset': offset,
            'limit': limit
        }
        if start_time:
            qs['startTime'] = format_date(start_time)
        if end_time:
            qs['endTime'] = format_date(end_time)
        opts = {
            'url': f'{self._host}/users/current/accounts/{account_id}/user-log',
            'method': 'GET',
            'headers': {
                'auth-token': self._token
            },
            'params': qs
        }
        result = await self._httpClient.request(opts)
        if result and isinstance(result, List):
            for r in result:
                r['time'] = date(r['time'])
        return result
