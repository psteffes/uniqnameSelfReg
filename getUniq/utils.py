#import logging

#logger = logging.getLogger(__name__)

# Validate an entry is eligible based on the umichGetUniqname ObjectClass
def getuniq_eligible(entry):

    try:
        eligible = False
        if entry['umichGetUniqStatus'] == 'STARTED' and entry['umichGetUniqEntitlingRoles'] != '':
            eligible = True

    except Exception as e:
        pass

    return eligible
