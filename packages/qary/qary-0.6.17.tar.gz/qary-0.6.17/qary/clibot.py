#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         bot = qary.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!

```bash
$ bot -b 'pattern,parul' -vv -p --num_top_replies=1
YOU: Hi
bot: Hello!
YOU: Looking good!
```
"""
try:
    from collections.abc import Mapping
except ImportError:  # python <3.7
    from collections import Mapping
import importlib
import json
import logging
import os
import sys
import yaml

import numpy as np
import pandas as pd

from qary import constants
from qary.skills.base import normalize_replies

__author__ = "see AUTHORS.md and README.md: Travis, Nima, Erturgrul, Aliya, Xavier, Maria, Hobson, ..."
__copyright__ = "Hobson Lane"
__license__ = "The Hippocratic License (MIT + *Do No Harm*, see LICENSE.txt)"


log = logging.getLogger(__name__)

log.info(f'sys.path: {sys.path}')
log.info(f'constants: {dir(constants)}')
log.info(f'BASE_DIR: {constants.BASE_DIR}')
log.info(f'SRC_DIR: {constants.SRC_DIR}')
log.info(f'sys.path (after append): {sys.path}')
from qary.scores.quality_score import QualityScore  # noqa

BOT = None


class CLIBot:
    """ Conversation manager intended to interact with the user on the command line, but can be used by other plugins/

    >>> CLIBot(skill_module_names='parul,pattern'.split(','), num_top_replies=1).reply('Hi')[1]
    'Hello!'
    """

    def __init__(
            self,
            skill_module_names=constants.DEFAULT_BOTS,
            num_top_replies=None,
            **quality_kwargs):
        self.skill_inits = []
        self.skills = []
        if isinstance(skill_module_names, str):
            skill_module_names = [name.strip().lower() for name in skill_module_names.split(',')]
        self.skill_module_names = skill_module_names
        if not isinstance(self.skill_module_names, Mapping):
            self.skill_module_kwargs = dict(zip(self.skill_module_names, [{}] * len(self.skill_module_names)))
        log.info(f'CLIBot(skill_module_names={self.skill_module_names}')
        log.info(f'CLIBot(skill_module_kwargs={self.skill_module_kwargs}')
        for module_name, module_kwargs in self.skill_module_kwargs.items():
            module_kwargs = {} if module_kwargs is None else dict(module_kwargs)
            self.add_skill(module_name=module_name, **module_kwargs)
        self.num_top_replies = constants.DEFAULT_CONFIG['num_top_replies'] if num_top_replies is None else min(
            max(int(num_top_replies), 1), 10000)
        self.repliers = [obj.reply if hasattr(obj, 'reply') else obj for obj in self.skills if obj is not None]
        log.debug(f'Loaded skills: {self.skills}')
        self.quality_score = QualityScore(**quality_kwargs)

    def add_skill(self, module_name, **module_kwargs):
        log.info(f'Adding module named skills.{module_name}')
        self.skill_inits.append(dict(skill_name=module_kwargs))
        skill_module = importlib.import_module(f'qary.skills.{module_name}')
        new_skill_objs = []
        if skill_module.__class__.__name__ == 'module':
            module_vars = tuple(vars(skill_module).items())
            for skill_class in (c for n, c in module_vars if n.endswith('Skill') and callable(getattr(c, 'reply', None))):
                log.info(f'Adding a Skill class {skill_class} from module {skill_module}...')
                new_skill_objs.append(skill_class(**module_kwargs))
        elif skill_module.__class__.__name__.endswith('Skill'):
            skill_class = skill_module
            skill_module = skill_class.__module__
            skill_kwargs = module_kwargs
            log.warning(f"TODO: test import of specific bot classes like "
                        f'"qary.skills.{skill_class.__module__}.{skill_class.__class__}"')
            new_skill_objs.append(skill_class(**skill_kwargs))
        self.skills.extend(new_skill_objs)
        return new_skill_objs

    def log_reply(self, history_path=constants.HISTORY_PATH, *args, **kwargs):
        if str(history_path).lower().endswith('.json'):
            history = []
            try:
                with open(history_path, 'r') as f:
                    history = json.load(f)
            except IOError as e:
                log.error(str(e))
                with open(history_path, 'w') as f:
                    f.write('[]')
            except json.JSONDecodeError as e:
                log.error(str(e))
                log.info(f"Saving history.json contents to {history_path}.swp before overwriting")
                with open(history_path, 'r') as f:
                    data = f.read()
                with open(f'{history_path}.swp', 'w') as f:
                    f.write(data)
            history.append(kwargs)
            with open(history_path, 'w') as f:
                json.dump(history, f)
        else:
            history = [kwargs]
            with open(history_path, 'a') as f:
                yaml.dump(history, f)

    def reply(self, statement='', context=None):
        ''' Collect replies from from loaded skills and return best reply (str). '''
        log.info(f'statement={statement}')
        replies = []
        # Collect replies from each bot.
        for skill in self.skills:
            bot_replies = []
            log.info(f'Running {skill.__class__}.reply() ')
            # FIXME: create set_context() method on those skills that need it and do away with context try/except
            try:
                bot_replies = skill.reply(statement, context=context)
                log.debug(f"{skill.__class__}.reply(): {bot_replies}")
            except TypeError as e:
                log.warning(
                    f"TypeError: {skill.__class__}.reply({statement}) probably got an unexpected keyword argument 'context': {e}")
                bot_replies = skill.reply(statement)
            except Exception as e:
                log.error(
                    f'Error trying to run {skill.__class__}.reply("{statement}", context={context})')
                log.error(str(e))
                if constants.args.debug:
                    raise e
            bot_replies = normalize_replies(bot_replies)
            replies.extend(bot_replies)

        # Weighted random selection of reply from those with top n confidence scores
        log.info(f"{len(replies)} replies from {len(self.skills)} skills:")
        log.info(repr(replies))
        if len(replies):
            log.info(f'Found {len(replies)} suitable replies, limiting to {self.num_top_replies}...')
            replies = self.quality_score.update_replies(replies, statement)
            replies = sorted(replies, reverse=True)[:self.num_top_replies]

            conf_sums = np.cumsum(list(r[0] for r in replies))
            roll = np.random.rand() * conf_sums[-1]

            reply = False
            for i, threshold in enumerate(conf_sums):
                if roll < threshold:
                    reply = replies[i]
            if reply is False:
                log.error(f"Error rolling dice to select reply."
                          f"\n    roll:{roll}"
                          f"\n    threshold: {threshold}"
                          f"\n    conf_sums: {conf_sums}\n"
                          f"\n    replies: {pd.DataFrame(replies)}")
                reply = replies[0]
        else:
            log.warning(f"No replies ({replies}) were returned by {self.skills}!!")
            reply = "Sorry, something went wrong. None of my skills had anything to say..."
        self.log_reply(**dict(
            statement=statement,
            reply_text=reply.text,
            conversation_manager=str(self.__module__),
            reply_confidence=reply.confidence if reply.confidence is None else float(reply.confidence),
            skills=[str(s.__module__) for s in self.skills])
        )
        return reply


def run_skill():
    global BOT
    if BOT is None:
        BOT = CLIBot(
            skill_module_names=constants.args.bots,
            num_top_replies=constants.args.num_top_replies,
            semantic=constants.args.semantic,
            sentiment=constants.args.sentiment,
            spell=constants.args.spell)
    if constants.args.persist:
        print('Type "quit" or "exit" to end the conversation...')

    log.debug(f'FINAL PROCESSED ARGS AFTER INSTANTIATING CLIBot:\n{vars(constants.args)}\n')
    return BOT


def cli(args,
        exit_commands='exit quit bye goodbye cya hasta seeya'.split(),
        max_turns=constants.MAX_TURNS):
    global BOT
    BOT = run_skill() if BOT is None else BOT
    state = {}
    user_statement = ' '.join(args.words).strip() or None
    if user_statement is not None:
        max_turns = 0
    history = [dict(user=user_statement, bot=None, **state)]
    log.warning(f'user_cli_statement: `{user_statement}`')
    while True:
        if user_statement and user_statement.lower().strip() in exit_commands:
            log.warning(f'exit command received: `{user_statement}`')
            break
        log.warning(f"Computing a reply to {user_statement}...")
        bot_statement_tuple = BOT.reply(user_statement)
        bot_statement = bot_statement_tuple[1]
        history[-1]['bot'] = bot_statement
        if bot_statement is not None:
            print(f'{args.nickname}: ')
            print(bot_statement)
        if max_turns > 0 or not user_statement:
            user_statement = input("YOU: ")
            history.append(dict(user=user_statement, skill=None, **state))
    history = pd.DataFrame(history)
    history.to_csv(os.path.join(constants.DATA_DIR, 'history.csv'))
    return history


def main():
    global BOT
    BOT = run_skill() if BOT is None else BOT
    # args = constants.parse_argv(argv=sys.argv)
    statements = cli(constants.args)
    if constants.args.loglevel >= 50:
        return
    return statements


if __name__ == "__main__":
    statements = main()
