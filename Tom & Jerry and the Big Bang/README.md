*Contributers: Renuka Sahani and Suraj Desai*

# Tom & Jerry and the Big Bang

> Setup for a project/competition amongst students to train a winning Reinforcement Learning agent for the classic game Bomberman.

## Agents

* [Spike] agent with full sight but convolution layers in the network
* [Tom] reinforcement learning agent
* [Jerry] imitates the rule based agent

## Tips & Tricks

Setup environment:

```python
pip install -r requirements.txt
```

Train agent:

```python
python -m main play --agents Spike --train 1 --n-round 2500 --no-gui
```

Play agent:

```python
python -m main play --agents Spike
```

To run a demo of our agent **Tom** download the repository and run ``python main.py play --agents Tom rule_based_agent rule_based_agent rule_based_agent``.

Our Github Repository Link: https://github.com/Renuka-Sahani/Tom---Jerry-and-the-Big-Bang.git