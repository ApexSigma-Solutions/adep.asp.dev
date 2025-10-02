---
title: I built a local coding AI for VS Code and it’s shockingly good
source: https://www.makeuseof.com/local-coding-ai-vs-code-shockingly-good/
author:
  - "[[Yadullah Abidi]]"
published: 2025-09-25
created: 2025-09-27
description: There's a better way to code with AI than those pesky online subscriptions.
tags:
  - WebClip
status: "[processed][unprocessed]"
---
# I built a local coding AI for VS Code and it’s shockingly good

**Author:** Yadullah Abidi
**Published:** 2025-09-25
**Source:** [I built a local coding AI for VS Code and it’s shockingly good](https://www.makeuseof.com/local-coding-ai-vs-code-shockingly-good/)
**Status:** #unprocessed
**tags:** 
 
## Content

AI models have made coding a far easier job, especially for beginners. Previously, you might have had to spend days or even weeks getting to grips with a programming language, let alone write functional code. Now, an entirely functional app is a single prompt away.

However, most online coding assistants are locked behind subscriptions—accessible only for a short time before you exhaust your limits. There are [free AI tools that can save you money on subscriptions](https://www.makeuseof.com/free-ai-tools-save-subscription-money/), but when it comes to coding, nothing beats a local AI coding assistant.

## Local beats the cloud for coding AI

### No latency, no limits, just pure coding speed

There are obvious benefits to using a local coding AI as compared to online options like ChatGPT or GitHub's Copilot. For starters, you don't have to pay a single cent in subscription costs. Pretty much every AI tool indeed gives some sort of free access to its users, but if you're serious about coding, you'll exhaust those free limits rather quickly.

![Local AI model running in VS Code. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-local-ai.jpg?q=49&fit=crop&w=500&dpr=2)

Local AI model running in VS Code.

In most cases, the free plan also sticks you with an inferior model compared to what a paid subscription would get. So not only is the amount of help you need limited, but the quality isn't as good as it can be, either.

An experienced programmer who knows what they're working with can perhaps get away with this, assuming they only use the AI for figuring out parts of their code. However, if you're learning how to code or building an app from scratch, you're going to need the best help you can get it, and a lot of it.

A local AI is also great for privacy. Online AI tools will almost always use your code to train their models, which is the reason why most of them are banned in professional environments. On the other hand, a local AI runs on your machine, is available around the clock, and your code or queries aren't sent to a server for processing.

![Local AI model running on VS Code. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-local-ai-image.jpg?q=49&fit=crop&w=500&dpr=2)

Credit: Yadullah Abidi / MakeUseOf

As you'll soon discover, they also aren't very hard to set up. The only catch is that you're limited by your hardware. Now you don't need top-of-the-line rigs with GPUs that consume more power than your house to run most open-source models available on the internet for free, but having good hardware does help.

Essentially, the higher the number of parameters for the model, the more RAM, storage, and VRAM you need. There are lower fidelity models that can run on weaker hardware as well, but the response and code quality might not be as good as you'd like.

## How I built my own AI coding sidekick

### You don’t need a data center to make this work

The first step of the process is to get an AI model running locally on your system. There are [plenty of apps to enjoy the benefits of a local LLM](https://www.makeuseof.com/best-apps-to-run-llm-locally/), such as [Ollama](https://ollama.com/) and [LM Studio](https://lmstudio.ai/). I recommend using LM Studio as it has a graphic interface that you can use to search and download models, configure them, and even chat with a model with support for file uploads.

Next is the AI model you'll be running. LM Studio lets you download open-source AI models from HuggingFace. You can download models like the DeepSeek R1, Qwen, gpt-oss, and more. I use DeepSeek, but I recommend you experiment with different models based on your specific requirements and PC hardware.

Installing and setting up LM Studio with an AI model is a rather easy process. Download LM Studio from the [official website](https://lmstudio.ai/) and run the installer. Follow these steps after running LM Studio for the first time:

1. You may be prompted to go through a setup wizard. This can be skipped by clicking the grey **Skip** button on the top-right.
2. Once the main interface loads up, LM Studio should automatically start downloading any drivers or updates it needs. Wait for these to finish before proceeding.
3. Click the magnifying glass icon to open the **Discover** tab and search for the model you want to download. Click the green **Download** button at the bottom left to proceed.
4. Once the model is done downloading, head over to the **Chat** section and click the dropdown at the top of the display to load your downloaded model.

- ![LM Studio asset download screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-1.jpg?q=49&fit=contain&w=360&h=202&dpr=2)
	LM Studio asset download screen.

- ![LM Studio asset download screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-1.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio model download screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-2.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio model selection screen.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-3.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio local chat screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-4.jpg?q=49&fit=crop&w=145&h=80&dpr=2)

- ![LM Studio asset download screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-1.jpg?q=49&fit=contain&w=2560&h=1440&dpr=2)
	LM Studio asset download screen.
- ![LM Studio model download screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-2.jpg?q=49&fit=contain&w=2560&h=1440&dpr=2)
	LM Studio model download screen.
- ![LM Studio model selection screen.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-3.jpg?q=49&fit=contain&w=2560&h=1440&dpr=2)
	LM Studio model selection screen.
- ![LM Studio local chat screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-4.jpg?q=49&fit=contain&w=2560&h=1440&dpr=2)
	LM Studio local chat screen.

- ![LM Studio asset download screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-1.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio model download screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-2.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio model selection screen.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-3.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio local chat screen. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-setup-4.jpg?q=49&fit=crop&w=145&h=80&dpr=2)

At this point, you should be able to chat with your model. If everything works as expected, you can now start a local server for the model to make it accessible to other programs on your PC.

1. Head over to the **Developer** section. Make sure your downloaded model is loaded. You'll see a green **READY** tab if it is. If it isn't, select the model from the drop-down menu at the top.
2. Head over to the **Load** tab on the right and set a context length. I use 15,000, but your number can vary based on total available memory and requirements. Reload the model to apply changes.
3. Enable the **Status** slider at the top to start the local server.

- ![LM Studio server context length setting page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-2.jpg?q=49&fit=contain&w=360&h=202&dpr=2)
	LM Studio server context length setting page.

- ![LM Studio server page.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-1.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio server context length setting page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-2.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio server page with active server. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-3.jpg?q=49&fit=crop&w=145&h=80&dpr=2)

- ![LM Studio server page.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-1.jpg?q=49&fit=contain&w=2560&h=1440&dpr=2)
	LM Studio server page.
- ![LM Studio server context length setting page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-2.jpg?q=49&fit=contain&w=2560&h=1440&dpr=2)
	LM Studio server context length setting page.
- ![LM Studio server page with active server. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-3.jpg?q=49&fit=contain&w=2560&h=1440&dpr=2)
	LM Studio server page with active server.

- ![LM Studio server page.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-1.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio server context length setting page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-2.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![LM Studio server page with active server. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/lm-studio-server-3.jpg?q=49&fit=crop&w=145&h=80&dpr=2)

If everything goes well, you're now hosting an accessible instance of the AI model, which can be used by other applications on your PC as well as devices on your local network.

## AI, meet VS Code

### Feels like Copilot, but it’s 100% yours

Once you've got LM Studio running with your model of choice, it's time to integrate your AI model into VS Code. Follow these steps:

1. Open VS Code and install the Continue extension. You can search for it in the Extension Marketplace within VS Code.
2. Click the Continue icon in the VS Code sidebar and click the settings gear icon for the extension.
3. Head over to the **Models** settings and click the plus icon in the top right to add a model.
4. Select LM Studio from the **Provider** drop-down. The **Model** drop-down should be set to **Autodetect**. Click **Connect** to proceed.
5. You'll be redirected to the **Models** settings page. Under the **Chat** model drop-down, you should see your downloaded model.

- ![Extension Marketplace in VS Code with Continue page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-1.jpg?q=49&fit=contain&w=360&h=202&dpr=2)
	Extension Marketplace in VS Code with Continue page.

- ![Extension Marketplace in VS Code with Continue page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-1.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![Continue extension running in VS Code. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-2.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![Continue extension model settings.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-3.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![Continue extension new model page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-4.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![Continue extension new model page showing local AI. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-5.jpg?q=49&fit=crop&w=145&h=80&dpr=2)

- ![Extension Marketplace in VS Code with Continue page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-1.jpg?q=49&fit=contain&w=2880&h=1704&dpr=2)
	Extension Marketplace in VS Code with Continue page.
- ![Continue extension running in VS Code. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-2.jpg?q=49&fit=contain&w=2880&h=1704&dpr=2)
	Continue extension running in VS Code.
- ![Continue extension model settings.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-3.jpg?q=49&fit=contain&w=2880&h=1704&dpr=2)
	Continue extension model settings.
- ![Continue extension new model page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-4.jpg?q=49&fit=contain&w=2880&h=1704&dpr=2)
	Continue extension new model page.
- ![Continue extension new model page showing local AI. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-5.jpg?q=49&fit=contain&w=2880&h=1704&dpr=2)
	Continue extension new model page showing local AI.

- ![Extension Marketplace in VS Code with Continue page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-1.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![Continue extension running in VS Code. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-2.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![Continue extension model settings.](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-3.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![Continue extension new model page. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-4.jpg?q=49&fit=crop&w=145&h=80&dpr=2)
- ![Continue extension new model page showing local AI. ](https://static0.makeuseofimages.com/wordpress/wp-content/uploads/wm/2025/09/vs-code-continue-5.jpg?q=49&fit=crop&w=145&h=80&dpr=2)

And that's it. You should now be able to access your downloaded model from within VS Code. [Every VS Code user needs to watch out for malicious extensions](https://www.makeuseof.com/vscode-malicious-extensions/), so check before downloading to ensure you're getting the right one. Continue has various modes that let you talk to the AI model in varying contexts and applications, so feel free to play around with it to find what works best for you. In most cases, using the **Agent** mode will get you the best results. There's a handy tutorial built into the extension that'll help you get to grips with all the features.

Performance largely depends on the AI model that you choose and your PC's hardware. On my HP Omen Transcend 14 with a Core Ultra 7 155H, 16GB RAM, and an RTX 4060, most queries take less than 30 seconds to process. For larger queries or files, the response time can go into minutes. The generated code has been quite accurate, and I can mostly get it to work within a couple of prompts.

	Whether this performance is better than an online coding tool worth $20 a month or more is up to you to decide. In my case, a lo cal coding AI with reasonably accurate code generation and privacy protection is the most important factor. Being able to make your own local coding AI gives you the freedom to test multiple models to find what works best for you, without ever spending a dime.

## My Notes

*Add your thoughts and connections here*