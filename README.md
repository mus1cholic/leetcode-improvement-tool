# Leetcode Improvement Tool (LIT)

A Leetcode tool to help you ace your next interview!

## About

Have you ever wondered aimlessly on the Leetcode website, trying out random medium questions only for some to be extremely hard and others to be rather easily? Don't you wish for a system to give you questions appropriate for your current leetcode skill range? That's what LIT is for. With LIT, you are able to quantitatively measure your current skill through your "Projected Rating", which is a combination of your current contest rating as well as the difficulty of all your previously solved problems. With this, LIT is then able to recommend you problems that it think will either be "Easy", "Medium", or "Hard". After all, a "Hard" problem for you may not be the same for others.

With LIT's recommendation system, you are able to be ensured that the current problem you are working on will be a difficulty relative to your choosing. Not only that, LIT also breaks down your skillset through a list of pre-determined topics, and can even recommend you questions appropriate for your weakest skillsets!

## Current Features

- Calculates your "Projected Rating" by topic
- Recommends a random problem based on your projected rating or through custom filters
- Easy front-end interaction via Discord

## Planned Features

- Suggests a "weak" problem based on your current weakest topics (current status: planned)
- Determine a way of simulating rating on questions not presented in ratings.txt (current status: on hold)
- Automatic "study group" on Discord server (current status: contingent on the above features)
- Create sessions, solving the problem of same account but taking a break in between (current status: not yet implemented)
- Better Github CI/CD (current status: not yet implemented)
- Better API due to rate-limiting (current status: not yet implemented)

## Credits

This tool uses the question rating system made with https://github.com/zerotrac/leetcode_problem_rating, and also calls Leetcode's APIs through https://github.com/alfaArghya/alfa-leetcode-api