#import logging

#logger = logging.getLogger(__name__)

# Validate an entry is eligible based on the umichGetUniqname ObjectClass
def getuniq_eligible(entry):

    try:
        eligible = False
        print('umichgetuniqstatus={}'.format(entry['umichGetUniqStatus']))
        if entry['umichGetUniqStatus'][0] == 'ELIGIBLE' and entry['umichGetUniqEntitlingRoles'][0] != '':
            eligible = True

    except Exception as e:
        pass

    return eligible
