from smtplib import SMTPException

from django.core.mail import send_mail

from opac.mailers import MailerError


class HoldingCreatedMailer:
    """取置連絡をするメーラー。

    Parameters
    ----------
    holding
        対象の取置
    """
    def __init__(self, holding):
        self._name = holding.user.username
        self._book = holding.stock.book
        self._expiration_date = holding.expiration_date
        self._email = holding.user.email

    def exec(self):
        """メールを送信する。

        Raises
        ------
        MailerError
            メール送信でエラーが発生した場合
        """
        try:
            send_mail(
                '蔵書取り置きのご連絡 ○○○図書館',
                f'''{self._name} さんが予約されていた {self._book} を取り置きしました。
                取置期限は{self._expiration_date}です。
                ''',
                'from@django-opac.com',
                [self._email],
                fail_silently=False,
            )
        except SMTPException as e:
            raise MailerError(self.__class__, e)
