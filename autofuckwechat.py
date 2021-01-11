# -*- coding: utf-8 -*-

import pyautogui as pg
import time, sys
from tqdm import tqdm

pg.FAILSAFE = True   # move the mouse to the upper-left to abort the program
pg.position()  # current mouse x and y
pg.size()  # current screen resolution width and height

# %%
def migrate_account_subscription(n_accounts, i_start=0):
    # move focus to accounts list
    pos_header = pg.locateCenterOnScreen('./header.png')
    pos_header = (pos_header.x, pos_header.y) if pos_header is not None else (974, 185)
    pg.click(pos_header)
        
    limit_check = True
    
    while pg.locateCenterOnScreen('./pin.png') is None:
        pg.hotkey('tab')
    pg.hotkey('shift', 'tab')
    
    pg.press('right', presses=i_start, interval=0.01)
    
    if pg.confirm(text='Ready to start?', title='Ready to start?', buttons=['OK', 'Cancel']) == 'Cancel':
        sys.exit()
    
    for i in tqdm(list(range(n_accounts))[i_start:]):    # loop over account list
        # Send
    #    pg.click(pos_header)
        pg.press('enter', interval=0.1)     # wait 0.1s for fucking WeChat to load
        pg.keyDown('shift')
        pg.press('tab', presses=3)
        pg.keyUp('shift')
        pg.press('enter', interval=0.1)
        
        pos_receiver = pg.locateCenterOnScreen('./receiver.png')
        while pos_receiver is None:
            time.sleep(0.01)
            pos_receiver = pg.locateCenterOnScreen('./receiver.png')
        pg.click(pos_receiver.x, pos_receiver.y)  # select receiver
        
        if pg.locateOnScreen('./confirm_sending.png'):
            pg.click(x=1141, y=806)  # send
        else:
            print(f'Receiver not matching for account {i+1}/{n_accounts}')
            if pg.confirm(
                    text='Receiver not matching. Abort?', title='Sending Exception', buttons=['OK', 'Cancel']) == 'OK':
                sys.exit()
            else:
                pg.press('esc')
                continue
        
        # Receive
#        time.sleep(2)
        pg.click(x=230, y=850, interval=1)  # click the last received card
        pos_subscribe = pg.locateCenterOnScreen('./subscribe.png')
        if pos_subscribe is not None:
            pg.click(pos_subscribe.x, pos_subscribe.y, interval=0.1)
            while pg.locateOnScreen('./subscribe_success.png') is None:
                time.sleep(0.1)
                if pg.locateOnScreen('./cannot_subscribe.png'):
                    break
                if pg.locateOnScreen('./limit.png'):
                    sys.exit(f"Reached temporary subscription limit. Aborting at account {i}/{n_accounts}.")
            pg.rightClick()
        while pg.locateOnScreen('./subscribed.png') is None:
            time.sleep(0.1)
        pg.rightClick()     # back to chating panel

        i += 1
        if limit_check == True:
            if i - i_start >= 40 and pg.confirm(
                    text=f"Reaching temporary subscription limit. \nBetter to resume next time at {i+1}/{n_accounts}. \n\nAbort?", 
                    title='Reaching temporary subscription limit', 
                    buttons=['Yes', 'No']
                    ) == 'Yes':
                sys.exit(f"Reaching temporary subscription limit. Better to resume next time at {i+1}/{n_accounts}.")
            else:
                limit_check = False

        pg.click(pos_header)    # move accounts list to frontground
        pg.press('right')
        
# %%
if __name__ == "__main__":
  migrate_account_subscription(n_accounts=225, i_start=0)