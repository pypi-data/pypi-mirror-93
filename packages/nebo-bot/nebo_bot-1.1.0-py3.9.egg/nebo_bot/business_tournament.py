import logging
from nebo_bot.result_codes import *
from nebo_bot.utils import timeout


class BusinessTournament:

    def __init__(self, bot_core):
        self.bot = bot_core
        self.max_timeout = 240

    @timeout(120)
    def get_award(self):
        self.bot.get('/')
        if self.bot.business_tournament_finish:
            self.bot.get('/inspectors')
            if not self.bot.press('Получить награду!'):
                self.bot.handler_send_message.get_award_business_tournament(self, self.bot.user_id)
                return GET_AWARD_BUSINESS_TOURNAMENT
            logging.debug('Получена награда с бизнес турнира')

    def run(self):
        raise Exception("WTF")




