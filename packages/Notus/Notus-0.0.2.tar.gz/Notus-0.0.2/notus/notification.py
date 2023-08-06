#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 26-12-2020
           """

__all__ = ["notify", "JobNotificationSession"]

from warg import AlsoDecorator


def notify(msg: str) -> None:
    try:
        from notus.win10 import win10_toaster

        win10_toaster.Win10Toaster().show_toast(msg, threaded=True)
    except Exception as e:
        try:
            from notus.gtk_dbus import gtk_toaster

            gtk_toaster.GtkToast().show_toast(msg)
        except Exception as e1:
            print(e, e1)


class JobNotificationSession(AlsoDecorator):
    """
    # speed up evaluating after training finished
    """

    def __init__(self, job_id: str):
        self.job_id = job_id

    def __enter__(self):
        notify(f"{self.job_id} Started")
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        notify(f"{self.job_id} Ended")


if __name__ == "__main__":
    notify("test")

    with JobNotificationSession("test2"):
        pass
