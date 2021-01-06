# -*- coding: utf-8 -*-

import pyautogui as pg
import time, sys
from tqdm import tqdm

pg.FAILSAFE = True   # move the mouse to the upper-left to abort the program
#pg.PAUSE = 1         # pause after each pg call
#n_accounts = 285
pg.position()  # current mouse x and y
pg.size()  # current screen resolution width and height
#pg.onScreen(x, y)  # True if x & y are within the screen.

# %%
def migrate_account_subscription(n_accounts, i_start=0):
    # move focus to accounts list
    pos_header = pg.locateCenterOnScreen('./header.png')
    #if pos_header is not None:
    #    pg.click(pos_header.x, pos_header.y)
    #else:
    #    pg.click(974, 185)
    pos_header = (pos_header.x, pos_header.y) if pos_header is not None else (974, 185)
    pg.click(pos_header)
        
    while pg.locateCenterOnScreen('./pin.png') is None:
        pg.hotkey('shift', 'tab')
    pg.hotkey('shift', 'tab')
    
    #pg.press('enter', interval=5)
    if pg.confirm(text='Ready to start?', title='Ready to start?', buttons=['OK', 'Cancel']) == 'Cancel':
        sys.exit()
#    time.sleep(5)
    
    
    for i in tqdm(list(range(n_accounts))[i_start:]):    # loop over account list
        if i != 0:
            pg.click(pos_header)    # move accounts list to frontground
            pg.press('right')
            
        # Send
    #    pg.click(pos_header)
        pg.press('enter', interval=0.1)     # wait 0.1s for fucking WeChat to load
        pos_send = pg.locateCenterOnScreen('./send.png')  # returns center x and y
        while pos_send is None:
            time.sleep(0.01)
            pos_send = pg.locateCenterOnScreen('./send.png')
        pg.click(pos_send.x, pos_send.y)
        
        pg.click(x=790, y=380)  # select receiver
        
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
        time.sleep(0.1)
        pg.click(x=218, y=850, interval=1)
        pos_subscribe = pg.locateCenterOnScreen('./subscribe.png')
        if pos_subscribe is not None:
            pg.click(pos_subscribe.x, pos_subscribe.y, interval=0.1)
            while pg.locateOnScreen('./subscribe_success.png') is None:
                time.sleep(0.1)
                if pg.locateOnScreen('./cannot_subscribe.png'):
                    break
                if pg.locateOnScreen('./limit.png'):
                    sys.exit("Reached temporary subscription limit. Aborting at account {i}/{n_accounts}.")
            pg.rightClick()
        while pg.locateOnScreen('./subscribed.png') is None:
            time.sleep(0.1)
        pg.rightClick()     # back to chating panel
        i += 1
        if i - i_start >= 35 and pg.confirm(
                text=f"Reaching temporary subscription limit. \nBetter to resume next time at {i+1}/{n_accounts}. \n\nAbort?", 
                title='Reaching temporary subscription limit', 
                buttons=['Yes', 'No']
                ) == 'Yes':
            sys.exit(f"Reaching temporary subscription limit. Better to resume next time at {i+1}/{n_accounts}.")

# %%
if __name__ == "__main__":
  migrate_account_subscription(n_accounts=230, i_start=45)