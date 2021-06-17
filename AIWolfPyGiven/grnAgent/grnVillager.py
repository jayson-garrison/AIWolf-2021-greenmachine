
#!/usr/bin/env python
from __future__ import print_function, division

# This sample script connects to the AIWolf server
# and responds appropriately to all server requests.
# It does not say anything and gives itself as the
# target id for any request, resulting in random actions.

# Additionally, it prints to the standard input all the
# information that it received from the server, which can
# be useful when developing your own client.

import AIWolfPyGiven.aiwolfpy
import AIWolfPyGiven.aiwolfpy.contentbuilder as cb
import logging, json

myname = 'greenmachine'

class grnVillager(object):
    def __init__(self, agent_name):
        # myname
        self.myname = agent_name
        logging.basicConfig(filename=self.myname+".log",
                            level=logging.DEBUG,
                            format='')

    def getName(self):
        logging.debug("# GETNAME")
        return self.myname

    # new game (no return)
    def initialize(self, base_info, diff_data, game_setting):
        logging.debug("# INITIALIZE")
        logging.debug("Game Setting:")
        logging.debug(json.dumps(game_setting, indent=2))
        logging.debug("Base Info:")
        logging.debug(json.dumps(base_info, indent=2))
        logging.debug("Diff Data:")
        logging.debug(diff_data)
        self.base_info = base_info
        self.game_setting = game_setting
        # print(base_info)
        # print(diff_data)

    # new information (no return)
    # add to lists (majority of the work)
    def update(self, base_info, diff_data, request):
        logging.debug("# UPDATE")
        logging.debug("Request:")
        logging.debug(request)
        logging.debug("Base Info:")
        logging.debug(json.dumps(base_info, indent=2))
        logging.debug("Diff Data:")
        logging.debug(diff_data)

        self.base_info = base_info
        # print(base_info)
        # print(diff_data)

    # Start of the day (no return)
    def dayStart(self):
        logging.debug("# DAYSTART")
        return None

    # conversation actions: require a properly formatted
    # protocol string as the return.
    # act based on the lists
    def talk(self):
        logging.debug("# TALK")
        return cb.over()

    # targetted actions: Require the id of the target
    # agent as the return
    # act based on the lists
    def vote(self):
        logging.debug("# VOTE")
        return self.base_info['agentIdx']

    # Finish (no return)
    def finish(self):
        logging.debug("# FINISH")
        return None

agent = grnVillager(myname)

# run
if __name__ == '__main__':
    AIWolfPyGiven.aiwolfpy.connect_parse(agent)




