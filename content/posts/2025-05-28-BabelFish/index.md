---
title: "BabelFish: Building a Slang-Aware NLP Interface from Backend to Frontend"
author: "Ferdinand Theil"
# authorAvatarPath: "/avatar.jpeg"
date: 2025-05-28T11:52:47+01:00
summary: "A technical write-up on building BabelFish, a platform for analyzing word embeddings with a focus on Twitch-style slang"
description: ""
toc: true
readTime: false
autonumber: false
math: false
tags: []
showTags: false
hideBackToTop: false
# fediverse: "@instance.url"
draft: false
---

This is a write-up of my project *BabelFish*, which I’ve been working on intermittently since March.
It’s not finished yet, but I figured now is a good time to document my progress and the issues I’ve run into during development.

Currently, BabelFish is a website and API that lets you analyze words, sentences, and word embeddings, with a particular focus on Twitch-style slang.
I’m currently overhauling the data collection pipelines and building new models for Twitch and Bluesky.
A stretch goal would be to incorporate time into the analysis—showing trends in sentiment over time across different platforms.

## Getting Started

I had previously trained some machine learning models based on a paper called *FeelsGoodMan: Inferring Semantics of Twitch Neologisms*[^feelsgoodman].
The goal was to build an interface that let my friends play with the models I’d built.
I wanted to make this because I struggled to share and explain what the models did, since they only ran locally on my laptop.

As a backend programmer, this was a great opportunity to build a frontend and try my hand at a more full-stack project.

After some research and conversations with friends who knew frontend tech, I settled on the following stack:

* Svelte
* FastAPI

Because the models were built in Python using libraries like Gensim[^gensim] and Scikit-learn[^scikit], I needed the API to be in Python.
I chose not to build everything in Python, though—I wanted to learn new technologies, and I’d already made things in Flask before.

Also, since frontend work mostly happens in JavaScript, I figured anything I learned from one JS framework would likely transfer to others.
Honestly, I don’t have a strong reason for picking Svelte over something else—people just seemed to like it.

## Plumbing Up My Backend

FastAPI turned out to be both a great and terrible choice for this project.
Building the initial API was fast and easy. Most of my time went into designing the API endpoints rather than implementing them.
I ended up with a design that was at least consistent, though getting response type-checking to work with Pydantic[^pydantic] was a huge headache.

One of Python’s longstanding issues is distribution, so I try to build all my software as Python packages.
This wasn’t straightforward with FastAPI.

To summarize: I found [this discussion](https://github.com/fastapi/fastapi-cli/discussions/167) asking for the exact feature I needed.
After digging through the code, I found the relevant section:

{{<highlight python "linenos=inline, lineNoStart=18">}}
def get_default_path() -> Path:
    potential_paths = (
        "main.py",
        "app.py",
        "api.py",
        "app/main.py",
        "app/app.py",
        "app/api.py",
    )

    for full_path in potential_paths:
        path = Path(full_path)
        if path.is_file():
            return path

    raise FastAPICLIException(
        "Could not find a default file to run, please provide an explicit path"
    )

{{</highlight>}} [^fastapi-cli-ref]

This means I can’t run my code based on the module name—it expects a path instead (even though Uvicorn supports modules just fine—FastAPI CLI just doesn’t implement it).

Remembering that Uvicorn had support for this, I checked whether I could call it directly.
I was hopeful—there was a [closed issue](https://github.com/encode/uvicorn/issues/2554) asking for exactly what I wanted.
I tried it, but… nothing.

`self.should_reload` was always `False`, with no way to override it

{{<highlight python "linenos=inline, lineNoStart=281">}}
        if (reload_dirs or reload_includes or reload_excludes) and not self.should_reload:
            logger.warning(
                "Current configuration will not reload as not all conditions are met, " "please refer to documentation."
            )
{{</highlight>}} [^uvicorn-ref]

For some reason, FastAPI tries to infer the module structure from a file path instead of just letting you provide a Python package name.
(Uvicorn does support this—it can use the module name to run your code!)

Uvicorn allows you to run code via the module name or object,
but it only automatically reloads if it knows the path to watch—something it can’t infer if you use a module name. (Even though you can explicitly provide {{<hl python>}}reload_paths{{</hl>}}...)

In the end, I gave up on automatic reloads.

I'm sure the rest of the project will go much better.
Now it’s time to set up a Svelte project and start accessing my cool new API.

Hey, wait...

## What the Hell is CORS?

CORS, or Cross-Origin Resource Sharing, is a security layer that lets servers specify which origins (i.e., domains or servers) are allowed to access their resources.
It exists to prevent attacks where malicious JavaScript tries to fetch and load data from a server the attacker controls. [^cors]

This is called a **Cross-Origin Request**, which happens to be *exactly* what I’m trying to do.

{{<figure 
  src="cors_cross_origin.png"
  alt="A screenshot of firefox console showing a Cross-Origin-Request Error"
  caption="Cross-Origin-Request Error"
>}}

After spending way too long messing around with `Access-Control-Allow-Origin` and `Origin` headers, I reached out to a friend to see how they deal with CORS.
They pointed out that this is actually a really awful way of accessing the data and it's far better to route the request through Vite using a proxy.

{{<highlight typescript>}}
const upstream = {
	target: 'http://localhost:8000/',
	secure: true,
	changeOrigin: false,
	logLevel: 'info',
  };

export default defineConfig({
	server: {
		allowedHosts: true,
		proxy: {
			'/api': upstream,
		},
	},
	plugins: [sveltekit()]
});
{{</highlight>}}

It's that simple. Now all requests that fetch `/api` will be forwarded to my upstream API and I managed to sidestep the problem this time.

## Hey Svelte is pretty fun

Now that I've gone through the awful process of setting up these frameworks, programming in svelte is actually pretty nice. 
I used RealTime Colors[^realtimecolors] to pick out some themes and spent an afternoon going through different blogs and ~stealing~ borrowing some design ideas.
This included using the {{<hl css>}}@media (prefers-color-scheme){{</hl>}} to setup automatic dark/light theming, along with some scaling options using {{<hl css>}}@media (min-width){{</hl>}}.

After spending some time learning some basic svelte via their tutorials, I was able to start winging it and setting up an interactive frontend. 
It's surprisingly easy and intuitive!

For something like this a search box, you could use something like this.
{{<highlight svelte>}}
<section class="sentiment-search">
    <h4>Sentiment analysis</h4>
    <!-- <textarea bind:value={query} placeholder="Enter text here..."></textarea> -->
    <input bind:value={query} placeholder="Enter text here..." />
    <button on:click={fetchResults}>Analyze Sentiment</button>

    <progress value={compound_score} max=2></progress>
    <p>Sentiment Score: {compound_score.toFixed(2)}</p>
    <div class="response-box">
        <p>{response_text}</p>
    </div>
</section>
{{</highlight>}}

{{<highlight typescript>}}
$: if (query) {
    clearTimeout(timeout); // debounce
    timeout = setTimeout(fetchResults, 300);
} else {

    results = [];
}
{{</highlight>}}

Svelte is fun.

All in all, This process come together pretty well over the course of a few days. 
I've added a bunch of fun new features such as an interesting error page and some new visualisations. 
At the moment I'm still working on building a new dataset with modern data. Maybe I'll come back and update this blog post!


[^feelsgoodman]: https://arxiv.org/abs/2108.08411
[^gensim]: https://radimrehurek.com/gensim/
[^scikit]: https://scikit-learn.org/
[^pydantic]: https://docs.pydantic.dev/latest/
[^fastapi-cli-ref]: https://github.com/fastapi/fastapi-cli/blob/9a4741816dc288bbd931e693166117d98ee14dea/src/fastapi_cli/discover.py#L18
[^uvicorn-ref]: https://github.com/encode/uvicorn/blob/90f43699c79bcd2b0676186fc6d3b9baf679d3c8/uvicorn/config.py#L281-L284
[^cors]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
[^realtimecolors]: https://www.realtimecolors.com/
