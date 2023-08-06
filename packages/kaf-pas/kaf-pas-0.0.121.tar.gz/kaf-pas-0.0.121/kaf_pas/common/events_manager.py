import logging

from events.events_manager import EventsManager

logger = logging.getLogger(__name__)


class EventStack:
    eventsManager = EventsManager()

    def __init__(self):
        from kaf_pas.planing.models.production_ext import OperationEvent

        self.EVENTS_TEST = self.eventsManager.get_event('events.test', 'События.Test', compulsory_reading=True)

        self.EVENTS_PRODUCTION_READY_2_LAUNCH = self.eventsManager.get_event('events.production.ready2Launch', 'События.Производство.Выполнен расчет готовности к запуску', compulsory_reading=False)
        self.EVENTS_PRODUCTION_READY_2_LAUNCH.__class__ = OperationEvent

        self.EVENTS_PRODUCTION_MAKE_ROUTING = self.eventsManager.get_event('events.planing.route.make', 'События.Планирование.Маршрутизация.Формирование', compulsory_reading=False)
        self.EVENTS_PRODUCTION_MAKE_ROUTING.__class__ = OperationEvent

        self.EVENTS_PRODUCTION_DELETE_ROUTING = self.eventsManager.get_event('events.planing.route.delete', 'События.Планирование.Маршрутизация.Удаление', compulsory_reading=False)
        self.EVENTS_PRODUCTION_DELETE_ROUTING.__class__ = OperationEvent

        self.EVENTS_PRODUCTION_MAKE_LAUNCH = self.eventsManager.get_event('events.production.launch.make', 'События.Производство.Запуск.Формирование', compulsory_reading=False)
        self.EVENTS_PRODUCTION_MAKE_LAUNCH.__class__ = OperationEvent

        self.EVENTS_PRODUCTION_DELETE_LAUNCH = self.eventsManager.get_event('events.production.launch.delete', 'События.Производство.Запуск.Удаление', compulsory_reading=False)
        self.EVENTS_PRODUCTION_DELETE_LAUNCH.__class__ = OperationEvent

        self.EVENTS_PRODUCTION_ORDER_CREATE = self.eventsManager.get_event('events.production.order.create', 'События.Производство.Задание на производство.Формирование', compulsory_reading=True)
        self.EVENTS_PRODUCTION_ORDER_CREATE.__class__ = OperationEvent

        self.EVENTS_PRODUCTION_ORDER_RE_CREATE = self.eventsManager.get_event('events.production.order.re-create', 'События.Производство.Задание на производство.Переформирование', compulsory_reading=True)
        self.EVENTS_PRODUCTION_ORDER_RE_CREATE.__class__ = OperationEvent

        self.EVENTS_PRODUCTION_ORDER_DELETE = self.eventsManager.get_event('events.production.order.delete', 'События.Производство.Задание на производство.Удаление', compulsory_reading=True)
        self.EVENTS_PRODUCTION_ORDER_DELETE.__class__ = OperationEvent

        # self.EVENTS_PRODUCTION_ORDER_GROUPING = self.eventsManager.get_event('events.production.order.grouping', 'События.Производство.Задание на производство.Группирование', compulsory_reading=False)
        # self.EVENTS_PRODUCTION_ORDER_GROUPING.__class__ = OperationEvent

        self.EVENTS_DOWNLOAD_CONFIRM = self.eventsManager.get_event('events.download.confirm', 'События.Закачка.Подтверждение', compulsory_reading=False)
        self.EVENTS_DOWNLOAD_CONFIRM.__class__ = OperationEvent

        self.EVENTS_DOWNLOAD_DONE = self.eventsManager.get_event('events.download.done', 'События.Закачка.Выполнеие', compulsory_reading=False)
        self.EVENTS_DOWNLOAD_DONE.__class__ = OperationEvent

        self.EVENTS_DOWNLOAD_DELETE = self.eventsManager.get_event('events.download.delete', 'События.Закачка.Удаление', compulsory_reading=False)
        self.EVENTS_DOWNLOAD_DELETE.__class__ = OperationEvent
