from datetime import timedelta

from django.db import Error, IntegrityError, transaction
from django.utils import timezone

from opac.models.transactions import Lending
from opac.queries.errors import AlreadyExistsError, QueryError
from opac.queries.reservation import FirstReservationToHoldingQuery


class HoldingLendQuery:
    """取置の貸出処理を行うクエリ。アトミックです。

    Parameters
    ----------
    holding
        対象の取置
    """
    def __init__(self, holding):
        self._holding = holding

    @transaction.atomic
    def exec(self):
        """クエリを実行する。

        Detail
        ------
        1. 取置に対応する貸出を作成する
        2. 取置を削除する

        Raises
        ------
        AlreadyExistsError
            既に貸出が存在していた場合
        QueryError
            その他のエラーが発生した場合
        """
        try:
            Lending.objects.create(
                stock=self._holding.stock,
                user=self._holding.user,
                due_date=timezone.localdate() + timedelta(days=14)
            )
            self._holding.delete()
        except IntegrityError as e:
            raise AlreadyExistsError(self._holding, e)
        except Error as e:
            raise QueryError(self._holding, e)


class HoldingCancelQuery:
    """取置の取り消し処理を行うクエリ。アトミックです。

    Parameters
    ----------
    holding
        対象の取置
    """
    def __init__(self, holding):
        self._holding = holding

    @transaction.atomic
    def exec(self):
        """クエリを実行する。

        Detail
        ------
        蔵書に予約が存在する場合
            1. 取置を削除する
            2. 最初の予約に対応する取置を作成する
            3. 最初の予約を削除する

        蔵書に予約が存在しない場合
            1. 取置を削除する

        Returns
        -------
        取置を作成した場合
            作成した取置

        取置を作成しなかった場合
            None

        Raises
        ------
        QueryError
            クエリでエラーが発生した場合
        """
        stock = self._holding.stock
        try:
            self._holding.delete()
            created_holding = FirstReservationToHoldingQuery(stock).exec()
        except Error as e:
            raise QueryError(self.__class__, self._holding, e)
        else:
            return created_holding
