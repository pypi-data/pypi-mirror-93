# -*- coding=utf-8 -*-
import threading


class NacosTimer(object):

    def __init__(self, name, fn, interval=7, daemon=False, *args, **kwargs):
        """
        NacosTimer
        :param name:      timer name
        :param fn:        function which scheduler
        :param interval:  scheduler interval, default 7s
        :param args:      args in function
        :param kwargs:    kwargs in function
        """
        #
        self.name = name
        # Thread.Timer
        self.timer = None
        # function which callable
        self.fn = fn
        # timer interval default 7s
        self.interval = interval
        # whether ignore invoke exception
        self.ignore_ex = False
        self.on_result = None
        self.on_exception = None
        # function args
        self.args = args
        # function kwargs
        self.kwargs = kwargs
        self.daemon = daemon

    def alive(self):
        if self.timer is None:
            return False
        return self.timer.is_alive()

    def set_on_exception(self, fn):
        if callable(fn):
            self.on_exception = fn

    def set_on_result(self, fn):
        if callable(fn):
            self.on_result = fn

    def scheduler(self):
        try:
            res = self.fn(*self.args, **self.kwargs)
            if self.on_result:
                self.on_result(res)
        except Exception as ex:
            if self.on_exception:
                self.on_exception(ex)
            if not self.ignore_ex:
                raise ex
        self.timer = threading.Timer(self.interval, self.scheduler)
        self.timer.daemon = self.daemon
        self.timer.start()

    def cancel(self):
        if self.timer:
            self.timer.cancel()


class NacosTimerManager(object):
    def __init__(self, ):
        self.timers_container = {}
        self.executed = False

    def all_timers(self):
        return self.timers_container

    def add_timer(self, timer):
        self.timers_container[timer.name] = timer
        return self

    def execute(self):
        """
        scheduler all timer in manager
        :return: None
        """
        if self.executed:
            return
        for name, timer in self.timers_container.items():
            if timer.alive():
                continue
            timer.scheduler()
        self.executed = True

    def cancel_timer(self, timer_name=None, ):
        """
        cancel timer , and  nacos timer still in container
        it can execute again.
        :param timer_name:
        :return: None
        """
        timer = self.timers_container.get(timer_name)
        if timer:
            timer.cancel()

    def cancel(self):
        """
        cancel all timer in container
        :return: None
        """
        for _, timer in self.timers_container.items():
            timer.cancel()

    def stop_timer(self, timer_name):
        """
        cancel nacos timer and remove it from timer container
        :param timer_name:
        :return: None
        """
        self.cancel_timer(timer_name)
        self.timers_container.pop(timer_name)

    def stop(self):
        """
        remove all timer, and it can not execute again
        """
        self.cancel()
        self.timers_container.clear()
