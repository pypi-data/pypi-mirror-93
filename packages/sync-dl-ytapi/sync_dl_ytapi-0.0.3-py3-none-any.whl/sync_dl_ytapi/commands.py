


import shelve

import sync_dl.config as cfg

from sync_dl_ytapi.helpers import getPlId,pushOrderMoves
from sync_dl_ytapi.ytApiWrappers import getYTResource,getItemIds,moveSong
    
#def checkOptDepend():
#    '''Ensures optional dependancies are installed'''
#    while True:
#        # Test importing Encryption/dencryption obfuscated code (needed to decrypt oauth api client secrets)
#        try:
#            from sync_dl.yt_api.encrypted import getDecryptedProxy, encryptFileProxy, encryptBytesProxy
#        except:
#            cfg.logger.error("Unable to Load Obfuscated Code on This Platform (required to use youtube api)")
#            return False
#
#        # try to import google auth libraries, if unable pip install them
#        try:
#            print("test1")
#            import google.auth
#            print("test2")
#            import google_auth_oauthlib
#            print("test3")
#            import google_api_python_client
#            print("test4")
#            import cryptography
#
#            #from sync_dl.yt_api.helpers import getPlId,pushOrderMoves
#            #from sync_dl.yt_api.ytApiWrappers import getYTResource,getItemIds,moveSong
#            break
#        except Exception as e:
#            print(e)
#            answer = input("Missing Optional Dependancies For This Command.\nWould You Like to Install Them? (y/n): ").lower()
#            if answer!='y':
#                return False
#
#            import subprocess
#            subprocess.call(["pip",'install','google-auth','google-auth-oauthlib','google-api-python-client','cryptography'])
#
#    return True




def pushLocalOrder(plPath):
    cfg.logger.info("Pushing Local Order to Remote...")

    youtube = getYTResource()
    
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

