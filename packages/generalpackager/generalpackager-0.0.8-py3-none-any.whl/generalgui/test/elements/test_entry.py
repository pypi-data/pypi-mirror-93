"""Tests for Entry"""

from test.shared_methods import GuiTests

from generalgui import Page, Entry, Button, Label, App


class EntryTest(GuiTests):
    def test__clickNextButton(self):
        page = Page(App())
        entry = Entry(page, "hello")
        Label(page, "random")
        Button(page, "Change default", lambda: 5)
        self.assertEqual([5], entry._clickNextButton())

        entry2 = Entry(page, "hello")
        Button(page, "Change default", lambda: 3)
        self.assertEqual([3], entry2._clickNextButton())

        page.app.remove()

    def test__removeWord(self):
        entry = Entry(Page(App()))
        entry.setValue("hello there")
        entry._removeWord()
        self.assertEqual("hello x", entry.getValue())

        entry.setValue("hello there")
        entry.setMarker(5)
        entry._removeWord()
        self.assertEqual("x there", entry.getValue())

        entry.setValue("hello there")
        entry.setMarker(6)
        entry._removeWord()
        self.assertEqual("helloxthere", entry.getValue())

        entry.setValue("hello there")
        entry.setMarker(6)
        entry._removeWord(delete=True)
        self.assertEqual("hello x", entry.getValue())

        entry.setValue("hello there")
        entry.setMarker(5)
        entry._removeWord(delete=True)
        self.assertEqual("helloxthere", entry.getValue())

        entry.app.remove()

    def test_getValue_and_setValue(self):
        entry = Entry(Page(App()), "default")
        self.assertEqual("default", entry.getValue())

        entry.setValue("hello there")
        self.assertEqual("hello there", entry.getValue())

        entry.setValue("")
        self.assertEqual("default", entry.getValue())

        entry.setValue(None)
        self.assertEqual("default", entry.getValue())

        entry.setValue(True)
        self.assertIs(True, entry.getValue())

        entry.setValue(5.2)
        self.assertEqual(5.2, entry.getValue())

        entry.setValue(5)
        self.assertEqual(5, entry.getValue())

        entry.setValue("5")
        self.assertEqual(5, entry.getValue())

        entry.setValue("none")
        self.assertEqual(None, entry.getValue())

        entry.app.remove()

    def test_default(self):
        entry = Entry(Page(App()), "default")
        entry.clearIfDefault()
        self.assertEqual("", entry.getValue())

        entry.setDefault("test")
        self.assertEqual("", entry.getValue())

        entry.callBind("<FocusOut>")
        self.assertEqual("test", entry.getValue())

        entry.clearIfDefault()
        self.assertEqual("", entry.getValue())

        entry.setValue("hello")
        self.assertEqual("hello", entry.getValue())

        entry.clearIfDefault()
        self.assertEqual("hello", entry.getValue())

        entry.setValue("not default")
        entry.callBind("<FocusOut>")
        self.assertEqual("not default", entry.getValue())

        entry.setDefault("not default")
        entry.clearIfDefault()
        self.assertEqual("", entry.getValue())

        entry.callBind("<FocusOut>")
        self.assertEqual("not default", entry.getValue())

        entry.setDefault(True)
        self.assertEqual(True, entry.getValue())

        entry.app.remove()




















