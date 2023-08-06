"""Shared methods by Element and Page"""

from generallibrary.types import typeChecker
from generallibrary.functions import defaults

from generalgui.shared_methods.decorators import ignore

from generalvector import Vec2

from tkinter import TclError


def spreadsheetSyncSizesWrapper(func, *args, **kwargs):
    """

    :param generalgui.Page or generalgui.element.Element self:
    :param func:
    :param args:
    :param kwargs:
    :return:
    """
    r = func(*args, **kwargs)
    self = args[0]

    if spreadsheet := self.parentPage.getFirstParentByClass("Spreadsheet"):
        spreadsheet.syncSizes()
    return r


class Element_Page:
    """
    Pure methods that Element and Page share.
    """
    def __init_subclass__(cls, **kwargs):
        """
        Wrap subclasses functions that can effect a parent spreadsheet's cell sizes.

        :param kwargs:
        :return:
        """
        methodsToWrap = ("setSize", "setValue")
        for methodName in methodsToWrap:
            if method := getattr(cls, methodName, None):
                setattr(cls, methodName, lambda *args, m=method, **kwargs: spreadsheetSyncSizesWrapper(m, *args, **kwargs))

    def hasGridParameters(self):
        """
        :param generalgui.element.Element or generalgui.Page self: Element or Page
        """
        return "column" in self.getTopElement().packParameters and "row" in self.getTopElement().packParameters

    def grid(self, pos):
        """
        Change this element's grid pack parameters and then call _grid.

        :param generalgui.element.Element or generalgui.Page self: Element or Page
        :param Vec2 pos: Grid position
        """
        self.packParameters.update(column=pos.x, row=pos.y)
        self._grid()

    def _grid(self):
        """
        Grids this Element's widget using the packParameters attribute.

        :param generalgui.element.Element or generalgui.Page self: Element or Page
        """
        if self.removed:
            raise AttributeError(f"{self} cannot be gridded since it's removed")

        pars = defaults(self.packParameters, sticky="NSEW")
        try:
            self.getTopWidget().grid(**pars)
        except Exception as e:
            print(e, self, self.getTopWidget(), pars)
            raise e

    def getParentPartPage(self):
        """
        Get the page of this element's or page's parentPart

        :param generalgui.element.Element or generalgui.Page self: Element or Page
        """
        if typeChecker(self.parentPart, "App", error=False):
            return self.app
        else:
            return self.parentPart.parentPage

    def getParentPartOrPage(self):
        """
        Get the parentPart of this part unless this part is topElement to it's parentPage, in which case parentPage is returned.

        :param generalgui.element.Element or generalgui.Page self: Element or Page
        """
        if typeChecker(self.parentPage, "App", error=False):
            return self.parentPage

        elif self.parentPage.topElement == self:
            return self.parentPage
        else:
            return self.parentPart



    def pack(self):
        """
        Packs this Element's widget using the packParameters attribute.

        :param generalgui.element.Element or generalgui.Page self: Element or Page
        """
        if typeChecker(self, "Page", error=False):
            if self.topElement is None:
                raise AttributeError("Cannot pack Page without a topElement.")
            self.topElement.pack()

        else:

            if self.hasGridParameters():
                self._grid()

            else:
                try:
                    self.getParentPartPage().packPart(self)
                    # self.parentPart.parentPage.packPart(self)
                except TclError as e:
                    print(self, self.packParameters, self.parentPart)
                    raise e

            if self.parentPage.scrollable:
                self.app.widget.update()  # To get correct scroll region
                self.parentPage.canvas.callBind("<Configure>")  # Update canvas scroll region manually

    def _place(self, pos):
        """
        Helper for place

        :param Vec2 pos: Coords for widget
        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        """
        self.getTopElement().widget.place(x=pos.x, y=pos.y)

    def place(self, pos):
        """
        Places a page with coordinates

        :param Vec2 pos: Coords for widget
        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        """
        self.pack()

        appSize = self.app.getSize()
        self._place(pos)
        self.app.widget.update()
        size = self.getSize()
        bottomRightPos = self.getBottomRightPos()

        if not bottomRightPos <= appSize:
            pos = pos.clamp(Vec2(0, 0), (appSize - size - 2).max(0))
            self._place(pos)

    def getTopPage(self):
        """
        Get the top page that has it's App as it's 'parentPage' attribute and has this element or page as a descendant.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :rtype: generalgui.page.Page
        """
        parentPages = self.getParents(includeSelf=True)
        return parentPages[-1]

    @ignore
    def getSiblings(self, ignore=None):
        """
        Get a list of all siblings of this element or page. Doesn't include self.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :param any ignore: A single child or multiple children to ignore. Is converted to list through decorator.
        :rtype: list[generalgui.element.Element or generalgui.page.Page]
        """
        children = self.parentPage.getChildren(ignore=ignore)

        if self in children:
            selfIndex = children.index(self)
            siblings = children[selfIndex + 1:]
            siblings.extend(children[0:selfIndex])
            return siblings
        else:
            return children

    @ignore
    def showSiblings(self, ignore=None, mainloop=True):
        """
        Calls the 'show' method on all siblings of this Element or Page retrieved from the 'getSiblings' method.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :param any ignore: A single child or multiple children to ignore. Is converted to list through decorator.
        :param mainloop: Whether to call mainloop or not
        """
        for sibling in self.getSiblings(ignore=ignore):
            sibling.show(mainloop=False)
        if mainloop:
            self.app.mainloop()

    @ignore
    def hideSiblings(self, ignore=None):
        """
        Calls the 'hide' method on all siblings of this Element or Page.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :param any ignore: A single child or multiple children to ignore. Is converted to list through decorator.
        """
        for sibling in self.getSiblings(ignore=ignore):
            sibling.hide()

    @ignore
    def removeSiblings(self, ignore=None):
        """
        Calls the 'remove' method on all siblings of this Element or Page.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :param any ignore: A single child or multiple children to ignore. Is converted to list through decorator.
        """
        for sibling in self.getSiblings(ignore=ignore):
            sibling.remove()

    @ignore
    def nextSibling(self, ignore=None):
        """
        Get the next sibling.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :param any ignore: A single child or multiple children to ignore. Is converted to list through decorator.
        """
        siblings = self.getSiblings(ignore=ignore)
        if siblings:
            return siblings[0]
        else:
            return None

    @ignore
    def previousSibling(self, ignore=None):
        """
        Get the previos sibling.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :param any ignore: A single child or multiple children to ignore. Is converted to list through decorator.
        """
        siblings = self.getSiblings(ignore=ignore)
        if siblings:
            return siblings[-1]
        else:
            return None

    def show(self, hideSiblings=False, mainloop=True):
        """
        Show this Element or Page if it's not shown. Propagates through all parent pages so they automatically are shown as well if needed.
        Even creates window automatically if it hasn't been created yet.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :param hideSiblings: Whether to hide siblings or not
        :param mainloop: Whether to call mainloop on App's widget or not
        """
        if hideSiblings:
            self.parentPage.hideChildren()

        for ele_page in self.getParents(includeSelf=True):
            if ele_page.isShown():
                break
            if not ele_page.isPacked():
                ele_page.pack()

        self.app.show(mainloop=mainloop)

    def hide(self):
        """
        Hide this Element or Page if it's packed.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        """
        if self.isPacked:
            if self.hasGridParameters():
                self.getTopWidget().grid_forget()
            else:
                self.getTopWidget().pack_forget()

    def toggleShow(self, mainloop=True):
        """
        Hides Element or Page if it's packed and shows it if it's not packed.

        :param generalgui.element.Element or generalgui.page.Page self: Element or Page
        :return: Whether it's shown or not after call
        :param mainloop: Whether to call mainloop or not when being shown
        """
        if self.isPacked():
            self.hide()
            return False
        else:
            self.show(mainloop=mainloop)
            return True

