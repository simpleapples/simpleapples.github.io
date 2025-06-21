---
date: "2018-03-14T21:00:00+00:00"
title: "The Person Who Loves You the Most Will Help You Understand Blockchain Without Breaking a Sweat"
categories:
  - Python
---

![](/images/20180314_01.png)

Blockchain is a hot topic these days. You can hear people talking about blockchain or trading cryptocurrencies in any office building elevator. Through this article, I hope to give you a comprehensive understanding of the concept of blockchain. After grasping the concept, **the next article will demonstrate how to implement a blockchain network with approximately 300 lines of Python code.**

# Blocks and Chains

A block is, well, a block (what else could it be?), and when you link these blocks together one by one, like a chain, it’s called a blockchain (hold your thoughts, keep reading).

![Blocks and Blockchain](/images/20180314_02.jpg)

These are chains, often used to lock up electric scooters downstairs. But if you look closely, doesn’t this chain resemble something? ⛓

![Deoxyribonucleic Acid](/images/20180314_03.gif)

Smart! Your high school biology teacher is smiling at you! This is the legendary deoxyribonucleic acid (DNA), which also has a chain structure and **carries genetic information**. In blockchain, the "block" is akin to the deoxyribonucleotide in a DNA molecule, and the "chain" is similar to the chain structure of a DNA molecule.

The difference in value between DNA and a chain lies in DNA carrying a lot of genetic **information**, whereas a chain carries nothing. For blockchain, carrying information is also a crucial feature (without carrying information, it wouldn’t even be useful for locking up scooters).

When a blockchain carries financial information, it becomes something particularly powerful—a ledger (we gave it a Gen Z name—Bitcoin).

# Peer-to-Peer

To sound more professional, let’s refer to the paper by Bitcoin’s creator, Satoshi Nakamoto, [“Bitcoin: A Peer-to-Peer Electronic Cash System”](https://bitcoin.org/bitcoin.pdf). From the title of this paper, we can see that blockchain is based on **Peer-to-Peer**. Let’s explore what Peer-to-Peer means.

Peer-to-Peer, abbreviated as P2P (not the internet lending P2P), is a type of peer-to-peer network. See the diagram (I’m not sure how else to explain it).

![P2P Network](/images/20180314_04.jpg)

In the diagram, each square head is a Peer (node). Notice that these square heads have something in common—they are all identical (not only do they look the same, but each head is connected to every other head). This is the biggest feature of a P2P network—**decentralization**. In a P2P network, there is no central node; all nodes are equal, and any node can communicate with any other node, with no single node having the final say.

# Consensus Mechanism

You, your good friend Lao Wang, and a girl you both like, Ah Yuan (yes, the round and chubby Yuan), form a three-node P2P network. According to the P2P network definition, none of you can have the final say. One day, on Ah Yuan’s birthday, both you and Lao Wang give her a big cake. The question arises: which cake should Ah Yuan eat first?

Since no one can have the final say, and you can’t have a duel with Lao Wang (if computers did this, humanity might be doomed), a civilized way to decide is needed—negotiation. And negotiation requires rules, known as the **consensus mechanism**.

![](/images/20180314_05.png)

# Proof-of-work

There are many types of consensus mechanisms in blockchain, and Proof-of-work (POW) is one of them. Proof-of-work is somewhat like a martial arts contest. Both you and Lao Wang are good to Ah Yuan, and she finds it hard to decide whose cake to eat first. So, she invites two equally skilled martial arts experts and lets you and Lao Wang each spar with an expert. Whoever wins against the expert gets their cake eaten first. If both of you win, the first to win counts.

![](/images/20180314_06.jpg)

# Putting It All Together

Having understood the concepts of POW, consensus mechanism, P2P, blocks, and chains, we can piece them together to see what happens.

![The Birth of Blockchain!](/images/20180314_07.jpeg)

We assign each node in the P2P network a chain, making all chains in the network equal. Then, we add a block with information to one of these chains. The P2P network synchronizes this block to all chains, meaning this information is stored in all nodes.

To sum up the above in one sentence (which sounds impressive):

**Blockchain is an intelligent peer-to-peer network that uses a distributed database to identify, disseminate, and record information, also known as the Internet of Value.**

Do you have a better understanding of blockchain now?