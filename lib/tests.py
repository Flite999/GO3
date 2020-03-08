"""
    This file is part of Gig-o-Matic

    Gig-o-Matic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from django.core import mail
from django.test import TestCase

from lib.email import send_messages_async

from gig.models import Gig
from member.models import Member
from band.models import Band, Assoc
from lib.caldav import save_calfeed, get_calfeed, make_calfeed
from pyfakefs.fake_filesystem_unittest import TestCase as FSTestCase
import os
from datetime import timedelta
from django.utils import timezone
import pytz

class EmailTest(TestCase):

    def test_send_messages_async(self):
        self.assertEqual(len(mail.outbox), 0)
        send_messages_async([mail.EmailMessage('Subject', 'Body', 'from@example.com', ['to@example.com'])])
        self.assertEqual(len(mail.outbox), 1)

    def test_send_many_messages_async(self):
        self.assertEqual(len(mail.outbox), 0)
        send_messages_async([mail.EmailMessage('Subject', 'Body', 'from@example.com', ['to@example.com'])] * 5)
        self.assertEqual(len(mail.outbox), 5)


class CaldavTest(TestCase):
    def setUp(self):
        """ fake a file system """
        self.super = Member.objects.create_user(email='a@b.c', is_superuser=True)
        self.band_admin = Member.objects.create_user(email='d@e.f')
        self.joeuser = Member.objects.create_user(email='g@h.i')
        self.janeuser = Member.objects.create_user(email='j@k.l')
        self.band = Band.objects.create(name='test band')
        Assoc.objects.create(member=self.band_admin, band=self.band, is_admin=True)
        self.testgig = self.create_gig()

    def tearDown(self):
        """ make sure we get rid of anything we made """
        Member.objects.all().delete()
        Band.objects.all().delete()
        Assoc.objects.all().delete()
        Gig.objects.all().delete()

    def create_gig(self):
        the_date = timezone.datetime(year=2020, month=2, day=29, hour=14, minute=30,tzinfo=pytz.timezone(self.band.timezone))
        return Gig.objects.create(
            title="New Gig",
            band_id=self.band.id,
            date=the_date,
        )

    def test_calfeed(self):
        cf = make_calfeed('flim-flam', [], self.joeuser.preferences.language, self.joeuser.cal_feed_id)
        self.assertTrue(cf.startswith(b'BEGIN:VCALENDAR'))
        self.assertTrue(cf.find(b'flim-flam')>0)
        self.assertTrue(cf.endswith(b'END:VCALENDAR\r\n'))

    def test_calfeed_event(self):
        cf = make_calfeed(b'flim-flam', self.band.gigs.all(),self.joeuser.preferences.language, self.joeuser.cal_feed_id)
        self.assertTrue(cf.find(b'EVENT')>0)

    def test_calfeed_event_no_enddate(self):
        cf = make_calfeed(b'flim-flam', self.band.gigs.all(),self.joeuser.preferences.language, self.joeuser.cal_feed_id)
        self.assertTrue(cf.find(b'DTSTART;VALUE=DATE-TIME:20200229T143000Z')>0)
        # with no end date set, caldeef should show an end date of an hour after start
        self.assertTrue(cf.find(b'DTEND;VALUE=DATE-TIME:20200229T153000Z')>0)

    def test_calfeed_event_enddate(self):
        # set the end date and make sure the calfeed is updated
        self.testgig.enddate = self.testgig.date + timedelta(hours=2)
        self.testgig.save()
        cf = make_calfeed(b'flim-flam', self.band.gigs.all(),self.joeuser.preferences.language, self.joeuser.cal_feed_id)
        self.assertTrue(cf.find(b'DTSTART;VALUE=DATE-TIME:20200229T143000Z')>0)
        self.assertTrue(cf.find(b'DTEND;VALUE=DATE-TIME:20200229T163000Z')>0)


class CaldavFileTest(FSTestCase):

    def setUp(self):
        """ fake a file system """
        self.super = Member.objects.create_user(email='a@b.c', is_superuser=True)
        self.band_admin = Member.objects.create_user(email='d@e.f')
        self.joeuser = Member.objects.create_user(email='g@h.i')
        self.janeuser = Member.objects.create_user(email='j@k.l')
        self.band = Band.objects.create(name='test band')
        Assoc.objects.create(member=self.band_admin, band=self.band, is_admin=True)
        self.testgig = self.create_gig()
        self.setUpPyfakefs()
        os.mkdir('calfeeds')

    def tearDown(self):
        """ make sure we get rid of anything we made """
        Member.objects.all().delete()
        Band.objects.all().delete()
        Assoc.objects.all().delete()
        Gig.objects.all().delete()

    def create_gig(self):
        the_date = timezone.datetime(year=2020, month=2, day=29, hour=14, minute=30,tzinfo=pytz.timezone(self.band.timezone))
        return Gig.objects.create(
            title="New Gig",
            band_id=self.band.id,
            date=the_date,
        )

    def test_calfeed_save_and_get(self):
        save_calfeed('testfile1',b'')
        cf = get_calfeed('testfile1')
        self.assertEqual(cf,'')

    def test_calfeed_save_content(self):
        save_calfeed('testfile2',b'hi')
        cf = get_calfeed('testfile2')
        self.assertEqual(cf,'hi')






