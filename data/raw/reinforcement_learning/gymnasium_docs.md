---
source_id: gymnasium_docs
title: "An API standard for reinforcement learning with a diverse collection of reference environments"
domain: reinforcement_learning
topic: environments
url: https://gymnasium.farama.org/
license: MIT
language: en
source_type: official_documentation
---
## An API standard for reinforcement learning with a diverse collection of reference environments

Gymnasium is a maintained fork of OpenAI’s Gym library. The Gymnasium interface is simple, pythonic, and capable of representing general RL problems, and has a migration guide for old Gym environments:

```

import

gymnasium

as

gym

# Initialise the environment

env

=

gym

.

make

(

"LunarLander-v3"

,

render_mode

=

"human"

)

# Reset the environment to generate the first observation

observation

,

info

=

env

.

reset

(

seed

=

42

)

for

_

in

range

(

1000

):

# this is where you would insert your policy

action

=

env

.

action_space

.

sample

()

# step (transition) through the environment with the action

# receiving the next observation, reward and if the episode has terminated or truncated

observation

,

reward

,

terminated

,

truncated

,

info

=

env

.

step

(

action

)

# If the episode has ended then we can reset to start a new episode

if

terminated

or

truncated

:

observation

,

info

=

env

.

reset

()

env

.

close

()

```
