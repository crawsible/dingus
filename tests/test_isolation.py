from __future__ import with_statement
import urllib2
import os

from dingus import Dingus, patch, patch_all, isolate


class WhenPatchingAnObject:
    @patch('urllib2.urlopen')
    def should_replace_object_with_dingus(self):
        assert isinstance(urllib2.urlopen, Dingus)

    def should_restore_object_after_patched_function_exits(self):
        @patch('urllib2.urlopen')
        def patch_urllib2():
            pass
        patch_urllib2()
        assert not isinstance(urllib2.urlopen, Dingus)

    def should_be_usable_as_context_manager(self):
        with patch('urllib2.urlopen'):
            assert isinstance(urllib2.urlopen, Dingus)
        assert not isinstance(urllib2.urlopen, Dingus)

    def should_be_able_to_provide_explicit_dingus(self):
        my_dingus = Dingus()
        with patch('urllib2.urlopen', my_dingus):
            assert urllib2.urlopen is my_dingus

    def should_name_dingus_after_patched_object(self):
        with patch('urllib2.urlopen'):
            assert str(urllib2.urlopen) == '<Dingus urllib2.urlopen>'

    def should_set_wrapped_on_patched_function(self):
        def urllib2():
            pass
        patch_urllib2 = patch('urllib2.urlopen')(urllib2)
        assert patch_urllib2.__wrapped__ == urllib2


class WhenPatchingMultipleObjects:
    @patch_all(['urllib2.urlopen', 'os.path.exists'])
    def should_replace_objects_with_dinguses(self):
        assert isinstance(urllib2.urlopen, Dingus)
        assert isinstance(os.path.exists, Dingus)

    def should_restore_object_after_patched_function_exits(self):
        @patch_all(['urllib2.urlopen', 'os.path.exists'])
        def patch_urllib2():
            pass
        patch_urllib2()
        assert not isinstance(urllib2.urlopen, Dingus)
        assert not isinstance(os.path.exists, Dingus)

    def should_be_usable_as_context_manager(self):
        with patch_all(['urllib2.urlopen', 'os.path.exists']):
            assert isinstance(urllib2.urlopen, Dingus)
            assert isinstance(os.path.exists, Dingus)
        assert not isinstance(urllib2.urlopen, Dingus)
        assert not isinstance(os.path.exists, Dingus)

    def should_be_able_to_provide_explicit_dingus(self):
        my_dingus = Dingus()
        my_other_dingus = Dingus()
        with patch_all({
            'urllib2.urlopen': my_dingus,
            'os.path.exists': my_other_dingus
        }):
            assert urllib2.urlopen is my_dingus
            assert os.path.exists is my_other_dingus

    def should_handle_dictionaries_and_lists(self):
        my_third_dingus = Dingus()
        with patch_all(
                ['urllib2.urlopen'],
                {'os.path.exists': my_third_dingus}
        ):
            assert isinstance(urllib2.urlopen, Dingus)
            assert os.path.exists is my_third_dingus


class WhenIsolating:
    def should_isolate(self):
        @isolate("os.popen")
        def ensure_isolation():
            assert not isinstance(os.popen, Dingus)
            assert isinstance(os.walk, Dingus)

        assert not isinstance(os.walk, Dingus)
        ensure_isolation()
        assert not isinstance(os.walk, Dingus)


class WhenIsolatingSubmoduleObjects:
    def should_isolate(self):
        @isolate("os.path.isdir")
        def ensure_isolation():
            assert not isinstance(os.path.isdir, Dingus)
            assert isinstance(os.path.isfile, Dingus)

        assert not isinstance(os.path.isfile, Dingus)
        ensure_isolation()
        assert not isinstance(os.path.isfile, Dingus)
