


import shelve

import sync_dl.config as cfg

from sync_dl_ytapi.helpers import getPlId,pushOrderMoves
from sync_dl_ytapi.ytApiWrappers import getItemIds,moveSong

from sync_dl_ytapi.credentials import credentialManager, credTask
    
def pushLocalOrder(plPath):
    cfg.logger.info("Pushing Local Order to Remote...")


    youtube = credentialManager(credTask.getYTResource)
    
    with shelve.open(f"{plPath}/{cfg.metaDataName}", 'c',writeback=True) as metaData:
        url = metaData["url"]
        localIds = metaData["ids"]

    plId = getPlId(url)

    remoteIdPairs = getItemIds(youtube,plId)

    remoteIds,remoteItemIds = zip(*remoteIdPairs)

    cfg.logger.debug(f'Order Before Push: \n'+'\n'.join( [f'{i}: {str(remoteId)}' for i,remoteId in enumerate(remoteIds) ] ))

    moves = pushOrderMoves(remoteIds,remoteItemIds,localIds)



    for move in moves:
        newIndex, songId,itemId = move

        moveSong(youtube,plId,songId,itemId,newIndex)

def logout():
    credentialManager(credTask.logout)
    