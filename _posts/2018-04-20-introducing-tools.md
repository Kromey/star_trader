---
title: "Introducing: Tools"
layout: post
category: Devlog
tags: economy simulation bugfix
---
Not much exciting happened this week, not visibly anyway. I refactored some code and redid how a few of the internals calculate their values, none of which should have any impact on the results of the economy simulation.

There is a new feature to announce, however: Tools!

Jobs now have the option of specifying that they require any number of Tools to perform their work. If an Agent lacks the required number of Tools, then they have to place a Bid on the Market asking to buy what they need -- because really a Tool is just another Good, made by and bought from another Agent.

Tools don't quite function like Goods when being used by Agents, however: Rather than being consumed in every round of work, they have a "break chance". For example, in my (super-simplistic) testing economy, Glass Makers require as a Tool a "Blower", which they can buy from the Blower Maker Agents. In their job definition, their Blower is defined to break 10% of the time.

Also unlike other Goods, Agents don't just try to fill their inventories with Tools. Rather, they just try to keep the exact number on hand they need to do their work. This means that a tool breaking at the beginning of the Production phase can severely short-chance an Agent in terms of how much that Agent can sell in the next Trade phase; on the other hand, an Agent whose Tool breaks on the last cycle they can do that turn anyway isn't too bad off. However, because Orders are placed *before* Production happens that turn, but the Trade phase happens *after* that, in both cases Agents cannot perform *any* work on the next turn!

This might be too steep a penalty, but then again the goal of this simulation isn't to provide a fair playing field for the Agents. Instead, its purpose is simply to provide a model that results in fluctuating "market prices" that should response to the PC's buying and selling (if the PC has the resources to buy/sell at volumes the market would even really care about, that is). So if a few extra Agents go bankrupt because of the harsh penalties from Tools breaking on them, that may not really even matter in the long run, especially given that in the game Markets are going to each have *tons* of Agents...
