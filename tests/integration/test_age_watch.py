# vim:ts=4:sw=4:et:
# Copyright 2012-present Facebook, Inc.
# Licensed under the Apache License, Version 2.0
import WatchmanTestCase
import tempfile
import os
import os.path
import time
import json


class TestAgeOutWatch(WatchmanTestCase.WatchmanTestCase):

    def makeRootAndConfig(self):
        root = self.mkdtemp()
        with open(os.path.join(root, '.watchmanconfig'), 'w') as f:
            f.write(json.dumps({
                'idle_reap_age_seconds': 1
            }))
        return root

    def test_watchReap(self):
        root = self.makeRootAndConfig()
        self.watchmanCommand('watch', root)

        # make sure that we don't reap when there are registered triggers
        self.watchmanCommand('trigger', root, {
            'name': 't',
            'command': ['true']})

        # wait long enough for the reap to be considered
        time.sleep(10)

        watch_list = self.watchmanCommand('watch-list')
        self.assertEqual(self.normFileList(watch_list['roots']), [root])

        self.watchmanCommand('trigger-del', root, 't')

        # Make sure that we don't reap while we hold a subscription
        res = self.watchmanCommand('subscribe', root, 's', {
            'fields': ['name']})

        if self.transport == 'cli':
            # subscription won't stick in cli mode
            expected = []
        else:
            expected = self.normFileList([root])

        self.waitFor(lambda: self.normFileList(
            self.watchmanCommand('watch-list')['roots']) == expected)

        watch_list = self.watchmanCommand('watch-list')
        self.assertEqual(self.normFileList(watch_list['roots']), expected)

        if self.transport != 'cli':
            # let's verify that we can safely reap two roots at once without
            # causing a deadlock
            second = self.makeRootAndConfig()
            self.watchmanCommand('watch', second)
            self.assertFileList(second, ['.watchmanconfig'])

            # and unsubscribe from root and allow it to be reaped
            self.watchmanCommand('unsubscribe', root, 's')

        # and now we should be ready to reap
        self.waitFor(lambda: len(
            self.watchmanCommand('watch-list')['roots']) == 0)

        self.assertEqual(
            self.watchmanCommand('watch-list')['roots'], [])
