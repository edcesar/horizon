#
#  This file is Copyright (C) 2010 Feike Boomstra.
#  Distributed under the Boost Software License, Version 1.0.
#  (See accompanying file LICENSE_1_0.txt or copy at
#  http://www.boost.org/LICENSE_1_0.txt)
#


from DraughtConstants import *
from Tkinter import *
from DraughtDisplayOnly import *

dc = DraughtConstants()

class ClickMoveTag:
    def __init__(self, re_play, tag):
        self.re_play = re_play
        self.tag = tag
        return

    def __call__(self, event):
        self.re_play.click(self.tag)
        return




class DraughtRePlay:
    
    def __init__(self, main):
        self.main = main
        return
    
    def control_down_arrow_clicked(self):
        tag = self.main.ActiveTag
        for k in range(0,10):
            tag = self.incr_tag(tag, True)
        self.click(tag)        
        return
    
    def down_arrow_clicked(self):
        tag = self.main.ActiveTag
        for k in range(0,10):
            tag = self.incr_tag(tag)
        self.click(tag)        
        return

    def control_up_arrow_clicked(self):
        tag = self.main.ActiveTag
        for k in range(0,10):
            tag = self.decr_tag(tag, True)
        self.click(tag)        
        return
    
    def up_arrow_clicked(self):
        tag = self.main.ActiveTag
        for k in range(0,10):
            tag = self.decr_tag(tag)
        self.click(tag)        
        return
    
    def left_arrow_clicked(self):
        self.click(self.decr_tag(self.main.ActiveTag))
        return
    
    def control_left_arrow_clicked(self):
        self.click(self.decr_tag(self.main.ActiveTag, True))
        return

    def right_arrow_clicked(self):
        self.click(self.incr_tag(self.main.ActiveTag))
        return
    
    def control_right_arrow_clicked(self):
        self.click(self.incr_tag(self.main.ActiveTag, True))
        return
    
    def page_down_clicked(self):
        tag = self.main.ActiveTag
        games, pnts = self.decompose_tag(tag)
        game = games[-1]
        pnt = pnts[-1]
        game_nr = pnts[0]
        if pnt == game.half_ply_length(): # at the end ?
            if len(pnts) > 2:             # variant ?
                new_tag = self.compose_tag([game_nr, games[0].half_ply_length()])
            else:
                if len(self.main.Games) > game_nr + 1:
                    game_nr = game_nr + 1
                    self.main.ActiveGame = self.main.Games[game_nr]
                new_tag = self.compose_tag([game_nr, self.main.ActiveGame.half_ply_length()])
        else:
            new_tag = self.compose_tag([game_nr, self.main.ActiveGame.half_ply_length()])
        self.click(self.compose_tag([game_nr,0])) # at the begin to force move-display
        self.click(new_tag)    
        return
    
    def page_up_clicked(self):
        tag = self.main.ActiveTag
        games, pnts = self.decompose_tag(tag)
        game = games[-1]
        pnt = pnts[-1]
        game_nr = pnts[0]
        if pnt == 0: # at the begin ?
            if len(pnts) > 2:             # variant ?
                new_tag = self.compose_tag([game_nr, 0])
            else:
                if game_nr > 0:
                    game_nr = game_nr - 1
                    self.main.ActiveGame = self.main.Games[game_nr]
                new_tag = self.compose_tag([game_nr, 0])
        else:
            new_tag = self.compose_tag([game_nr, 0])
        self.click(new_tag)    
        return

    def incr_tag(self, tag, cntl = False):
        games, pnts = self.decompose_tag(tag)
        game = games[-1]
        pnt = pnts[-1]
        if pnt == game.half_ply_length(): # at the end ?
            if len(pnts) > 2:             # variant ?
                pnts = pnts[:-1]
                return self.incr_tag(self.compose_tag(pnts))
            # we are at the lowest level
            game_nr = pnts[0]
            if len(self.main.Games) > game_nr + 1:
                game_nr = game_nr + 1
                self.main.ActiveGame = self.main.Games[game_nr]
                return self.compose_tag([game_nr, 0])
            else:
                return self.compose_tag([game_nr, games[0].half_ply_length()])
                
        else:
            if cntl == True:
                game.HalfPlyPointer = pnt
                half_ply = game.get_half_ply_pointer_record()
                if half_ply.Variant == '':
                    if pnt < game.half_ply_length(): pnts[-1] = pnt + 1
                    return self.compose_tag(pnts)
                else:   # we must go to the begin of the variant
                    pnts.append(0)
                    return self.compose_tag(pnts)
            else:    
                if pnt < game.half_ply_length(): pnts[-1] = pnt + 1
                return self.compose_tag(pnts)
    
    def decr_tag(self, tag, cntl = False):
        games, pnts = self.decompose_tag(tag)
        if games == []: return tag
        game = games[-1]
        pnt = pnts[-1]
        if pnt == 0:                      # at the begin ?
            if len(pnts) > 2:             # variant ?
                pnts = pnts[:-1]
                return self.decr_tag(self.compose_tag(pnts))
            # we are at the lowest level
            game_nr = pnts[0]
            if game_nr > 0:
                game_nr = game_nr - 1
                self.main.ActiveGame = self.main.Games[game_nr]
            return self.compose_tag([game_nr, 0])
        else:
            if cntl == True:
                pnt = pnt - 1
                pnts[-1] = pnt
                game.HalfPlyPointer = pnt
                half_ply = game.get_half_ply_pointer_record()
                if half_ply.Variant == '':
                    return self.compose_tag(pnts)
                else:   # we must go to the end of the variant
                    pnts.append(half_ply.Variant.half_ply_length())
                    return self.compose_tag(pnts)
            else:    
                pnts[-1] = pnt - 1
                return self.compose_tag(pnts)
    
    def decompose_tag(self,tag):

        if len(tag) < 7:
            print "Invalid tag: ", tag
            return ([], [])

        game_nr = int(tag[0:3])
        pnt = int(tag[4:7])
        game = self.main.Games[game_nr]
        games = [game, game]
        pnts = [game_nr, pnt]
        
        k = 8
        while len(tag) >= k + 3:
            pnt = int(tag[k:k+3])
            pnts.append(pnt)
            game = game.get_half_ply_pointer_record().Variant
            games.append(game)
            k = k+ 4
        return (games, pnts)
    
    def compose_tag(self, pnts):
        tag = str(pnts[0]).zfill(3)
        for k in range(1, len(pnts)):
            tag = tag + '_' + str(pnts[k]).zfill(3)
        return tag
    
    def click(self, tag):
        self.display_till_tag(tag)
        if self.main.ActiveTag <> '':
            self.main.panel.notation.tag_config(self.main.ActiveTag, background = "white")
        self.main.panel.notation.tag_config(tag, background = "yellow")
        self.main.ActiveTag = tag
        return
    

    def display_till_tag(self, tag):
        level = 0
        if len(tag) < 7:
            print "Invalid tag: ", tag
            return
        game_nr = int(tag[0:3])
        pnt = int(tag[4:7])
        game = self.main.Games[game_nr]
        if len(self.main.CurrentDisplayGame) == level:
             self.main.CurrentDisplayGame.append(game)
        game.HalfPlyPointer = pnt
        game.build_till_pointer()
        game.refresh_display()
        
        k = 8
        while len(tag) >= k + 3:
            level = level + 1
            prev_pnt = pnt
            prev_game = game
            pnt = int(tag[k:k+3])
            game = game.get_half_ply_pointer_record().Variant
            if len(self.main.CurrentDisplayGame) == level:
                 self.main.CurrentDisplayGame.append(game)
            elif self.main.CurrentDisplayGame[level] <> game:
                del_game = self.main.CurrentDisplayGame[level]
                if del_game.ActivePanel <> '':
                    del_game.ActivePanel.top.destroy()
                    del_game.ActivePanel = ''
                self.main.CurrentDisplayGame[level] = game
            if game.ActivePanel == '':
                print "New panel"
                new = FloatingBoard(self.main, self.end_new_game, level, prev_game.ActivePanel.top)
                new.top.geometry(self.main.NewPanelGeometry[level])                
                game.ActivePanel = new
                self.CopyBeginPosition(prev_game, game)
            game.HalfPlyPointer = pnt
            game.build_till_pointer()
            game.refresh_display()
            k = k + 4
        # check whether there are "old" variants displayed
        for k in range(level + 1, len(self.main.CurrentDisplayGame)):
            old_variant = self.main.CurrentDisplayGame.pop()
            if old_variant.ActivePanel <> '':
                self.main.NewPanelGeometry[k] = old_variant.ActivePanel.top.geometry()
                old_variant.ActivePanel.top.destroy()
                old_variant.ActivePanel = ''
        return
    
    def end_new_game(self, level):             # user wants to remove the new panel
        prev_tag = self.current_tag(self.main.CurrentDisplayGame[level-1])
        for k in range(level, len(self.main.CurrentDisplayGame)):
            old_variant = self.main.CurrentDisplayGame.pop()
            if old_variant.ActivePanel <> '':
                self.main.NewPanelGeometry[k] = old_variant.ActivePanel.top.geometry()
                old_variant.ActivePanel.top.destroy()
                old_variant.ActivePanel = ''
        self.click(prev_tag)
        return
 
    def CopyBeginPosition(self, game, new_game):
        new_game.BeginPosition.WhiteMan = game.CurrentPosition.WhiteMan[:]
        new_game.BeginPosition.WhiteKing = game.CurrentPosition.WhiteKing[:]
        new_game.BeginPosition.BlackMan = game.CurrentPosition.BlackMan[:]
        new_game.BeginPosition.BlackKing = game.CurrentPosition.BlackKing[:]
        new_game.BeginPosition.ColorOnMove = game.CurrentPosition.ColorOnMove
        new_game.PreviousActiveGame = self.main.ActiveGame
        new_game.PreviousHalfPlyPointer = game.HalfPlyPointer
        self.main.ActiveGame = new_game
        return


   