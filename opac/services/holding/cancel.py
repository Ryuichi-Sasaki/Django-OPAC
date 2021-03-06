from opac.mailers import HoldingCreatedMailer, MailerError
from opac.queries import QueryError, HoldingCancelQuery
from opac.queries.errors import AlreadyExistsError
from opac.services import \
    FirstReservationHoldingAlreadyExistsError, ServiceError


class HoldingCancelService:
    """取置の取り消しを行うサービス。

    Parameters
    ----------
    holding
        対象の取置
    """
    def __init__(self, holding):
        self._holding = holding

    def exec(self):
        """サービスを実行する。

        Raises
        ------
        ServiceError
            取り消し処理でエラーが発生した場合。
        """
        try:
            created_holding = HoldingCancelQuery(self._holding).exec()
            if created_holding:
                HoldingCreatedMailer(created_holding).exec()
        except AlreadyExistsError as e:
            raise FirstReservationHoldingAlreadyExistsError(e)
        except (MailerError, QueryError) as e:
            raise ServiceError(e)
