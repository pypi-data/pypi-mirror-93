# Display card output and retreive input
# Armaan Bhojwani 2021

import curses
from random import shuffle
import sys
import textwrap

from . import lightcards, progress


class Display():
    def __init__(self, stack, headers, obj):
        self.stack = stack
        self.headers = headers
        self.obj = obj

    def run(self, stdscr):
        """Set important options before beginning"""
        self.win = stdscr
        curses.curs_set(0)  # Hide cursor
        curses.init_pair(1, curses.COLOR_CYAN, 0)
        curses.init_pair(2, curses.COLOR_RED, 0)
        curses.init_pair(3, curses.COLOR_YELLOW, 0)
        self.get_key()

    def leave(self):
        """Pickle stack before quitting"""
        if self.obj.getIdx() == len(self.stack):
            self.obj.setIdx(0)

        progress.dump(self.stack, lightcards.get_orig())
        sys.exit(0)

    def ntotal(self):
        """Get toal number of starred cards"""
        return(len([card for card in self.stack if card.getStar()]))

    def disp_bar(self):
        """
        Display the statusbar at the bottom of the screen with progress, star
        status, and card side.
        """
        (mlines, mcols) = self.win.getmaxyx()

        # Calculate percent done
        if len(self.stack) <= 1:
            percent = "100"
        else:
            percent = str(round(self.obj.getIdx() /
                                len(self.stack) * 100)).zfill(2)

        # Print yellow if starred
        if self.stack[self.obj.getIdx()].getStar():
            star_color = curses.color_pair(3)
        else:
            star_color = curses.color_pair(1)

        # Create bar component
        bar_start = "["
        bar_middle = self.stack[self.obj.getIdx()].printStar()
        bar_end = f"] [{self.ntotal()}/{str(len(self.stack))} starred] " + \
            f"[{percent}% (" + \
            str(self.obj.getIdx() + 1).zfill(len(str(len(self.stack)))) + \
            f"/{str(len(self.stack))})] [" + \
            f"{self.headers[self.obj.getSide()]} (" + \
            f"{str(self.obj.getSide() + 1)})] "

        # Put it all togethor
        self.win.hline(mlines - 2, 0, 0, mcols)
        self.win.addstr(mlines - 1, 0, bar_start, curses.color_pair(1))
        self.win.addstr(bar_middle, star_color)
        self.win.insstr(bar_end, curses.color_pair(1))

    def menu_print(self, string, err=False):
        """Print messages on the menu screen"""
        self.win.clear()
        if err:
            color = curses.color_pair(2)
        else:
            color = curses.color_pair(1)
        self.disp_menu(keygrab=False)
        self.win.addstr("\n\n" + string, color)
        self.menu_grab()

    def menu_grab(self):
        """Grab keypresses for the menu screen"""
        while True:
            key = self.win.getkey()
            if key == "q":
                if len(self.stack) == self.obj.getIdx():
                    self.leave()
                elif len(self.stack) < self.obj.getIdx():
                    self.obj.setIdx(0)
                self.get_key()
            elif key == "y":
                self.stack = lightcards.get_orig()[1]
                self.menu_print("Stack reset!")
            elif key == "a":
                self.stack.sort()
                self.menu_print("Stack alphabetized!")
            elif key == "u":
                [x.unStar() for x in self.stack]
                self.menu_print("All unstarred!")
            elif key == "d":
                [x.star() for x in self.stack]
                self.menu_print("All starred!")
            elif key == "t":
                self.stack.reverse()
                self.menu_print(
                    "self.stack reversed!")
            elif key == "z":
                shuffle(self.stack)
                self.menu_print("Stack shuffled!")
            elif key == "f":
                for x in self.stack:
                    x[0], x[1] = x[1], x[0]
                (self.headers[0], self.headers[1]) = (self.headers[1],
                                                      self.headers[0])
                self.menu_print("Cards flipped!")
            elif key == "s":
                # Check if there are any starred cards before proceeding, and
                # if not, don't allow to proceed and show an error message
                cont = False
                for x in self.stack:
                    if x.getStar():
                        cont = True
                        break

                if cont:
                    self.stack = [x for x in self.stack if x.getStar()]
                    self.menu_print("Stars only!")
                else:
                    self.menu_print("ERR: None are starred!", err=True)
            elif key in ["h", "KEY_LEFT"]:
                self.obj.setIdx(len(self.stack) - 1)
                self.get_key()
            elif key == "r":
                self.obj.setIdx(0)
                self.get_key()

    def disp_menu(self, keygrab=True, quit=False):
        """
        Display a menu once the end of the deck has been reached, offering
        multiple options on how to continue.
        """

        quit_text = "[q]: back"
        if quit:
            quit_text = "[q]: quit"

        self.win.addstr("LIGHTCARDS MENU", curses.color_pair(1) +
                        curses.A_BOLD)
        self.win.hline(1, 0, curses.ACS_HLINE, 15)
        self.win.addstr(2, 0, "[y]: reset stack to original state\n" +
                        "[a]: alphabetize stack\n" +
                        "[z]: shuffle stack\n" +
                        "[f]: flip all cards in stack\n" +
                        "[t]: reverse stack order\n" +
                        "[u]: unstar all\n" +
                        "[d]: star all\n" +
                        "[s]: update stack to include starred only\n\n" +
                        "[r]: restart\n" +
                        quit_text)

        if keygrab:
            self.menu_grab()

    def wrap_width(self):
        """Calculate the width at which the body should wrap"""
        (_, mcols) = self.win.getmaxyx()
        wrap_width = mcols - 20
        if wrap_width > 80:
            wrap_width = 80
        return wrap_width

    def disp_card(self):
        """
        Display the contents of the card
        Shows a header, a horizontal line, and the contents of the current
        side.
        """
        self.win.clear()
        (_, mcols) = self.win.getmaxyx()
        if self.obj.getIdx() == len(self.stack):
            self.disp_menu(quit=True)
        else:
            # If on the back of the card, show the content of the front side in
            # the header
            num_done = str(self.obj.getIdx() +
                           1).zfill(len(str(len(self.stack))))
            if self.obj.getSide() == 0:
                top = num_done + " | " + self.headers[self.obj.getSide()]
            else:
                top = num_done + " | " + self.headers[self.obj.getSide()] + \
                    " | \"" + str(self.stack[self.obj.getIdx()][0]) + "\""
            header_width = mcols
            if mcols > 80:
                header_width = 80

            self.win.addstr(textwrap.shorten(top, width=header_width,
                                             placeholder="…"), curses.A_BOLD)

            # Add horizontal line
            lin_width = header_width
            if len(top) < header_width:
                lin_width = len(top)
            self.win.hline(1, 0, curses.ACS_HLINE, lin_width)

            # Show current side
            self.win.addstr(2, 0, textwrap.fill(
                self.stack[self.obj.getIdx()][self.obj.getSide()],
                width=self.wrap_width()))
        self.disp_bar()
        self.disp_sidebar()

    def disp_help(self):
        """Display help screen"""
        self.win.clear()
        self.win.addstr("LIGHTCARDS HELP", curses.color_pair(1) +
                        curses.A_BOLD)
        self.win.hline(1, 0, curses.ACS_HLINE, 15)
        self.win.addstr(2, 0, textwrap.fill(
            "Welcome to lightcards. Here are some keybindings to get you " +
            "started:", width=self.wrap_width()) +
                        "\n\nh, left          previous card\n" +
                        "l, right         next card\n" +
                        "j, k, up, down   flip card\n" +
                        "i, /             star card\n" +
                        "0, ^, home       go to the start of the deck\n" +
                        "$, end           go to the end of the deck\n" +
                        "H, ?             open this screen\n" +
                        "e                open the input file in $EDITOR\n" +
                        "m                open the control menu\n\n" +
                        textwrap.fill(
                            "More information can be found in the man page, " +
                            "or by running `lightcards --help`.",
                            width=self.wrap_width()) +
                        "\n\nPress [q], [H], or [?] to go back.")
        while True:
            key = self.win.getkey()
            if key in ["q", "H", "?"]:
                self.get_key()

    def get_key(self):
        """
        Display a card and wait for the input.
        Used as a general way of getting back into the card flow from a menu
        """

        self.disp_card()
        while True:
            key = self.win.getkey()
            if key == "q":
                self.leave()
            elif key in ["l", "KEY_RIGHT"]:
                self.obj.forward(self.stack)
                self.obj.setSide(0)
                self.disp_card()
            elif key in ["h", "KEY_LEFT"]:
                self.obj.back()
                self.obj.setSide(0)
                self.disp_card()
            elif key in ["j", "k", "KEY_UP", "KEY_DOWN"]:
                self.obj.flip()
                self.disp_card()
            elif key in ["i", "/"]:
                self.stack[self.obj.getIdx()].toggleStar()
                self.disp_card()
            elif key in ["0", "^", "KEY_HOME"]:
                self.obj.setIdx(0)
                self.obj.setSide(0)
                self.disp_card()
            elif key in ["$", "KEY_END"]:
                self.obj.setIdx(len(self.stack) - 1)
                self.obj.setSide(0)
                self.disp_card()
            elif key in ["H", "?"]:
                self.disp_help()
            elif key == "m":
                self.win.clear()
                self.disp_menu()
            elif key == "e":
                (self.headers, self.stack) = lightcards.reparse()
                self.get_key()

    def disp_sidebar(self):
        """Display a sidebar with the starred terms"""
        (mlines, mcols) = self.win.getmaxyx()
        left = mcols - 19

        self.win.addstr(0, mcols - 16, "STARRED CARDS",
                        curses.color_pair(3) + curses.A_BOLD)
        self.win.vline(0, mcols - 20, 0, mlines - 2)
        self.win.hline(1, left, 0, mlines)

        i = 0
        for card in self.stack:
            if i > mlines - 6:
                self.win.addstr(2 + i, left, f"... ({self.ntotal() - i} more)")
                break
            elif card.getStar():
                term = card[0]
                if len(card[0]) > 18:
                    term = card[0][:18] + "…"
                self.win.addstr(2 + i, left, term)

                i += 1

        if i == 0:
            self.win.addstr(2, left, "None starred")
