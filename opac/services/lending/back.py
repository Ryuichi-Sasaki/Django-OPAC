from opac.mailers import HoldingCreatedMailer, MailerError
from opac.queries import LendingBackQuery, QueryError
from opac.queries.errors import AlreadyExistsError
from opac.services.errors import \
    FirstReservationHoldingAlreadyExistsError, ServiceError


class LendingBackService:
    """貸出の返却処理と取置ユーザーへのメール送信を行うサービス。

    Parameters
    ----------
    lending
        対象の貸出
    """
    def __init__(self, lending):
        self._lending = lending

    def exec(self):
        """サービスを実行する。

        Raises
        ------
        ServiceError
            返却処理やメール送信でエラーが発生した場合。
        """
        try:
            created_holding = LendingBackQuery(self._lending).exec()
            if created_holding:
                HoldingCreatedMailer(created_holding).exec()
        except AlreadyExistsError as e:
            raise FirstReservationHoldingAlreadyExistsError(e)
        except (MailerError, QueryError) as e:
            raise ServiceError(e)
