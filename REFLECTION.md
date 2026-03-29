1. How far did the agent get?
Copilot built files, the app launched, and the login screen appeared. But when the AI review came back, every single one of the acceptance criteria was marked as failing. The app looked complete on the surface but was missing most of what the spec actually asked for. The security was also weaker than specified.
2. Where did I intervene?
I intervened a few times. One problem was when Copilot had actually put the files it created extra folders I wasn't expecting and I had to hunt around to find the right place to run the app. A more detailed spec probably would have helped with the folder issue, but the python3 thing is the kind of environment detail that's hard to predict ahead of time.
3. How useful was the AI review?
More useful than I expected. It caught the password security issue, which was a real problem I wouldn't have noticed just by running the app and clicking around. The other failures it flagged were also real. The main weakness was that it listed everything at the same level, a minor naming issue got the same treatment as a broken security feature, which made it hard to know what to fix first.
4. What I'd change about the spec
I'd be more specific about the folder structure, just saying "all files should be in the root of the project" would have saved a lot of confusion. I'd also make the acceptance criteria more concrete and testable rather than describing general behaviors. The more precise the spec, the less room the agent has to make its own decisions and get things wrong.
5. When would I use this workflow?
It works well when you have a clear idea of what you want and you can write it down before you start. The spec forces you to think through the details upfront, which is genuinely valuable. But if you're still figuring out what you want as you go, writing a full spec first feels like overkill, regular back-and-forth is faster and more flexible in that case. 
